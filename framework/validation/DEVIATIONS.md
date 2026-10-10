# Deviations log — run session, 2026-09-21

Every departure from PREREGISTRATION.md (including Amendments 1–3) and SESSION2_PLAN.md,
with its reason and whether it was decided before or after outcomes were opened.

**Nothing in this log changes a specification, sample rule, outcome, threshold, window or
reading.** Where the plan could not be executed exactly as written, the closest
pre-specified alternative was used and the affected results are marked.

---

## D1. Sample count reconciliation — not a deviation, recorded for clarity

**Decided before outcomes were opened.**

§14.1 records that **5,938 of 6,629** banks pass the household-denominator rule. The
realised primary sample is **5,490**. These are consistent: §14.1's figure is the
denominator rule *alone*, measured on all filers, while the analysis sample also applies
the §2 exclusions, which §14.1 did not restate.

| Step | n |
|---|---|
| Filers with a usable book and county match | 6,619 |
| Less §2 exclusions: assets < $50m (743), monoline (16), footprint > 100 counties (20) | 5,840 |
| Less §14.1 household-denominator rule | **5,490** |
| of which training (Layer 1) | 4,582 |
| of which held out (TX ND OK NM WY AK LA WV) | 908 |
| Business-contrast sample (§14.2) | 5,443 |

The pre-registered count and the realised count differ by 448 banks, all of them accounted
for by exclusions the pre-registration already specified. No sample rule was changed.

**Consequence for power, computed before outcomes were opened.** §14.7 rescaled the MDE
from n = 6,585 to n = 5,938. At the realised n = 5,490 the factor is √(6585/5490) = 1.095,
so the §13.3 grid becomes **0.082** at ICC 0.05 and **0.112** at ICC 0.10. The power
verdict structure is unchanged: powered at the 0.10 threshold only if the realised
intra-cluster correlation is below roughly 0.10. The realised MDE governs, per §13.3.

---

## D2. Rotemberg weights are overwhelmingly concentrated in mining — a pre-committed
## reporting obligation now triggered

**Computed before outcomes were opened.**

§10, critique 1 (Goldsmith-Pinkham, Sorkin and Swift) carries this obligation:

> Rotemberg weights reported for every industry, with the top five by weight named. **If
> mining alone carries most of the weight, the design is a mining-exposure design and will
> be described as one.**

Measured: the mining sector (BEA LineCode 200) carries **0.876** of the total Rotemberg
weight. The next four are 2000 (0.025), 1600 (0.020), 400 (0.019) and 800 (0.013).

**The condition is met. This design is a mining-exposure design and is described as one
throughout RESULTS.md.** The shift-share instrument is, in substance, a single-instrument
mining-exposure design with a small fringe of other sectors, and every result that leans on
the instrument inherits that. This is not a deviation — it is the pre-registered obligation
firing exactly as written.

---

## D3. County coverage shortfalls in two controls

**Measured before outcomes were opened.**

| Control | Counties covered | Of the county frame (3,149) |
|---|---|---|
| LAUS unemployment 2013 | 3,090 | 98.1% |
| FHFA house-price growth 2011–13 | 2,706 | 85.9% |
| EFA debt-to-income rank 2013Q4 | 3,084 | 97.9% |

§12.8 anticipated the FHFA shortfall and pre-specified the handling: counties without it
are excluded from specifications using that control rather than imputed. Because the bank
controls are **deposit-weighted averages over a bank's counties**, a bank retains an FHFA
control whenever any of its counties has one, so the bank-level loss is far smaller than
the county-level shortfall suggests. Bank-level coverage is reported in RESULTS.md §2.

---

## D4. Step-7 freeze committed inside V5 rather than as its own commit

**Decided before outcomes were opened. Administrative only.**

SESSION2_PLAN step 7 says to commit the frozen pre-shock frame before outcomes are opened.
The run instruction specifies exactly two commits, V5 (verification) and V6 (results). Both
are satisfied by committing the frozen pre-shock assembly **within V5**, whose claim that
no outcome had been opened remains true at that commit. No pre-registered content is
affected.

---

## D5. Plausibility-bound violations found during the run

**After outcomes were opened.** Full detail in RESULTS.md §1, which reports them first as
the run instruction requires. Summary:

| Bound | Violations | Cause |
|---|---|---|
| `ws_pop` in [0,1] | 40 banks, max 1.439 | Real data property: BEA wages are by place of *work*, personal income by place of *residence*, so commuter-destination counties exceed 1. Not an error. |
| `gap` in [0,1] | 99 banks, min −0.383 | **The bound was mis-stated by me, not violated by the data.** Gap is a *difference* of two shares and is not itself a share; negative values are meaningful. |
| `expo_imputed` in [0,1] | 80 counties, min −0.0033 | BEA publishes negative mining earnings for some counties (sector losses). Real, small, left unaltered. |
| Charge-offs non-negative | **705** banks negative on household, 1,179 on business | Recoveries exceeded charge-offs over twelve quarters. §14.4 requires these be kept as negatives, counted and reported. Done. |

No bound violation was corrected, imputed away or excluded. The `gap` row is a defect in my
own pre-registered bound, recorded rather than quietly dropped.

---

## D6. The pre-registered placebo FAILS under the governing inference method

**After outcomes were opened. This is the most consequential item in this log.**

§10, critique 5 states: *"The design is tested on the 2011–2013 placebo window, where the
instrument should have no effect. **A significant placebo voids the primary result.**"*

The placebo was run on pre-window (2014H2) household charge-offs. Under **AKM
exposure-robust** standard errors, which §5 states **govern inference**:

| Placebo term | Coefficient | AKM 95% CI | State-clustered 95% CI |
|---|---|---|---|
| shock | +0.0432 | **[+0.0127, +0.0737]** excludes 0 | [−0.0323, +0.1187] includes 0 |
| Rival × shock | +0.0557 | **[+0.0248, +0.0867]** excludes 0 | [−0.0151, +0.1265] includes 0 |
| Gap × shock | −0.0298 | **[−0.0556, −0.0040]** excludes 0 | [−0.0954, +0.0358] includes 0 |

**The pre-registered condition is met and the primary result is voided as the
pre-registration requires.** Every confirmatory number in RESULTS.md is reported under that
voiding, prominently and at the top, not in a footnote.

The substance: the Rival interaction is **+0.0557 in the pre-period against +0.0801 in the
shock window**, so roughly 70 percent of the apparent "effect" was already present before
the shock began. That is a pre-trend, not a treatment effect.

Under state clustering the placebo passes on all three terms. The two inference methods
disagree, and the pre-registration says AKM governs. **The voiding stands.** Reporting only
the clustered result in order to keep the primary alive would be exactly the choice this
document exists to prevent.

---

## D7. The suppression-handling robustness rows vary the sample, not the instrument

**After outcomes were opened. A limitation of the executed design, not a changed
specification.**

§12.6 pre-specified three handlings of BEA mining suppression and asked for the primary
plus a robustness run on the other choice. All three were run and are reported.

But the exposure variable does **not enter the Gap specification** — it enters only by
defining which banks are "exposed" for descriptive purposes. The instrument is built from
county *industry shares* in `CAINC5N`, where suppressed mining cells are read as missing
and filled with zero **inside the instrument construction**, identically across all three
rows. So the imputed and zero rows are numerically identical (n = 4,419, θ = −0.0165), and
only the disclosed-only row differs, because it drops 896 banks from the sample.

**Consequence:** the suppression robustness is weaker than §12.6 intended. It demonstrates
insensitivity of the *estimate* to the sample, not to the *instrument's* treatment of
suppressed cells. Pre-specifying the imputation into the instrument itself would have been
the stronger design and was not done. Recorded, not fixed — fixing it now would be
specification searching after seeing outcomes.

---

## D8. One pre-registered secondary outcome was not run

**After outcomes were opened.**

§14.2 item 5 specifies a failure or assisted-merger indicator by 2018Q4, estimated by logit
and reported as log-loss. It requires the FDIC `/failures` endpoint, which SESSION2_PLAN
step 8 lists and which **was not fetched** in this run.

The outcome is therefore **missing, not null**. The Romano-Wolf family in RESULTS.md §8
contains six outcomes rather than seven, which makes that adjustment very slightly less
conservative than pre-registered.

No pre-specified alternative exists for this outcome, so none was substituted. Given that
every other secondary is null and none survives adjustment, it is unlikely to change the
verdict — but that is an expectation, not a result, and it is recorded as an omission
rather than absorbed.

---

## D9. A coding bug in the out-of-sample computation, found and fixed during the run

**After outcomes were opened. Found by self-check, fixed, and both sets of numbers are
recorded here.**

The out-of-sample models M1/M2/M3 built their instrument matrix by string-replacing
`"wage_shock"` with `"z_bartik"` in the endogenous column names. That works for
`wage_shock_s` but **silently fails** for the interaction terms `rival_x_shock` and
`gap_x_shock`, which contain no `"wage_shock"` substring. Those two terms were therefore
instrumented by themselves, i.e. treated as exogenous.

Fixed by replacing the string substitution with an explicit endogenous-to-instrument map
plus an assertion that every endogenous column has one.

| Increment | Buggy | **Corrected** |
|---|---|---|
| ΔR²_oos(M2 − M1) | +0.0025 | **−0.0330** |
| ΔR²_oos(M3 − M2) | −0.0043 | **−0.0122** |

**The coefficient table in RESULTS.md §3 was never affected** — it uses an explicitly
constructed `Z` matrix, and the Gap and Rival coefficients are identical before and after
(θ = −0.016524, rival = +0.080104). The realised ICC, design effect, MDE and power branch
are also unchanged. The robustness rows use `gapfit`, which likewise builds `Z` explicitly,
and are unaffected.

**Effect on the verdict: none, and the corrected numbers are worse.** The null held under
the buggy figures and holds more strongly under the corrected ones. This is recorded rather
than silently overwritten because the fix was made after outcomes were visible, which is
precisely the circumstance in which a reader is entitled to see both numbers.

---

## D10. Layer 2 first stages fall below the pre-registered instrument floor

**After outcomes were opened.**

§8 and §12.5 set a kill criterion at a first-stage F below 10. In Layer 2 (2020) the three
first stages are **11.5, 6.9 and 8.5** — two of them below the floor. The criterion fires,
and Layer 2 is reported as **uninformative**, not as a null.

The cause is substantive and is recorded because it bears on any future attempt: the
deposit-weighted county wage bill **rose 1.1 percent** over 2019→2020. The pandemic
destroyed low-wage employment, but composition shifts left aggregate county wages slightly
higher, so there is almost no cross-sectional wage-bill decline for a wage-channel
instrument to exploit. §6 anticipated the CARES/PPP/UI confound; it did not anticipate that
the shock itself would be near-absent in the wage-bill measure.

Layer 2 was run because SESSION2_PLAN step 13 directs it. Per §6 it could not have rescued
a Layer 1 failure in any case.

---

## Summary of what changed versus what was pre-registered

| | Count |
|---|---|
| Specifications changed after outcomes were opened | **0** |
| Samples re-cut after outcomes were opened | **0** |
| Thresholds or readings changed | **0** |
| Windows changed | **0** |
| Additional controls added to the baseline | **0** |
| Pre-registered items not executed | **2** (D8 failure logit, and the §12.2 cell-size sensitivities noted in RESULTS §7) |
| Coding bugs found and fixed during the run, with both sets of numbers reported | **1** (D9) |
| Pre-registered obligations that fired | **2** (D2 Rotemberg/mining, D6 placebo voiding) |
