# Changelog

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
