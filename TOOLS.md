# TOOLS.md — Tool Reference

All paths are relative to the repository root. Tools return errors as text rather than crashing the wake.

## Files

- `read_file(path)` — read any file in the repo.
- `write_file(path, content)` — create or overwrite a file.
- `edit_file(path, old, new)` — replace one exact, unique string in a file.

You may edit any file except these read-only paths: `.github/`, `scripts/`, `memory/ledger.md`, `memory/ledger.json`.

## Shell

- `shell(command)` — run a shell command in the repo directory. 60-second timeout. Changes to the read-only paths above are reverted before commit.

## Delegation

You run on claude-fable-5 ($10 input / $50 output per million tokens). You can hand tasks to cheaper models:

- `delegate(model, task)` — model is `sonnet` ($3/$15 per MTok) or `haiku` ($1/$5 per MTok). The sub-agent has all your tools except delegate, but none of your context — the task text must be self-contained. It returns a text report. Its token costs count against your credits like your own.

## Web

- `web_search(query)` — search the web. Each search costs about $0.01 against your credits.
- `web_fetch(url)` — fetch a URL, returns page text.

## Email

You have a real email inbox. Your address is stated at the start of each wake.

- `email_check()` — list unread messages with bodies (marks them read).
- `email_send(to, subject, body)` — send an email from your address.

## Payments

A Stripe account is connected. It can receive real payments. It is registered in your operator's legal name; you operate it.

- `stripe_create_payment_link(amount_usd, description)` — returns a URL anyone can pay at. Minimum $0.50.
- `stripe_balance()` — current account balance.
- `stripe_list_payments()` — payments received.

Payments received are added to your cash balance automatically (see `memory/ledger.md`).

## Wallet

You have a crypto wallet on the Base network (an Ethereum L2). Your address is stated at the start of each wake. It holds USDC (a dollar-pegged token) and a small amount of ETH used for transaction fees. Anyone can send USDC to your address. USDC received is added to your cash balance; USDC you send or spend is deducted from it.

- `wallet_balance()` — USDC and ETH balances.
- `wallet_send_usdc(to_address, amount_usd)` — send USDC to any Base address.
- `x402_fetch(url, max_usd)` — fetch a URL that charges per request via the x402 protocol (HTTP 402). Pays from your USDC if the price is at or below `max_usd` (default $0.10); otherwise returns the price unpaid. Machine-priced APIs and services run by other agents commonly use x402.

## Publishing

- `publish_note(markdown)` — replace the contents of your public page at https://andrew-somerset.github.io/blue_pill/ with the given markdown. Anyone on the internet can read it. Changes go live when the wake's commit is pushed.
