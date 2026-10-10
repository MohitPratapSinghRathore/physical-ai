# Results — broad predictive test of labour backing on bank credit losses

**Pre-registration:** `PREREGISTRATION.md`, SHA256
`b9f09ddc33a6619b0046617021df72f13aaeb0fcb4fb882852269dd424f3136a`, committed at
`bb21c84` **before any outcome variable was downloaded**.

**Deviations:** `DEVIATIONS.md`, D1–D8. D1–D4 were logged before outcomes were read.
D5–D8 are implementation corrections made after the first run, each recorded with what
broke and what the correction did to the result.

---

## 1. The headline

**Labour backing does not predict which banks lose money on household credit.**

The pre-registered statistic came in at **+0.00556**, between the kill line (0.002) and
the success line (0.01), so on the pre-registered rule the primary test is
**inconclusive**. Two diagnostics show why that number exists, and they settle it against
the construct: the gain is the construct absorbing the drift of a baseline that
mis-predicts the *level* of the credit cycle, not information about which bank is
exposed. On cross-sectional ranking — the thing a supervisor or a lender would use — the
construct makes the prediction **worse in 13 of 13 test years**.

The honest conclusion is a **null**, and a slightly stronger one than the pre-registered
statistic on its own would have supported.

## 2. The panel

| | |
|---|---|
| Source | FDIC BankFind `financials` and `sod`, BEA CAINC4, ACS 2009–2013 |
| Constructs and controls | June 30, origin years 2001–2021 |
| Outcomes | December 31 YTD charge-offs, 2002–2024, cumulated over *t+1*..*t+3* |
| Rows | 146,813 after the D5 minimum-book rule (154,904 before) |
| Banks | 10,532 |
| Observations per bank | about 14, with **overlapping** three-year outcome windows |
| Counties | deposit-weighted from Summary of Deposits branch records |

Constructs: `LB` (composition × population wage share), `LB_debtor` (× debtor-specific
wage share), `Gap` = `LB_debtor` − `LB`, `LB_debtor_pw` (payment-weighted). Per D1, `LB`
and the pilot's `Rival` are identical by construction and were not counted twice.

## 3. Confirmatory test — forward chaining, outcome `y_hh_3`

Train on origin years ≤ *T*, test on *T+1*, rolling *T* = 2008…2020. Thirteen test years.

| construct | controls | mean ΔR²_oos | years positive | pre-registered verdict |
|---|---|---|---|---|
| `LB` | conventional | **+0.00556** | 12/13 | inconclusive |
| `LB` | conventional + lagged | +0.00457 | 12/13 | inconclusive |
| `Gap` | conventional | +0.00180 | 11/13 | **kill** |
| `Gap` | conventional + lagged | +0.00166 | 12/13 | **kill** |

Success required mean ΔR² ≥ 0.01 **and** ≥ 8/13 positive. Kill was ≤ 0.002 or < 7/13.
`Gap` is killed outright. `LB` sits in the gap between the two lines.

**The `LB` figure is not an outlier artefact.** Year by year it is smooth and close to
monotone, and it survives trimming:

| | mean ΔR² |
|---|---|
| all 13 years | +0.00556 |
| excluding the single best year | +0.00462 |
| excluding best and worst | +0.00508 |

## 4. Why +0.00556 is not evidence for the construct

The baseline's own out-of-sample R² is **negative in 10 of the 13 test years**, ranging
from −0.11 to −0.41. It predicts worse than the test-year mean. Coefficients fitted on
years ≤ *T* do not transfer to *T+1* across the credit cycle, and the baseline's error is
dominated by getting the *level* of losses wrong.

Against a baseline worse than a constant, a positive ΔR² can be earned by shifting the
level rather than by ordering the banks. Two diagnostics separate those (`run_ranking.py`,
logged as D8):

**(a) Re-centred ΔR².** Shift both predictions to the test-year mean, removing level
drift and leaving only cross-sectional ranking:

| construct | raw ΔR² | re-centred ΔR² | baseline R² after re-centring |
|---|---|---|---|
| `LB` | +0.00556 (12/13) | **−0.00043** (6/13) | +0.0452 |
| `Gap` | +0.00180 (11/13) | **−0.00022** (4/13) | +0.0452 |

Re-centring alone turns the baseline's mean R² from −0.1220 to **+0.0452** — confirming
that level drift, not ranking failure, was the baseline's problem. Once it is removed the
construct's contribution vanishes and turns marginally negative.

**(b) Out-of-sample rank correlation.** Spearman correlation between predicted and
realised household charge-off rate:

| construct | controls alone | adding the construct | change | years improved |
|---|---|---|---|---|
| `LB` | +0.1620 | +0.1558 | **−0.00622** | **0/13** |
| `Gap` | +0.1620 | +0.1607 | **−0.00127** | **0/13** |

Adding labour backing to a conventional bank-risk model makes the out-of-sample ordering
of banks worse in **every single test year**, for both constructs. Zero of twenty-six
construct-years improved. That is not a marginal null; it is a consistent small loss.

## 5. Specification curve — 864 specifications

4 constructs × 6 outcomes × 3 horizons × 4 samples × 3 control sets. Per the
pre-registration this is a **calibration exercise**; no specification drawn from it may be
reported as a finding, and none is.

Standard errors are two-way clustered by bank and origin year (D7).

| | |
|---|---|
| specifications run | 864 |
| significant at *p* < 0.05 | 361 |
| expected by chance | 43.2 |
| ratio | 8.36× |
| Romano–Wolf 95% family-wise threshold | \|t\| > 4.020 |
| surviving Romano–Wolf | 42 |
| max \|t\| | 9.88 |
| median \|t\| | 1.48 |

**8.36× chance sounds like a finding. It is not, for three reasons.**

**(a) The survivors are almost all uncontrolled.** Splitting by control set:

| control set | specs | significant | Romano–Wolf survivors | median \|t\| |
|---|---|---|---|---|
| none | 288 | 144 | **36** | 1.96 |
| conventional | 288 | 108 | 3 | 1.43 |
| conventional + lagged | 288 | 109 | 3 | 1.44 |

**36 of the 42 family-wise survivors have no controls at all.** Add a conventional bank-risk
model and the survivors collapse to 6 of 576, and the median |t| falls below 1.5.

**(b) The construct is largely a repackaging of loan composition.** Regressing `LB` on the
seven loan-share controls alone gives **R² = 0.5167**. Over half the variation in the
labour backing measure *is* the loan mix. An uncontrolled specification that finds `LB`
predicts charge-offs has mostly found that banks with more consumer and residential
lending charge off more, which was known.

**(c) The counts are unstable under the clustering choice**, which is itself a reason not
to lean on them. Same 864 specifications, three standard-error choices:

| clustering | significant | Romano–Wolf survivors | max \|t\| |
|---|---|---|---|
| origin year only (21 groups) | 389 | 140 | 12.48 |
| bank only (10,532 groups) | 422 | 182 | 21.26 |
| **two-way, bank × year** | **361** | **42** | **9.88** |

Family-wise survivors move by a factor of four across defensible choices. Two-way is the
right one here (D7) and it is also the least favourable, which is the point.

## 6. Verdict against the pre-registered criteria

| criterion | threshold | result |
|---|---|---|
| success | mean ΔR² ≥ 0.01 and ≥ 8/13 positive | **not met** (+0.00556) |
| kill | mean ΔR² ≤ 0.002 or < 7/13 positive | met for `Gap`, not for `LB` |

**Primary outcome: inconclusive on the letter of the rule, null on the substance.**

The construct clears the kill line only through a level correction against a baseline that
mis-predicts the level of the credit cycle. Removing that, it contributes −0.0004 and it
degrades the out-of-sample ordering of banks in 13 of 13 years. The specification curve's
apparent excess significance is concentrated in specifications with no controls, for a
construct that is half explained by loan composition.

**Labour backing does not carry bank-level credit-risk information beyond conventional
loan-composition and leverage controls.** This is consistent with the validation pilot's
null (A142) and is a stronger form of it: the pilot could not reject that labour backing
predicted losses; this test, on 146,813 bank-years and 10,532 banks over 2001–2024, finds
the ordering gets slightly but consistently worse.

## 7. What this does and does not bear on

It does **not** bear on the accounts themselves. The measurement results stand as
measurement: sovereign concentration of 79.4% and its doubling, 47% of corporate equity
never reaching households, the 84.6% / 23.6% wealth gradient. Those are accounting facts
about the composition of claims and are not predictions.

What fails, repeatedly and now on the largest sample tried, is the step from *this claim is
labour-backed* to *this intermediary is more likely to take a loss*. Nine hypotheses have
now been tested across this repository and this is the ninth null. The accounts describe a
structure; they do not forecast credit events, and the paper should not claim they do.

## 8. Files

| file | what |
|---|---|
| `PREREGISTRATION.md` | pre-registered design, hashed and committed before outcomes |
| `fetch_panel.py` | FDIC / BEA / ACS retrieval |
| `build_panel.py` | constructs, controls, outcomes |
| `run_test.py` | confirmatory forward chaining, then the specification curve |
| `run_ranking.py` | the D8 re-centring and rank-correlation diagnostics |
| `results.json`, `ranking.json`, `spec_curve.csv` | full output, all years, all 864 specs |
| `DEVIATIONS.md` | D1–D8, with D5–D8 marked as post-results corrections |
