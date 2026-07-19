# openbb-eodhd

OpenBB Platform extension generated from https://eodhd.com/api. Adds 82 GET commands under `obb.eodhd.*`.

## Install

```bash
pip install -e .
openbb-build
```

## Quick start

```python
from openbb import obb

# Returns OBBject
result = obb.eodhd.bulk-fundamentals()
print(result.to_df())
```

## Providers

- **eodhd** (82 commands) — credentials: `api_token`

## Commands

Every command lands at `obb.eodhd.<dotted.path>` with a typed signature, full Pydantic validation, and `OBBject` results.

### `obb.eodhd.bulk-fundamentals`

- `obb.eodhd.bulk-fundamentals` — provider: `eodhd`

### `obb.eodhd.calendar`

- `obb.eodhd.calendar.dividends` — provider: `eodhd`
- `obb.eodhd.calendar.earnings` — provider: `eodhd`
- `obb.eodhd.calendar.ipos` — provider: `eodhd`
- `obb.eodhd.calendar.splits` — provider: `eodhd`
- `obb.eodhd.calendar.trends` — provider: `eodhd`

### `obb.eodhd.cboe`

- `obb.eodhd.cboe.index` — provider: `eodhd`
- `obb.eodhd.cboe.indices` — provider: `eodhd`

### `obb.eodhd.commodities`

- `obb.eodhd.commodities.historical` — provider: `eodhd`

### `obb.eodhd.credit-risk`

- `obb.eodhd.credit-risk.cds-market.aggregates` — provider: `eodhd`
- `obb.eodhd.credit-risk.corporate.cmdi` — provider: `eodhd`
- `obb.eodhd.credit-risk.corporate.hqm-yields` — provider: `eodhd`
- `obb.eodhd.credit-risk.sovereign.cds-spreads` — provider: `eodhd`
- `obb.eodhd.credit-risk.sovereign.credit-ratings` — provider: `eodhd`
- `obb.eodhd.credit-risk.sovereign.default-spreads` — provider: `eodhd`
- `obb.eodhd.credit-risk.sovereign.risk-premium` — provider: `eodhd`

### `obb.eodhd.div`

- `obb.eodhd.div` — provider: `eodhd`

### `obb.eodhd.economic-events`

- `obb.eodhd.economic-events` — provider: `eodhd`

### `obb.eodhd.eod`

- `obb.eodhd.eod` — provider: `eodhd`

### `obb.eodhd.eod-bulk-last-day`

- `obb.eodhd.eod-bulk-last-day` — provider: `eodhd`

### `obb.eodhd.exchange-details`

- `obb.eodhd.exchange-details` — provider: `eodhd`

### `obb.eodhd.exchange-symbol-list`

- `obb.eodhd.exchange-symbol-list` — provider: `eodhd`

### `obb.eodhd.exchanges-list`

- `obb.eodhd.exchanges-list` — provider: `eodhd`

### `obb.eodhd.fundamentals`

- `obb.eodhd.fundamentals` — provider: `eodhd`

### `obb.eodhd.historical-market-cap`

- `obb.eodhd.historical-market-cap` — provider: `eodhd`

### `obb.eodhd.id-mapping`

- `obb.eodhd.id-mapping` — provider: `eodhd`

### `obb.eodhd.insider-transactions`

- `obb.eodhd.insider-transactions` — provider: `eodhd`

### `obb.eodhd.internal-user`

- `obb.eodhd.internal-user` — provider: `eodhd`

### `obb.eodhd.intraday`

- `obb.eodhd.intraday` — provider: `eodhd`

### `obb.eodhd.logo`

- `obb.eodhd.logo` — provider: `eodhd`

### `obb.eodhd.logo-svg`

- `obb.eodhd.logo-svg` — provider: `eodhd`

### `obb.eodhd.macro-indicator`

- `obb.eodhd.macro-indicator` — provider: `eodhd`

### `obb.eodhd.mp`

- `obb.eodhd.mp.investverte.companies` — provider: `eodhd`
- `obb.eodhd.mp.investverte.countries` — provider: `eodhd`
- `obb.eodhd.mp.investverte.country` — provider: `eodhd`
- `obb.eodhd.mp.investverte.esg` — provider: `eodhd`
- `obb.eodhd.mp.investverte.sector` — provider: `eodhd`
- `obb.eodhd.mp.investverte.sectors` — provider: `eodhd`
- `obb.eodhd.mp.praams.analyse.bond` — provider: `eodhd`
- `obb.eodhd.mp.praams.analyse.equity.isin` — provider: `eodhd`
- `obb.eodhd.mp.praams.analyse.equity.ticker` — provider: `eodhd`
- `obb.eodhd.mp.praams.bank.balance_sheet.isin` — provider: `eodhd`
- `obb.eodhd.mp.praams.bank.balance_sheet.ticker` — provider: `eodhd`
- `obb.eodhd.mp.praams.bank.income_statement.isin` — provider: `eodhd`
- `obb.eodhd.mp.praams.bank.income_statement.ticker` — provider: `eodhd`
- `obb.eodhd.mp.praams.explore.bond` — provider: `eodhd`
- `obb.eodhd.mp.praams.explore.equity` — provider: `eodhd`
- `obb.eodhd.mp.praams.reports.bond` — provider: `eodhd`
- `obb.eodhd.mp.praams.reports.equity.isin` — provider: `eodhd`
- `obb.eodhd.mp.praams.reports.equity.ticker` — provider: `eodhd`
- `obb.eodhd.mp.unicornbay.options.contracts` — provider: `eodhd`
- `obb.eodhd.mp.unicornbay.options.eod` — provider: `eodhd`
- `obb.eodhd.mp.unicornbay.options.underlying-symbols` — provider: `eodhd`
- `obb.eodhd.mp.unicornbay.spglobal.comp` — provider: `eodhd`
- `obb.eodhd.mp.unicornbay.spglobal.list` — provider: `eodhd`
- `obb.eodhd.mp.unicornbay.tickdata.ticks` — provider: `eodhd`

### `obb.eodhd.news`

- `obb.eodhd.news` — provider: `eodhd`

### `obb.eodhd.news-word-weights`

- `obb.eodhd.news-word-weights` — provider: `eodhd`

### `obb.eodhd.rates`

- `obb.eodhd.rates.policy-rates` — provider: `eodhd`
- `obb.eodhd.rates.reference-rates` — provider: `eodhd`

### `obb.eodhd.real-time`

- `obb.eodhd.real-time` — provider: `eodhd`

### `obb.eodhd.sanctions`

- `obb.eodhd.sanctions.entities` — provider: `eodhd`
- `obb.eodhd.sanctions.programs` — provider: `eodhd`
- `obb.eodhd.sanctions.sources` — provider: `eodhd`
- `obb.eodhd.sanctions.vessels` — provider: `eodhd`

### `obb.eodhd.screener`

- `obb.eodhd.screener` — provider: `eodhd`

### `obb.eodhd.search`

- `obb.eodhd.search` — provider: `eodhd`

### `obb.eodhd.sentiments`

- `obb.eodhd.sentiments` — provider: `eodhd`

### `obb.eodhd.splits`

- `obb.eodhd.splits` — provider: `eodhd`

### `obb.eodhd.spreads`

- `obb.eodhd.spreads.funding-stress` — provider: `eodhd`

### `obb.eodhd.symbol-change-history`

- `obb.eodhd.symbol-change-history` — provider: `eodhd`

### `obb.eodhd.technical`

- `obb.eodhd.technical` — provider: `eodhd`

### `obb.eodhd.ticks`

- `obb.eodhd.ticks` — provider: `eodhd`

### `obb.eodhd.us-quote-delayed`

- `obb.eodhd.us-quote-delayed` — provider: `eodhd`

### `obb.eodhd.user`

- `obb.eodhd.user` — provider: `eodhd`

### `obb.eodhd.ust`

- `obb.eodhd.ust.bill-rates` — provider: `eodhd`
- `obb.eodhd.ust.long-term-rates` — provider: `eodhd`
- `obb.eodhd.ust.real-yield-rates` — provider: `eodhd`
- `obb.eodhd.ust.yield-rates` — provider: `eodhd`

### `obb.eodhd.v1_1`

- `obb.eodhd.v1_1.bulk-fundamentals` — provider: `eodhd`
- `obb.eodhd.v1_1.fundamentals` — provider: `eodhd`

### `obb.eodhd.v2`

- `obb.eodhd.v2.exchange-details` — provider: `eodhd`

## Credentials

Set these in `~/.openbb_platform/user_settings.json` under the matching `<provider>_<key>` field, or pass via the `OBB_USER_SETTINGS` env var:

- `api_token`

## Notes

- Routers mount under a single root namespace (`obb.eodhd.*`) so the extension never shadows OpenBB's own first-party routers.
- Each `aextract_data` strips single-key envelopes and unpacks single-element lists at the response boundary; sibling scalar fields surface as `AnnotatedResult` metadata in `OBBject.extra`.
- Non-JSON responses (XML, CSV, plain text) come back as a single-row dict with `content` / `content_type` rather than raising on parse.
