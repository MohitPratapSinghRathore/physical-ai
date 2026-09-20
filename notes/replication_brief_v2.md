# Replication brief, version 2

**Round one matched 21 of 51 attempted quantities.** The replicator's verdict was that this
brief is strong on error prevention and weak on parameter disclosure: it named sources
without stating the values drawn from them, left three load-bearing terms undefined, and
omitted the model structure for two whole sections. That verdict is accepted in full. This
version states **every parameter value**, defines **every term**, and gives the **full
mechanics** for the four sections that produced no values at all.

Round one is closed. Its sealed file is frozen at
`notes/sealed/sealed_expected_values_round1_ARCHIVED.json` and its mismatches are classified
in `notes/replication/round1_mismatch_classification.md`. **This brief is scored against
`notes/sealed/sealed_expected_values_round2.json`.**

**Purpose.** A fresh instance, with no sight of `src/`, rebuilds the quantities below from
raw public data and compares them with the sealed round-two file. A rebuilt value outside its
stated tolerance means the claim resting on it does not stand until the difference is
explained.

**How to use this.** Do not read `src/`. Do not read `notes/findings.md` or
`notes/claims_register.md`: both contain the answers. Read this file, fetch the sources named,
follow the constructions, and only then open the sealed file. Record every rebuilt value
before you open it, and say so in your report if you open it early; a declared broken blind is
worth more than a silent one.

**Cognitive exposure measures task overlap, not displacement and not timing.** Every cognitive
figure below is a statement about which occupations an index ranks highly, not a forecast that
those occupations will be displaced. Top-quintile occupations include likely-augmented work.

---

## 0. What changed between round one and round two, and why you cannot check yourself against round one

Five published quantities moved because **this project was wrong**, not because the brief was
unclear. If you reproduce round one's numbers you have reproduced errors.

| Correction | Effect |
|---|---|
| The break-even capital tax rate double-counted tau_k and mixed two wage bill totals | case A range 0.214 to 0.378 becomes **0.125 to 0.301**; case B 0.561 to 0.860 becomes **0.182 to 0.650** |
| The wage bill base was FRED COE compensation in the fiscal modules and the occupational grid in the second-round module; both become FRED WASCUR | fiscal dollar figures fall **17.6 percent**; second-round demand figures rise **35.4 percent** |
| HI carried the OASDI payroll share and a total-income denominator | HI trust fund ratios fall **4.5 percent** |
| The auto aggregate sat on FRED MVLOAS, discontinued after 2024Q4 | auto under-reporting factor 1.7431 becomes **1.9036** |
| Trust fund figures were derived; they are now read from the 2026 Trustees Report | OASDI payroll income 1,323.2bn becomes **1,322.6bn**; HI 462.4bn becomes **403.2bn** |

---

## 0a. Data you need, with series identifiers and vintages

| Source | Identifier | Vintage | What |
|---|---|---|---|
| ACS PUMS 2023 1-year | `csv_pus.zip`, `csv_hus.zip` | 2023, national | person and housing files |
| SIPP 2025 | `pu2025_csv.zip` | 2025 panel, pipe delimited | household balances and occupation |
| O*NET | `db_31_0_text.zip` | **31.0** | Abilities, Work Activities, Work Context |
| Felten AIOE | authors' replication package | as published | occupational AI exposure |
| Eloundou GPT | authors' replication package | as published | occupational GPT exposure |
| IRS SOI | `23in14ar.xls` | tax year **2023** | Table 1.4, sources of income by size of AGI |
| FRED | `WASCUR` | 2026Q2, 13,365.2bn | **wages and salaries. THE BASE.** |
| FRED | `COE` | 2026Q2, 16,224.3bn | compensation of employees. **NOT the base** |
| FRED | `GDP` | annual mean of quarterly nominal, 2026, 32,175.9bn | denominator for every share of output |
| FRED | `FGRECPT` | annual mean 2026, 5,980.631bn for the receipts ratio, 5,926.564bn as the public budget capacity | federal current receipts |
| FRED | `GFDEBTN` | 2026Q1, in MILLIONS | total public debt |
| FRED | `FGCCSAQ027S` | latest, 1,605.134bn | federal student loan assets |
| FRED | `REVOLSL` | 2026-07, **in MILLIONS**, 1,357.2bn | revolving consumer credit |
| FRED | `LREM25TTUSM156S` | OECD, monthly | prime-age 25 to 54 employment to population ratio |
| NY Fed | Household Debt and Credit, **2026Q2** | mortgage 13,100bn, student 1,650bn, **auto 1,713bn**, card 1,263bn | the report's own data workbook, "Page 3 Data" |
| NY Fed | same workbook, "Page 12 Data" | 2026Q2 | percent of balance 90+ days delinquent by loan type |
| Federal Reserve | 2026 DFAST results, June 2026 | Tables 2, 4 and 9 | see section 5c below |
| BLS | *Displaced Workers Summary* | 14 biennial releases | see section 1 |
| SSA | 2026 Trustees Reports summary tables | Tables 4, 5, 7, 8 | see section 3 |
| CBO | Preliminary Estimate of the Effects of H.R. 748, revised 27 April 2020 | publication 56334 | the cited public budget reference point |

**FRED series read as billions when the provider states MILLIONS produce scaling factors in
the thousands.** `REVOLSL` and `GFDEBTN` are in millions. Read the units from the provider.

**FRED MVLOAS is discontinued after 2024Q4. Do not use it.** Round one's auto aggregate came
from it and was two years stale against every other input.

**SIPP cannot be read with a pandas C parser at default settings on a 16GB machine.** Stream
the pipe-delimited file line by line and keep `MONTHCODE == 12` only.

**ACS housing records with `NP = 0` are VACANT UNITS and must be dropped.** They carry a
housing weight, no household, no income and no occupant. Leaving them in inflates the
household count by 9.6 percent, to 145.33m against a true occupied 131.33m.

---

## 0b. The definitions round one left undefined

### The working core

Used throughout and never defined in version 1. **Two definitions exist in this project and
you need both**, because different modules use different ones and the difference is small but
real.

**Definition A, the SIPP credit modules** (sections 4 and 5, and every under-reporting and
coverage figure):

> a household with **at least one employed member** AND a **reference person aged 25 to 64**.

**Definition B, the ACS stress engine** (the DSTI and distress figures):

> a household containing **at least one EMPLOYED MEMBER AGED 25 TO 64**.

B is the current definition and supersedes A for a displacement question, because it is the
worker's age that matters, not the reference person's. A is retained where it is, and the
round-one coverage shares are computed on A. The replicator reached "reference person under
65" by sensitivity testing and landed within 0.011 on all four books; the residual is the
lower bound at 25 and the employment test.

**Weights.** Household level, **reference-person weights** (`WPFINWGT` on the record with
`ERELRPE` in {1, 2}), positive weight only, `MONTHCODE == 12`, deduplicated to household by
`SSUID` and `ERESIDENCEID`. Balances are the `THDEBT_*` household aggregates: `THDEBT_HOME`,
`THDEBT_CC`, `THDEBT_VEH`, `THDEBT_ED`. In ACS, `WGTP` for households and `PWGTP` for
persons; never mix the two systems in one ratio.

**Employment test.** `RMESR` in SIPP; `ESR` in {1, 2, 4, 5} in ACS.

### The exposure group

> the **top employment-weighted quintile** of the index, within the set of occupations the
> index and the ACS occupation crosswalk both cover.

The replicator guessed this correctly. It is stated now so it need not be guessed.

### The speed limit

Version 1 used the phrase in its error table ("about 2.5 times too large") without defining
it, and the replicator could not confirm or refute the claim. **The claim is withdrawn as
stated.** The speed limit is the maximum annual displacement flow the labour market absorbs
without the implied slack leaving the observed data range, and it is not a single number: it
is a RANGE of 0.0005 to 0.0715 a year across the full specification table, median 0.0273. The
ratio between the two slack specifications is 1.11 on the slope, not 2.5. Do not attempt to
reproduce a "2.5 times" figure; it is not one this project can support.

---

## 1. rho(slack): reemployment against labour market slack

**Construction.** Regress the reemployment rate on **prime-age (25 to 54) nonemployment**, one
observation per DWS vintage, ordinary least squares.

    rho = intercept + slope * x

**y, stated exactly, because version 1 did not.**

| | |
|---|---|
| Release | *Displaced Workers Summary*, USDL news release, biennial |
| Table | **Table 1**, the **TOTAL row** |
| Universe | **long-tenured** displaced workers, three or more years on the lost job, **all ages, both sexes** |
| Quantity | number **employed at the survey date** divided by the total displaced |
| Vintages | **14**, survey months **January 2000 through January 2026** |
| Range of y | 0.49 (2010) to 0.74 (2000) |
| NOT this | the prime-age reemployment rate; the full-time wage and salary reemployed rate; anything from Table 7 |

**x, stated exactly.**

    x = 100 - (prime-age 25 to 54 employment to population ratio)

from OECD `LREM25TTUSM156S` via FRED, taken **as of** each DWS survey month, that is, the
latest observation at or before it. For thirteen of the fourteen vintages that IS the January
observation. For the January 2026 vintage it is not: the OECD series lags and its latest
observation is **2025-09**, giving x = **19.31091**, which is the prime-age nonemployment
rate the trigger dashboard publishes. A strict January rule drops the 2026 vintage and gives
n = 13 and a different fit. Range **18.27241 to 24.70612**, and those endpoints are sealed so
you can check your x before you check anything else.

**The window matters and version 1 did not state it.** Fourteen vintages, 2000 to 2026. A
window of 1998 to 2024 gives the same n and the same x construction and a materially
different intercept and slope. That difference was the whole of round one's gap on this fit.

**Do NOT regress on the unemployment rate.** That fit is circular: displacement raises
unemployment, and workers who exit the labour force leave the unemployment rate unchanged
while they are exactly the workers who did not get reemployed. **See appendix A for the
important caveat on this instruction**, which version 1 overstated.

**Do NOT use 16-and-over nonemployment.** It conflates ageing with slack.

**Sealed:** `rho_slack.intercept`, `.slope`, `.r_squared`, `.n`, `.x_range_low`,
`.x_range_high`.

---

## 2. The fiscal condition: R, tau_k, and the required tau_k

**The condition.** The wage-based fiscal system is neutral to displacement when

    tau_k * s + tau_l * rho * omega  >=  tau_l + g * (1 - rho)

which restates, writing **R = rho * omega** for the retained wage share, at s = 1 and g = 0,
as

    R  >=  1 - tau_k / tau_l

### 2a. R, and a correction to version 1

**Version 1 said rho is "evaluated at current slack". That is wrong about this project and it
sent the replicator down a wrong path.** `R_2026` uses the **DIRECTLY OBSERVED** 2026 rho.
The fitted line of section 1 is used **only** on the extended axis of section 3, where slack
moves away from anything observed.

| Parameter | Value | Construction |
|---|---|---|
| rho, 2026 | **0.6610** | DWS Table 1 total row: 2,199 of 3,324 thousand employed, January 2026 |
| omega, central | **0.8597817** | counterfactual blended, below |
| omega, low | 0.8292219 | |
| omega, high | 0.9075879 | |
| **R_2026** | **0.568316** | rho x omega, central |

**omega, the full decomposition, which version 1 omitted entirely.** DWS **Table 7** total
row prices only full-time to full-time moves and reports a **banded** distribution, not a
mean. Two assumption layers, both stated:

1. **Band midpoints.** Of 1,342 thousand who lost full-time wage and salary jobs, were
   reemployed full time and reported earnings on the lost job: 369 earning 20 percent or more
   below, 317 below but within 20 percent, 354 equal or above within 20 percent, 302 20
   percent or more above. The two closed bands take midpoints **0.90** and **1.10**. The two
   OPEN bands take **0.65 below and 1.35 above** in the central case, 0.60/1.30 conservative,
   0.70/1.40 generous. This yields `omega_full_time_only` = **0.9853** central.
2. **Destination blending.** The engine applies omega to EVERY reemployed worker, while Table
   7 prices only full-time moves. Of 1,942 thousand reemployed: 1,593 to full-time wage and
   salary (share **0.82029**), 197 to part time (**0.10144**), 152 to self-employment or
   unpaid family work (**0.07827**). Part time is assigned **0.50** of the prior wage (the
   sourced part-time to full-time earnings ratio is 0.3206 in 2025, so 0.50 is an upper
   bound); self-employment **0.85** central, 0.70 low, 1.00 high. This yields
   `omega_blended_nominal` = **0.907268** central.
3. **The counterfactual adjustment, and it is what makes 0.8598 rather than 0.9073.** The
   condition compares tax raised after displacement against tax that WOULD have been raised
   on the same workers absent displacement, and the counterfactual wage bill grows with
   economy-wide wages. ECI wages growth **3.649 percent a year** (2023 to 2026), elapsed time
   **1.5 years** central (1.0 low, 2.0 high). `omega_blended_counterfactual` = **0.859782**.

**A replicator who uses the nominal omega will get 0.5997 for R, not 0.5683.** The
counterfactual one is the right estimand for this condition and version 1 never said which
was used.

**Historical R holds omega FIXED at the 2026 value** and varies only rho, because earlier
releases do not publish Table 7 in a parsed form. That is an assumption and if omega is
procyclical, historical R in slack years is overstated.

### 2b. tau_l, all three readings stated

Version 1 said there were three and stated none.

| Reading | Value | Construction |
|---|---|---|
| `AMR_0.255` | **0.255** | Acemoglu, Manera and Restrepo (2020), BPEA 2020(1), 231-300, the published effective labour tax rate. Includes the employer side and is a marginal rather than average concept |
| `bottom_up_0.301` | **0.301** | ours, LOW state and local variant |
| `bottom_up_0.318` | **0.318** | ours, HIGH state and local variant |

**The bottom-up construction, per dollar of FRED WASCUR wages and salaries (13,365.2bn):**

    federal income tax on wages = FRED W055RC1Q027SBEA federal personal current taxes
                                  (2,571.4bn) x the IRS SOI 2023 wage share of AGI (0.6675)
                                  / WASCUR                                    = 0.1285
    federal payroll             = federal social insurance contributions (2,074.4bn)
                                  / WASCUR                                    = 0.1552
    state and local, HIGH       = state and local personal current taxes
                                  (FRED W071RC1Q027SBEA) x 0.6675 / WASCUR
    state and local, LOW        = half the high figure, because nine states levy no wage
                                  income tax

**THE BASE IS WASCUR AND THIS IS THE SINGLE MOST IMPORTANT NUMBER IN THIS BRIEF.** tau_l is
built as taxes over wages and salaries, so it must be APPLIED to wages and salaries. Round one
applied it to compensation of employees (COE, 16,224.3bn), which additionally includes
employer pension and health contributions that bear neither the income tax nor the payroll
tax. Every dollar fiscal figure in round one was 21.4 percent too large as a result.

### 2c. tau_k, the full decomposition with every value

    tau_k = sigma_rent * tau_rent + (1 - sigma_rent) * tau_normal
    tau_rent = domestic share * 0.21

| Input | Values carried | Source |
|---|---|---|
| **sigma_rent**, the pure-rent share of capital income | **0.351** sourced; 0.50 and 0.75 as labelled SCENARIOS with no source | Barkai (2020), J. Finance 75(5): pure profit share rises 13.5 points, capital share falls from 32 to 25 percent of gross value added. 13.5 / (25 + 13.5) = 0.351 |
| **domestic share** of profit booked at home | **1.00** closed economy; **0.52**; **0.60**; **0.00** imported capital | Torslov, Wier and Zucman: "close to 40% of multinational profits are shifted to tax havens globally"; 48 percent of foreign-affiliate pre-tax profit made in havens |
| **tau_stat** | **0.21** | US statutory federal corporate rate since the 2017 Act |
| **tau_normal**, the effective rate on the NORMAL return | **0.05** post-TCJA; 0.10 for the 2010s; 0.20 for 2000 | Acemoglu, Manera and Restrepo (2020), verbatim: "Effective capital taxes on software and equipment ... 10 percent in the 2010s and 5 percent after the 2017 tax reforms, though they used to be about 20 percent in 2000" |

**THE EXPENSING RESULT, which version 1 omitted and which decides the whole section.** Under
full immediate expensing a business-level capital tax becomes a cash-flow tax, which exempts
the normal return and falls only on rents. Auerbach (2017), NBER WP 23881, verbatim: "Hence,
the cash-flow tax acts as a tax on pure profits, exempting only the normal return from
taxation." AMR show the same algebra: "with immediate expensing (alpha_j = 1), we have
tau_k,j passthrough,equity = 0".

**Full expensing is in force in 2026**: 26 USC 168(k)(1)(A) gives 100 percent and the
phase-down in 168(k)(6) is repealed by Pub. L. 119-21 sec. 70301(b)(1)(B), 4 July 2025. So
**tau_normal is 0.05, the post-TCJA figure, and the near-zero end of the grid is real.** A
replicator who sets tau_normal in 0.10 to 0.20 will get a grid floor around 0.114 instead of
0.032, and because that floor already sits above the required rate the fiscal condition will
appear to PASS. That is exactly what happened in round one. **It is the single error most
likely to reverse this project's headline result, and it comes from one unstated number.**

**The sourced grid** (sigma_rent held at the sourced 0.351, all four domestic shares, all
three tau_normal values): **0.03245 to 0.20351**.

| Corner | Arithmetic |
|---|---|
| minimum 0.03245 | imported capital (domestic 0.00), tau_normal 0.05: `0.351 x 0 + 0.649 x 0.05` |
| **operative 0.07078** | domestic 0.52, tau_normal 0.05: `0.351 x (0.52 x 0.21) + 0.649 x 0.05` |
| maximum 0.20351 | closed economy, tau_normal 0.20: `0.351 x 0.21 + 0.649 x 0.20` |

The **operative** rate, 0.0708, is the one every verdict is taken against: it is the current
tax code with observed profit shifting. Call it that; version 1 did not name it at all.

### 2d. The required tau_k and the verdict

    required tau_k = tau_l * (1 - R)

| tau_l | required tau_k |
|---|---|
| 0.255 | **0.110079** |
| 0.301 | **0.129937** |
| 0.318 | **0.137276** |

**The result to look for: the required tau_k exceeds the OPERATIVE 0.0708 at every reading of
tau_l, and the condition fails.** It also fails under the replicator's own R of 0.6233, which
round one confirmed independently.

**The clause that must travel with it, and version 1 did not carry it.** The required rate
does NOT exceed the top of the sourced range, 0.20351, at any reading of tau_l. The condition
is unclosable **under the tax code as it stands**, not under every reading of the corporate
tax literature. State it that way.

**Sealed:** `fiscal.R_2026`, `fiscal.tau_k_sourced_low`, `.tau_k_sourced_high`,
`.tau_k_needed_bottom_up_0.301`, `.tau_k_needed_AMR_0.255`, `.condition_passes`.

---

## 3. Fiscal and trust fund magnitudes at 10 and 25 percent of the total wage bill

**The axis is the share of the TOTAL wage bill displaced**, never the share of an exposed
group. A top quintile is a moving denominator across indices and is not comparable.

**Terminal-year loss, not cumulative divided by horizon.** A cumulative loss is a stock; an
annual loss is a flow. The terminal-year loss is close to horizon-invariant; the cumulative
loss rises with horizon.

### 3a. The exact loss expression, which version 1 did not give

    D    = d_wb * W                                   W = FRED WASCUR = 13,365.2bn
    k    = tau_l * (1 - R) - tau_k + g * (1 - rho)
    terminal-year loss = k * D
    cumulative loss    = k * D * (H + 1) / 2          linear ramp over H years
    present value      = sum over t of k*D*(t/H) / (1.03)^t

**The sealed figures are at:** tau_l `bottom_up_0.301`, tau_k `barkai_rent_0.351` (0.0708),
outlays `no_outlays` (g = 0), rho mode `fitted`, **horizon 10**, and are the **MEAN ACROSS
THE THREE EXPOSURE GROUPS** at that dose. Version 1 stated none of those five and a
replicator cannot match without all of them. The discount rate is **0.03**.

**R on the extended axis** is not the observed 2026 value: it is `rho * omega * (0.58 ^
max(times - 1, 0))`, where rho comes from the section 1 fitted line solved as a fixed point
against the stock-flow identity

    nonemp = nonemp_0 + 100 * d_emp * (1 - rho) * (1 - 0.462)

with an exit share of **0.462** and a switcher omega of **0.58** (Huckfeldt 2022, AER 112(4),
occupation switchers lose 42 percent initially against 21 percent for stayers). Rows where
terminal nonemployment exceeds the observed maximum of **24.71** are flagged outside the data
and must be reported as extrapolations, not estimates.

**The loss is NOT linear in the dose.** The sealed terminal loss goes 85.17 to 301.89 between
the 10 and 25 percent doses, a ratio of 3.54 against a dose ratio of 2.5, because R falls as
the dose rises. A linear rebuild cannot match.

### 3b. The trust funds, with the denominators stated

Version 1 insisted the denominator is fund payroll income and never gave it. Both are read
from the **2026 Trustees Reports summary tables, Table 5** (program income, 2025):

| Fund | Payroll income | Total income | Payroll share |
|---|---|---|---|
| OASDI | **1,322.6bn** (OASI 1,130.7 + DI 191.9) | 1,449.3bn | **0.9126** |
| HI | **403.2bn** | 462.4bn | **0.8720** |

**462.4bn is HI TOTAL income**, including interest (9.1), government contributions (1.1),
beneficiary premiums (6.0), taxes on benefits (41.1) and other (1.9). It is not a payroll
denominator. **The two funds have DIFFERENT payroll shares and using OASDI's for HI
overstates every HI ratio by a factor of 1.047.**

**The ratio construction, which makes the rate and the wage bill base both cancel:**

    OASDI ratio = (d_wb * total_wage * taxable_share_of_group / total_taxable)
                  * (1 - R) * 0.9126
    HI ratio    = d_wb * (1 - R) * 0.8720

where `taxable_share_of_group` is the share of that exposure group's wage bill under the
**2026 OASDI contribution and benefit base of 184,500 dollars** and `total_taxable` the same
for all workers. HI has no cap, so its expression carries no taxable share. The additional
0.9 percent Medicare surtax above 200,000 is NOT modelled.

Because the base cancels, **these ratios did not move when the wage bill base was corrected.**

**Bound to check before reporting anything:** every trust fund loss must lie between 0 and
100 percent of that fund's payroll income. Dividing a general-revenue loss by a payroll-only
denominator produced 107 and 215 percent in an earlier version of this work.

### 3c. Trust fund reserves and depletion, new in round two

Round one recorded these as blocked. They are now read from **Table 4** (end of 2025) and
**Tables 7, 8, 10 and 12**:

| Fund | Reserves, end 2025 | Net change 2025 | Depleted | Scheduled benefits payable then |
|---|---|---|---|---|
| OASI | 2,338.3bn | **-200.0bn** | **2032 Q4** | 78 percent |
| DI | 223.0bn | +39.8bn | not within 75 years | 100 percent |
| OASDI combined | 2,561.3bn | -160.2bn | **2034 Q3** | 83 percent |
| HI | 255.7bn | **+18.2bn** | **2033 Q2** | 89 percent |

**160.2bn is the OASDI NET CHANGE IN RESERVES in 2025**, the amount by which cost exceeded
TOTAL income including interest. It is not an HI figure and not a payroll-only balance.

**HI was NOT in deficit in 2025: its reserves ROSE.** The Trustees put the first year HI cost
exceeds income excluding interest at 2026 and including interest at 2027. Any text saying HI
is already in deficit is wrong.

**Depletion timing is carried as a capacity measure in its own right.** A reserve stock says
how much; a depletion date says how long, and for a fund running down that is the number a
supervisor uses.

**Sealed:** `fiscal_magnitudes.terminal_year_loss_bn_at_10pct` and `_at_25pct`,
`.pct_of_receipts_at_10pct` and `_at_25pct`, `trust_funds.*`.

---

## 4. Survey under-reporting factors

**Two different objects, and they must not be multiplied into one.**

    under-reporting factor = official aggregate / FULL SIPP household universe
    coverage share         = working-core balance / FULL SIPP household universe

Only the first is a survey correction. The second is a fact about which households the
analysis subsample covers. The official aggregate divided by the working-core balance is the
first DIVIDED BY the second and embeds a coverage adjustment inside a survey correction.

**Construction.** Reference-person weights, household level, `MONTHCODE == 12`, positive
weight, **working core definition A** of section 0b for the coverage share.

**The official aggregates, all four on the same 2026Q2 vintage:**

| Book | Aggregate | Source |
|---|---|---|
| mortgage | 13,100bn | NY Fed HHDC 2026Q2 |
| student | 1,650bn | NY Fed HHDC 2026Q2 |
| card | 1,357.2bn | FRED `REVOLSL`, **stated in MILLIONS**, 2026-07 |
| auto | **1,713bn** | NY Fed HHDC 2026Q2, the report's own data workbook, "Page 3 Data" |

**On the auto aggregate.** FRED MVLOAS was discontinued after 2024Q4 and round one used it,
two years stale against every other input. Fed G.19 no longer publishes a live motor vehicle
loan balance. The NY Fed report is the replacement and it is already the source for two of
the other three books. The PDF gives auto only as a quarterly percentage change; take the
level from the workbook.

**On the card aggregate.** Revolving consumer credit (REVOLSL, 1,357.2bn) and the NY Fed
credit card balance (1,263bn) are different objects. This project uses REVOLSL. That is a
stated choice, not an oversight.

**The identity to check:** factor divided by coverage share reproduces the working-core
figure to three decimals.

**Sealed:** `under_reporting.{loan}` and `under_reporting.coverage_share.{loan}`.

---

## 5. Household first-round losses at 10 percent of the total wage bill

**Round one produced no value here. This section is rewritten from nothing.** It answers
additions 1 to 6 of the replication report.

**Losses are exposure at default times LOSS GIVEN DEFAULT.** Not exposure at default times a
portfolio loss rate. The second form applies the probability of default twice, and in this
project it made the credit channel look 21.7 times smaller than it is.

### 5a. The dose-to-household mapping (report addition 1, the one that blocked the section)

**There is no selection of households.** A dose is not converted into a named set of displaced
households. It is converted into a **probability applied to every working-core household**,
as follows.

1. **The share of working-core EARNERS displaced is set equal to the share of the total wage
   bill displaced, to first order.** Call it `s`. At a 10 percent dose, `s = 0.10`.
2. For each household, let `n` be its number of employed members. Then

       n >= 2:   p_one = 2 * s * (1 - s)        p_two = s ** 2
       n == 1:   p_one = s                      p_two = 0

   that is, a binomial draw over the household's earners at rate `s`, capped at two.
3. The household's **default probability uplift** is

       dp = p_one * 0.050 + p_two * 0.080

4. **Exposure at default** for a book is `sum over households of dp * weight * balance`,
   then multiplied by that book's under-reporting factor from section 4.
5. **Loss** is exposure at default times LGD.
6. **Bank-held slice** is the DFAST implied portfolio balance for that book divided by the
   national household balance for that book, capped at 1.

**The exposure group does not enter the first-round credit mapping at all**, which is why
report addition 2 has no answer of the kind expected: the dose is applied economy-wide across
the working core, not to an exposure group's households. The exposure group enters the
FISCAL side (section 3) and the second round (section 11), where the sealed note "50 percent
cognitive AIOE dose" belongs.

### 5b. The default uplifts (report addition 6)

From Gerardi, Herkenhoff, Ohanian and Willen, verified from
`data/raw/manual/GHOW2018_cant_pay.pdf`:

| | |
|---|---|
| one displaced earner in the household | **+5.0 percentage points** of default probability |
| both head and spouse with a spell | **+8.0 percentage points**, which is SUPERADDITIVE, not 10 |
| job loss expressed as an equity equivalent | a **35 percent** decline in equity |

Version 1 said "more than 8.0 points" and the replicator correctly objected that "more than
8.0" is not a number. **The number used is 8.0.**

### 5c. The DFAST parameters, with locators (report additions 3 and 4)

Document: **2026 Federal Reserve Stress Test Results, June 2026**,
`federalreserve.gov/publications/files/2026-dfast-results-20260624.pdf`, 68 pages, 32 banks,
horizon 2026:Q1 to 2028:Q1, nine quarters.

**Table 2**, severely adverse scenario: unemployment peak **10.0 percent** (a rise of 5.5
points), real GDP peak to trough **-4.6 percent**, house prices **-30 percent**, CRE prices
-39 percent, equity -58 percent, BBB spread +4.7 points.

**Table 4**: aggregate CET1 **12.8 percent** of **12,583.7bn** RWA at 2025:Q4, falling to a
projected minimum of **11.2 percent**; regulatory minimum 4.5 percent per 12 CFR 217.10.
Losses absorbed in the test: **708bn**.

**Table 9**, projected aggregate loan losses, severely adverse:

| Line | Loss, bn | Loss rate | Implied portfolio balance, bn |
|---|---|---|---|
| TOTAL loan losses | **624.9** | 6.9 percent | |
| First-lien mortgages, domestic | **22.5** | **1.5 percent** | **1,500** |
| Junior liens and HELOCs, domestic | 5.5 | 3.2 percent | 172 |
| Credit card | **203.0** | **17.1 percent** | **1,187.1** |
| **Other consumer** | **54.1** | **7.3 percent** | **741.1** |
| Commercial and industrial | 158.2 | | |
| Commercial real estate, domestic | 76.5 | | |

**THE "OTHER CONSUMER" LINE IS SHARED BY AUTO AND STUDENT AND THIS MUST BE STATED WHEREVER
EITHER APPEARS.** The Federal Reserve does not break auto out from student loans. Both rows
are therefore scored against the SAME 54.1bn loss and the SAME 741.1bn implied balance. The
replicator inferred this correctly from the sealed pairs; it should never have had to be
inferred. It means the auto and student percentages of the Fed loss are not independent of
one another and cannot be summed.

**Bank-held shares** follow from the implied balances above over the national aggregates of
section 4: mortgage `1500 / 13100` = 0.115, card `1187.1 / 1357.2` = 0.875, auto
`741.1 / 1713` = 0.433, student `741.1 / 1650` = 0.449. Note that the auto share MOVED when
the auto aggregate was corrected, and that the auto loss did not, because the same aggregate
sits in the under-reporting factor and in the bank share and cancels.

### 5d. LGD ranges, and which end "hi" is (report addition 5)

| Book | LGD range |
|---|---|
| mortgage (first lien) | **0.25 to 0.40** |
| credit card | **0.80 to 1.00** |
| auto | **0.45 to 0.65** |
| student | **0.75 to 1.00** |

**"hi" is the TOP of the LGD range.** `loss_hi = exposure at default x the upper LGD x the
bank-held share`.

**Order of operations, which version 1 left open:** the under-reporting scale-up is applied
to exposure at default FIRST, then the LGD, then the bank-held share. The default uplift is
inside exposure at default and therefore comes before all three.

**Where the mortgage LGD range comes from:** the Fed's own first-lien loss rate of 1.5 percent
over nine quarters implies, for a cumulative default rate `d`, an LGD of `0.015 / d`. At a 4
to 6 percent cumulative default rate in a severely adverse scenario that is 0.25 to 0.375,
which brackets the conventional 30 to 40 percent severity.

**Scope, which must travel with every one of these numbers.** This is a FIRST-ROUND figure. It
holds house prices, consumer demand, business revenue and the employment of non-displaced
workers fixed. The Federal Reserve's severely adverse scenario moves all of those together.
Comparing the two is a **LOWER BOUND** on bank losses, not an estimate.

**Sealed:** `household_first_round.{loan}_bank_loss_hi_bn_at_10pct` and
`.{loan}_pct_of_fed_at_10pct` for each of the four books.

---

## 6. The OASDI earnings cap contrast, and the pay control

**Construction.** For each exposure group, the share of the group's wage bill that sits under
the **2026 contribution and benefit base of 184,500 dollars**, weighted by person weights, on
employed workers with positive earnings. Compute it on ACS annual wage income and,
independently, on SIPP annualised monthly earnings.

**Wage vintage.** ACS 2023 wages are used **without inflating** to 2026 against the 2026 cap.
That understates the share above the cap and is a stated choice; version 1 left it open.

**Which Eloundou measure.** The replication package supplies alpha, beta and gamma under both
human and model labels. This project uses **human-labelled beta**.

**The crosswalk and the aggregation rule** (the replicator's own diagnosis of their AIOE gap).
ACS publishes broad and wildcarded SOC codes such as `5191XX` while both exposure indices are
detailed six-digit SOC. Aggregate index scores to the ACS SOCP code using **OES May 2021
employment-weighted means within each matched prefix**, and report the match rate: AIOE
matches 476 of 530 ACS SOCP codes, GPT 524. **The 54-code gap is enough to move the AIOE
group's pay composition**, so a replicator whose AIOE match rate differs from 476 should
expect the AIOE rows to differ and should say so rather than treat it as a discrepancy.

### 6a. The pay control has FOUR cells, not one

Version 1 described one reweighting and sealed four. Both dimensions:

**Two outcome variables:**

1. `share_under_OASDI_cap`, the cap contrast above.
2. `distress_pp_per_bn`, the increment in the share of obligated working-core households
   above a 50 percent debt-service-to-income ratio, per billion dollars of wage income
   destroyed. **Version 1 never mentioned this variable anywhere.**

**Two reweighting directions:**

- **direction a**: the COGNITIVE group is reweighted onto the EMBODIED group's distribution
  across deciles of individual annual wage income.
- **direction b**: the EMBODIED group is reweighted onto the COGNITIVE group's.

`share_of_gap_that_is_pay` is `1 - (adjusted gap / raw gap)` in each cell. Version 1's stated
"54 to 99 percent" band spans BOTH directions and never said so: 0.539456 is the ACS AIOE
direction-b value on the cap outcome.

**The finding.** Neither exposure-type contrast survives the pay control. Between 1.0 and 11.4
percent of the raw gap remains at the weaker end, and the SIPP Eloundou GPT cap contrast
**reverses sign** (both a and b exceed 1). Report a **PAY mechanism with an exposure-type
CORRELATE**, not an exposure-type mechanism.

**Sealed:** `cap_contrast.{dataset}.{group}`; `pay_control.{dataset}_{outcome}_{index}` with
`raw_gap`, `share_of_gap_that_is_pay_a` and `share_of_gap_that_is_pay_b`.

---

## 7. The incidence comparison

**Round one produced no value here.** This section answers report additions 7, 8 and 9.

Same TOTAL employment loss of **10 percent of employment**, delivered three ways.

### 7a. The three cases, defined (report addition 7)

| Case | Definition |
|---|---|
| **(a) incumbents** | the loss falls on **employed workers in exposed occupations**. Worker-level displacement probability `p(r) = min(1, a * r ** gamma)` where `r` is the employment-weighted percentile rank of the occupation's exposure score, `gamma = 3.0`, and `a` is solved by bisection so the employment-weighted mean of `p` equals the target share of total employment |
| **(b) entrants** | the loss falls on **people aged 22 to 29 who are not hired**. Their balance sheets are those of households containing a person aged 22 to 29. Calibrated for cognitive exposure to Brynjolfsson, Chandar and Chen (August 2026): employment of 22 to 25 year olds in AI-exposed occupations stands **19 percent** below the less-exposed counterfactual, operating through reduced hiring rather than separations |
| **(c) sourced mix** | **attrition absorbs job destruction up to the BLS labour force exit rate of 3.86 percent a year; the remainder falls on incumbents.** That rate is the source version 1 promised and did not attach (report addition 8) |

**Within-occupation incidence**, a second and separate dimension: `uniform`,
`lowest_wage_first`, `highest_wage_first`. The tilt is a multiplicative factor `m(q)` in the
worker's within-occupation wage percentile `q`, proportional to `(1 - q) ** 2` or `q ** 2`,
rescaled by bisection so the employment-weighted expected count is unchanged, then clipped to
[0, 1] and rescaled again until the count matches to 1e-6.

### 7b. The equity interaction

The outcome is a default probability, not a DSTI crossing, because Gerardi and coauthors show
affordability thresholds miss most defaults: only 30 percent of defaulters would need to drop
below subsistence to stay current, and 38 percent could pay without reducing consumption at
all. The GHOW uplifts of section 5b are interacted with each household's equity position: a
household whose equity is already below the level at which a further **35 percent** decline
would put it underwater is in the double-trigger region. Equity is **home value minus home
debt** in SIPP. **ACS has no mortgage balance, so the equity split is SIPP-only** and ACS
carries the tenure and scale side.

### 7c. What the spread is taken over (report addition 9)

**Max over min across the three cases (a), (b) and (c)**, holding the total employment loss
fixed.

**The result:** on household COUNTS incidence moves the answer by 5 to 9 percent. On the
DOLLARS those households owe it moves it by 1.75 to 3.01 times. **No dollar figure from this
engine may be quoted without naming the incidence assumption.** The count figures are robust
to it and can stand alone.

**Sealed:** `incidence.household_count_spread_low` and `_high`, `.dollar_spread_low` and
`_high`.

---

## 8. What a replicator should expect to find wrong if they follow the old path

These are errors this project made. A replicator who reproduces them has followed the wrong
construction, not found a discrepancy.

| Error | Symptom |
|---|---|
| Vacant units counted as households | 145.33m households instead of 131.33m |
| Portfolio loss rate applied to exposure at default | credit losses 21.7 times too small |
| General-revenue loss over a payroll-only denominator | trust fund losses above 100 percent |
| Cumulative loss divided by horizon | terminal loss falls with horizon instead of holding flat |
| Aggregate over the working-core balance | under-reporting factors 14 to 26 percent too large |
| REVOLSL or GFDEBTN read as billions | scaling factors in the thousands |
| rho fitted on the unemployment rate | see appendix A; the caveat matters |
| **tau_normal set at 0.10 to 0.20** | **the fiscal condition appears to PASS. New in v2: it is the error most likely to reverse the headline** |
| **A wage tax rate applied to compensation of employees** | **every fiscal dollar figure 21.4 percent too large. This one was ours** |
| **The OASDI payroll share applied to HI** | **every HI ratio 4.7 percent too large. This one was ours** |
| **A break-even rate computed from a loss that already nets out tau_k** | **a break-even rate above tau_l, which is impossible. This one was ours** |
| **FRED MVLOAS used for the auto aggregate** | a 2024Q4 figure among 2026 inputs |

---

## 9. Tolerances

Survey-based quantities carry a **2 percent relative** tolerance for weight and vintage
differences; fitted coefficients **5 percent relative**; ratios and shares an **absolute 0.01**.
A rebuilt value outside its tolerance means the claim resting on it does not stand until the
difference is explained.

**Plausibility bounds are not tolerances and are not negotiable.** State the bound before the
number, every time. The bounds now enforced, which version 1 did not carry:

- a share is 0 to 1; a rate is 0 to 100 percent
- a loss on a tax cannot exceed that tax base
- a loss cannot exceed the balance it sits on
- a subset cannot exceed its total
- **a break-even capital tax rate under case A cannot exceed tau_l + g**
- **no break-even capital tax rate, either case, can exceed 1**
- **case B break-even cannot fall below case A**
- **a break-even rate exists only while the post-shortfall surplus is positive**

Round one broke the first two of those four break-even bounds, once on each side: this
project's case A maximum of 0.378371 exceeded tau_l, and the replicator's case B maximum of
1.0979 exceeded 1.

---

## 10. The sovereign share of losses

**Round one produced no value here.** This section answers report additions 10 to 14.

**Construction.** At each dose, sum every loss that ultimately lands on the federal government
and compare with the sum landing on private balance sheets.

### 10a. What counts as federal

| Component | Basis |
|---|---|
| general revenue | the public budget row, section 3 |
| OASDI and HI | payroll-funded federal trust funds, section 3b |
| federal student | **97.3 percent** of the student book, FRED `FGCCSAQ027S` 1,605.134bn against the NY Fed 1,650bn |
| FHA | the Mutual Mortgage Insurance Fund is a federal fund; a loss there is federal on the first dollar |
| GSE beyond capacity | the Enterprises are in conservatorship, so beyond their own layers the Treasury senior preferred agreement binds |

**Private:** bank mortgage portfolios; CRT and private mortgage insurance investors; residual
mortgage holders; auto and card lenders; the private slice of the student book; and in the
second-round column, the whole of the Fed-mapped bank loss.

**Not counted anywhere:** scenario outlays, reported on their own line because they are a
policy choice rather than a loss; and VA, which has no separate fund and whose losses are
federal on the first dollar but whose book size was not sourced.

**The federal student share is the single fact that moves the answer most.** A replicator who
uses a bank-held share for student loans will get a materially lower federal share.

### 10b. The waterfall on the agency book, in order (report addition 11)

**Credit risk transfer and private mortgage insurance are LOSS TRANSFERS taken BEFORE
Enterprise capital, not additions to it.** The order, and it is easy to get wrong:

    transferred        = min(GSE loss, CRT risk in force + PMI risk in force)
    retained           = GSE loss - transferred
    absorbed           = min(retained, Enterprise capital + one year of PPNR)
    beyond             = max(0, retained - Enterprise capital - one year of PPNR)   FEDERAL

| Layer | Value | Source and locator |
|---|---|---|
| **CRT risk in force** | **210.0bn**, 3.2 percent of about 6.7tn UPB | FHFA *Credit Risk Transfer Progress Report, Fourth Quarter 2023*, `data/raw/manual/FHFA_CRT_progress_4Q2023.pdf`. **FLAGGED AS STALE**, 4Q2023 against a 2026 book |
| **PMI risk in force** | Fannie Mae **201.355bn**, Freddie Mac **181.5bn**, total **382.855bn** | 2025 Forms 10-K. Fannie: total mortgage insurance risk in force 201,355m, 6 percent of the single-family conventional guaranty book; loans with credit enhancement 1,663bn UPB, 47 percent of the book. Freddie: primary MI on 22 percent of the portfolio, CRT and other on 52 percent, 39 percent not credit enhanced; insurers' maximum loss limits 181.5bn |
| **Enterprise capital** | **190.436bn** combined net worth: Fannie **112.667bn** at 2026-03-31 (10-Q, CIK 0000310522, `StockholdersEquity`), Freddie **77.769bn** at 2026-06-30 (10-Q, CIK 0001026214) | SEC XBRL company facts |
| **One year of pre-provision pre-tax earnings** | **34.24bn** | FY2025 Forms 10-K via the SEC XBRL API: net income plus income tax expense plus the provision for credit losses |
| capital + 1y earnings | **224.676bn** | the layer that must be exhausted before the federal layer binds |

**FLAG that must travel with every agency figure:** the GSEs are in conservatorship. Net worth
is not loss-absorbing capital of the same kind as bank CET1 and the Treasury senior preferred
agreements sit behind it. This is a scale comparison, not a solvency test.

### 10c. FHA (report addition 12)

| | |
|---|---|
| insurance in force | **1,647.0bn**, FY2025 |
| capital ratio | **11.47 percent**, statutory minimum 2 percent |
| economic net worth | **188.911bn** |

**FLAGGED PROXY**, recorded in `lit/unverified.md`: hud.gov returns HTTP 403 to this
environment on every route, so the FY2025 MMI Fund figures come from secondary reporting and
are not cited to the source document. A replicator with HUD access should treat this as the
weakest sourced number in the section.

### 10d. The mortgage holder split (report addition 13)

| Holder | Share of the 13,100bn book | Basis |
|---|---|---|
| GSE (agency) | **51.1 percent** | 6,694bn |
| FHA | **12.6 percent** | 1,647bn |
| bank portfolio | **11.5 percent** | 1,500bn, the DFAST implied first-lien balance |
| **residual** | **24.9 percent** | the remainder |

**The residual is treated as PRIVATE in full.** That is a stated choice and it is the
conservative one for the sovereign claim, because any federal fraction inside the residual
would raise the federal share rather than lower it. Three of the four shares are read from a
publisher; the residual is the arithmetic remainder.

### 10e. The second-round federal term

The federal side grows in the second round too: the demand shortfall is itself taxed income,
so general revenue falls again. It is charged at the same effective labour tax rate used
throughout:

    second-round federal = 0.301 * severity ratio * 0.046 * GDP

**Sealed:** `sovereign.federal_share_first_round_min` and `_max`,
`.federal_share_with_second_round_min` and `_max`, `.federal_student_share`.

---

## 11. The second round: the model, stated

**Round one produced no value here, because version 1 gave five input ranges and no
equations.** This section answers report additions 15 to 19.

### 11a. The chain, end to end (report addition 15)

    D    = delivered dose * W                          W = FRED WASCUR = 13,365.2bn
    dW   = (1 - R) * D                                 net fall in aggregate wage income
    dC   = (mpc_L - mpc_K) * dW                        demand shortfall
    severity ratio  s = (dC / Y) / 0.046               against the Fed's GDP fall
    bank losses     = 624.9 * f(s)                     f is the loss mapping, 11c
    job losses, pct = 100 * okun * (dC / Y)
    house price fall, pct = 100 * elasticity * dW / W

**There is no separate demand-to-revenue or revenue-to-loss step.** The module maps the demand
shortfall onto the Federal Reserve's own severely adverse scenario by ratio and applies the
Fed's published loss totals scaled by that ratio. That is the whole of the mapping, and saying
so plainly is what version 1 failed to do. Business credit, CRE and cards enter ONLY through
this mapping.

### 11b. The income measure the house price elasticity acts on (report addition 16)

**`dW / W`, the net fall in aggregate wage income as a share of the national wage bill.** Not
GDP, not household disposable income, not the displaced group's own income. The replicator
inferred a single income fall of about 31.4 percent from the sealed pairs; at the headline
scenario that is exactly `dW / W` at a 50 percent cognitive AIOE dose.

### 11c. The three loss mappings, with functional forms (report addition 17)

| Mapping | Form | What it assumes |
|---|---|---|
| **linear** | `f(s) = s` | losses scale one for one with severity beyond the Fed's point |
| **capped at fed** | `f(s) = min(s, 1)` | refuses to extrapolate beyond the Fed's own severity |
| **convex** | `f(s) = s ** 1.5` | the shape loss curves usually take |

**No source exists for any of them beyond the Fed's single point.** All three are STATED
ASSUMPTIONS and the spread between them is the honest statement of what is not known.

### 11d. Every input range, with its source

| Input | Range | Grid points carried | Source |
|---|---|---|---|
| MPC out of labour income | 0.70 to 1.00 | **0.70, 0.90, 1.00** | Mian, Straub and Sufi, NBER WP 26941; Fagereng, Holm and Natvik, AEJ Macro 13(4), 2021 |
| MPC out of capital income | 0.35 to 0.55 | **0.35, 0.45, 0.55** | the same two |
| Income elasticity of house prices | 0.21 to 1.50 | **0.21, 0.27, 0.38, 0.81, 1.00, 1.50** | Harter-Dreiman (OFHEO WP 03-2, 2003) 0.27 national, 0.38 constrained, 0.21 unconstrained; Duca, Muellbauer and Murphy (JEL 59(3), 2021) at the top |
| Okun coefficient | 0.372 to 0.50 | **0.372, 0.402, 0.421, 0.50** | Ball, Leigh and Loungani (JMCB 49(7), 2017) Table 1: -0.421 (HP 100), -0.372 (HP 1000), -0.402 (first differences). **0.50 is the earlier assumption, above the whole sourced range, carried only to show what it did** |
| Loss mapping | three | linear, capped, convex | no source; stated assumptions |

**The MPC ranges are a spread, not an estimate.** Both sources measure TRANSITORY shocks and
displacement is persistent. A persistent loss has a higher marginal propensity than a
transitory one for a liquidity-constrained household and a lower one for an unconstrained
one, so the spread between the two MPCs is if anything understated.

### 11e. The grid (report addition 18)

**3 x 3 x 6 x 4 x 3 = 648 combinations**, at the headline scenario, which is the **50 percent
cognitive AIOE dose**. Version 1 listed five inputs with ranges and never said how many points
each carried. Round one's replicator inferred a three-by-three-by-three grid from a sealed
share of 17/27; that share is now **0.740741 = 20/27**, and it still factorises that way
because `demand_event_first` depends only on the two MPCs and the house price elasticity, which
carry 3, 3 and 6 points but collapse to 3 distinct severity levels and 6 elasticities. State
the full grid; do not infer it.

### 11f. The two severities that are compared (report addition 19)

| | |
|---|---|
| **demand severity** | `(dC / Y) / 0.046`, the demand shortfall as a share of GDP over the Fed's GDP fall |
| **house price severity** | `(elasticity * dW / W) / 0.30`, the implied house price fall over the Fed's 30 percent |
| `demand_event_first` | demand severity **strictly greater than** house price severity |

**The variance decomposition** is a one-way analysis: for each input, the variance of the group
means of the target across that input's levels, divided by the total variance of the target,
`ddof = 0`. It is a share of variance explained by that input alone and the shares do not sum
to 1 because interactions are not allocated.

### 11g. The result and the one clause to check hardest

**The ratio is robust. The level is not.** Across the sourced ranges the second-round bank loss
at the headline dose spans a factor of nine, and roughly nine tenths of the total arrives
through consumer spending, house prices and business credit rather than through displaced
borrowers' own loans.

**"A demand event first, the opposite of 2008" holds at every Harter-Dreiman elasticity and
fails entirely at an elasticity of 1.5.** A replicator who uses only the 2003 estimate will
confirm it; one who uses the modern survey will not. **Report the share of combinations, not
a verdict.**

**Sealed:** `second_round.bank_losses_bn_min`, `_max`, `_median`,
`.house_price_fall_pct_min` and `_max`, `.demand_event_first_share`.

---

## 12. Case A and case B

**They are not interchangeable and every number must carry its case.**

**Notation, fixed here because version 1 used `dW` for two different things:**

| | |
|---|---|
| `D` | the **GROSS** displaced wage bill, `delivered dose x W` |
| `dW` | the **NET** wage income fall, `(1 - R) * D` |
| `dC` | `(mpc_L - mpc_K) * dW` |
| `w_s` | `W / Y`, the wage share of output, **0.4154** on WASCUR over GDP |
| `tau_k` | the **operative** 0.0708, the same rate the loss is built on |

**Case A, output preserved.** The displaced wage bill accrues to capital. The labour tax is
lost on the NET fall; the capital tax is levied on the GROSS displaced wage bill. That
asymmetry is where the `(1 - R)` comes from and version 1 got it wrong.

    fiscal loss      = tau_l * dW - tau_k * D  =  [tau_l * (1 - R) - tau_k] * D
    break-even tau_k = tau_l * (1 - R) + g * (1 - rho),  which at g = 0 is  tau_l * (1 - R)

**Case B, output falls with demand.** The shortfall is not offset, so output falls by it, the
surplus rises by less, and a second round of wage income goes with the output fall.

    fiscal loss      = case A loss + tau_k * dC + tau_l * w_s * dC
    break-even tau_k = tau_l * ((1 - R) * D + w_s * dC) / (D - dC)

**Version 1's section 12 was wrong** and is the reason round one's replicator could not
reconcile the sealed values with the stated formula. It wrote the case A loss as
`tau_l * dW - tau_k * dW`, which gives a break-even of `tau_l`, not `tau_l * (1 - R)`.

**The bounds** of section 9 apply and must be checked before anything is reported. Case A's
maximum is `tau_l` exactly, reached where R falls to zero. Case B may legitimately exceed
`tau_l`, because the base shrinks as the loss grows, but it may not exceed 1.

**Every fiscal figure published by this project before the closing session is a CASE A
figure.** Case B is the internally consistent one whenever the second-round module is quoted.

**Sealed:** `cases.case_B_over_A_min` and `_max`, `.break_even_tau_k_case_A_min` and `_max`,
`.break_even_tau_k_case_B_min` and `_max`.

---

## 13. Debt paths

**Report increments, never levels.** A debt-to-GDP path under r above g compounds the EXISTING
debt whether or not anything is displaced. Compute a no-displacement baseline under the same r
and g and report the difference.

**The three regimes** (version 1 named one):

| Regime | r | g |
|---|---|---|
| reserve currency | 0.040 | 0.040 |
| reserve currency adverse | 0.050 | 0.035 |
| emerging market | 0.090 | 0.030 |

**The recursion**, horizons 10 and 20 years:

    baseline_{t+1} = baseline_t * (1 + r) / (1 + g)
    path_{t+1}     = path_t * (1 + r) / (1 + g) + annual fiscal loss / Y
    increment      = 100 * (path_H - baseline_H)

**The increments are CASE B figures.** Version 1's section 13 never said which case, even
though section 12 insists every figure carries its case.

**The starting ratio**, and version 1 left the GDP concept open: FRED `GFDEBTN` at **2026Q1**,
read as MILLIONS, over the **ANNUAL MEAN of quarterly nominal GDP for 2026** (32,175.9bn),
giving **1.214121**. Using the single quarter's GDP instead gives 1.2259, and everything
downstream moves with it. The replicator reproduced the 20-year baseline exactly once given
our start ratio, which is the cleanest single confirmation of round one.

**The trap:** under r = 9 percent against g = 3 percent, a starting ratio of 121.4 percent
reaches about 377 percent in twenty years **with no displacement at all**. A level path
presented as a result about automation is almost entirely that baseline.

**Sealed:** `debt.debt_to_gdp_start`, `.baseline_20y_emerging_market`,
`.increment_pp_at_10pct_reserve_currency_20y`, `.increment_pp_at_10pct_emerging_market_20y`.

---

## Appendix A. The slack measure, and the limit of the instruction in section 1

**This appendix exists because version 1 stated a preference as though it were unconditional
and it is not.**

Section 1 instructs against fitting rho on the unemployment rate. The mechanism argument for
that stands on its own: displacement raises unemployment, workers who exit the labour force
leave the unemployment rate unchanged, and they are exactly the workers who did not get
reemployed, so the unemployment rate is the wrong slack measure for a reemployment hazard.

**But the empirical claim attached to it is false, and on both windows tested.**
`src/slack_window_check.py` fits both specifications on the full sample and on a post-2008
window; its full-sample fits reproduce this project's stored fits to five decimal places.

| Window | n | rho on prime-age nonemployment, R squared | rho on the unemployment rate, R squared | better fit |
|---|---|---|---|---|
| full sample, 2000 to 2026 | 14 | 0.77333 | **0.81191** | the unemployment rate |
| post-2008, 2010 to 2026 | 9 | 0.73199 | **0.93993** | the unemployment rate |

**The unemployment rate fits better on BOTH windows, and its advantage is LARGER post-2008,
not smaller.** This was written expecting to record a post-2008 restriction on the
preference. There is none. There is no window on which prime-age nonemployment wins on fit.

**So the preference is a preference on MECHANISM alone and has to be defended that way every
time it is stated.** The mechanism argument is unaffected and still stands: the unemployment
rate cannot measure the slack a reemployment hazard responds to, because the workers who
leave it unchanged by exiting the labour force are exactly the workers who did not get
reemployed. The post-2008 result is what a circularity should look like as exits became more
important: the circular fit gets BETTER, not worse.

**What this means for a replicator.** Fit both. Report both. Anyone who selects the
specification on R squared will select the circular one on either window, and they will not
be making an arithmetic error; they will be making a mechanism error. Say which you chose and
why.

The full coefficients:

| Window | specification | intercept | slope |
|---|---|---|---|
| full | prime-age nonemployment | 1.22798 | -0.02749 |
| full | unemployment rate | 0.80901 | -0.03043 |
| post-2008 | prime-age nonemployment | 1.17818 | -0.02541 |
| post-2008 | unemployment rate | 0.77942 | -0.02784 |

The related claim in version 1's error table, that the circular fit gives "a speed limit about
2.5 times larger", is **withdrawn**: the slope ratio between the two specifications is
**1.107** on the full sample and **1.096** post-2008. See section 0b on the speed limit.

---

## Appendix B. Embodiment P, the construction version 1 deferred and did not supply

Version 1 pointed at `notes/paei_c_method.md` and the file was not given to the replicator, so
every group split resting on P was rebuilt on a substitute index. The construction is
reproduced here in full so the brief is self-contained. The method note remains at
`notes/paei_c_method.md` for the frontier and the functional forms.

**Source: O*NET 31.0**, `db_31_0_text.zip`, files `Abilities.txt`, `Work Activities.txt`,
`Work Context.txt`, with `Scales Reference.txt` for the scale minima and maxima.

**P, embodiment intensity, is the mean of 15 elements**, each min-max rescaled to 0 to 1 on
its own published scale:

| Element | Name | File | Scale |
|---|---|---|---|
| 1.A.2.a.1 | Arm-Hand Steadiness | Abilities | IM |
| 1.A.2.a.2 | Manual Dexterity | Abilities | IM |
| 1.A.2.a.3 | Finger Dexterity | Abilities | IM |
| 1.A.2.b.2 | Multilimb Coordination | Abilities | IM |
| 1.A.3.a.1 | Static Strength | Abilities | IM |
| 1.A.3.a.4 | Trunk Strength | Abilities | IM |
| 1.A.3.b.1 | Stamina | Abilities | IM |
| 1.A.3.c.3 | Gross Body Coordination | Abilities | IM |
| 4.A.3.a.1 | Performing General Physical Activities | Work Activities | IM |
| 4.A.3.a.2 | Handling and Moving Objects | Work Activities | IM |
| 4.A.3.a.3 | Controlling Machines and Processes | Work Activities | IM |
| 4.A.3.a.4 | Operating Vehicles, Mechanized Devices, or Equipment | Work Activities | IM |
| 4.C.2.d.1.b | Spend Time Standing | Work Context | CX |
| 4.C.2.d.1.g | Spend Time Using Hands to Handle, Control, or Feel Objects | Work Context | CX |
| 4.C.2.d.1.h | Spend Time Bending or Twisting Your Body | Work Context | CX |

**The replicator's substitute** was the mean Importance over 1.A.2 (psychomotor) and 1.A.3
(physical abilities) only: eight of the fifteen elements, and none of the Work Activities or
Work Context ones. It reproduced the sealed embodied cap share to 0.0042 in ACS and 0.0004 in
SIPP. **Do not read that as validation of either index.** The more likely explanation, which
they offered themselves, is that the cap share is insensitive to how the embodied group is
drawn, because the embodied group sits tightly under the cap in both surveys. Rebuild P from
the full 15 and report whether the agreement survives.

**S, environmental structure**, is a difference of two rescaled means, enablers minus
frictions, recentred on 0.5:

*Enablers:* 4.C.3.b.2 Degree of Automation, 4.C.3.b.7 Importance of Repeating Same Tasks,
4.C.3.d.3 Pace Determined by Speed of Equipment, 4.C.2.a.1.a Indoors Environmentally
Controlled, 4.C.2.d.1.i Spend Time Making Repetitive Motions, 4.C.3.b.4 Importance of Being
Exact or Accurate.

*Frictions:* 4.C.3.a.4 Freedom to Make Decisions, 4.C.3.b.8 Determine Tasks Priorities and
Goals, 4.C.2.a.1.c Outdoors Exposed to All Weather, 4.C.2.b.1.e Exposed to Cramped Work Space,
4.C.1.a.4 Contact With Others, 4.C.1.b.1.f Deal With External Customers or the Public,
4.C.3.a.1 Consequence of Error.

**S is demoted and is not load-bearing.** It behaves as a sector proxy and fails as an
occupation-level construct. It appears here only because PAEI(c) is defined in terms of it.

**PAEI(c), the two functional forms:**

    smooth:     PAEI(c) = P * S ** (1 - c)
    threshold:  exposed at c if the structure deficit <= c, magnitude P

**Two corrections the data forced, and both must be carried:**

1. **The raw S scale is degenerate under a threshold.** S has standard deviation 0.071 and
   range 0.29 to 0.70, so thresholding the raw deficit produces a step function: nothing
   exposed below c = 0.25, 37.6 percent at c = 0.50, 100 percent at c = 0.70. The reported
   threshold results use **S_rank**, the employment-weighted percentile rank of S. The raw
   version is retained in the outputs so the degeneracy stays visible.
2. **The threshold rule needs an embodiment gate.** Ungated, the occupations switching between
   medium and high capability were led by Lawyers (P = 0.095) and Chief Executives
   (P = 0.132), which is nonsense. Switchers are gated at the **median P of 0.413** and the
   headline exposure measures are weighted by P.

**Coverage, which bounds everything built on P.** Of 530 ACS occupation codes, 491 are in the
Census 2018 OCCP-to-SOC crosswalk and 375 also have an O*NET 31.0 match. That is 72.4 percent
of the PUMS wage bill and 58.9 percent of NIPA wages and salaries. The uncovered occupations
have a HIGHER mean P (0.410 against 0.368, Welch p = 0.0019), so exposure built on the covered
set is **understated**, and the bounded employment-weighted mean P is 0.380 against 0.348 on
the covered set alone.

---

## Appendix C. What round two should test that round one could not

1. **Sections 5, 7, 10 and 11 at all.** They produced no values in round one. Everything in
   sections 5, 7, 10 and 11 above is new and none of it has ever been checked from outside.
2. **The labour backing quantities**, which are not in this brief and are the subject of a
   separate pass.
3. **The corrected break-even grid.** The bounds in section 9 are new. Break them if you can.
4. **The wage bill base.** If you think WASCUR is the wrong base, say so with the argument,
   because the whole fiscal block scales with it.
5. **Whether the embodied cap share is genuinely insensitive to how P is built**, which round
   one raised and could not settle.
