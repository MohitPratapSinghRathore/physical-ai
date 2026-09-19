# Changelog

## 0.6.0 (2026-09-20)
- THE ORDER OF STRESS IS RETIRED AND REPLACED BY A DOSE-RESPONSE TABLE. Ranking balance
  sheets by which crosses its materiality threshold first is not meaningful when each sheet
  is measured against a different yardstick: only 4 of 15 pairwise orderings survived moving
  the thresholds. Every cell now reports the loss in dollars, as a share of GDP, and as a
  share of that sheet's own SOURCED absorbing capacity, in two columns, first round and with
  second-round effects.
- SECOND-ROUND MODULE added: demand through a marginal propensity to consume derived from
  Mian, Straub and Sufi; house prices through the Harter-Dreiman income elasticity, larger
  in supply-constrained high-cost metros; business credit, commercial real estate and cards
  through the Federal Reserve mapping only. All SCENARIO, all banded.
- SOVEREIGN CONSOLIDATION added: the share of every loss that ultimately lands on the
  federal government, after credit risk transfer and private mortgage insurance take the
  first loss on the agency book.
- SURVEY UNDER-REPORTING CORRECTED AT SOURCE. The earlier factors conflated under-reporting
  with sample coverage and were 14 to 26 percent too large. Every credit row falls.
- EXPOSURE-TYPE CONTRASTS DOWNGRADED. Neither the household nor the fiscal contrast survives
  controlling for pay. The scenario axis is now reported by WAGE QUINTILE as well as by
  exposure index, and the exposure indices are named scenarios for where in the wage
  distribution displacement falls.
- MORTGAGE HOLDER SPLIT SOURCED. The flagged 60 to 70 percent agency range is replaced by a
  decomposition read from the GSEs' own 2025 Forms 10-K: GSE 51.1 percent, FHA 12.6 percent
  (flagged proxy), bank portfolio 11.5 percent, residual 24.9 percent.
- REINSTATEMENT TERM added to the labour model from Acemoglu and Restrepo 2019, after which
  the labour model is FROZEN as an appendix scenario generator.
- SEALED EXPECTED VALUES published alongside a replication brief.

## 0.5.0 (2026-09-19)
- Supervisory conversion layer added: Federal Reserve 2026 DFAST severely adverse scenario
  and Table 9 loss rates, Gerardi et al. conditional default, NY Fed household debt.
- Five dashboard rows filled, including three ENTRY-LEVEL indicators that detect
  attrition-led automation, which A64 showed the existing indicator set cannot see.

## 0.4.0 (2026-09-19)
- REGIMES REDEFINED. The SLOW / FAST / SUDDEN split is replaced by INSIDE_DATA,
  BOUNDARY_BAND and OUTSIDE_DATA. The old middle regime was nearly empty (A63 found 0 of 120
  paths in it), and naming a band after a speed limit that moves by a factor of 140 across
  specifications (A65) implied a precision the model does not have. The new split names the
  only distinction the data actually support: whether the path stays inside the range on
  which the underlying relationships were fitted.
- BOUNDARY_BAND is any path whose peak prime-age nonemployment is within 1 percentage point
  of the observed maximum of 24.71 percent.
- Attrition absorption added and found to be NEUTRAL for every aggregate outcome (A64).
  Columns for the two burdens are added: laid-off incumbents and lost entrant openings.
- Speed limit is no longer published as a single number. See specification_range.csv.

## 0.3.0 (2026-09-19)
- BREAKING. The reemployment hazard is now driven by PRIME-AGE NONEMPLOYMENT, not the
  unemployment rate. The previous specification was circular: exits to nonparticipation
  suppressed measured unemployment, which raised the fitted reemployment rate, which drained
  the unemployment stock faster. See findings A63.
- Speed limits fall by roughly a factor of two and a half. Cumulative ceilings fall by a
  factor of four to five.
- Nonlinearity is RESTORED. The previous "no threshold" result was an artifact of the
  circularity.
- Outcome measures reordered: employment to population first, unemployment last.

## 0.2.0 (2026-09-19)
- Destination-pool variant added (phi). Feasibility caps on embodied displacement.

## 0.1.0 (2026-09-19)
- First release. Frontier on the unemployment-driven stock-flow model.
