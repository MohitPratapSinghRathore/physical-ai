# Round one: every mismatch classified, and what was done about it

Item 2 of the replication-repair session, 2026-09-20.

The independent replication attempted 51 quantities and matched 21. This file classifies all
30 mismatches into the five classes the owner specified, names the cause, and says what was
done. The machine-readable version is `data/processed/replication_round1_classification.csv`
and it is produced by `src/replication_round1_response.py`, which also computes the R
sensitivity in section 3 below.

**The headline: ten of the thirty are ours, and all ten are now fixed. Five of those ten
moved a published number.** The rest are the brief's, the replicator's, or a defensible
difference of construction that the brief failed to pin down.

---

## 1. The counts

| Primary class | Count | What it means |
|---|---|---|
| brief insufficiency | 15 | the brief did not contain enough to rebuild the quantity |
| our error | 8 | this project's value was wrong |
| replicator error | 5 | the rebuild was wrong, by their account or ours |
| definitional choice | 2 | both sides right about different constructions |
| data vintage | 0 (1 contributing) | both sides right about different vintages |

Counting contributing causes as well, **ten mismatches are ours in whole or in part** (eight
primary plus two contributing) and **twenty-five involve a brief omission** (fifteen primary
plus ten contributing). The replicator's own verdict, that the brief is
strong on error prevention and weak on parameter disclosure, is confirmed by the arithmetic:
the brief is implicated in five of every six failures.

---

## 2. The ten that are ours

Five distinct defects produced them. Each is fixed in code this session and each is stated
here with what moved.

### 2.1 The break-even capital tax rate was not a tax rate at all

This is the one the owner flagged first, and the replicator found it from a plausibility
bound alone, without ever seeing `src/`. Sealed `break_even_tau_k_case_A_max` was 0.378371,
above the highest reading of tau_l, 0.318, which `tau_l * (1 - R)` makes impossible unless R
is negative.

**What the code actually computed.** Two defects multiplying:

1. **The capital tax was counted twice.** The expression divided `case_A_fiscal_loss_bn` by
   the surplus. But that loss is the loss AT the operative tau_k of 0.0708: it is
   `[tau_l * (1 - R) - tau_k] * D`, with tau_k already netted out. A break-even rate is the
   tau_k at which the loss is zero, so dividing a loss that already contains a tau_k by
   anything cannot produce one.
2. **Two different wage bills sat in one ratio.** The numerator came from
   `src/fiscal_extended_axis.py`, which scaled the dose by compensation of employees
   (16,224.3bn). The denominator was built from `capacities.json total_wage_bill_bn`, this
   project's occupational grid (9,870.2bn). A spurious factor of 1.6438 rode on top.

Together the old expression was

    old value = (comp / grid) x [tau_l - tau_k / (1 - R)]

and at the top of the grid, where R falls to zero, that is
`1.6438 x (0.301 - 0.0708) = 0.37840`, which reproduces the sealed figure exactly and
identifies it as an artefact. A third inconsistency sat in the same block: the case B term
`tau_k * dC` used the MIDPOINT of the sourced tau_k range, 0.11798, while the case A loss it
was added to embeds 0.0708.

**The correct definitions**, now in `src/consistency.py` and in brief v2:

| | |
|---|---|
| gross displaced wage bill | `D = delivered dose x W` |
| net wage income fall | `dW = (1 - R) * D` |
| demand shortfall | `dC = (mpc_L - mpc_K) * dW` |
| case A break-even | `tau_l * (1 - R) + g * (1 - rho)`, which with g = 0 is `tau_l * (1 - R)` |
| case B break-even | `tau_l * ((1 - R) * D + (W / Y) * dC) / (D - dC)` |

The brief's own section 12 is also wrong and is corrected: it writes the case A loss as
`tau_l * dW - tau_k * dW`, which yields a break-even of tau_l, not `tau_l * (1 - R)`. The
labour tax is lost on the NET fall `(1 - R) * D` while the capital tax is levied on the whole
displaced wage bill `D`, and it is that asymmetry that produces the `(1 - R)`.

**The missing plausibility bounds**, now enforced in `src/consistency.py` and folded into
`src/verify/plausibility_audit.py` so they run with every other check:

- `0 <= case A break-even <= tau_l + g`. A rate on the surplus cannot exceed the labour tax it
  has to replace plus any added outlays. This is the bound the sealed 0.378371 broke.
- `0 <= break-even, either case <= 1`. No tax rate exceeds 100 percent. This is the bound the
  replicator's own case B broke, at 1.0979 on their grid.
- `case B >= case A`. Case B raises the loss and shrinks the base, so it cannot be the lower.
- `D - dC > 0`. A break-even rate exists only while a surplus remains to tax.

All seven checks pass on the corrected grid.

**Recomputed cases A and B.**

| | round one, withdrawn | round two |
|---|---|---|
| case A break-even, range | 0.213835 to 0.378371 | **0.124614 to 0.301000** |
| case B break-even, range | 0.560866 to 0.860022 | **0.181771 to 0.649569** |
| case B loss over case A | 1.250 to 1.443 | **1.383 to 1.677** |

The case A maximum is now exactly tau_l, 0.301, because it is reached where R falls to zero
and `tau_l * (1 - 0) = tau_l`. That is the bound binding with equality, which is the right
behaviour rather than a coincidence.

**On the replicator's case B of 1.0979.** Our own maximum is 0.649569. Their figure is not
reachable under the corrected formula at any point on our grid, and it was not reachable as a
tax rate at all, which they said themselves. Their instability came from a case B expression
whose denominator approached zero at their lowest tau_l, which is a consequence of the
missing tau_l readings rather than of the formula. **The 0.56 to 0.86 range does not stand.
It is withdrawn and replaced by 0.182 to 0.650.**

### 2.2 The wage bill base was wrong throughout

The dose is a share of the total wage bill. Converting it to dollars needs a base, and three
different ones were in use:

| total | value | where |
|---|---|---|
| this project's occupational grid | 9,870.2bn | `capacities.json`, the second-round module |
| NIPA wages and salaries, FRED WASCUR | 13,365.2bn | the denominator tau_l is built on |
| NIPA compensation of employees, FRED COE | 16,224.3bn | the fiscal modules |

**WASCUR is the right one and it is not a judgement call.** tau_l is built in
`src/fiscal_channel.py` as federal taxes divided by WASCUR. A rate and its base must be the
same object. Compensation of employees additionally includes employer contributions to
pension and health plans, which bear neither the income tax nor the payroll tax, so applying
a wage tax rate to compensation taxes income that is not taxed. The occupational grid is
73.9 percent of WASCUR and `src/coverage_reconciliation.py` already reconciles the two.

There is one assumption in the fix and it is now stated: the exposed group's share of
national wages and salaries is taken to equal its share of the occupational grid.

Effect: **fiscal dollar figures fall 17.6 percent; second-round demand figures rise 35.4
percent.** Ratios that carry the base top and bottom, including the trust fund ratios and
the corrected break-even rate, do not move at all.

### 2.3 HI was given the OASDI payroll share, and a total-income denominator

Two separate defects on one fund:

- The payroll share of fund income was taken as 0.9126 for both funds. That is OASDI's.
  HI's own is `403.2 / 462.4 = 0.8720`, so every HI ratio was 4.7 percent too large.
- The fiscal modules used 462.4bn as an HI payroll denominator. That is HI TOTAL income,
  including interest, government contributions and beneficiary premiums. The fund's own
  payroll income is 403.2bn.

Both now read from the 2026 Trustees summary tables the owner placed in `data/raw/owner/`.

### 2.4 The brief misdescribed how rho enters R

Not a code defect, a documentation defect, and it sent the replicator down a wrong path. See
section 3.

### 2.5 The auto aggregate sat on a discontinued series

Item 5 of this session, and it is a vintage problem the replicator flagged in their
insufficiencies list rather than a mismatch. FRED MVLOAS ended at 2024Q4 while every other
input is 2026. See section 5.

---

## 3. The R disagreement, resolved, with the sensitivity the owner asked for

### Exactly which series y is

The brief said "the BLS Displaced Worker Survey reemployment rate" and BLS publishes several.
Ours, stated here so it never has to be guessed again:

| | |
|---|---|
| Release | *Displaced Workers Summary*, USDL news release, biennial |
| Table | **Table 1**, the TOTAL row |
| Universe | **long-tenured** displaced workers, three or more years on the lost job, **all ages, both sexes** |
| Quantity | the number **employed at the survey date** divided by the total displaced |
| Latest value | 2,199 of 3,324 thousand employed in January 2026, rho = 0.6615 |
| Vintages | **14**, survey months **January 2000 through January 2026**, one per release |
| Not used | the prime-age rate; the full-time wage and salary reemployed rate; Table 7 |

The replicator used the same concept over **1998 through 2024**: same n, a window shifted by
one release at each end. Since their x construction reproduces our `x_range` endpoints to
five decimals, **that window difference is the whole of the intercept and slope gap.** Their
inference that our 2010 value must be near 55 was wrong; ours is 49, the published figure.
They inferred it from our fitted line rather than from our data.

### Where R actually comes from, and the brief error that hid it

The replicator reverse-engineered an omega of 0.815 from the assumption that our rho is the
FITTED value at current slack. It is not. **`R_2026` uses the DIRECTLY OBSERVED 2026 rho of
0.6610**, and the fitted line is used only on the extended axis, where slack moves away from
anything observed. Section 2 of the brief says rho is "evaluated at current slack", which
describes the fitted value and is simply wrong about the code. That sentence is corrected in
brief v2.

So the gap decomposes into two roughly equal parts, neither of them a coding difference:

| | ours | replicator |
|---|---|---|
| rho | 0.6610, observed | 0.6926, fitted |
| omega | 0.8598, counterfactual blended central | 0.90, assumed |
| R | **0.568316** | **0.6233** |

### R under the replicator's series, as a sensitivity

| construction | rho | omega | R | required tau_k at tau_l 0.301 | verdict at the operative 0.0708 |
|---|---|---|---|---|---|
| ours: observed rho, our omega | 0.6610 | 0.8598 | **0.5683** | 0.1299 | **FAILS** |
| their fitted rho, our omega | 0.7080 | 0.8598 | 0.6087 | 0.1178 | **FAILS** |
| our fitted rho, our omega | 0.6971 | 0.8598 | 0.5994 | 0.1206 | **FAILS** |
| observed rho, their omega | 0.6610 | 0.9000 | 0.5949 | 0.1219 | **FAILS** |
| their fitted rho, their omega | 0.7080 | 0.9000 | 0.6372 | 0.1092 | **FAILS** |
| their reported R | | | 0.6233 | 0.1134 | **FAILS** |

**The fiscal condition fails under both sides' parameters, at every reading of tau_l, at the
operative effective capital tax rate of 0.0708.** That is the one headline the replication
confirms outright rather than merely matching, and it is confirmed by an instance that
started out contradicting it.

The weaker clause has to travel with it, and it is stated in section 4.

---

## 4. What the repair WEAKENS, reported first because it weakens the thesis

Claim 168 said there is "no reading of the corporate tax literature in which the break-even
capital tax rate is an available instrument". **On the corrected numbers that is false as
stated.** The sourced range of effective capital tax rates tops out at 0.20351, and:

- case A break-even is at or below 0.20351 in **10 of 15** cells on the dose grid, minimum
  0.12461;
- case B break-even is at or below it in **5 of 15** cells, minimum 0.18177.

At small and moderate doses the break-even rate is inside the sourced range. The claim
survives only in its narrower form, which is the one the evidence supports:

> **The break-even capital tax rate exceeds the OPERATIVE effective rate of 0.0708 in every
> cell of the grid, in both cases, and exceeds the top of the sourced range only at larger
> doses.**

That is a statement about the tax code as it stands, not about what the literature says is
attainable, and it is a materially weaker claim than the one it replaces. Claim 168 is
downgraded accordingly, and claim 167's numbers are withdrawn.

---

## 5. The auto series, and the vintage the replicator flagged

FRED MVLOAS, motor vehicle loans owned and securitized, was discontinued after 2024Q4 while
every other input in the project is 2026. Fed G.19 no longer publishes a live motor vehicle
loan balance either, so the replacement is the **NY Fed Household Debt and Credit report**,
already the source for the mortgage and student aggregates and on the same 2026Q2 vintage:
**auto loan balance 1,713bn**, read from the report's own data workbook rather than the PDF,
which gives auto only as a quarterly percentage change.

Effect: the auto under-reporting factor moves from 1.7431 to **1.9036**. **The auto bank loss
does not move at all**, because the bank-held share is the DFAST implied balance over the
same national aggregate, so the two carry the same denominator and it cancels. That
insensitivity is worth reporting to a stress-test designer on its own.

Cards stay on FRED REVOLSL. Revolving consumer credit and the NY Fed credit card balance are
different objects, 1,357.2bn against 1,263bn, and the brief names REVOLSL. That is now a
stated choice rather than an implicit one.

---

## 6. What the replicator got wrong, for the record

Five mismatches, and they conceded four before seeing any of this.

- **tau_normal.** They set the effective rate on the normal return in 0.10 to 0.20 where full
  expensing drives it to near zero. Their grid floor of 0.1141 against our 0.03245 is that
  mistake measured, and because their floor sat above the required rate the fiscal condition
  passed mechanically. The brief never stated the expensing result, so this is half ours.
- **The AIOE crosswalk.** Their AIOE match covered 476 of 530 ACS SOCP codes against 524 for
  GPT, because ACS publishes broad and wildcarded SOC codes while AIOE is detailed six-digit.
  Prefix averaging blurred 54 codes and moved the group. Again the brief stated no
  aggregation rule, so again it is half ours.

---

## 7. The two that are neither side's fault

`debt.debt_to_gdp_start` and the 20-year baseline that follows from it. Both sides use FRED
GFDEBTN at 2026Q1; the denominator differs, ours the ANNUAL MEAN of quarterly nominal GDP
(32,175.9bn, the `capacities.json` convention used everywhere in this project), theirs the
single quarter. The replicator reproduces our 3.7674 exactly at our start ratio, which is the
cleanest confirmation in the whole exercise. Brief v2 pins the GDP concept down.
