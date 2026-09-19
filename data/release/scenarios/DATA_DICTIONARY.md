# Data dictionary

## scenarios/paths.csv

| Column | Meaning | Status |
|---|---|---|
| regime | SLOW, FAST or SUDDEN. SLOW is inside the speed limit; FAST is above it but inside the observed prime-age nonemployment range; SUDDEN is outside that range | derived |
| exposure_type | embodied, cognitive_AIOE, cognitive_GPT, both | definition |
| phi | destination-pool shrinkage. 0 assumes new work is created at the historical rate indefinitely | SCENARIO ASSUMPTION |
| horizon_years | 2, 5, 10 or 20 | definition |
| d_annual | annual displacement flow, share of employment | SCENARIO ASSUMPTION |
| ep_ratio | prime-age employment to population ratio at the horizon, percent | ESTIMATED inside the observed range, SCENARIO outside it |
| ep_drop_pp | fall in that ratio from the 2026 baseline, percentage points | as above |
| never_reemployed_share | cumulative share of all inflows to unemployment never reemployed | as above |
| wage_income_rel_baseline | aggregate wage income relative to the 2026 baseline, composition-adjusted for repeat displacement at omega | as above |
| unemployment | prime-age unemployment rate. Reported LAST because exits to nonparticipation suppress it | as above |
| rho_implied | reemployment share implied by the model's own slack | ESTIMATED |
| outside_data | TRUE when prime-age nonemployment exceeds 24.71 percent, the worst vintage in the sample | derived |

## Status vocabulary

- **ESTIMATED**: derived from measured data within the range on which the underlying
  relationships were fitted.
- **SCENARIO ASSUMPTION**: chosen by the analyst, varied over a stated grid, not measured.
- **OUTSIDE DATA**: computed by extrapolating a fitted relationship beyond its observed
  range. Reported as a band, never as a point estimate.

## What is NOT in this release yet

House price change by metro type and the fiscal position path are NOT included. They require
the supervisory conversion layer (Federal Reserve stress test loss rates, a verified house
price elasticity) which is not yet built. The columns are deliberately absent rather than
filled with placeholders.
