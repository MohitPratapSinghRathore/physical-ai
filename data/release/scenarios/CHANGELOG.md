# Changelog

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
