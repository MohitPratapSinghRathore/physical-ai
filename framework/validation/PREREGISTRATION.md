# Pre-registration: does labour backing carry risk information?

**Committed 2026-09-20, branch `validation-pilot`, before any outcome variable for any
candidate shock period was downloaded, opened or plotted.** The git history of this
branch is the timestamp. If any commit touching an outcome series precedes this file in
the history of this branch, this document is void and the exercise is exploratory.

Author's standing commitment, stated up front: **a null result will be reported as a null
result.** If the criteria in §8 are not met, the conclusion entered into the record is
that the labour backing accounts are descriptive accounting of the claim stock and **not**
a risk measure, and the manuscript's claims about them will be confined accordingly.

**Amended by Amendment 1 (§12, 2026-09-20), which adds a third construct and changes the
decision rule; Amendment 2 (§13, 2026-09-20), which restates the confirmatory test in Gap
form, fixes a power rule, and adds a structural calibration test; and Amendment 3 (§14,
2026-09-21), which replaces the primary outcome with household-class charge-offs, adds a
business-loan contrast, and commits the calibration bands. All three were written before
any outcome variable was opened. Read §12, §13 and §14 alongside §1, §3, §4, §7 and §8:
where they conflict, the later amendment governs. §14 is the last amendment before the
run.**

---

## 1. What is being tested

Whether a bank's **labour backing**, measured *before* a local labour-income shock, adds
explanatory or predictive information about its subsequent credit losses **beyond
conventional supervisory measures**.

The exercise is adversarial by design. The prior, after the construct diagnostics in
FEASIBILITY.md §0, is that it will **not** — because the class-level coefficients are
near-binary and the composition leg is 90 percent reproducible from loan shares alone.

### Hypotheses

- **H0 (the maintained hypothesis).** Conditional on conventional controls, bank labour
  backing has no incremental association with subsequent credit losses, and no
  differential association across banks facing larger instrumented local wage shocks.
- **H1 (level).** Higher pre-shock labour backing predicts higher subsequent losses,
  conditional on conventional controls.
- **H2 (interaction, the one that matters).** The loss response to an instrumented local
  wage-bill shock is **larger in magnitude** for banks with higher pre-shock labour
  backing. This is the hypothesis that corresponds to the accounts' actual claim: labour
  backing is a measure of *exposure to labour income*, so it should show up as a
  sensitivity, not as a level.

**H2 is the primary hypothesis.** H1 is secondary. A level result without an interaction
result is weak evidence, because the level is confounded with everything that makes a
bank a household lender.

### The leg-separation requirement

Because the construct is the product of a composition leg and a geography leg, and
because a rival with no access to the accounts reproduces 94 percent of its variance
(FEASIBILITY.md §0), **every specification below is run three times**: with the full
measure, with the composition leg alone, and with the geography leg alone. In addition,
each is run against a **rival construct** built without the accounts:

    rival = (household share of book) × (county wage share)

**If the full measure does not beat the rival construct on the held-out set, the result
is reported as a win for local labour exposure and explicitly NOT as a win for the
labour backing accounts.** This is a pre-committed reporting rule, not a judgement call
to be made after seeing the numbers.

---

## 2. Sample and exclusions

- **Universe.** All FDIC-insured institutions filing at 2014-06-30 with positive assets
  and a positive loan-plus-securities book. 6,738 filers; 6,637 after requiring branch
  deposits that map to a county with BEA income data.
- **Exclusions, fixed now.**
  1. Institutions with under $50m in assets at 2014-06-30 (ratio instability).
  2. Credit-card banks and other monoline institutions: consumer share of book above
     0.90, or C&I above 0.90.
  3. Banks with no branch deposits in any county with BEA wage data (foreign, bankers'
     banks, trust-only, internet-only with a single nominal branch).
  4. Banks whose deposit footprint spans more than 100 counties — the deposit-weighted
     county wage share is not meaningful for a national footprint. Reported separately
     as a sensitivity with the threshold at 25 and at unlimited.
  5. Institutions that fail, merge or are acquired **for reasons unrelated to the
     episode** before 2015-01-01.
- **Survivorship.** Banks that fail or are acquired *during* the window are **retained**;
  see the primary outcome in §3, which is defined so that exit is not censoring.
- **Unit of observation.** The bank. One row per institution.

---

## 3. Outcomes

### Primary outcome

> **SUPERSEDED by Amendment 3, §14.1.** The primary outcome is now cumulative net
> charge-offs on HOUSEHOLD loan classes, scaled by the pre-shock household class book.
> The definition below is retained for the record and is now secondary outcome (1).

**Cumulative net charge-offs on total loans and leases, 2015Q1 through 2017Q4, as a
percentage of average gross loans over the window.** FDIC `/financials` field `NTLNLSQ`
aggregated over twelve quarters, denominated by mean `LNLSGR`.

Banks that fail or are acquired mid-window enter with charge-offs accumulated to their
last filing, annualised over the quarters filed, and carry an indicator. This makes exit
an observation rather than a missing value.

One primary outcome. One confirmatory test (H2, full measure, Layer 1 hold-out).

### Secondary outcomes

Reported with multiplicity control (§9), never substituted for the primary:

1. Peak non-performing assets ratio over the window (`P9ASSET` + nonaccrual over assets).
2. Change in tier 1 leverage ratio, 2014Q2 to 2017Q4.
3. Failure or assisted-merger indicator by 2018Q4 (rare: expect double digits at most;
   logit, and reported as log-loss rather than R²).
4. Cumulative net charge-offs on **non-mortgage consumer** loans specifically — the
   sharpest test, because that is where the accounts assign the highest coefficients.
5. Return on assets, window mean.

---

## 4. Constructs

All measured at 2014-06-30 or earlier. Definitions are fixed by this document and by
`build_constructs.py` as committed here; any later change is a deviation and is logged
in §11.

**Bank labour backing.**

    LB_bank = [ Σ_c w_c · β_c ] · wageshare(bank counties)

where `w_c` is class c's share of the bank's gross loan-plus-securities book at 2014Q2;
`β_c` is the class-level direct labour backing coefficient read unmodified from
`framework/labor_backing/claim_class_rules.csv`; and `wageshare` is the 2014 SOD
deposit-weighted mean across the bank's counties of the 2013 BEA wage-and-salary share
of personal income. Class mapping is the `CLASS_MAP` table in `build_constructs.py`.

**What variation this has that loan composition alone does not.** Stated precisely,
because the honest answer is "less than it appears": the composition leg alone is 0.899
explained by the seven loan-composition shares, so it adds little. The full measure is
0.515 explained by them, so it does carry independent variation — but that variation is
**almost entirely the geography leg**, which is orthogonal to the composition leg
(r = 0.011) and is a county wage-share exposure obtainable without the accounts. A model
of composition shares + county wage share + their interactions explains 0.939 of the
full measure. **The accounts' distinctive content in this construct is about 6 percent
of its variance.** This is disclosed here, before estimation, and governs the reporting
rule in §1.

**County labour backing.** `household debt / personal income × wage share of personal
income`, from the Federal Reserve EFA county DTI and BEA CAINC4. Variants, all
pre-specified: (a) DTI × wage share; (b) DTI × (wage + proprietors' share); (c) DTI ×
(1 − transfer share), which is the "income not insulated by transfers" reading.
**Contingent on the owner confirming the EFA county DTI start date.** If county DTI does
not reach 2013, the county leg is dropped and the fact is reported; it is not replaced
with a substitute chosen after the fact.

**Conventional benchmarks (the baseline model).** Tier 1 leverage ratio; loan
composition shares (1-4 family residential, consumer, CRE, construction, C&I,
agricultural, securities); supervisory CRE concentration (construction + CRE over tier 1
capital); log assets; deposits/assets; brokered deposits/deposits; loans/assets; county
deposit-weighted unemployment rate (LAUS, 2013); county deposit-weighted personal income
per capita (BEA, 2013); county deposit-weighted house price growth 2011–2013 (FHFA).

**Shock.** Local change in the wage bill: the deposit-weighted county change in earnings
over base-year personal income, 2014 to 2016.

**Instrument.** Bartik/shift-share from 2013 county industry shares (BEA CAINC5N,
2-digit NAICS) and national industry earnings growth 2014–2016, **leave-one-out**: the
national growth rate for each industry excludes the own county's contribution.

    z_j = Σ_k s_{jk,2013} · g_{k,−j}

aggregated to the bank by 2014 deposit weights.

---

## 5. Specifications

Let `i` index banks, `y` the primary outcome, `X` the conventional controls, `LB` labour
backing, `Δw` the local wage-bill shock instrumented by `z`.

- **(S1) Baseline.**            `y_i = α + X_i'γ + ε_i`
- **(S2) Augmented, level.**    `y_i = α + X_i'γ + δ·LB_i + ε_i`      → H1
- **(S3) Interaction, 2SLS.**   `y_i = α + X_i'γ + δ·LB_i + φ·Δw_i + **θ·(LB_i × Δw_i)** + ε_i`, with `Δw` and `LB×Δw` instrumented by `z` and `LB×z`. → **H2, θ is the coefficient of interest**
- **(S4) Rival.** S3 with `LB` replaced by `rival = household share × county wage share`.
- **(S5) Legs.** S3 with `LB` replaced by the composition leg, and again by the geography leg.

Standard errors clustered by state, and separately by the Adão–Kolesár–Morales
exposure-robust method (§10). Both reported; the AKM version governs inference.

Functional form fixed now: outcome in percentage points, untransformed, winsorised at the
1st and 99th percentiles. `LB` and `Δw` standardised to mean 0 SD 1 within the training
set only, so that θ is read per standard deviation and the held-out set is not used to
set the scaling.

---

## 6. Held-out design, fixed now

- **Layer 1 (primary, confirmatory).** Train on banks whose deposit-weighted footprint is
  majority outside {TX, ND, OK, NM, WY, AK, LA, WV}; test on the rest. Chosen before any
  outcome was seen. This holds out the bulk of oil exposure and is the harder test.
- **Layer 2 (secondary).** The 2020 episode, construct rebuilt on 2019Q2 balance sheets
  and 2018 county income, outcome window 2020Q1–2022Q4. Confounded by CARES/PPP/UI, which
  is stated in advance and is why it cannot rescue a Layer 1 failure.

The training set is used for all model selection, winsorisation limits and standardisation.
The held-out set is touched **once**, at the end, and the result of that single pass is
what is reported.

---

## 7. Metric for incremental information

1. **Out-of-sample R²** on the held-out set for S1 versus S2/S3, fit on training only:
   `ΔR²_oos = R²_oos(augmented) − R²_oos(baseline)`. For the binary outcome, improvement
   in **log-loss** instead.
2. **The interaction coefficient θ from S3, with its 95 percent confidence interval**,
   AKM exposure-robust.
3. The same two quantities for the rival construct (S4) and for each leg (S5).

---

## 8. Success and kill criteria, as numbers

**Success requires all three, on the Layer 1 held-out set:**

1. `ΔR²_oos ≥ 0.02` for S3 over S1 (two percentage points of held-out variance); **and**
2. θ has the predicted sign (higher labour backing → larger loss response to a negative
   wage shock) with a 95 percent AKM CI excluding zero, and |θ| ≥ 0.10 standard
   deviations of the outcome per SD×SD; **and**
3. the full measure beats the rival construct: `ΔR²_oos(S3) − ΔR²_oos(S4) ≥ 0.005`.

**Kill criteria — any one of these and the result is reported as a null:**

1. `ΔR²_oos ≤ 0.005` for S3 over S1; **or**
2. the 95 percent CI for θ includes zero; **or**
3. `ΔR²_oos(S3) ≤ ΔR²_oos(S4)`, i.e. the accounts add nothing over the rival; **or**
4. the first-stage F for the shift-share instrument is below 10.

**The zone between.** If criteria 1 and 2 are met but 3 is not, the finding is reported
as **"local labour exposure predicts losses; the labour backing accounts add nothing
beyond it."** That is a real finding about the accounts and it is a negative one. It will
be stated in those words.

---

## 9. Multiple testing

- **One confirmatory test.** H2, full measure, primary outcome, Layer 1. Nothing else can
  establish the claim.
- The five secondary outcomes are a family: **Romano–Wolf stepdown** p-values over 10,000
  bootstrap replications, reported alongside unadjusted values. Holm–Bonferroni reported
  as a conservative cross-check.
- The leg and rival specifications (S4, S5) are **diagnostic, not confirmatory**; they can
  only weaken the claim, never establish it, so they carry no multiplicity penalty.
- Sensitivity variants (footprint thresholds, county-leg variants, winsorisation) are
  reported as a **specification curve** over all combinations, with the pre-registered
  specification marked. No p-value from the curve is used for inference.

---

## 10. Known critiques of shift-share designs, and how each is reported

The design is a Bartik instrument and inherits the full set of objections. Each is
reported, not merely acknowledged:

1. **Goldsmith-Pinkham, Sorkin and Swift (2020).** Identification comes from the exposure
   shares, not the shocks; the estimator is a weighted sum of just-identified IVs.
   → **Rotemberg weights reported for every industry**, with the top five by weight named.
   If mining alone carries most of the weight, the design is a mining-exposure design and
   will be described as one. Pre-industry balance tests on the high-weight industries.
2. **Borusyak, Hull and Jaravel (2022).** Validity can instead rest on quasi-random
   *shocks* with many independent ones. → The shock-level (industry-level) specification
   is reported in parallel, with the effective number of independent shocks.
3. **Adão, Kolesár and Morales (2019).** Conventional standard errors over-reject badly
   because observations with similar exposure have correlated residuals. → **AKM
   exposure-robust standard errors govern inference**; state-clustered are shown only for
   comparison.
4. **Leave-one-out.** National growth excludes own-county contribution, so mechanical
   correlation between the shock and own-county outcomes is removed.
5. **Pre-trends.** The design is tested on the 2011–2013 placebo window, where the
   instrument should have no effect. A significant placebo voids the primary result.

---

## 11. What will be reported if the result is null

The null is the expected outcome and it is a publishable one. It will be reported as:

> Bank labour backing measured before the 2014–2016 oil-price collapse did not add
> information about subsequent credit losses beyond conventional supervisory measures.
> The point estimate on the interaction was θ = [value], 95 percent CI [.., ..], and the
> out-of-sample R² improvement was [value] against a pre-registered threshold of 0.02.

with the full specification curve, both legs, the rival construct, and the Rotemberg
weights, in the same document and at the same prominence as a positive result would have
received.

**And the standing consequence, committed now:**

> The labour backing accounts stand as **descriptive accounting of the claim stock**, not
> as a risk measure. They describe what services a claim in the first round. They do not,
> on this evidence, forecast who loses money when labour income falls. Any language in
> the manuscript implying predictive or supervisory risk content will be removed or
> confined to an explicit conjecture with this null attached.

A null does not retract the sovereign-concentration finding, which is a measurement of
who holds the claims and does not depend on predictive validity. That distinction will be
drawn explicitly so the null is neither overread nor underread.

**Deviations log.** Any departure from this document is recorded here with its date, its
reason, and whether it was decided before or after seeing held-out outcomes. An empty log
is a claim that there were none.

| Date | Deviation | Reason | Before/after hold-out seen |
|---|---|---|---|
| 2026-09-20 | Amendment 1 (§12): third construct added, decision rule now three nested models | Feasibility showed the coefficients are near-binary, so the original measure is 94% reproducible without the accounts | Before. No outcome variable had been opened. |
| 2026-09-20 | Amendment 2 (§13): confirmatory test restated in Gap form as the primary presentation; power rule fixed; structural calibration test added | The Gap is the accounts' entire distinctive contribution, so it should be the estimand rather than something recovered by differencing two models | Before. No outcome variable had been opened. |
| 2026-09-21 | Amendment 3 (§14): primary outcome changed from total net charge-offs to household-class net charge-offs; business-loan contrast added as a pre-stated placebo; structural calibration bands committed | Exposed banks carry half again as much C&I lending (median share 0.167 against 0.108), so energy-business losses would have masqueraded as a wage-channel result in a total-loss outcome | Before. No outcome variable had been opened. |

---

## 12. Amendment 1, 2026-09-20: the debtor-specific construct

**Written and committed before any outcome variable for any candidate shock period was
downloaded, opened or plotted.** Where this section conflicts with §1, §4, §7 or §8, this
section governs.

### 12.1 Why

The feasibility check found the accounts' class coefficients are near-binary — every
household class between 0.727 and 0.883, every business class 0.0 by rule. A bank measure
built from them is therefore close to a relabelling of the household share of the book: a
rival researcher using only FDIC loan shares and the **population-wide** county wage share
reproduces **94 percent** of its variance.

That diagnostic points at where any distinctive content must live. The population-wide
wage share is the wage dependence of a county's residents in aggregate. What the accounts
actually assert is a claim about **debtors** — the households that owe the mortgage or the
card balance. Those are not the same people, and a county's mortgage holders can be far
more wage-dependent than the county as a whole. Amendment 1 therefore adds a third
construct that measures wage dependence **among debtors specifically**, and makes it the
only construct that can vindicate the accounts.

### 12.2 The debtor-specific local wage shares

**Vintage, stated as required.** ACS **2009–2013 5-year PUMS**, restricted to records
carrying `PUMA10` — survey years 2012–2013 on 2010 PUMA geography.

Two facts forced this choice and both are disclosed:

1. **The repo's own ACS is the 2023 1-year file**, which is *post-shock* for every
   candidate episode and cannot be used for a pre-shock construct. The 2013 vintage was
   downloaded for this purpose. This is a departure from the instruction to build from the
   ACS already in the repo, and the reason is that the instruction's own pre-shock
   requirement overrides it.
2. The 2009–2013 5-year file mixes 2000- and 2010-definition PUMAs. Restricting to
   `PUMA10` keeps one geography and matches the 2010 tract-to-PUMA crosswalk. The cost is
   roughly three fifths of the 5-year sample; **6,019,599 households** remain.

**Definition.** For each PUMA and each debtor group, the aggregate wage share of household
income:

    wageshare(g) = Σ_h w_h · wage_h  /  Σ_h w_h · income_h    over households h in group g

where `wage_h` is the sum of person-level `WAGP` within the household, `income_h` is
`HINCP`, both put in constant 2013 dollars by `ADJINC`, and `w_h` is `WGTP`. Households
with non-positive `HINCP` are excluded from the ratio.

Groups: **mortgage** (`TEN` = 1, owned with a mortgage), **renter** (`TEN` = 3), **all**
occupied households. Payment-weighted variants use `w_h · MRGP · 12` for mortgage holders
and `w_h · GRNTP · 12` for renters, which matches the mortgage-service weighting the
accounts already use.

**Coverage and cell sizes, reported as required**, 2,402 PUMAs:

| Group | PUMAs | Median cell (unweighted households) | Cells below 100 | County wage share, median |
|---|---|---|---|---|
| Mortgage | 2,402 | 430 | 16 | 0.7845 |
| Renter | 2,402 | 254 | 85 | 0.7753 |
| All | 2,402 | 968 | 0 | 0.6856 |

**Minimum cell-size rule, fixed now.** A PUMA × group cell with fewer than **100**
unweighted households is dropped before aggregation to counties. A county with no
surviving PUMA cell for a group is missing for that group and is excluded from the primary
sample for specifications using it; the count of such counties is reported. The threshold
is 100, chosen now and not after seeing results; 50 and 200 are reported as sensitivities.

**PUMA to county.** 2010 tract-to-2010-PUMA crosswalk, aggregated with **housing-unit**
weights (`HU10` from the Census tract gazetteer) rather than tract counts. The repo's
existing crosswalk uses tract counts and its own code flags that as an approximation;
housing units are the correct basis for a household-level measure. 2,378 PUMAs map to
3,221 county parts; the county wage shares cover 3,143 counties for the mortgage and all
groups and 3,131 for renters.

### 12.3 The bank-level debtor-specific measure

    LB_debtor = Σ_c  w_c · β_c · wageshare_debtor(group(c), bank counties)

with the group matched to the class: **mortgage-holder** share for 1–4 family residential;
**renter** share for multifamily (the tenant pays the rent that services it, which is the
accounts' own reasoning); **all-household** share for card, auto, other consumer, Treasury
and municipal holdings; **zero by rule** for every business class, unchanged. The local
share is the 2014 SOD deposit-weighted mean across the bank's counties.

The rival, unchanged from §1:

    LB_rival = [ Σ_c w_c · β_c ] · wageshare_population(bank counties)

### 12.4 Pre-shock result, reported before any outcome, verdict first

6,619 banks at 2014-06-30. **The rival alone explains 0.640 of the debtor-specific
measure, which is below the 0.90 threshold set for abandoning the refinement. The
refinement therefore does have content the rival lacks, and the pilot proceeds with three
constructs rather than two.**

That is the favourable reading and it is real. The unfavourable reading is also real and
is stated next to it:

| Information set available to a rival with no access to the accounts | R² explaining `LB_debtor` |
|---|---|
| Rival construct alone | **0.640** |
| Population-wide county wage share alone | 0.007 |
| Loan composition shares alone | 0.874 |
| **Composition shares + population wage share + interactions** | **0.888** |
| Rival construct + loan composition shares | **0.917** |

On the benchmark that was used for the original measure — composition shares plus the
population wage share plus interactions — the distinctive content rises from
**6.1 percent** of variance (original measure, R² 0.939) to **11.2 percent**
(debtor-specific, R² 0.888). **The refinement roughly doubles the accounts' distinctive
content and it is still about one ninth of the variance.** Nobody should read §12.4 as a
vindication.

Supporting quantities:

| Quantity | Value |
|---|---|
| corr(`LB_debtor`, `LB_rival`) | 0.800 |
| corr(mortgage-holder wage share, population wage share), bank level | **0.332** |
| corr(all-household wage share, population wage share), bank level | 0.521 |
| corr(mortgage-holder wage share, all-household wage share) | 0.818 |
| Mean mortgage-holder wage share / all-household / population | 0.797 / 0.713 / 0.433 |

The 0.332 is where the new information is: the wage dependence of a county's mortgage
holders is close to unrelated to the wage dependence of the county as a whole. The level
difference between 0.797 and 0.433 is mostly denominator, not signal — ACS household
income excludes items BEA personal income includes — so only the cross-sectional variation
is used, never the level.

**Payment weighting adds nothing.** The payment-weighted construct correlates 0.799 with
the rival against 0.800 for the household-weighted version, and its R² against every
information set above matches to three decimals. It is retained as a pre-specified
sensitivity and is **not** the primary construct. (An earlier run showed a much larger
difference; that was a coding error in which the undefined payment weight for the
all-household group was written as zero, and it is recorded here so the corrected number
is not mistaken for a revision of a real finding.)

### 12.5 Amended hypotheses and decision rule

The confirmatory test is unchanged in form — H2, the interaction with the instrumented
local wage shock, primary outcome, Layer 1 hold-out. There are now **three nested models**:

- **(M1) Baseline.** Conventional controls only. (§5 S1)
- **(M2) Baseline + rival.** Adds `LB_rival` and its interaction with the instrumented shock.
- **(M3) Baseline + rival + debtor-specific.** Adds `LB_debtor` and its interaction, **on top of M2**.

`LB_debtor` is entered alongside the rival, not instead of it, so that its coefficient is
identified off the variation the rival does not contain.

**Success for the ACCOUNTS requires M3 to beat M2** — not merely M1 — on the Layer 1
held-out set:

1. `ΔR²_oos(M3 − M2) ≥ 0.02`; **and**
2. the interaction coefficient on `LB_debtor × instrumented shock` has the predicted sign
   with a 95 percent AKM exposure-robust CI **excluding zero**, and magnitude ≥ 0.10 SD
   per SD×SD.

The numeric thresholds are unchanged from §8 and are deliberately applied to the M3-over-M2
increment rather than to M3-over-M1.

**Kill criteria, amended.** Any one of these and the accounts are reported as adding
nothing:

1. `ΔR²_oos(M3 − M2) ≤ 0.005`; **or**
2. the CI on the `LB_debtor` interaction includes zero; **or**
3. the first-stage F for the shift-share instrument is below 10.

**The reporting rule, restated so it cannot be evaded.** If M2 beats M1 but M3 does not
beat M2, the result is reported in these words: **"local labour exposure predicts losses;
the labour backing accounts add nothing beyond it."** If neither beats M1, the result is
the null of §11. Only M3 beating M2 vindicates the accounts, and the §11 null language
stands for every other outcome.

§8's original criteria continue to govern the *original* `LB_bank` measure, which is still
estimated and reported. They no longer decide the fate of the accounts; §12.5 does.

### 12.6 Mining-earnings suppression, pre-specified

BEA suppresses county mining earnings with `(D)` where publication would disclose an
individual employer: **1,324 of 3,127 counties** in 2013, plus 14 `(NA)`. Suppressed
counties are small-but-nonzero, never zero, and they remain inside the state total.
Measured now:

- Suppressed earnings are **5.4 percent** of state mining totals pooled, so the hidden
  quantity is small in aggregate — but the residual exceeds 10 percent of the state total
  in **33 of 48** states, because suppression bites hardest where mining is small.
- **2,193 banks** hold more than half their deposits in suppressed counties; 3,198 hold
  none.
- QCEW publishes a mining **establishment count** for **1,296 of the 1,324** suppressed
  counties even though it suppresses their wages, so an allocation basis exists.

**Primary sample, fixed now: impute.** For each state, the residual (state mining earnings
less the sum of its disclosed counties) is allocated across that state's suppressed
counties **in proportion to QCEW 2013 private mining establishment counts**
(`industry_code` 21, `agglvl_code` 74, `own_code` 5). A suppressed county with no QCEW
establishment row is assigned zero. Exposure is then `imputed mining earnings / county
earnings` on the same footing as disclosed counties.

**Robustness run on the other choice, also fixed now:** restrict to the 1,789 counties with
disclosed values, dropping suppressed counties from the exposure measure entirely
(`disclosed-only`). A third variant sets suppressed counties to zero.

**How the exposed-bank sample changes**, deposit-weighted 2014, as measured:

| Exposure threshold | Suppressed treated as zero | Disclosed-only | Difference |
|---|---|---|---|
| > 2% | 1,266 banks | 1,361 | +95 |
| > 5% | 842 | 908 | +66 |
| > 10% | 461 | 504 | +43 |

The exposed sample moves by under 10 percent across handlings, so the design is not
fragile to this choice. The imputed variant is expected to sit between the two and its
count is reported in the run. If the primary and robustness runs disagree on the §12.5
verdict, **the disagreement is the finding** and both are reported with equal prominence.

### 12.7 EFA county debt-to-income: interval-valued, handled as a rank

The owner's handoff warned that the EFA county download gives interval bounds rather than
point estimates. Confirmed from the file: `household-debt-by-county.csv`, 338,868 rows,
**1999Q1 to 2025Q4 quarterly** (start date now verified from the bytes, not documentation),
3,139 counties in 2013Q4, each row carrying only `low` and `high`.

Inspection of the 2013Q4 bins shows **nine roughly equal-count bins** (312, 297, 300, 294,
347, 297, 317, 337, 327 counties), widths 0.18 to 0.82. The variable is therefore in
substance an **ordinal rank**, not a censored continuous measure.

**Pre-specified handling: use the bin index as an ordinal rank**, rescaled to [0,1] by
`(bin − 1)/8`, and enter it as a rank regressor. **Bin midpoints will not be used as
observed continuous values**, per the owner's warning. Sensitivities, fixed now: (a) bin
midpoint, reported only as a robustness check and never as the primary; (b) the bin index
as a set of eight dummies. Connecticut's planning-region conversion affects recent years
only; 2013Q4 carries the eight historic counties and the pre-shock construct is unaffected.

This makes the county labour backing construct of §4 feasible on a rank basis. The §4
contingency — "if county DTI does not reach 2013, the county leg is dropped" — is **not**
triggered: coverage reaches 1999.

### 12.8 FHFA county house prices

Owner-fetched file verified: SHA256 `534e9fd3…df79afd1` matches the handoff. 106,253 rows,
1975–2025, 2,796 unique counties. **2,757 counties carry both 2011 and 2013 index values**,
so the pre-shock house-price control of §4 is available for 2,757 of 3,113 counties.
Counties without it are reported and are excluded from specifications using that control
rather than having it imputed. One malformed 9-character FIPS row is dropped.

---

## 13. Amendment 2, 2026-09-20: the Gap form, its power, and a structural calibration test

**Written and committed before any outcome variable for any candidate shock period was
downloaded, opened or plotted.** No script in `framework/validation/` reads a charge-off,
non-performing, ROA or failure field. The *predicted* loss of §13.4 is built here; the
*realised* loss it will be tested against is not touched.

Where this section conflicts with §12, this section governs. §12.5's three nested models
survive as reported alternatives; §13.3 replaces them as the **primary presentation**.

### 13.1 The algebra, recorded

The measure is

    LB = Σ_c  w_c · β_c · ω_c

where `w_c` is class c's share of the bank's loan-plus-securities book, `β_c` the class
labour backing coefficient, and `ω_c` the local wage share applying to class c.

The coefficients take two values and essentially only two. Write `β_H` for the household
classes — home mortgage 0.840, credit card 0.740, auto 0.774, other consumer 0.816,
multifamily 0.728, a range of 0.11 around a mean near 0.80 — and `β_B = 0` for every
business class by rule. Then, if a single local wage share `ω` is applied to every class,

    LB ≈ β_H · ω · Σ_{c ∈ H} w_c  =  β_H · ω · h

where `h` is the **household share of the book**. That is the whole identity: a constant
times the household loan share times the local wage share. Both `h` and `ω` are public —
`h` from the call report, `ω` from BEA — so a rival with no access to the accounts can
build `β_H · ω · h` up to the constant, which a regression absorbs. This is why the rival
reproduces the measure, and it is an algebraic fact about the coefficient vector, not an
empirical accident. It was confirmed empirically in §12.4 at R² 0.917.

The residual `Σ_c w_c (β_c − β_H) ω` is the within-household spread of the coefficients.
It is small because the spread is small.

**It follows that the accounts can only contribute through `ω_c` varying by class** — that
is, through debtor-specific wage shares. Hence:

### 13.2 The decomposition LB_debtor = Rival + Gap

    LB_debtor = Σ_c w_c · β_c · ω_c^debtor
    Rival     = (Σ_c w_c · β_c) · ω^pop
    Gap       = LB_debtor − Rival = Σ_c w_c · β_c · (ω_c^debtor − ω^pop)

**Gap is the accounts' entire distinctive contribution in this design.** Everything else in
`LB_debtor` is reproducible from public loan shares and the population-wide wage share.

**Measured on pre-shock data, 6,585 banks at 2014-06-30:**

| Quantity | Value |
|---|---|
| Var(Gap) | **0.005423** |
| SD(Gap) | 0.073639 |
| SD(Rival) | 0.092768 |
| SD(LB_debtor) | 0.122442 |
| SD(Gap) / SD(LB_debtor) | **0.601** |
| Var(Gap) / Var(LB_debtor) | **0.362** |
| **corr(Gap, Rival)** | **0.0705** |

Two things follow and they point in opposite directions, so both are stated.

**Favourable.** Gap is **not** a rounding error: it carries 36 percent of the variance of
the debtor-specific measure, and it is **nearly orthogonal to the Rival** (r = 0.07). That
orthogonality is what makes the §13.3 test identifiable — the two regressors will not
fight each other.

**Unfavourable.** Gap is substantially a **loan-composition** object, not a pure
debtor-wage-dependence object. Its correlations with the conventional controls:

| Control | corr with Gap |
|---|---|
| 1–4 family residential share | **0.558** |
| C&I share | **−0.416** |
| CRE share | −0.347 |
| Supervisory CRE concentration | −0.262 |
| Log assets | −0.184 |
| Agricultural share | −0.178 |
| Brokered / deposits | −0.166 |
| Construction share | −0.165 |
| Securities share | 0.150 |
| Loans / assets | −0.137 |
| Consumer share | 0.094 |
| **Rival** | **0.071** |
| Tier 1 leverage | 0.062 |
| Deposits / assets | 0.024 |

A bank's Gap is driven more by how much residential mortgage it holds than by anything
specific to its debtors: the `w_c` weights in `Σ_c w_c β_c (ω_c − ω^pop)` move more than
the `(ω_c − ω^pop)` differentials do. **The conventional controls must therefore be in the
regression for the Gap coefficient to mean what it claims to mean**, and §13.3 keeps them
there. If a run is ever reported without them, the Gap coefficient is a mortgage-share
coefficient wearing a different name.

**Distribution across banks**, and across the exposed sample (deposit-weighted 2013 mining
exposure above 10 percent, 461 banks):

| | All banks | Exposed banks |
|---|---|---|
| Mean | 0.1233 | 0.1126 |
| SD | 0.0736 | 0.0636 |
| p10 | 0.0427 | 0.0399 |
| Median | 0.1141 | 0.1086 |
| p90 | 0.2198 | 0.1951 |

Gap is positive essentially everywhere — a county's debtors are more wage-dependent than
its population, always — so the identifying variation is in its *magnitude*, not its sign.
The exposed sample is slightly tighter than the full sample (SD 0.064 against 0.074), which
costs a little power exactly where the shock bites.

### 13.3 The confirmatory test, restated in Gap form

**This is now the primary presentation.** It is algebraically equivalent to M3 versus M2
of §12.5, since `LB_debtor = Rival + Gap` and both enter linearly.

    y_i = α + X_i'γ
        + φ_R · Rival_i + φ_G · Gap_i
        + λ · Δw_i
        + ρ · (Rival_i × Δw_i)
        + **θ · (Gap_i × Δw_i)**
        + ε_i

`X` is the full conventional control set of §4, `Δw` the local wage-bill shock instrumented
by the leave-one-out shift-share `z` of §4, and both interactions instrumented by
`Rival × z` and `Gap × z`. Rival and Gap are standardised to mean 0 SD 1 **within the
training set only**.

**The accounts' contribution is θ, the coefficient on Gap × shock, and the out-of-sample
increment from adding that term.** The thresholds are unchanged from §8 and §12.5:

1. `ΔR²_oos` from adding `Gap` and `Gap × Δw` to the Rival-only model ≥ **0.02**; **and**
2. θ has the predicted sign with a 95 percent AKM exposure-robust CI excluding zero, and
   |θ| ≥ **0.10** outcome SD per SD×SD.

M1, M2 and M3 are still estimated and reported, as alternatives, with the note that M3−M2
and the Gap term are the same test.

#### The power rule, fixed in advance

Gap's pre-shock variance is small in absolute terms, so a null must be readable as *no
effect* or *underpowered* by a rule set before the data are seen.

Computed on pre-shock data: SD of the standardised `Gap × shock` interaction is **1.063**;
its R² on the controls and the Rival interaction is **0.065**, leaving a residual SD of
**1.028**; n = 6,585 in 53 state clusters, mean cluster size 124.

The minimum detectable effect at 80 percent power and a 5 percent two-sided test, in
outcome standard deviations, is dominated by the **clustering design effect**:

| Intra-cluster correlation | Design effect | MDE at model R² 0.10 | at 0.30 | at 0.50 | Powered at 0.10? |
|---|---|---|---|---|---|
| 0.00 | 1.00 | 0.032 | 0.028 | 0.024 | yes |
| 0.02 | 3.46 | 0.059 | 0.052 | 0.044 | yes |
| **0.05** | **7.16** | 0.085 | **0.075** | 0.064 | **yes** |
| 0.10 | 13.32 | 0.116 | 0.103 | 0.087 | **no** (except at R² 0.50) |
| 0.20 | 25.65 | 0.161 | 0.142 | 0.120 | no |

**The study is powered for the 0.10 threshold if and only if the intra-cluster correlation
of the outcome across states is below roughly 0.10.** That is not knowable now, and
pretending otherwise would be the kind of assumption this document exists to prevent.

**Pre-committed rule.** In the run, the realised design effect is computed from the ratio
of the state-clustered variance to the unclustered variance of θ̂, and the realised MDE is
computed from it. Then:

- If the CI on θ excludes zero and |θ̂| ≥ 0.10 → **the accounts contribute** (subject to
  the other §12.5 criteria).
- If the CI includes zero **and** the realised MDE ≤ 0.10 → **"no effect"**. The design
  could have seen an effect of the pre-registered size and did not.
- If the CI includes zero **and** the realised MDE > 0.10 → **"underpowered"**. The
  result is reported as uninformative about the accounts, explicitly **not** as a null,
  and the realised MDE is quoted so a reader can see what the study could and could not
  have detected.

The third branch is a real possibility, not a hedge, and it is written here so that it
cannot be chosen after seeing the answer.

### 13.4 Structural calibration test, no free parameters

For each bank,

    predicted_loss_i = Σ_c  loans_{i,c} · β_c · ω_{i,c} · dose_i · s_c

with `dose_i` the deposit-weighted fractional decline in the county wage bill 2014→2016,
floored at zero, and `s_c` the class loss sensitivity taken **unchanged** from the
manuscript's household credit engine.

#### The engine values, recorded before outcomes are touched

**Source file:** `data/processed/verify/hand_check_credit.csv`
**Commit:** `origin/master` at `0b5f2b8` (A138, "revision round 2")
**Git blob:** `233e413becfec072b4a5f4cc6357f9f6e7499f79`
**SHA256 of contents:** `a70b6ca41a4bb57dde30393428e41f27cb340c9316f7e614ce4a37c09ef37726`
21 lines, 4 loan classes × 5 dose levels.

Loss given default, read off as `loss_lo_bn / exposure_at_default_bn` and
`loss_hi_bn / exposure_at_default_bn`, constant across dose to five decimals:

| Class | LGD low | LGD high |
|---|---|---|
| Mortgage | 0.25 | 0.40 |
| Card | 0.80 | 1.00 |
| Auto | 0.45 | 0.65 |
| Student | 0.75 | 1.00 |

Effective default uplift per unit dose, `(exposure_at_default / total_balance) / 0.05`
taken at the engine's lowest dose (0.05), which is the closest grid point to the shocks
actually observed:

| Class | Uplift per unit dose | s_lo | s_mid | s_hi |
|---|---|---|---|---|
| Mortgage | 0.083039 | 0.020760 | 0.026988 | 0.033215 |
| Card | 0.081397 | 0.065118 | 0.073258 | 0.081397 |
| Auto | 0.082222 | 0.037000 | 0.045222 | 0.053445 |
| Student | 0.080090 | 0.060068 | 0.070079 | 0.080090 |

`s = uplift_per_unit_dose × LGD`. These twelve numbers are the whole calibration and
none of them is fitted. The engine's default uplift is class-invariant at each dose
(0.3756pp at dose 0.05, rising to 5.0957pp at dose 0.75); the small class differences in
the uplift column come from differing balance-to-borrower ratios, and are the engine's own.

**Class mapping, fixed now.** `LNRERES` → mortgage; `LNREMULT` → mortgage (property-secured
proxy; the engine has no multifamily class, and this is flagged as the one judgement call
in the mapping); `LNCRCD` → card; `LNAUTO` → auto; `LNCONOTH` → student (the residual
consumer line, which is where bank-held student debt sits). Business classes carry β = 0
and drop out. Securities carry no credit loss in this window and are set to zero.

**Robustness, pre-specified:** the engine's full non-linear dose grid with piecewise-linear
interpolation, instead of the low-dose linearisation. The observed doses are small enough
that the two should agree closely; if they do not, both are reported.

#### The test

Regress realised cumulative net charge-offs over the §3 window, scaled by pre-shock gross
loans, on `predicted_loss` scaled the same way. Report the slope, its AKM exposure-robust
interval, the intercept, and out-of-sample fit in the Layer 1 held-out states. Run it
**twice**, once with `ω = ω^pop` (rival wage share) and once with `ω = ω_c^debtor`, and
report both. Run the `s_lo`, `s_mid` and `s_hi` variants.

**Pre-committed reading, fixed now:**

- Slope interval **contains 1** → **"engine calibrated"**.
- Slope **significantly positive but excluding 1** → **"direction right, magnitude off by
  a factor of β̂"**, with the factor stated explicitly as the point estimate and interval.
- Slope **indistinguishable from zero** → **"engine not supported in this episode"**.
- Slope significantly **negative** → reported as such; it would contradict the engine.

#### Two problems with this test, measured now and stated before it is run

These are disclosed in advance because both will shape how the result must be read, and
neither is visible from the design alone.

**Problem 1: only 806 of 6,585 banks have a non-zero predicted loss.** The dose is a
*decline* in the county wage bill, and the national wage bill **rose 5.7 percent** over
2014–2016. Only 806 banks had a deposit-weighted wage-bill decline; for the other 88
percent the structural prediction is exactly zero. The regression is therefore identified
off 806 banks, of which the mining-exposed subset does most of the work. The effective
sample is an order of magnitude smaller than the headline n, and the slope's interval will
reflect that.

**Problem 2: the predicted losses are very small in absolute terms.** Predicted loss as a
percentage of pre-shock gross loans:

| Variant | Mean, all banks | Mean, exposed banks | p90 | Max |
|---|---|---|---|---|
| Rival ω, s_mid | 0.0042% | 0.0388% | 0.0031% | 0.515% |
| Debtor ω, s_mid | 0.0073% | 0.0644% | 0.0065% | 0.709% |

Realised cumulative net charge-offs over twelve quarters are, for typical banks, on the
order of tenths of a percent to a few percent of loans. **The engine's marginal prediction
is one to two orders of magnitude smaller.** The intercept will absorb baseline losses, so
the slope tests only the marginal relationship — but the strong prior, stated now, is that
the slope will land **far above 1**, and the most likely verdict is therefore **"direction
right, magnitude off by a factor"** rather than "engine calibrated". If the slope does come
back near 1, that should be treated as surprising and checked rather than celebrated.

Stating this in advance is the point: a slope of 30 reported without this paragraph would
look like a refutation of the engine, when it is substantially a statement about the size
of the doses the oil episode actually delivered.

**A third limitation, on what the test can distinguish.** The rival-ω and debtor-ω versions
of the predicted loss correlate at **0.946**. The structural test therefore has very little
power to say which wage share is the right one; it tests the engine's magnitude, not the
accounts' distinctive content. **Only §13.3 tests the accounts.** The two must not be
conflated in the write-up, and a favourable structural result is not evidence for the
accounts.

### 13.5 Relationship to the existing criteria

§8 governs the original `LB_bank`. §12.5 governs M1/M2/M3. §13.3 is the primary
presentation and is equivalent to M3−M2. §13.4 is a separate question — whether the
manuscript's engine is quantitatively right — and carries its own reading, above. A null
in §13.3 and a favourable §13.4, or the reverse, is a coherent and reportable outcome; the
two are not substitutes and neither rescues the other.

---

## 14. Amendment 3, 2026-09-21: outcome split, calibration bands, engine verification

**The last amendment before the run. Written and committed before any outcome variable for
any candidate shock period was downloaded, opened or plotted.** Where this section
conflicts with §3, §12 or §13, this section governs.

Disclosure of what was touched to write this section: FDIC field *names* were validated by
requesting them with a filter matching zero rows, and separately on the **pre-shock**
2014-06-30 quarter printing only the returned key names, never a value. Pre-shock loan
balances and the owner-fetched LAUS file were read as predictors. No charge-off,
non-performing, failure or ROA **value** for any quarter was retrieved.

### 14.1 What the primary outcome was, and what it now is

**It was total.** §3 specified "cumulative net charge-offs on total loans and leases,
2015Q1 through 2017Q4, as a percentage of average gross loans", field `NTLNLSQ` over
`LNLSGR`.

**That is now wrong and is replaced.** Banks in oil counties lost directly on
energy-related *business* lending. Those losses are a first-order consequence of the oil
price, not of the wage channel, and in a total-charge-off outcome they would load onto the
shock and onto anything correlated with it — including the Gap — and masquerade as a
wage-channel result.

The concern is not hypothetical. Measured on pre-shock 2014Q2 balance sheets:

| | Median C&I share of gross loans |
|---|---|
| Exposed banks (mining exposure > 10%) | **0.167** |
| All other banks | **0.108** |

Exposed banks carry **half again as much C&I lending** as everyone else. A total-loss
outcome would be substantially an energy-business-loss outcome in exactly the subsample
that identifies the design.

**The primary outcome is now: cumulative net charge-offs on HOUSEHOLD loan classes —
residential real estate, credit card, auto, other consumer — over 2015Q1 to 2017Q4, scaled
by pre-shock (2014-06-30) loans in those same classes.**

    numerator   = Σ over quarters of  NTRERES + NTCRCD + NTAUTO + NTCONOTH
    denominator = LNRERES + LNCRCD + LNAUTO + LNCONOTH  at 2014-06-30

Scaling by the **pre-shock** class book rather than a window average keeps the denominator
untouched by the shock and outside the outcome definition.

This is the outcome the accounts actually make a claim about. The labour backing
coefficients are non-zero only on household classes; business classes are zero by rule. An
outcome confined to household classes is therefore the one the theory predicts, and
narrowing it is a tightening of the test, not a weakening.

**Sample rule, fixed now.** A bank enters the primary analysis only if its household class
book is at least **5 percent of gross loans and at least $5 million** at 2014-06-30.
Measured: **5,938 of 6,629 banks qualify (89.6 percent), including 407 exposed banks.**
Banks failing the rule are excluded from the primary outcome and reported as excluded.

### 14.2 Secondary outcomes, including the business-loan contrast

Reported with the §9 multiplicity control. The multiplicity family is amended to:

1. **Total net charge-offs** (`NTLNLSQ` over `LNLSGR`) — the former primary, retained so
   the effect of the redefinition is visible rather than hidden.
2. **Business-loan net charge-offs as a placebo-style contrast**: C&I plus commercial real
   estate (`NTCI + NTRENRES`), scaled by `LNCI + LNRENRES` at 2014-06-30. Denominator rule
   as above: **5,762 banks qualify (86.9 percent), 415 exposed.** 5,388 banks qualify on
   both splits, 385 of them exposed.
   **Pre-stated expectation: the Gap term should NOT predict business-loan charge-offs once
   the controls are in.** The accounts assign business classes a coefficient of zero, so a
   Gap effect here would indicate the Gap is proxying for local economic distress in
   general rather than for household wage dependence.
   **If the Gap predicts business-loan losses as strongly as household losses, the
   household result is not evidence for the accounts** and will be reported as a general
   local-distress effect. This is a pre-committed reading.
   A variant adding construction (`NTRECONS`) is reported alongside.
3. **Non-performing loans on the same split**: 90-days-past-due and nonaccrual on
   residential (`P9RERES`, `NARERES`) and on C&I (`P9CI`, `NACI`), plus card (`NACRCD`),
   each scaled by the matching pre-shock class book, measured at the window peak.
4. Change in tier 1 leverage ratio, 2014Q2 to 2017Q4.
5. Failure or assisted-merger indicator by 2018Q4 (logit; log-loss, not R²).

The contrast in (2) is the single most informative secondary and is reported next to the
primary in every table, not relegated to an appendix.

### 14.3 Energy lending exposure: no public bank-level proxy exists

**Checked and the answer is no.** The FDIC BankFind `financials` endpoint returns no
energy, oil, gas, extraction or mining lending field: every candidate name
(`LNENERGY`, `LNOILGAS`, `LNCIOIL`, `LNEXTRACT`, `LNMINING`, and others) is silently
dropped from the response while `LNCI` returns normally, which is how that API reports an
unknown field. Schedule RC-C of the call report has no energy category for this period;
energy concentrations are disclosed only in the 10-Ks of large banks, unsystematically and
not for the community banks that make up this sample.

**So the design relies on what §14.1 and §14.2 provide instead:** the household-class
outcome, which excludes business lending by construction, and the business-loan contrast,
which measures the channel that an energy control would otherwise have absorbed.

**One constructed proxy is pre-specified as a robustness control only, never in the
baseline:** `energy_adjacent_CI = (C&I share of gross loans) × (deposit-weighted county
mining exposure)`. It is kept out of the baseline deliberately, because it correlates
**0.840** with the mining exposure that drives the instrument, so including it would absorb
a large part of the treatment itself. Its use is confined to a single reported robustness
row, with that correlation quoted beside it.

### 14.4 Field construction: the call report is year-to-date

A detail that will otherwise be got wrong in the run. The FDIC exposes quarterly-derived
charge-off fields with a `Q` suffix for some classes but **not all**. Verified by name:

| Exists | Does not exist |
|---|---|
| `NTLNLSQ`, `NTRERESQ`, `NTCRCDQ`, `NTAUTOQ`, `NTCIQ` | **`NTCONOTHQ`**, **`NTRENRESQ`** |

The unsuffixed fields (`NTCONOTH`, `NTRENRES`, and the rest) are **year-to-date within the
calendar year**. **Pre-specified rule:** where a `Q` field exists, use it; where it does
not, construct the quarterly flow by differencing the YTD series within each calendar year
(Q1 = Q1 YTD; Q2 = Q2 − Q1; Q3 = Q3 − Q2; Q4 = Q4 − Q3), and never sum YTD values across
quarters. A negative constructed quarter (recoveries exceeding charge-offs) is kept as a
negative, not floored at zero.

### 14.5 Structural calibration test: interpretation bands committed now

§13.4 recorded that the engine's predicted losses are one to two orders of magnitude below
typical realised charge-off rates. That is not only an artefact of small doses. The
manuscript itself states the reason, in `paper/sections/appendix_detail.tex`: the credit
engine has a **first-round scope**, "which holds house prices, spending, business revenue
and the employment of everyone not displaced fixed, so **every credit loss is a floor**."

A floor is exactly what a slope above one measures. The bands are therefore:

- **Slope interval contains 1** → **"engine calibrated at the first round."** Realised
  losses match the first-round prediction, which given the floor property would itself be
  notable and should be reported as such rather than assumed.
- **Slope positive and well above 1, interval excluding 1** → **"direction supported;
  realised losses exceed first-round predictions by a factor of β̂ (interval stated),
  consistent with second-round transmission but not proof of it."**
- **Slope indistinguishable from zero** → **"not supported in this episode."**
- **Slope significantly negative** → reported as such; it would contradict the engine.

**The second band cannot separate second-round transmission from omitted channels, and
will say so in those words.** A slope of, say, 30 is equally consistent with: second-round
transmission through local spending and house prices, which is the manuscript's mechanism;
energy-business losses leaking into the outcome, which §14.1 is designed to prevent but
cannot eliminate; credit supply contraction; or simple omitted-variable bias in the
predicted-loss term. **The test measures the size of the gap between first-round prediction
and realised loss. It does not attribute that gap.** Any write-up that reads a large slope
as confirmation of the second-round mechanism is overreading it, and this paragraph exists
to make that overreading visible if it happens.

The `s_lo` / `s_mid` / `s_hi` variants and the rival-ω / debtor-ω variants are all reported.
§13.4's third limitation stands: those two ω variants correlate 0.946, so the structural
test says almost nothing about the accounts.

### 14.6 Engine file verification against the pinned hash

**Checked as instructed. The file is UNCHANGED and the pinned values stand.**

Master advanced from `0b5f2b8` (A138) to **`a1b6a0e` (A139, "final manuscript pass,
disclosure, scope, relief demoted, length")** since Amendment 2 was written.

| Check | Result |
|---|---|
| Commits touching `data/processed/verify/hand_check_credit.csv` in `0b5f2b8..a1b6a0e` | **none** |
| Git blob at `0b5f2b8` | `233e413becfec072b4a5f4cc6357f9f6e7499f79` |
| Git blob at `a1b6a0e` | `233e413becfec072b4a5f4cc6357f9f6e7499f79` — **identical** |
| SHA256 of contents, both | `a70b6ca41a4bb57dde30393428e41f27cb340c9316f7e614ce4a37c09ef37726` — **identical** |

**Nothing differs.** The twelve loss sensitivities recorded in §13.4 are unchanged and
remain the pinned values. No value has been altered, silently or otherwise.

**Standing rule for the run:** re-verify this SHA256 immediately before the structural test
and record the result in RESULTS.md. If it has changed by then, the run uses the **pinned**
values from §13.4, reports the new ones alongside, and states what differs. The pinned
values are not updated without an explicit amendment.

### 14.7 Consequential edits elsewhere in this document

- **§3's primary outcome is superseded** by §14.1. §3's secondary list is superseded by
  §14.2.
- **§8, §12.5 and §13.3 thresholds are unchanged.** They now apply to the household-class
  outcome. The power calculation of §13.3 was computed on the interaction's pre-shock
  variance and the sample size, neither of which the outcome redefinition changes, except
  that the primary sample falls from 6,585 to **5,938** banks. The MDE scales as
  `√(6585/5938) = 1.053`, so the ICC 0.05 / R² 0.30 figure moves from 0.075 to
  **0.079** and the ICC 0.10 figure from 0.103 to **0.108**. **The power verdict is
  unchanged: powered at the 0.10 threshold if and only if the intra-cluster correlation is
  below roughly 0.10.** The realised-MDE rule of §13.3 governs either way.
- §11's null language applies unchanged to the new primary outcome.
