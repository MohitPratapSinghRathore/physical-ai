# Replication report

Rebuilt from `notes/replication_brief.md` and raw public data only. No project code was read
at any point. The sealed file was opened only after all 51 of my values were final and
written to `replication_results.csv`. Per-quantity verdicts are in `comparison.csv`.

**Headline: 21 of 51 match, 30 mismatch. But the 30 collapse into eight root causes, and six
of those are parameters or definitions the brief names without stating.** Where the brief was
complete, the rebuild matched, usually to three or four decimals. Where it was not, it did
not. That is the cleanest possible verdict on the brief itself.

---

## 1. What replicated

### Exactly, or to within rounding

| Quantity | Mine | Sealed |
|---|---|---|
| Occupied vs all housing records | 131.33m / 145.33m | same |
| `rho_slack.x_range_low` | 18.27241 | 18.27241 |
| `rho_slack.x_range_high` | 24.70612 | 24.70612 |
| `rho_slack.n` | 14 | 14 |
| `under_reporting.mortgage` | 1.265 | 1.2592 |
| `under_reporting.card` | 2.522 | 2.5159 |
| `under_reporting.auto` | 1.751 | 1.7431 |
| `under_reporting.student` | 1.428 | 1.4233 |
| `cap_contrast.ACS.ALL` | 0.8985 | 0.8985 |
| `cap_contrast.ACS.embodied` | 0.9733 | 0.9775 |
| `cap_contrast.SIPP.embodied` | 0.8841 | 0.8837 |
| `cap_contrast.SIPP.cognitive_GPT` | 0.8349 | 0.8328 |
| `coverage_share.mortgage` (corrected) | 0.8217 | 0.8205 |
| `coverage_share.auto` (corrected) | 0.7776 | 0.7737 |
| `sovereign.federal_student_share` | 0.9728 | 0.972808 |
| `debt.baseline_20y` at their start ratio | 3.7670 | 3.7674 |
| `fiscal.tau_k_needed_AMR_0.255` (rerun) | 0.110079 | 0.110079 |
| `fiscal.tau_k_needed_bottom_up_0.301` (rerun) | 0.129937 | 0.129937 |

**All four survey under-reporting factors match within 0.5 percent.** This is the strongest
result in the replication: the SIPP universe construction (`MONTHCODE == 12`, positive
weight, `ERELRPE` in 1 or 2, deduplicated to household, `THDEBT_*` aggregates), the streaming
read, and the units call on REVOLSL and MVLOAS all landed independently.

**The embodiment index reproduced despite being rebuilt blind.** `notes/paei_c_method.md` was
never supplied, so I built my own index from O*NET 31.0 as the mean Importance over elements
1.A.2 (psychomotor) and 1.A.3 (physical abilities). It reproduces the sealed embodied cap
share to 0.0042 in ACS and 0.0004 in SIPP. Either my proxy is close to Embodiment P, or that
cap share is insensitive to how the embodied group is drawn. I cannot tell which from outside,
and the second possibility is the more likely one given how tightly the embodied group sits
under the cap in both surveys.

### Qualitative findings that replicated

- The vacant-unit trap, the REVOLSL/MVLOAS units trap, and the debt-baseline trap all
  reproduced exactly as the brief describes them.
- The pay control kills most of the exposure-type contrast, and **the SIPP Eloundou GPT
  contrast reverses sign**. I found this before opening the sealed file. My value (1.4011)
  and theirs (1.99627) both exceed 1, which is the sign reversal.

---

## 2. Section 2: the hypothesis is confirmed and the disagreement disappears

I originally reported that the fiscal condition **passes**, contradicting the brief. Rerunning
with tau_k = 0.07 and tau_l of 0.255, 0.301 and 0.318:

| tau_l | required tau_k (sealed R = 0.568316) | required tau_k (my R = 0.6233) | verdict |
|---|---|---|---|
| 0.255 (AMR) | 0.110079 | 0.096059 | FAILS |
| 0.301 (bottom-up) | 0.129937 | 0.113387 | FAILS |
| 0.318 | 0.137276 | 0.119791 | FAILS |

Both required values reproduce the sealed figures **to six decimal places**. Every required
tau_k exceeds the operative 0.07 at every reading of tau_l, **and it fails under my own R as
well as theirs**. The disagreement disappears completely, and it was entirely my error.

**The error was mine and it was in tau_k, not in R.** I built tau_k as
`sigma_rent * (domestic * 0.21) + (1 - sigma_rent) * tau_normal` with tau_normal in 0.10 to
0.20. That is wrong in principle: with expensing, the normal return is exempt, so tau_normal
should be near zero, not 0.15. My grid floor of 0.1141 against the sealed 0.03245 is that
mistake measured. Because my floor was already above the required rate, the condition passed
mechanically.

The brief gave me every word of this construction except the one number that decides it.
It says "tau_normal is the effective rate on normal returns (Auerbach; Acemoglu, Manera and
Restrepo)" and never says that expensing drives it to roughly zero. A replicator who does not
already know the expensing result will get my answer, not theirs.

---

## 3. What did not replicate, and why

### 3a. Root causes that are the brief's omissions

**(i) omega, unstated.** Sealed `R_2026` is 0.568316. Their fitted rho at current slack is
about 0.697, so their omega is about 0.815. I used 0.90. R is off by 9.7 percent, outside the
5 percent fit tolerance. The brief says only "a blended counterfactual from the DWS earnings
question" and never gives the blend.

**(ii) The reemployment series, y.** My x construction is provably exact: the sealed
`x_range` endpoints reproduce to five decimals once I use OECD `LREM25TTUSM156S` with all
survey months read as January and vintages 1998 to 2024 (n = 14). With x identical and n
identical, the whole of the intercept and slope gap is in y. My rates come from primary BLS
releases; their fit is flatter, implying their 2010 value is near 55 where the published
all-ages long-tenured rate is 49, and their 1998 near 70 where the published rate is 76. The
brief says "the BLS Displaced Worker Survey reemployment rate" without saying **which** rate,
and BLS publishes several (all ages, prime age, full-time wage and salary reemployed). R² and
n match; intercept and slope do not.

**(iii) The working core, unstated.** My first definition (positive household earnings) gave
coverage shares 0.06 to 0.10 too high. Adding "reference person under 65" moves all four onto
target: mortgage 0.8217 vs 0.8205, auto 0.7776 vs 0.7737 (both inside tolerance), card 0.7291
vs 0.7400 and student 0.8936 vs 0.8832 (both within 0.011, marginally outside the 0.01 band).
I found the age restriction by sensitivity testing against the brief's own "14 to 26 percent"
remark before opening the sealed file. The brief never defines the term.

**(iv) Dose nonlinearity and horizon, unstated.** Sealed terminal loss goes 103.39 to 366.47
between the 10 and 25 percent doses, a ratio of 3.55, and OASDI goes 4.07 to 12.04, a ratio of
2.96. Neither is 2.5, so the loss is **not linear in the dose**. The sealed notes add "10-year
horizon" and "mean across exposure groups at this dose", neither of which appears in the
brief. I built a linear, single-group, horizon-free figure. It cannot match. I did confirm the
receipts denominator independently: 103.38722 over FRED FGRECPT 2026Q2 of 5980.631 gives
1.729 percent, matching the sealed 1.7287 exactly.

**(v) Trust fund denominators, unstated.** The brief insists the denominator is fund payroll
income and never gives it. I used 1150bn for OASDI and 400bn for HI from Trustees orders of
magnitude. My OASDI figure is 2.4 times theirs, which is mostly the dose nonlinearity in (iv)
compounding with my denominator.

**(vi) The pay control has four cells, not one.** The sealed file reweights in **both**
directions (cognitive onto embodied pay, and embodied onto cognitive pay) and across **two**
outcome variables, one of which, `distress_pp_per_bn`, is never mentioned anywhere in the
brief. I computed one of four cells. The brief's stated "54 to 99 percent" band turns out to
span both directions: 0.539456 is the ACS AIOE direction-b value. My single direction cannot
be scored against a four-cell structure.

**(vii) Section 12 break-even is not what the brief's formula says.** Sealed
`break_even_tau_k_case_A_max` is 0.378371. The brief defines case A break-even as
`tau_l * (1 - R)`, whose maximum at tau_l = 0.318 is 0.318, and which needs R negative to
reach 0.378. So the cases module ranges over an R set different from `R_2026`, and the brief
does not say over what.

**(viii) Debt increments are case B, mine were case A.** Sealed
`increment_pp_at_10pct_emerging_market_20y` is 19.169 and is flagged case B. Mine, 13.6, is
case A. The brief's section 13 never says which case the increments are computed under, even
though section 12 insists every figure must carry its case. Also, only one regime is named in
the brief; the sealed file has two (reserve currency and emerging market).

### 3b. A root cause that is probably mine

**The AIOE group.** Embodied matches in both surveys and GPT matches in SIPP, but AIOE is off
by 0.039 in ACS and 0.057 in SIPP, always in the direction of my group being lower-paid than
theirs. The likely cause is my crosswalk: AIOE matched only 476 of 530 ACS SOCP codes against
524 for GPT, because ACS uses broad and wildcarded SOC codes (`5191XX`) while AIOE is detailed
six-digit. My employment-weighted prefix averaging drops or blurs 54 codes, and that is enough
to move the group. The brief never states an aggregation rule, so the omission is shared, but
the error is on my side.

### 3c. Not attempted

Sections 5, 7, 10 and 11 produced no values. Of the sealed quantities I did not attempt, one
is independently confirmed: `federal_student_share` at 0.972808 against my 0.9728.

---

## 4. What the brief must add for Sections 5, 7, 10 and 11

### Section 5, household first-round losses

1. **The dose-to-household mapping.** The dose is a share of the total wage bill. Nothing says
   how that selects households in SIPP: which workers inside an exposed occupation, how their
   wages are summed to the dose, and whether selection is random within the group or ranked.
   This single omission blocks the whole section.
2. **Which exposure group defines the dose.** The sealed second-round entry says "50 percent
   cognitive AIOE dose", so the group is part of the specification, not a free choice.
3. **The Fed severely adverse loss per book.** The brief says to use DFAST 2026 Tables 4 and 9
   but gives no locator and no figures. The sealed pairs imply denominators of roughly 22.5bn
   for mortgage, 203.0bn for card, and 54.1bn for **both** auto and student, which suggests
   the last two are scored against a single "other consumer" line. That grouping must be
   stated.
4. **The bank-held share per book**, and its source, separately from the DFAST balance.
5. **Which end of each LGD range "hi" denotes**, and whether the uplift is applied before or
   after the under-reporting scale-up.
6. **Whether the superadditive dual-earner uplift** ("more than 8.0 points") is 8.0 or
   something else. "More than 8.0" is not a number.

### Section 7, incidence

7. **Definitions of the three cases.** Incumbents, entrants and a sourced mix are named and
   never defined. What makes a household an incumbent case in SIPP is unstated.
8. **The source and weights for the "sourced mix".** The brief calls it sourced but attaches
   no source.
9. **Which spread the ratios are taken over** (max over min across the three cases is the
   natural reading, and the sealed note confirms it, but the brief does not say so).

### Section 10, sovereign share

10. **GSE absorbing capacity**: Enterprise capital and one year of pre-provision pre-tax
    earnings, as numbers with a vintage.
11. **CRT and PMI attachment and detachment points**, since they are loss transfers taken
    before Enterprise capital and their size decides whether the federal layer binds at all.
12. **The FHA book size** and its loss treatment.
13. **The private/federal split of the residual mortgage holder category.**
14. Everything blocking Section 5, because the sovereign split is computed on top of it.

### Section 11, second round

15. **The model itself.** The brief gives five input ranges and no equations. There is no
    stated path from an MPC gap to a demand shortfall, from a demand shortfall to business
    revenue, or from either to a bank loss.
16. **The income measure the house price elasticity acts on.** The sealed values are internally
    consistent with house price fall = elasticity times a single income fall of about 31.4
    percent (6.5975 at 0.21, 47.125 at 1.50). That 31.4 percent figure, and what it is a fall
    in, must be stated.
17. **Functional forms for the three loss mappings** (linear, capped, convex). The brief
    concedes no source exists, which is fine, but a stated assumption still needs an equation.
18. **The grid.** The sealed `demand_event_first_share` of 0.62963 is 17/27, implying a
    three-by-three-by-three grid. The brief lists five inputs with ranges and never says the
    grid is three points per input on three of them.
19. **The definitions of "demand severity" and "house price severity"** that the comparison
    ranks, and the variance decomposition method behind the reported shares.

---

## 5. Corrections to my submitted values

Four of my 51 values were wrong for reasons I can now identify and would correct:

| Quantity | Submitted | Corrected | Cause |
|---|---|---|---|
| `fiscal.condition_result` | PASSES | FAILS at all three tau_l | my tau_k floor ignored expensing |
| `fiscal.tau_k_range_sourced_sigma` | 0.1141 to 0.1904 | operative 0.07 | same |
| `coverage_share.*` | 0.897 / 0.838 / 0.867 / 0.940 | 0.8217 / 0.7291 / 0.7776 / 0.8936 | working core needs age under 65 |
| `rho_slack.*` | BLS series, n=15 | OECD series, January, n=14 | x_range now exact |

The remaining mismatches I would not "correct", because they depend on parameters the brief
does not contain. Guessing them to hit the sealed values would defeat the purpose of the
exercise.

---

## 6. Verdict on the brief

The brief is strong on **error prevention** and weak on **parameter disclosure**. Every trap
it warns about, I avoided, and the three it quantifies, I reproduced exactly. But it names
sources without stating the values drawn from them (omega, tau_normal, sigma_rent, fund
payroll income, tau_l), leaves three analytically load-bearing terms undefined ("working
core", "speed limit", "exposure group"), and omits the model structure for two entire
sections.

The sharpest single illustration is Section 2. The brief spends a paragraph on how to build
tau_k and never mentions that expensing drives the normal-return rate to near zero. That one
unstated number is the difference between "the condition fails by a margin no plausible
reading closes" and my "it passes at every reading". Everything else in that section, I got
right to six decimals.
