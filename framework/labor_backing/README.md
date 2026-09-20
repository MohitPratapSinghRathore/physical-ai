# The labour backing ratio

**PROVISIONAL THROUGHOUT. Produced in one session, 2026-09-20. Nothing here is a standing
claim. Nothing here has been independently replicated. Every quantity is sealed for
replication round two under `labour_backing` and `two_sided_bet` in
`notes/sealed/sealed_expected_values_round2.json`, and the mechanics are in section 14 of
`notes/replication_brief_v2.md`.**

The prior specification is `_unreviewed/feasibility.md`, which was read as a specification
and not as a result. Nothing else in `_unreviewed/` was used.

## The headline

| | |
|---|---|
| Direct labour backing ratio, 2025 | **0.270** (40,380bn of 149,407bn) |
| Range, all judgement calls except the one-step rule | 0.267 to 0.297 |
| Range including the one-step rule | 0.267 to 0.475 |
| **Federal government share of labour-backed claims** | **0.794** held, guaranteed or owed |
| Federal government share of the AI leg | **0.010** |
| Second-round (B2) backing of business revenue, separate | 0.338 |

Read `ONE_PAGE.md` first. Then `TWO_SIDED_BET.md`. Then
`../../lit/related_work_labour_backing.md`, which narrows the novelty claims.

## Rebuild

```
python framework/labor_backing/build_direct.py            # B1, B3, B4
python framework/labor_backing/build_indirect.py          # B2
python framework/labor_backing/build_quintile_connection.py  # B5, B8
python framework/labor_backing/build_ai_leg.py            # B11, B12
python framework/labor_backing/build_sensitivity.py       # B9 support and the charts
python framework/labor_backing/seal_labour_backing.py     # B10
python framework/labor_backing/update_dashboard.py        # B12 dashboard indicators
```

Order matters: `build_direct.py` writes the inputs the rest read. The first run downloads
two source packages into `_z1_cache.zip` and `_dfa_cache.zip`, which are gitignored
because they are re-downloadable and total 9MB.

## Sources

| File | Source |
|---|---|
| `_z1_cache.zip` | Federal Reserve Z.1 Financial Accounts, CSV package, `https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip`. **The whole release, not per-series FRED calls**: 2,901 level series and the Fed's own data dictionary in one download |
| `_dfa_cache.zip` | Federal Reserve Distributional Financial Accounts, `https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip` |
| `_fred/` | FRED `PCEC` and `PI`, with a manifest carrying title, units, source and retrieval date |
| everything else | already in `data/raw/` and `data/processed/` |

`z1_extract.csv` records every Z.1 series actually used, with the Federal Reserve's own
description and the first and last year, so the build is auditable without the zip.

## Files

**Memos.** `ONE_PAGE.md` (B9, the verdict), `TWO_SIDED_BET.md` (B11 and B12),
`cross_country_feasibility.md` (B6).

**Code.** `z1_loader.py` (the Z.1 reader and catalog), `config.py` (claim classes, tracing
rules, holder map, obligor map), then the six build scripts above.

**Results.** `claim_class_rules.csv` (B1), `direct_ratio_latest.json` and
`holder_matrix_latest.csv` (B3), `direct_ratio_timeseries.csv` (B4),
`indirect_extension*.{json,csv}` (B2), `quintile_labour_backing*.csv` (B5),
`connection_test.csv` and `connection_agreement.csv` (B8), `two_sided_bet*.{json,csv}`,
`payoff_table_by_holder.csv`, `government_claim_on_ai_leg.csv`, `historical_anchors.csv`
(B11 and B12), `sensitivity*.{csv,json}` and `fig_labour_backing_two_panel.png` (B9).

**Bounds.** `plausibility_direct.csv`, `plausibility_indirect.csv`,
`plausibility_quintile_connection.csv`, `plausibility_ai_leg.csv`. **75 checks, 0
violations.** Bounds are stated before the numbers, per the standing rule.

## The three things a reader should not miss

1. **The one-step rule moves the headline by 76 percent and nothing else moves it by more
   than 10.** The definition is the argument. This is why `ONE_PAGE.md` recommends one
   section rather than the central object of the paper.
2. **The sovereign result was produced without reference to the dose-response table and
   lands inside it.** 79.4 percent of labour-backed claims against an independently derived
   75.9 to 91.6 percent federal share of first-round losses.
3. **The novelty claim on the fiscal mechanism is retired**, not narrowed. Five prior works
   have it. See `../../lit/related_work_labour_backing.md`.
