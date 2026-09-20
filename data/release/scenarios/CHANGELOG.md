# Changelog

## 0.8.0 (2026-09-20)
Independent replication round one matched 21 of 51 quantities. This release is the repair.
The mismatches are classified in notes/replication/round1_mismatch_classification.md and the
rebuilt brief is notes/replication_brief_v2.md.

- THE BREAK-EVEN CAPITAL TAX RATE WAS WRONG AND IS CORRECTED. The replicator found the
  sealed case A maximum of 0.378371 above the highest reading of tau_l, which the brief's own
  definition tau_l * (1 - R) makes impossible. Two defects multiplied: the expression divided
  a loss that ALREADY nets out tau_k by a surplus, and numerator and denominator were built
  on two different wage bill totals. Case A is now 0.125 to 0.301 and case B 0.182 to 0.650,
  replacing 0.214 to 0.378 and 0.561 to 0.860. Plausibility bounds are now enforced: case A
  cannot exceed tau_l + g, no rate can exceed 1, and case B cannot fall below case A.
- THE WAGE BILL BASE IS CORRECTED THROUGHOUT. A dose is converted to dollars on FRED WASCUR
  national wages and salaries, the base tau_l is actually built on. The fiscal modules were
  using compensation of employees, which includes employer pension and health contributions
  that bear neither the income tax nor the payroll tax, and the second-round module was using
  this project's occupational grid, which is 73.9 percent of national wages. Fiscal dollar
  figures fall 17.6 percent; second-round demand figures rise 35.4 percent.
- THE TRUST FUND DENOMINATORS ARE READ FROM THE TRUSTEES REPORT, not derived. HI payroll
  income is 403.2bn, replacing 462.4bn, which is HI TOTAL income including interest,
  government contributions and premiums. HI's own payroll share of fund income, 0.8720,
  replaces the OASDI share of 0.9126 that was being applied to both funds.
- THE TRUST FUND RESERVE COLUMN IS FILLED and DEPLETION TIMING is added as a second capacity
  measure: OASI 2,338.3bn depleting 2032 Q4, DI 223.0bn not depleting within 75 years, HI
  255.7bn depleting 2033 Q2. HI was NOT in deficit in 2025: its reserves rose by 18.2bn.
- THE AUTO AGGREGATE MOVES OFF A DISCONTINUED SERIES. FRED MVLOAS ended at 2024Q4 while every
  other input is 2026. Replaced with the NY Fed Household Debt and Credit auto loan balance,
  1,713bn at 2026Q2, the same source and vintage as the mortgage and student aggregates. The
  auto under-reporting factor moves from 1.743 to 1.904; the auto bank loss does not move,
  because the bank-held share carries the same denominator and the two cancel.
- THE DASHBOARD gains auto loan delinquency, the trust fund reserve balances and the
  depletion dates, which standing requirement 4 asks for and which were previously recorded
  as blocked.

## 0.7.0 (2026-09-20)
- THE TABLE IS REORGANISED BY WAGE QUINTILE. Exposure type turned out to be a pay proxy in
  three independent tests, so the organising dimension is now where in the wage distribution
  displacement falls, and the exposure indices are named scenarios for that.
- CASE A AND CASE B. Every fiscal number now carries its case: output preserved with income
  redistributed to capital (A), or output falling with demand so the taxable surplus falls
  too (B). Case B raises the fiscal loss by 25 to 44 percent and the break-even capital tax
  rate from 0.21 to 0.38 up to 0.56 to 0.86.
- DEBT PATHS ARE INCREMENTS over a no-displacement baseline under the same interest rate and
  growth assumptions. The earlier 389 percent emerging-market figure is WITHDRAWN as a
  statement about automation: it was almost entirely baseline compounding.
- SECOND-ROUND SENSITIVITY across sourced ranges for the marginal propensity to consume, the
  income elasticity of house prices, the Okun coefficient and the loss mapping. The bank-loss
  headline spans a factor of nine, and "a demand event first" survives only conditionally.

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
