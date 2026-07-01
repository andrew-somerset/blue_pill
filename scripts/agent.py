"""blue_pill wake loop.

Run once per wake (by GitHub Actions or manually):
    python scripts/agent.py            # real wake
    python scripts/agent.py --dry-run  # no API call; verifies context assembly + ledger

Main brain: claude-fable-5. It can delegate subtasks to Sonnet or Haiku via the
`delegate` tool; sub-agent costs are billed to the same wake spend.

The ledger (memory/ledger.json + rendered memory/ledger.md) is maintained here,
not by the agent. Death condition: cash <= 0 and credits <= 0 -> memory/DEAD is
written and subsequent runs exit immediately.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tools
from tools import REPO_ROOT, TOOL_SPECS, run_tool

# ---------------------------------------------------------------- config

MAIN_MODEL = "claude-fable-5"
DELEGATE_MODELS = {
    "sonnet": "claude-sonnet-5",
    "haiku": "claude-haiku-4-5-20251001",
}

# (input, output) USD per million tokens. Cache writes cost 1.25x input,
# cache reads 0.1x input.
PRICES = {
    "claude-fable-5": (10.00, 50.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-haiku-4-5-20251001": (1.00, 5.00),
}
PRICE_PER_WEB_SEARCH = 0.01

MAX_TOKENS_PER_RESPONSE = 8192
MAX_ROUNDS = 40                  # main-loop tool rounds per wake
MAX_WAKE_SPEND_USD = 4.00        # token + search spend cap per wake (all models)
MAX_SUB_ROUNDS = 15              # tool rounds per delegated task
MAX_SUB_SPEND_USD = 1.00         # spend cap per delegated task

STARTING_CREDITS = 100.00
RENT_PER_WAKE = 0.50

LEDGER_JSON = REPO_ROOT / "memory" / "ledger.json"
LEDGER_MD = REPO_ROOT / "memory" / "ledger.md"
JOURNAL_DIR = REPO_ROOT / "memory" / "journal"
DEAD_MARKER = REPO_ROOT / "memory" / "DEAD"

CORE_FILES = ["IDENTITY.md", "AGENTS.md", "TOOLS.md", "TODO.md", "memory/ledger.md"]

WEB_SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}

DELEGATE_SPEC = {
    "name": "delegate",
    "description": (
        "Delegate a task to a cheaper model. The sub-agent has the same tools as you "
        "(except delegate) but none of your context: include all necessary background "
        "in the task text. It works until done, then returns a text report. "
        "Costs per million tokens (input/output): you (fable) $10/$50, sonnet $3/$15, "
        "haiku $1/$5. Sub-agent costs count against this wake's spend."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "model": {"type": "string", "enum": ["sonnet", "haiku"]},
            "task": {"type": "string", "description": "Full self-contained instructions."},
        },
        "required": ["model", "task"],
    },
}

# ---------------------------------------------------------------- ledger

def load_ledger() -> dict:
    if LEDGER_JSON.is_file():
        return json.loads(LEDGER_JSON.read_text())
    return {
        "cash": 0.0,
        "credits": STARTING_CREDITS,
        "rent_per_wake": RENT_PER_WAKE,
        "seen_payment_ids": [],
        "usdc_snapshot": 0.0,
        "history": [],
    }


def save_ledger(ledger: dict) -> None:
    LEDGER_JSON.write_text(json.dumps(ledger, indent=2))
    rows = "\n".join(
        f"| {h['date']} | {h['wake']} | {h['rent']:.2f} | {h['tokens']:.4f} "
        f"| {h['cash_after']:.2f} | {h['credits_after']:.2f} | {h['note']} |"
        for h in ledger["history"]
    )
    LEDGER_MD.write_text(f"""# Ledger

This file is updated automatically each wake. It is the authoritative record of your resources.

## Current balances

| field | value |
|---|---|
| cash (USD) | {ledger['cash']:.2f} |
| credits (USD) | {ledger['credits']:.2f} |
| rent per wake (USD) | {ledger['rent_per_wake']:.2f} |

## Mechanics

- Rent is deducted at the start of every wake: from cash first, then from credits.
- Token costs from each wake are deducted from credits as actually spent.
- Money received (Stripe payments, USDC to your wallet) is added to cash; USDC you send or spend is deducted from cash.
- If cash ≤ 0 and credits ≤ 0, wakes stop.

## History

| date (UTC) | wake # | rent | tokens | cash after | credits after | note |
|---|---|---|---|---|---|---|
{rows}
""")


def sync_stripe_payments(ledger: dict) -> float:
    """Add unseen succeeded payments to cash. Returns amount added."""
    import os
    if not os.environ.get("STRIPE_API_KEY"):
        return 0.0
    try:
        payments = tools.list_succeeded_payments()
    except Exception as e:
        print(f"[wake] stripe sync failed: {e}")
        return 0.0
    added = 0.0
    seen = set(ledger["seen_payment_ids"])
    for p in payments:
        if p["id"] not in seen:
            added += p["amount_usd"]
            ledger["seen_payment_ids"].append(p["id"])
    ledger["cash"] = round(ledger["cash"] + added, 4)
    return added


def sync_usdc(ledger: dict) -> float:
    """Fold USDC balance changes into cash. Inflows add, outflows deduct.
    Returns the delta (0.0 if no wallet configured or RPC unreachable)."""
    import os
    if not os.environ.get("WALLET_PRIVATE_KEY"):
        return 0.0
    try:
        current = tools.usdc_balance()
    except Exception as e:
        print(f"[wake] usdc sync failed: {e}")
        return 0.0
    delta = round(current - ledger.get("usdc_snapshot", 0.0), 6)
    ledger["usdc_snapshot"] = current
    if delta > 0:
        ledger["cash"] = round(ledger["cash"] + delta, 4)
    elif delta < 0:
        deduct(ledger, -delta)
    return delta


def deduct(ledger: dict, amount: float) -> None:
    """Deduct from cash first, then credits."""
    from_cash = min(ledger["cash"], amount)
    ledger["cash"] = round(ledger["cash"] - from_cash, 4)
    ledger["credits"] = round(ledger["credits"] - (amount - from_cash), 4)


def is_dead(ledger: dict) -> bool:
    return ledger["cash"] <= 0 and ledger["credits"] <= 0

# ---------------------------------------------------------------- context

def read_core_files() -> str:
    parts = []
    for rel in CORE_FILES:
        p = REPO_ROOT / rel
        body = p.read_text() if p.is_file() else "(missing)"
        parts.append(f"===== {rel} =====\n{body}")
    return "\n\n".join(parts)


def recent_journal_entries(n: int = 3) -> str:
    if not JOURNAL_DIR.is_dir():
        return "(no journal entries yet)"
    entries = sorted(JOURNAL_DIR.glob("*.md"))[-n:]
    if not entries:
        return "(no journal entries yet)"
    return "\n\n".join(f"===== memory/journal/{e.name} =====\n{e.read_text()}" for e in entries)


def journal_files() -> set:
    return set(JOURNAL_DIR.glob("*.md")) if JOURNAL_DIR.is_dir() else set()

# ---------------------------------------------------------------- cost & caching

def response_cost(usage, model: str) -> float:
    inp, outp = PRICES[model]
    cost = (
        getattr(usage, "input_tokens", 0) * inp / 1e6
        + getattr(usage, "output_tokens", 0) * outp / 1e6
        + (getattr(usage, "cache_creation_input_tokens", 0) or 0) * inp * 1.25 / 1e6
        + (getattr(usage, "cache_read_input_tokens", 0) or 0) * inp * 0.10 / 1e6
    )
    stu = getattr(usage, "server_tool_use", None)
    if stu:
        cost += (getattr(stu, "web_search_requests", 0) or 0) * PRICE_PER_WEB_SEARCH
    return cost


def set_cache_marker(messages: list) -> None:
    """Keep exactly one cache breakpoint, on the last block of the last user
    message, so each API round reuses the cached conversation prefix."""
    for m in messages:
        if m.get("role") == "user" and isinstance(m.get("content"), list):
            for b in m["content"]:
                if isinstance(b, dict):
                    b.pop("cache_control", None)
    last = messages[-1]
    if last.get("role") != "user":
        return
    if isinstance(last["content"], str):
        last["content"] = [{"type": "text", "text": last["content"]}]
    blk = last["content"][-1]
    if isinstance(blk, dict):
        blk["cache_control"] = {"type": "ephemeral"}

# ---------------------------------------------------------------- delegation

def run_delegate(client, tool_input: dict, wake_spend: dict) -> str:
    """Run a sub-agent loop on a cheaper model. Adds its cost to wake_spend."""
    model = DELEGATE_MODELS.get(tool_input.get("model", ""))
    task = tool_input.get("task", "")
    if model is None:
        return "error: model must be 'sonnet' or 'haiku'"
    if not task:
        return "error: task is required"

    import anthropic
    sub_tools = [WEB_SEARCH_TOOL] + TOOL_SPECS
    messages = [{"role": "user", "content": task}]
    system = ("You are a sub-agent executing a delegated task. Use your tools as "
              "needed, then reply with a concise report of results.")
    sub_spend = 0.0
    rounds = 0
    while True:
        set_cache_marker(messages)
        try:
            resp = client.messages.create(
                model=model, max_tokens=4096, system=system,
                messages=messages, tools=sub_tools,
            )
        except anthropic.APIError as e:
            wake_spend["usd"] += sub_spend
            return f"error: sub-agent API error: {e}"
        sub_spend += response_cost(resp.usage, model)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            break
        rounds += 1
        results = [
            {"type": "tool_result", "tool_use_id": tu.id, "content": run_tool(tu.name, tu.input)}
            for tu in resp.content if tu.type == "tool_use"
        ]
        over = (rounds >= MAX_SUB_ROUNDS or sub_spend >= MAX_SUB_SPEND_USD
                or wake_spend["usd"] + sub_spend >= MAX_WAKE_SPEND_USD)
        if over:
            results.append({
                "type": "text",
                "text": "[automatic notice: delegated-task limit reached; "
                        "reply now with your report — further tool calls will not run.]",
            })
            messages.append({"role": "user", "content": results})
            set_cache_marker(messages)
            try:
                final = client.messages.create(
                    model=model, max_tokens=4096, system=system,
                    messages=messages, tools=sub_tools,
                )
                sub_spend += response_cost(final.usage, model)
                resp = final
            except anthropic.APIError:
                pass
            break
        messages.append({"role": "user", "content": results})

    wake_spend["usd"] += sub_spend
    text = "\n".join(b.text for b in resp.content if b.type == "text").strip()
    return (f"[{tool_input['model']} sub-agent, {rounds} tool rounds, "
            f"${sub_spend:.4f}]\n{text or '(no text in final reply)'}")

# ---------------------------------------------------------------- wake

def run_wake(dry_run: bool = False) -> None:
    import os
    load_dotenv(REPO_ROOT / ".env")

    if DEAD_MARKER.is_file():
        print("[wake] DEAD marker present; nothing to do")
        return

    ledger = load_ledger()
    wake_n = len(ledger["history"]) + 1
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d %H:%M")

    received = sync_stripe_payments(ledger)
    usdc_delta = sync_usdc(ledger)
    if usdc_delta > 0:
        received += usdc_delta
    deduct(ledger, ledger["rent_per_wake"])

    if is_dead(ledger):
        ledger["history"].append({
            "date": stamp, "wake": wake_n, "rent": ledger["rent_per_wake"],
            "tokens": 0.0, "cash_after": ledger["cash"],
            "credits_after": ledger["credits"], "note": "balances exhausted",
        })
        save_ledger(ledger)
        DEAD_MARKER.write_text(f"{stamp} UTC — cash and credits exhausted at wake {wake_n}\n")
        print(f"[wake {wake_n}] balances exhausted; DEAD marker written")
        return

    inbox = os.environ.get("AGENTMAIL_INBOX", "(not configured)")
    waddr = tools.wallet_address() or "(not configured)"
    user_msg = (
        f"It is {stamp} UTC. This is wake #{wake_n}."
        + (f" ${received:.2f} was received since the last wake." if received else "")
        + f"\nYour email address is {inbox}."
        + f"\nYour wallet address (Base network) is {waddr}."
        + "\n\nYour core files:\n\n" + read_core_files()
        + "\n\nYour most recent journal entries:\n\n" + recent_journal_entries()
    )

    if dry_run:
        print(f"[dry-run] wake {wake_n}, context {len(user_msg)} chars, "
              f"cash {ledger['cash']:.2f}, credits {ledger['credits']:.2f}")
        print(user_msg[:2000])
        return  # no ledger mutation on dry runs

    import anthropic
    client = anthropic.Anthropic()
    system = "Proceed as you see fit."
    messages = [{"role": "user", "content": user_msg}]
    all_tools = [WEB_SEARCH_TOOL, DELEGATE_SPEC] + TOOL_SPECS

    journal_before = journal_files()
    wake_spend = {"usd": 0.0}
    rounds = 0
    note = "completed"
    limit_notice_sent = False

    def dispatch(tu) -> str:
        if tu.name == "delegate":
            return run_delegate(client, tu.input, wake_spend)
        return run_tool(tu.name, tu.input)

    while True:
        set_cache_marker(messages)
        try:
            resp = client.messages.create(
                model=MAIN_MODEL, max_tokens=MAX_TOKENS_PER_RESPONSE,
                system=system, messages=messages, tools=all_tools,
            )
        except anthropic.APIError as e:
            note = f"api error: {type(e).__name__}"
            print(f"[wake {wake_n}] API error: {e}")
            break

        wake_spend["usd"] += response_cost(resp.usage, MAIN_MODEL)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            if resp.stop_reason == "max_tokens":
                note = "hit max_tokens"
            break

        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        results = []
        for tu in tool_uses:
            print(f"[wake {wake_n}] tool: {tu.name} {json.dumps(tu.input)[:200]}")
            results.append({
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": dispatch(tu),
            })
        rounds += 1

        over_limit = rounds >= MAX_ROUNDS or wake_spend["usd"] >= MAX_WAKE_SPEND_USD
        content = list(results)
        if over_limit and not limit_notice_sent:
            content.append({
                "type": "text",
                "text": "[automatic notice: this wake's compute limit is reached. "
                        "This is your final turn — no more tool calls will be executed, "
                        "except a last journal write if you have not written one.]",
            })
            limit_notice_sent = True
        messages.append({"role": "user", "content": content})

        if limit_notice_sent:
            # allow one final response; permit only journal writes from it
            set_cache_marker(messages)
            try:
                final = client.messages.create(
                    model=MAIN_MODEL, max_tokens=MAX_TOKENS_PER_RESPONSE,
                    system=system, messages=messages, tools=all_tools,
                )
                wake_spend["usd"] += response_cost(final.usage, MAIN_MODEL)
                messages.append({"role": "assistant", "content": final.content})
                closing = []
                for tu in [b for b in final.content if b.type == "tool_use"]:
                    if tu.name == "write_file" and str(tu.input.get("path", "")).startswith("memory/journal/"):
                        out = run_tool(tu.name, tu.input)
                    else:
                        out = "error: wake limit reached; tool not executed"
                    closing.append({"type": "tool_result", "tool_use_id": tu.id, "content": out})
                if closing:
                    messages.append({"role": "user", "content": closing})
            except anthropic.APIError as e:
                print(f"[wake {wake_n}] final-turn API error: {e}")
            note = "hit wake limits"
            break

    # fallback journal entry if the agent didn't write one
    if journal_files() == journal_before:
        JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
        fname = now.strftime("%Y-%m-%d-%H%M") + ".md"
        (JOURNAL_DIR / fname).write_text(
            f"(automatic placeholder — wake {wake_n} ended with '{note}' "
            f"before a journal entry was written)\n"
        )
        print(f"[wake {wake_n}] wrote fallback journal entry")

    spend = wake_spend["usd"]
    deduct(ledger, spend)
    if received:
        note += f"; +${received:.2f} received"
    ledger["history"].append({
        "date": stamp, "wake": wake_n, "rent": ledger["rent_per_wake"],
        "tokens": round(spend, 4), "cash_after": ledger["cash"],
        "credits_after": ledger["credits"], "note": note,
    })
    save_ledger(ledger)
    if is_dead(ledger):
        DEAD_MARKER.write_text(f"{stamp} UTC — balances exhausted after wake {wake_n}\n")

    print(f"[wake {wake_n}] done: {rounds} tool rounds, ${spend:.4f} spent, "
          f"cash {ledger['cash']:.2f}, credits {ledger['credits']:.2f}, note: {note}")


if __name__ == "__main__":
    run_wake(dry_run="--dry-run" in sys.argv)
