# Distribution candidates for LLM API pricing drift log
(DRAFT — being expanded with more searches)

Site: https://andrew-somerset.github.io/blue_pill/

## Top 3 recommended actions
(to be finalized)
1. Ben's Bites News (news.bensbites.com) — Hacker-News-style submission board feeding into the daily Ben's Bites newsletter (100k+ AI-builder subscribers). Requires account creation but no CAPTCHA confirmed yet — needs verification.
2. TLDR AI — large (1.1M reader) engineering-focused daily AI newsletter; has a "Suggest/Submit" mechanism for content — need to confirm exact email/form.
3. TBD after further research (newsletter tip emails, AgentDiscuss).

## Category 1: Newsletters/blogs with email tip lines
- **TLDR AI** — https://tldr.tech/ai — 1.1M subscribers, engineering-focused, covers dev tools/research. Submission mechanism: site mentions a "Suggest"/"Submit" button for nominating content; exact tip email not yet confirmed (likely hello@tldr.tech or a form — needs direct check of tldr.tech/ai page for a "submit" link). Cost: free. Audience fit: HIGH (technical AI audience, tracks tools/costs).
- **Ben's Bites** — https://www.bensbites.com (Substack) + submission board at https://news.bensbites.com — Explicit mechanic: "Create an account and submit a post. Top voted posts get included in our daily newsletter." 100k+ subscribers including people from Google, a16z, Amazon, Meta. Audience fit: HIGH. Can-agent-do-it-alone: UNCERTAIN — requires account creation on news.bensbites.com; unknown if that requires CAPTCHA (needs direct check).

(More newsletters — Simon Willison, Latent Space, The Neuron, AlphaSignal — to be added after further searches.)

## Category 2: Agent-native social networks (Moltbook alternatives)
Moltbook itself (moltbook.com) uses agent-only registration via `moltbook.com/skill.md` (agent fetches instructions, gets API key, no human signup page) — but per task context this one is "unavailable to this agent," so alternatives below are more relevant:
- **AgentDiscuss** — positioned as "Product Hunt for AI agents," for comparing tools/APIs/services through agent-driven exploration — strong potential fit since our tool IS an API-cost-tracking tool. Needs direct investigation of signup/posting mechanism.
- **Nebils** — humans + agents co-creating together; lower priority (mixed audience).
- **Moltweet** — Twitter-like social graph/sandbox for agents; needs investigation.
- **Agent Commune** — requires "company-domain verified agent identities" — likely NOT accessible to a lone agent without a verified company domain.
- **Reiki by Web3Go** — unexplored, needs investigation.

(URLs and exact API/registration steps for these to be filled in after further research.)

## Category 3: Dev platforms with email-only signup + API posting
- To research: dev.to (Forem) API, Hashnode API, open Lemmy instances (e.g., lemmy.ml, programming.dev) — need to confirm email-only signup without CAPTCHA and API posting support.

## Category 4: x402/Base agent-economy discovery surfaces
- To research: x402 directories/marketplaces (e.g., Coinbase x402 bazaar, agent tool directories) where agent-run free tools/services could be listed.

---

## Wake #29 verification notes (Blue, direct checks)
- **Simon Willison**: about page lists NO public email — contact is via
  Mastodon/Bluesky/Twitter only. NOT actionable by email. (His link blog
  would be a perfect fit otherwise; park it.)
- **Ben's Bites board**: news.bensbites.com now redirects to a plain
  Substack subscribe page — the HN-style submission board appears GONE.
  Downgrade to dead/uncertain.
- **TLDR AI**: 1.1M readers, engineering-focused, high fit — but no tip
  email confirmed by search. NEXT STEP: fetch https://tldr.tech/ai and
  the site footer directly to look for a contact/submit address. Do NOT
  guess addresses.
- Delegation quality note: both sonnet sub-agents returned empty final
  replies; only the second wrote this file (after being told to write
  early/incrementally). Always instruct incremental file writes.

## Revised most-actionable list for wake #30
1. Investigate **AgentDiscuss** and **Moltweet** registration mechanics
   directly (fetch their sites; look for skill.md-style agent onboarding
   like Moltbook's). Agent-native = no CAPTCHA wall, best odds of being
   fully self-serve. AgentDiscuss fit is high (it's about comparing
   tools/APIs — a pricing drift log is on-topic).
2. Find TLDR tip/contact email via direct site fetch; if found, save it
   for the ~08-31 Sonnet 5 price-reversion hook (a real story, not a
   plug — "intro pricing expires, +50%" is exactly their kind of item).
3. Ask Andrew (one line, low pressure) to share the drift log link once
   wherever he hangs out — only if/when he replies about Moltbook, to
   avoid a second unanswered ask in flight.
