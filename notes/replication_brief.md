# Replication brief

**Purpose.** A fresh instance, with no sight of this repository's code, should be able to
rebuild the quantities below from raw public data and compare them with the sealed values in
`data/release/sealed_expected_values.json`. If a rebuilt value falls outside its stated
tolerance, the claim that rests on it does not stand.

**How to use this.** Do not read `src/`. Read this file, fetch the sources named, follow the
constructions, and only then open the sealed file. The sealed file contains the expected
values and the tolerances and nothing else.

**Cognitive exposure measures task overlap, not displacement and not timing.** Every
cognitive figure below is a statement about which occupations an index ranks highly, not a
forecast that those occupations will be displaced.

---

## 0. Data you need

| Source | What | Where |
|---|---|---|
| ACS PUMS 2023, 1-year | person and housing files, national | Census FTP, `csv_pus.zip` and `csv_hus.zip` |
| SIPP 2025 | public use file, pipe delimited | Census SIPP, `pu2025_csv.zip` |
| Felten AIOE | occupational AI exposure scores | the authors' replication package |
| Eloundou GPT | occupational GPT exposure | the authors' replication package |
| Embodiment P | built in this project from ONET | see `notes/paei_c_method.md` |
| IRS SOI 2023 | Table 1.4, sources of income by size of AGI | `23in14ar.xls` |
| FRED | FGRECPT, GDP, GFDEBTN, FGCCSAQ027S, REVOLSL, MVLOAS, LREM25TTUSM156S, LNS11300060 | fredgraph CSV endpoint |
| NY Fed | Household Debt and Credit, 2026:Q2 | mortgage 13,100bn, student 1,650bn |
| Federal Reserve | 2026 DFAST results | Tables 4 and 9 |
| BLS | Displaced Worker Survey, reemployment and exit rates | BLS |

**SIPP cannot be read with a pandas C parser at default settings on a 16GB machine.** Stream
the pipe-delimited file line by line and keep `MONTHCODE == 12` only.

**ACS housing records with `NP = 0` are VACANT UNITS and must be dropped.** They carry a
housing weight, no household, no income and no occupant. Leaving them in inflates the
household count by 9.6 percent, to 145.33m against a true occupied 131.33m, and makes every
one of them look like a zero-income non-working household.

---

## 1. rho(slack): reemployment against labour market slack

**Construction.** Regress the BLS Displaced Worker Survey reemployment rate on
**prime-age (25 to 54) nonemployment**, one observation per DWS vintage.

    rho = intercept + slope * x,   x = 100 * (prime-age population - prime-age employed)
                                       / prime-age population

**Do NOT regress on the unemployment rate.** That fit is circular: displacement raises
unemployment, and workers who exit the labour force leave the unemployment rate unchanged
while they are exactly the workers who did not get reemployed. The circular fit gives a
higher R squared and a speed limit about 2.5 times larger, and it is wrong.

**Do NOT use 16-and-over nonemployment either.** It conflates ageing with slack.

**Sealed:** `rho_slack.intercept`, `rho_slack.slope`, `rho_slack.r_squared`, `rho_slack.n`,
and the fitted range `rho_slack.x_range`, outside which the relation is an extrapolation of a
mechanism and not an estimate of one.

---

## 2. The fiscal condition: R, tau_k, and the required tau_k

**The condition.** The wage-based fiscal system is neutral to displacement when

    tau_k * s + tau_l * rho * omega  >=  tau_l + g * (1 - rho)

which restates, writing **R = rho * omega** for the retained wage share, as

    R  >=  1 - tau_k / tau_l

**R.** rho is reemployment from section 1 evaluated at current slack; omega is the
reemployment wage ratio, a blended counterfactual from the DWS earnings question.

**tau_k.** Not the statutory rate. Build it as

    tau_k = sigma_rent * (domestic share * 0.21) + (1 - sigma_rent) * tau_normal

where sigma_rent is the pure-rent share of capital income (Barkai), the domestic share is
the fraction of profit booked domestically (Torslov, Wier and Zucman), 0.21 is the statutory
federal corporate rate, and tau_normal is the effective rate on normal returns (Auerbach;
Acemoglu, Manera and Restrepo).

**Sealed:** `fiscal.R_2026`, `fiscal.tau_k_range_sourced_sigma`,
`fiscal.tau_k_needed_to_pass` at each of three readings of tau_l.

**The result to look for:** the required tau_k exceeds the top of the sourced tau_k range.
The condition fails on current parameters, and it fails by a margin that no plausible reading
of the inputs closes.

---

## 3. Fiscal and trust fund magnitudes at 10 and 25 percent of the total wage bill

**The axis is the share of the TOTAL wage bill displaced**, never the share of an exposed
group. A top quintile is a moving denominator across indices and is not comparable.

**Terminal-year loss, not cumulative divided by horizon.** A cumulative loss is a stock; an
annual loss is a flow. Dividing one by the other is an error this project made and corrected.
The terminal-year loss is close to horizon-invariant; the cumulative loss rises with horizon.

**Trust funds.** OASDI loses payroll tax on the wages displaced, and only on the part of
those wages **under the contribution and benefit base**, which was 184,500 dollars in 2026.
HI has no cap. The denominator must be the fund's own payroll income, not federal receipts:
dividing a general-revenue loss by a payroll-only denominator produced 107 and 215 percent in
an earlier version of this work, which violates the bound that the loss cannot exceed the
base.

**Bound to check before reporting anything:** every trust fund loss must lie between 0 and
100 percent of fund payroll income.

**Sealed:** `fiscal_magnitudes.terminal_loss_bn_at_10pct` and `at_25pct`,
`trust_funds.OASDI_pct_of_payroll_income_at_10pct` and `at_25pct`, and the grid maximum.

---

## 4. Survey under-reporting factors

**Two different objects, and they must not be multiplied into one.**

    under-reporting factor = official aggregate / FULL SIPP household universe
    coverage share         = working-core balance / FULL SIPP household universe

Only the first is a survey correction. The second is a fact about which households the
analysis subsample covers and belongs in the denominator discussion. The official aggregate
divided by the working-core balance is the first DIVIDED BY the second and embeds a coverage
adjustment inside a survey correction.

**Construction.** Reference-person weights, household level, `MONTHCODE == 12`, positive
weight. Aggregates: mortgage 13,100bn and student 1,650bn from the NY Fed; cards from FRED
REVOLSL and autos from FRED MVLOAS, **both of which the provider states in MILLIONS**. Read
the units from the provider. Treating them as billions produces scaling factors in the
thousands, which is how the error was caught.

**Sealed:** `under_reporting.mortgage`, `.card`, `.auto`, `.student`, and the corresponding
`coverage_share` values. The identity to check: factor divided by coverage share reproduces
the working-core figure to three decimals.

---

## 5. Household first-round losses at 10 percent of the total wage bill

**Losses are exposure at default times LOSS GIVEN DEFAULT.** Not exposure at default times a
portfolio loss rate. The second form applies the probability of default twice, and in this
project it made the credit channel look 21.7 times smaller than it is.

**Construction.**

1. Default uplift from Gerardi, Herkenhoff, Ohanian and Willen: an unemployed head is about
   5.0 percentage points more likely to default; a household in which both head and spouse
   have a spell is more than 8.0 points, which is SUPERADDITIVE, not 10.
2. Exposure at default = balance times the uplift, summed over households, scaled by the
   under-reporting factor from section 4.
3. Loss = exposure at default times LGD. Ranges used: mortgage 0.25 to 0.40, cards 0.80 to
   1.00, auto 0.45 to 0.65, student 0.75 to 1.00.
4. Bank-held slice = the Federal Reserve's DFAST balance for that book over the national
   aggregate.

**Sealed:** `household_first_round.{loan}_bank_loss_hi_bn_at_10pct` and
`.pct_of_fed_severely_adverse_at_10pct` for each of the four books.

**Scope, which must travel with every one of these numbers.** This is a FIRST-ROUND figure.
It holds house prices, consumer demand, business revenue and the employment of non-displaced
workers fixed. The Federal Reserve's severely adverse scenario moves all of those together.
Comparing the two is a LOWER BOUND on bank losses, not an estimate.

---

## 6. The OASDI earnings cap contrast

**Construction.** For each exposure group, the share of the group's wage bill that sits under
the 2026 contribution and benefit base of 184,500 dollars, weighted by person weights, on
employed workers with positive earnings. Compute it on ACS annual wage income and,
independently, on SIPP annualised monthly earnings.

**Sealed:** `cap_contrast.ACS.{group}` and `cap_contrast.SIPP.{group}` for embodied,
cognitive AIOE and cognitive GPT.

**The levels will differ between the two surveys** because the income concepts differ. The
CONTRAST is what is claimed.

**AND THEN THE CONTROL, which is the point.** Reweight the cognitive group onto the embodied
group's distribution across deciles of individual annual wage income and recompute. **The
contrast is almost entirely a pay effect**: between 54 and 99 percent of the raw gap
disappears, and in SIPP against Eloundou GPT it changes sign. Do not report the contrast as
an exposure-type mechanism.

**Sealed:** `pay_control.share_of_gap_that_is_pay` for each dataset and index.

---

## 7. The incidence comparison

Three cases for who inside an exposed occupation is displaced: incumbents, entrants, and a
sourced mix.

**Sealed:** `incidence.household_count_spread` and `incidence.dollar_spread`.

**The result:** on household COUNTS incidence moves the answer by 5 to 9 percent. On the
DOLLARS those households owe it moves it by 1.75 to 3.01 times. **No dollar figure from this
engine may be quoted without naming the incidence assumption.** The count figures are robust
to it and can stand alone.

---

## 8. What a replicator should expect to find wrong if they follow the old path

These are the errors this project made. A replicator who reproduces them has followed the
wrong construction, not found a discrepancy.

| Error | Symptom |
|---|---|
| Vacant units counted as households | 145.33m households instead of 131.33m |
| Portfolio loss rate applied to exposure at default | credit losses 21.7 times too small |
| General-revenue loss over a payroll-only denominator | trust fund losses above 100 percent |
| Cumulative loss divided by horizon | terminal loss falls with horizon instead of holding flat |
| Aggregate over the working-core balance | under-reporting factors 14 to 26 percent too large |
| REVOLSL and MVLOAS read as billions | scaling factors in the thousands |
| rho fitted on the unemployment rate | speed limit about 2.5 times too large |

---

## 9. Tolerances

Every sealed value carries a tolerance. Survey-based quantities are given a 2 percent
relative tolerance to allow for weight and vintage differences; fitted coefficients a 5
percent tolerance; ratios and shares an absolute tolerance of 0.01. A rebuilt value outside
its tolerance means the claim resting on it does not stand until the difference is explained.
