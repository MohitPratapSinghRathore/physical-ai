# Broad predictive test, and a specification curve

**2026-09-26, branch `predictive-panel` from master `c052f96` (A143). Written and committed
before any outcome for any year is downloaded.**

## Why this is not a re-run of the validation pilot

The pilot (archived at `acaf6ba`, published as a limitation in A142) tested a **narrow causal
question**: does labour backing measured before the 2014–16 oil collapse predict subsequent
household-loan charge-offs, conditional on supervisory controls, with the local wage shock
instrumented by a leave-one-out shift-share. It returned a null and its own placebo failed.

**It did not test whether labour backing carries any predictive information at all.** One
episode, one shock, one instrument, one cross-section. This tests the broad question:

> **Across all US banks and all available years, does labour backing improve out-of-sample
> prediction of bank credit losses over conventional supervisory measures?**

No instrument, no causal claim, no episode. Pure forecasting. **A positive result here would
not overturn the pilot's null** — the pilot answered a causal question and this one does not —
and the write-up must say so.

## Design, fixed now

**Panel.** All FDIC-insured institutions, one observation per bank-year, **origin years
2001–2021**. Labour backing and controls measured at June 30 of year *t*; outcomes over
*t+1* to *t+3*.

**Constructs at t.** `LB` = Σ class share × class coefficient × deposit-weighted county wage
share, exactly as `framework/labor_backing/claim_class_rules.csv` and the pilot define it;
plus `Rival` and `Gap` as in the pilot's Amendment 2.

**Controls at t.** Tier 1 leverage, loan composition shares (residential, consumer, CRE,
construction, C&I, agricultural, securities), supervisory CRE concentration, log assets,
deposits/assets, brokered/deposits, loans/assets, and **lagged charge-offs** (the single
strongest conventional predictor, included so the bar is honest).

**Outcome.** Cumulative net charge-offs on household classes over *t+1* to *t+3*, scaled by
the class book at *t*, winsorised 1/99 within the training set. Secondary outcomes listed
in the specification curve below.

**Validation.** Strictly forward-chaining. Train on origin years ≤ *T*, test on *T+1*.
Roll *T* from 2008 to 2020. **No test year is ever in any training set.** Metric is
out-of-sample R², and log-loss for the binary outcome.

## Success and kill criteria, as numbers

**Success requires both:**
1. Mean out-of-sample R² improvement from adding `LB` (or `Gap`) to the control model,
   averaged over rolling test years, **≥ 0.01**; and
2. The improvement is positive in **at least 8 of the 13 test years**.

**Kill:** mean ΔR²_oos **≤ 0.002**, or positive in fewer than 7 of 13 years.

The threshold is lower than the pilot's 0.02 deliberately: this is a forecasting question, not
a causal one, and a small stable improvement would be meaningful where a small causal
coefficient would not.

## The specification curve

Run **after** the confirmatory test, never instead of it. The grid is fixed here:

- **Constructs (4):** LB, Rival, Gap, LB payment-weighted
- **Outcomes (6):** household charge-offs, total charge-offs, business charge-offs,
  household NPL, tier 1 change, failure indicator
- **Horizons (3):** t+1, t+1..t+2, t+1..t+3
- **Samples (4):** all banks, assets > $1bn, assets < $1bn, banks in ≥ 5 counties
- **Control sets (3):** none, conventional, conventional + lagged outcome

**864 specifications.** For each, the coefficient on the construct and its p-value.

**What is reported, fixed now:**
- The count significant at p < 0.05, against the **43.2 expected by chance**.
- The same count after **Romano–Wolf** stepdown across the whole space.
- The full distribution of t-statistics against the null.
- **Every specification, not a selected subset.**

**This is a calibration exercise, not a search.** If the significant count is near the chance
expectation, that is the result and it will be reported as such. **No specification from this
curve may be reported as a finding**; the curve's only output is the count and the
multiplicity-corrected survivors.

## What will be reported if the result is null

> Labour backing does not improve out-of-sample prediction of bank credit losses over
> conventional supervisory measures, across all US banks over two decades, at any horizon
> tested. Mean out-of-sample R² improvement was [value] against a pre-registered threshold of
> 0.01. A specification curve over 864 combinations produced [n] hits at p < 0.05 against
> 43.2 expected by chance, and [m] surviving multiplicity correction.

And the standing consequence, unchanged from the pilot: **the accounts are descriptive
accounting of the claim stock, not a risk measure.**

## Plausibility bounds

Shares in [0,1]; no bank-year in both training and test; charge-off rates non-negative except
where recoveries exceed charge-offs, counted and reported; sample counts reported per year.
Violations reported first.
