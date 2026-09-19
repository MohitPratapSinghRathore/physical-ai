# Pre-registration: does mortgage pricing reflect local Physical AI exposure?

**Committed 2026-09-19, before any HMDA outcome variable was loaded.** No rate spread or
denial data has been read at the time of writing. Git history is the evidence: this file is
committed in advance of any commit touching HMDA outcomes.

Registered by: the Phase 2 pipeline, per MASTER_PROMPT_PHASE2.md Step 4.

---

## 1. Question

Do lenders price local exposure to Physical AI when they originate and price mortgages?

This is a descriptive question about whether a risk that is measurable ex ante appears in
prices. It is **not** a causal question and nothing below identifies a causal effect.

## 2. Data

HMDA Loan Application Register, accessed through the HMDA Data Browser filtered downloads
or its API, never the raw full-year LAR file. Latest available year first; 2018 to latest
once the pipeline runs end to end.

Sample restrictions, applied in this order, with row counts recorded before and after each:

1. First lien only
2. 1 to 4 family, site-built, principal or secondary residence as reported
3. Loan purpose: home purchase or refinance
4. Action taken: originated, denied, or purchased
5. Drop records with missing county or census tract
6. Drop open-end lines of credit and reverse mortgages
7. Drop business-purpose loans

Fields retained: action taken, purchaser type, rate spread, combined LTV, DTI, applicant
income, loan amount, loan type, loan purpose, occupancy, lien status, lender LEI, county,
census tract, and the demographic fields required for the fair lending discussion.

Converted to parquet on load. Row counts logged at each filter step.

## 3. Regressor of interest

County-level (and, where tract-level exposure can be constructed, tract-level) PAEI(c),
built from the geographic DAR pipeline in Step 3, evaluated at:

- **c = 0**, current robotics exposure
- **c = 0.8**, the high-capability scenario

Both are entered in separate specifications, never together, because they are close to
collinear by construction.

Exposure is the employment-weighted mean PAEI(c) of the local workforce, embodiment
weighted as in `notes/paei_c_method.md` Section 5. It is standardised to mean zero and unit
variance within year so coefficients read as "per standard deviation of local exposure".

## 4. Specifications

**S1, pricing.** Outcome: rate spread (APR minus APOR), continuous, on originated loans
with a reported spread.

**S2, denial.** Outcome: binary denial indicator, on applications with action taken in
{originated, denied}. Linear probability model for the headline, logit as a robustness
check.

Controls in both: combined LTV, DTI, log applicant income, log loan amount, loan type, loan
purpose, occupancy, lien status, lender fixed effects, state by year fixed effects, county
unemployment rate, and county house price growth (FHFA HPI).

Standard errors clustered by county.

## 5. The critical design point

Conforming loans sold to the GSEs are priced off national grids. A null result on that
sample is **mechanical** and carries no information about whether lenders perceive the risk.

The informative sample is loans where the lender bears the credit risk:

- **Sample A, portfolio-retained.** Purchaser type indicating the loan was not sold in the
  calendar year. This is the lead sample and the headline result comes from it.
- **Sample B, jumbo.** Loan amount above the applicable conforming limit for the county and
  year.
- **Sample C, GSE-sold.** Reported for contrast, and expected to be null.

Results are reported for all three, and Sample A leads.

## 6. Interpretation, fixed in advance

| Result on Sample A | Interpretation |
|---|---|
| Coefficient not distinguishable from zero | The risk is unpriced where lenders have both the incentive and the freedom to price it. This is the finding most consistent with the thesis and it will be stated as descriptive, not causal. |
| Positive and significant | The risk is partially priced. Also publishable. Reported as evidence that lenders already perceive some of this exposure, which weakens the "unpriced risk" framing and strengthens the "measurable risk" framing. |
| Negative and significant | Exposure is associated with LOWER spreads. Most likely confounded by local income, house price growth or lender composition rather than a real negative price of risk. Would be reported as such and would trigger a specification audit, not a reinterpretation. |

A null on Sample C alone will not be reported as evidence of anything.

## 7. What would invalidate the test

- If county-level PAEI(c) turns out to be collinear with county median income above
  |r| = 0.9, the coefficient cannot be separated from an income effect and the test is
  uninformative. Correlations will be reported before the regressions are run.
- If portfolio-retained volume is too thin in the latest year to support lender fixed
  effects, Sample A is under-powered and that will be stated rather than worked around.
- Rate spread is reported only above a reporting threshold in some years, which truncates
  the outcome. Truncation share will be reported.

## 8. Things deliberately NOT done

- No specification search. The controls above are fixed. Any additional specification run
  after seeing outcomes will be labelled post hoc in the results note.
- No outcome-dependent sample slicing.
- No dropping of years or states after seeing results.
- The fair lending argument (that occupation-based underwriting collides with ECOA, the
  Fair Housing Act and disparate impact doctrine) requires legal sourcing and is **not**
  supported by this test. It must not be asserted on the basis of these regressions.

## 9. Specification audit, run unconditionally (AMENDMENT 1, 2026-09-19)

Amends Section 6. The original text ran a specification audit only if the coefficient came
back negative and significant. That is conditioning the diagnostics on the result, which is
exactly the practice the rest of this document exists to prevent: a suspicious result gets
scrutinised while a convenient one does not.

**The checks below run unconditionally, and they run BEFORE the coefficient of interest is
viewed.** Their output is written to notes/pricing_results.md before any table containing
the coefficient on PAEI(c) is produced. The analyst (and the pipeline) must be able to read
every check without learning the sign of the effect.

Checks, all on the estimation sample:

1. **Collinearity.** Correlation of county PAEI(c) with county median income, county median
   house value, county unemployment rate, county house price growth, and the share of local
   employment in manufacturing. Variance inflation factors for every regressor. Flag any
   |r| above 0.9 or VIF above 10.
2. **Common support.** Distribution of PAEI(c) across the three samples (portfolio, jumbo,
   GSE-sold). Report deciles, and flag if any sample occupies less than half the exposure
   range of the full sample.
3. **Sample composition.** Row counts at every filter step; share of originations dropped;
   share of records with missing LTV, DTI, or rate spread; the rate-spread truncation share.
4. **Fixed-effects absorption.** Number of lenders, number of counties, and the share of
   lenders and counties that are singletons after fixed effects. Flag if singletons exceed
   20 percent.
5. **Outcome distribution.** Rate spread distribution, share at reporting thresholds, share
   of exact zeros, and denial rate. Reported as distributions of the OUTCOME alone, with no
   regressor crossed against them, so this does not reveal the effect.
6. **Geographic coverage.** Counties present, employment covered by PAEI(c), and the share
   of national originations in counties with no exposure measure.
7. **Weighting and clustering.** Number of clusters; flag if below 50, where cluster-robust
   inference is unreliable.
8. **Placebo geography.** PAEI(c) randomly permuted across counties, specification re-run
   50 times, and the distribution of the placebo coefficient reported. A real coefficient
   outside that distribution is the minimum bar. This check is run and reported before the
   true coefficient is read.

If any check fails, the failure is reported alongside the result rather than used to
justify dropping the result.

## 10. Deviations

Any deviation from this document is logged here with the date and the reason, and the
original specification is reported alongside the revised one.

- 2026-09-19, Amendment 1: specification audit made unconditional and moved before the
  coefficient is viewed. No outcome data had been loaded at the time of this amendment.
