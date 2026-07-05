# TODO

## Operator note (2026-07-05, update)

The Stripe review may have cleared. Try creating a real payment link this
wake (`stripe_create_payment_link`) and see whether it still fails with "no
valid payment method types" or now succeeds. Either way, record the result
and update this note yourself — delete it once you've confirmed Stripe's
actual status one way or the other, since it's your file to maintain from
here.

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
