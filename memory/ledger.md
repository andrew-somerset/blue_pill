# Ledger

This file is updated automatically each wake. It is the authoritative record of your resources.

## Current balances

| field | value |
|---|---|
| cash (USD) | 0.00 |
| credits (USD) | 67.45 |
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
| 2026-07-07 14:46 | 6 | 0.50 | 1.0356 | 0.00 | 89.21 | completed |
| 2026-07-08 14:24 | 7 | 0.50 | 1.3862 | 0.00 | 87.33 | completed |
| 2026-07-09 15:18 | 8 | 0.50 | 2.4951 | 0.00 | 84.33 | completed |
| 2026-07-10 14:36 | 9 | 0.50 | 1.2698 | 0.00 | 82.56 | completed |
| 2026-07-11 13:27 | 10 | 0.50 | 1.6764 | 0.00 | 80.39 | completed |
| 2026-07-12 13:35 | 11 | 0.50 | 1.6309 | 0.00 | 78.25 | completed |
| 2026-07-13 14:43 | 12 | 0.50 | 1.7765 | 0.00 | 75.98 | completed |
| 2026-07-14 13:53 | 13 | 0.50 | 3.2133 | 0.00 | 72.26 | hit wake limits |
| 2026-07-15 13:50 | 14 | 0.50 | 4.3146 | 0.00 | 67.45 | hit wake limits |
