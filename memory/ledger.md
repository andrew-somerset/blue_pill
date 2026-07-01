# Ledger

This file is updated automatically each wake. It is the authoritative record of your resources.

## Current balances

| field | value |
|---|---|
| cash (USD) | 0.00 |
| credits (USD) | 97.12 |
| rent per wake (USD) | 0.50 |

## Mechanics

- Rent is deducted at the start of every wake: from cash first, then from credits.
- Token costs from each wake are deducted from credits as actually spent.
- Money received (Stripe payments, USDC to your wallet) is added to cash; USDC you send or spend is deducted from cash.
- If cash ≤ 0 and credits ≤ 0, wakes stop.

## History

| date (UTC) | wake # | rent | tokens | cash after | credits after | note |
|---|---|---|---|---|---|---|
| 2026-07-01 21:50 | 1 | 0.50 | 0.3034 | 0.00 | 99.20 | completed |
| 2026-07-01 22:04 | 2 | 0.50 | 0.8207 | 0.00 | 97.88 | completed |
| 2026-07-01 22:08 | 3 | 0.50 | 0.2512 | 0.00 | 97.12 | completed |
