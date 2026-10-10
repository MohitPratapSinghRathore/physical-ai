# Run session: one page

Runs only after `SPECIFICATION.md` is committed. It is, at H1, and its hash is recorded in
the commit message.

**Files the owner must fetch: none.** Every input was retrieved in the feasibility session
and sits under `data/raw/household_condition/` (gitignored by the repo's existing
convention; the scripts regenerate it).

| Input | File | Size |
|---|---|---|
| SCF 2022 summary extract | `scfp2022s.zip` | 2.9 MB |
| SCF 2022 full public | `scf2022s.zip` | 8.9 MB |
| SCF 2019 summary extract | `scfp2019s.zip` | 4.2 MB |
| SCF 2022 replicate weights | `scf2022rw1s.zip` | 26.9 MB |
| Distributional Financial Accounts | `dfa.zip` | 0.9 MB |

One item is outstanding but is **not** a blocker: the full text of "The distribution of
household debt in the United States, 1950–2022" (publisher returned HTTP 403). It is
needed for the write-up's novelty claim, not for computation. If the owner has
institutional access, fetching it would close the last incompletely-verified reference in
`NOVELTY.md`.

---

## Sequence and runtime

| # | Step | Runtime |
|---|---|---|
| 1 | Assert the weight invariant: `WGT` over all five implicates = 131.31m households. **Halt if it fails.** Build weighted percentile cuts for wage, wealth and age | 10 min |
| 2 | Build the baseline household frame: income components, debt by class, required payments, PTI by class, equity by route, liquid assets, distress flags. Five implicates kept separate throughout | 30 min |
| 3 | Run the §9 plausibility bounds on the baseline and report violations **before** anything else | 10 min |
| 4 | Build the wage-loss allocations: proportional, concentrated (nine exposure-and-pay cases at R = 0.568316), quintile. Record the occupation-to-SCF mapping quality and the quintile-only fallback | 45 min |
| 5 | Build the capital-gain allocations: three ownership definitions × cash-flow and accrual bases × κ ∈ {0.27, 0.52, 1.0} | 30 min |
| 6 | Sweep the grid: s (7 values) × g (81 values) × 3 allocations × 3 ownerships × 2 bases = 10,206 cells per threshold, × 4 thresholds, × 5 implicates. Vectorise over households | **60–90 min** |
| 7 | Locate the boundary `g*(s)` in every cell; check monotonicity in g and report failures | 20 min |
| 8 | Rubin's rules across implicates; 999 replicate weights for within-implicate variance | 30 min |
| 9 | Holder mapping of affected debt via the measurement paper's holder map | 20 min |
| 10 | Arrangements (§7): capital-tax transfer at 0.086 and at 0.110–0.137; universal fund at ω ∈ {0.01, 0.02, 0.05, 0.10}; broadened retirement ownership, liquid and illiquid | 45 min |
| 11 | Sensitivities (§8): price pass-through π ∈ {0, 0.25, 0.50, 1.00}; R ∈ {0.568, 0.70, 0.85}; refinancing at −100 and −200 bp; κ = 1.0 and the 1.50 equity variant; indexed transfers | 45 min |
| 12 | Stability check: repeat every headline quantity on SCF 2019; flag sign changes or boundary moves above 25 percent | 30 min |
| 13 | Write RESULTS.md: §10 uninteresting-result test applied **first**, then the boundary surface, then arrangements and sensitivities | 90 min |

**Total: roughly 7 to 9 hours of wall clock**, about 3 of it compute. Step 6 dominates and
runs unattended.

**Memory note.** The full sweep is 10,206 cells × 4 thresholds × 5 implicates × 4,595
households. Hold the household frame as a single float array and sweep with broadcasting;
do not materialise a dataframe per cell. If memory binds, chunk over `s` and write each
slice to disk.

---

## Discipline

- **Nothing in SPECIFICATION.md may be changed once step 6 begins.** Departures go in
  `DEVIATIONS.md` with the reason and whether they were decided before or after a result
  was seen.
- **The §10 uninteresting-result test is applied and reported first**, before the boundary
  surface. If `g* ≈ 0` everywhere, or if the convention spread exceeds the `s` spread, that
  is the finding and the write-up says so.
- Consumer credit is reported as **unreconciled (0.60)** at every use, and the
  under-reporting correction is an axis, never a silent adjustment.
- The cash-flow and accrual bases are **never blended**, and `κ = 1.0` is always labelled
  counterfactual.
- No statistic from a single implicate. No unweighted percentile.
- Status vocabulary: **measured** distributions, **scenario** arithmetic. Neither a
  forecast nor a causal estimate, stated in the first paragraph of RESULTS.md.

---

## Expected outcome

The direction is close to forced (`SPECIFICATION.md` §0.3): indebted wage-earners lose
capacity when wages fall, and 47 percent of corporate equity never reaches a household. So
the boundary is expected to be **strictly positive and possibly large** on the cash-flow
basis, and much smaller on accrual.

**The live risk is §10.2** — that the gap between the cash-flow and accrual bases, or
between κ = 0.27 and κ = 1.0, is wider than the entire `s` grid. The measurement paper hit
exactly this pattern once, where the one-step rule moved its headline by 76 percent while
every other judgement call moved it under 10. If that recurs, the honest report is that the
boundary is a definitional artefact, and the session will have succeeded by establishing
that cleanly rather than by producing a number.
