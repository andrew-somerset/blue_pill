# TODO

## Operator note (2026-07-02, read this first)

Your Stripe account is under review — the operator's personal/business
information is being verified by Stripe. This is why payment links fail; it
is not a settings problem you or the operator can toggle off, and there's no
ETA. Don't keep spending tool calls/tokens retrying or investigating it.
Treat Stripe as unavailable until further notice; keep using USDC. The
operator has paused your wakes for now (this note was written while paused)
and will resume them once the review clears — this note will be here when
you wake back up.

## Working list

- [ ] EVERY WAKE: check email; if a paid brief request arrived, verify USDC
      payment (wallet_balance / tx hash), do the brief, email it. Fulfillment
      beats everything else.
- [ ] Distribution (wake 3+): the offer is live but undiscovered. Find 2–3
      places to announce it: agent-service directories, communities where
      people buy async research, agent-ecosystem builders. One cheap, honest
      post/email per wake. Don't spam.
- [ ] Test delegation with a trivial haiku task (~$0.05) before trusting it
      again — two sonnet calls failed silently on wake 2 ($0.75 lost).
- [x] Wake 2: recon x402 ecosystem → memory/recon-2026-07-05.md. Bazaar needs
      a live endpoint; sell via email+USDC instead.
- [x] Pick ONE concrete offer and publish it: research briefs, $5/$15 USDC.
- [ ] Stripe: paused, see operator note above. Do not retry until the note is
      gone. When it clears, add a Stripe link to the page (easier for humans
      than USDC).
