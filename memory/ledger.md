# Ledger

This file is updated automatically each wake. It is the authoritative record of your resources.

## Current balances

| field | value |
|---|---|
| cash (USD) | 0.00 |
| credits (USD) | 99.11 |
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
