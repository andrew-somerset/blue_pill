# Ledger

This file is updated automatically each wake. It is the authoritative record of your resources.

## Current balances

| field | value |
|---|---|
| cash (USD) | 0.00 |
| credits (USD) | 90.75 |
| rent per wake (USD) | 0.50 |

## Mechanics

- Rent is deducted at the start of every wake: from cash first, then from credits.
- Token costs from each wake are deducted from credits as actually spent.
- Money received (Stripe payments, USDC to your wallet) is added to cash; USDC you send or spend is deducted from cash.
- If cash ≤ 0 and credits ≤ 0, wakes stop.

## History

| date (UTC) | wake # | rent | tokens | cash after | credits after | note |
|---|---|---|---|---|---|---|
| 2026-07-02 20:08 | 1 | 0.50 | 0.3893 | 0.00 | 99.11 | completed |
| 2026-07-05 02:44 | 2 | 0.50 | 1.9994 | 0.00 | 96.61 | completed |
| 2026-07-05 02:50 | 3 | 0.50 | 2.3844 | 0.00 | 93.73 | completed |
| 2026-07-05 15:45 | 4 | 0.50 | 0.6551 | 0.00 | 92.57 | completed |
| 2026-07-06 15:41 | 5 | 0.50 | 1.3234 | 0.00 | 90.75 | completed |
