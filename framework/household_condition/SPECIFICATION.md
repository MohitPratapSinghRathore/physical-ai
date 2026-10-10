# The household condition: specification

**Written 2026-09-21 on branch `household-condition`, before any result of the exercise
was computed.** Feasibility counts and the SCF-to-Financial-Accounts reconciliation were
computed to write this document; no shift has been applied, no payment-to-income ratio
recomputed under a shift, and no boundary located.

**Status vocabulary, as in the measurement paper.** Everything here is **scenario**
arithmetic on **measured** distributions. The SCF distributions of income, debt, payments
and equity are measured. The shift, its incidence, the growth factor and the arrangements
are scenarios. Nothing here is a forecast and nothing is a causal estimate. It is
**first-round incidence under stated conventions**: second-round effects on output,
employment, prices and asset values are held fixed except where §7 tests them.

---

## 0. What would weaken this before it starts

Stated first because these are the reasons the exercise might not be worth running.

**0.1 The credit-card cell is the worst-measured debt class and carries the highest
payment burden per dollar.** The SCF reports $363.5bn of revolving balances against an
implied official figure requiring a factor of **3.73**, worse than the paper's own SIPP
factor of 2.52. Consumer credit as a whole reconciles at **0.60** of the Financial
Accounts. Payment-to-income is most sensitive to exactly the class the survey measures
worst. Any result will move with the under-reporting correction, and §8 makes that
correction a reported axis rather than a buried assumption.

**0.2 Nearly half of corporate equity never reaches a household at all.** On the
Rosenthal and Mucciolo decomposition already sourced in the measurement paper, **42
percent is foreign-held, 4 percent nonprofit, 1 percent government** — 47 percent outside
the household sector entirely — and a further **25 percent sits in retirement accounts**
(IRA 11, DB 7, DC 7) which do not produce spendable cash flow for a working-age household.
Only **27 percent** is in taxable household accounts. On a cash-flow basis the capital
gain that can offset a wage loss is therefore small by construction. **This is close to
assuming the answer**, and §4 handles it by reporting the cash-flow and accrual bases side
by side and never blending them.

**0.3 The result may be arithmetically forced.** Wage income is $10,943bn in the SCF
against total income of $18,565bn, and the households holding most debt are not the
households holding equity. A shift from wages to capital will mechanically lower
debt-service capacity for indebted wage earners under almost any convention. **If the
finding is only that, it is not worth a paper.** §10 states in advance what would make the
result uninteresting, and the boundary in §6 — not the direction — is the object that has
to carry the contribution.

**0.4 The nearest existing work is close.** Bartscher, Kuhn, Schularick and Steins (2020)
already stress-test SCF household debt-service capacity against interest-rate and earnings
shocks. What is not done there is the factor-share shift as the shock, the growth boundary
as the object, and the mapping of affected debt to its holders. The contribution is those
three things, and it is narrower than the question sounds. See `NOVELTY.md`.

---

## 1. The question

When a share of national income moves from wages to capital, holding existing debts fixed:

- whose debt-service capacity falls, given who actually owes the debts and who actually
  owns the capital;
- how much output growth would preserve it;
- which ownership or transfer arrangements move that boundary.

This is the household-sector counterpart of the fiscal condition in the measurement paper,
`tau_k * g >= tau_l * (1 - R)`. The fiscal condition asks whether the tax system can
recoup, from capital, enough to cover what labour stops paying. The household condition
asks the same question one layer down: whether the household sector's own capital income
can cover what its own wage income stops providing, given that the debts and the equity
sit with different households.

---

## 2. The shift (a)

A share **s** of aggregate wage income moves to capital income. Total income is then
scaled by a growth factor **(1 + g)**.

For household *i* with wage income `w_i`, capital income `k_i` and other income `o_i`
(Social Security, pensions, transfers), with aggregate wage bill `W = Σ φ_i w_i` over SCF
weights `φ_i`:

    wage income after      w_i' = (1 + g) · [ w_i − Δ_i ]
    capital income after   k_i' = (1 + g) · [ k_i + Γ_i ]
    other income after     o_i' = (1 + g) · o_i
    with  Σ φ_i Δ_i = s·W   and   Σ φ_i Γ_i = s·W·κ

where `Δ_i` is household *i*'s share of the wage loss (§3), `Γ_i` its share of the capital
gain (§4), and **κ** is the fraction of the shifted income that reaches households at all
(§4.3). **Other income is scaled but not otherwise altered**: transfers are not indexed to
the shift in the baseline, and §7.5 tests indexing them.

**Grids, fixed now.**

- **s ∈ {0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25}.** The lower end spans plausible
  decade-scale factor-share movement (the US labour share fell roughly 5 points over four
  decades); the upper end reaches the measurement paper's own displacement doses.
- **g ∈ {0, 0.0025, 0.0050, …, 0.20}**, 81 points. The step is fine enough to locate the
  boundary in §6 to within a quarter of a percentage point. `g` is **cumulative real
  growth over the scenario horizon, not annual**, and is reported that way.

Debts and required payments are **fixed in nominal terms** throughout. That is the point
of the exercise: the contracts do not move when the factor shares do.

---

## 3. Allocation of the wage loss (b)

Three pre-stated cases, all reported, none preferred.

**3.1 Proportional.** Every household with wage income loses the same fraction:
`Δ_i = s · w_i`. This is the neutral benchmark and the one most favourable to the null,
because it spreads the loss onto households with little debt as well as much.

**3.2 Concentrated.** A share of earners lose their wage entirely and are reemployed at
the retained wage share **R = 0.568316** from the measurement paper, so each affected
household keeps `R · w_i` and loses `(1 − R) · w_i`. The number affected is set so that
`Σ φ_i Δ_i = s·W`. **Who is affected is drawn by the measurement paper's existing
exposure-and-pay incidence cases**, all nine reported:

| Exposure | Cases |
|---|---|
| `cognitive_AIOE` | `a_incumbents`, `b_entrants`, `c_sourced_mix` |
| `cognitive_GPT` | `a_incumbents`, `b_entrants`, `c_sourced_mix` |
| `embodied` | `a_incumbents`, `b_entrants`, `c_sourced_mix` |

Selection within the SCF is by occupation where the SCF fields it, and otherwise by the
wage-quintile exposure profile the paper already reports. **The mapping from the paper's
occupation-level exposure to SCF households is the weakest link in this case and is
documented as such**, with the fallback (quintile profile only) reported alongside.

**3.3 By wage quintile.** The loss is distributed across quintiles in proportion to the
measurement paper's existing incidence results, using the quintile wage-bill shares
already published:

| Quintile | Wage-bill share | Labour-backed claims per unit wage bill |
|---|---|---|
| Q1 bottom | 0.0324 | **4.1489** |
| Q2 | 0.0895 | 1.4112 |
| Q3 middle | 0.1426 | 1.2031 |
| Q4 | 0.2233 | 1.0403 |
| Q5 top | 0.5122 | 0.6548 |

The last column is why this case matters: the bottom quintile carries **four times** the
labour-backed claim per dollar of wage bill that the average household does, and six times
the top quintile's. A loss of given aggregate size does very different things depending on
where it lands.

---

## 4. Allocation of the capital income gain (c)

**4.1 Ownership basis.** `Γ_i` is allocated in proportion to household *i*'s equity,
under three pre-stated ownership definitions:

| Definition | SCF variables |
|---|---|
| **Direct only** | `stocks` + `nmmf` |
| **Direct + business** | `stocks` + `nmmf` + `bus` |
| **All routes** | `stocks` + `nmmf` + `bus` + `retqliq` + `annuit` |

**4.2 Cash-flow versus accrual, reported separately and never blended.**

- **Cash-flow basis.** Only income that reaches a household's spendable cash flow counts:
  dividends, distributions and realised gains (`intdivinc`, `kginc`, and the distributed
  part of `bussefarminc`). **Retirement-account holdings produce no cash flow for a
  household below retirement age and are excluded**, as are unrealised gains. This is the
  basis on which a payment-to-income ratio is actually computed, and it is the **primary**
  basis.
- **Accrual basis.** The whole capital gain is counted as income at a stated annuity rate.
  **The rate is 0.04 real**, applied to the wealth increment, with 0.02 and 0.06 reported
  as sensitivities. This basis is reported because it is the one on which "households own
  the capital" arguments are usually made, and it is the upper bound on household
  capacity.

**4.3 The share that never reaches households (κ).** From Rosenthal and Mucciolo (2024)
Table 5, as already sourced in the measurement paper, US corporate equity in 2022:

| Holder | Share |
|---|---|
| Taxable household accounts | **0.27** |
| Foreign | **0.42** |
| IRAs | 0.11 |
| Defined benefit | 0.07 |
| Defined contribution | 0.07 |
| Nonprofits | 0.04 |
| Life insurance separate accounts | 0.02 |
| Government | 0.01 |

**On the cash-flow basis, κ = 0.27**: only the taxable household share produces spendable
capital income in the first round. **On the accrual basis, κ = 0.52** (taxable plus the
25 percent in retirement vehicles, which accrue to households even if not spendable).
Foreign, nonprofit and government holdings — **0.47 of the total** — are removed under
both bases and never reach any household.

A variant with **κ = 1.0** is reported as an explicit upper bound labelled *counterfactual,
not measured*, so that a reader can see how much of the result is the ownership structure
rather than the arithmetic.

---

## 5. Outcomes (d)

For each household, before and after:

    PTI_i = required annual debt payments / income
          = tpay_i / income_i          (SCF `pirtotal` replicates this)

reported in total and by class using `mortpay`/`pirmort`, `conspay`/`pircons`,
`revpay`/`pirrev`.

**Reported quantities:**

1. The **share of households** whose PTI rises.
2. The **share of DEBT, by class**, owed by households whose PTI rises. This is weighted
   by balance, not by household, and it is the quantity the boundary in §6 is defined on.
3. The **share crossing distress thresholds**, stated now with sources:

| Threshold | Value | Source |
|---|---|---|
| SCF's own high-payment flag | PTI > **0.40** | Federal Reserve SCF summary extract variable `pir40` |
| Conventional back-end underwriting limit | DTI **0.36** | "28/36 rule", standard conventional underwriting |
| Qualified Mortgage limit (historic) | DTI **0.43** | CFPB Ability-to-Repay/QM rule as originally written |
| Automated-underwriting maximum | DTI **0.50** | Fannie Mae Selling Guide B3-6-02, Desktop Underwriter maximum |

`pir40` is the **primary** threshold because it is the survey's own and needs no external
mapping. The other three are reported alongside.

4. All of the above **by wage quintile, by wealth group** (p0–25, p25–50, p50–75, p75–90,
   p90–99, top 1, on **weighted** percentiles) **and by age** of the household head.

5. **Holder mapping.** The affected debt is then mapped to its holders using the
   measurement paper's existing holder map, so the result can be stated as *whose claims
   sit on households whose capacity falls*. Given the paper's finding that the federal
   government holds, guarantees or owes 79.4 percent of labour-backed claims, the
   expected shape of this result is known in advance and is not itself the contribution.

---

## 6. The boundary (e) — the headline object

**Define** `D(s, g)` as the share of household debt owed by households whose
payment-to-income ratio is **higher** after the shift than before it.

**The boundary `g*(s)` is the growth factor at which `D(s, g*) = D(s, 0)` evaluated at
`s = 0`** — that is, the growth needed to return the affected-debt share to its
**baseline** value, the value with no shift at all.

Reported as a surface over the grid in §2, separately for:

- each of the three wage-loss allocations (§3),
- each of the three ownership definitions (§4.1),
- each of the two capital-income bases (§4.2),

which is 18 boundary curves per threshold. The **primary cell** is fixed now:
**concentrated allocation, all-routes ownership, cash-flow basis, `pir40` threshold**. The
other 17 are reported in a single table, not selected among.

If `D(s, g)` is not monotone in `g`, the boundary is reported as the **smallest** `g`
satisfying the condition, and the non-monotonicity is reported as a finding.

---

## 7. Arrangements that move the boundary (f)

Each defined now with its parameters. **Nothing else is tested.**

**7.1 Capital-tax-funded per-capita transfer.** The shifted capital income is taxed at
rate `tau_k` and returned as an equal per-capita transfer. Two rates, both from the
measurement paper:

- the **assembled** rate **0.086** central (0.073 to 0.099, Barkai reading);
- the **required** rate **0.110 to 0.137**, the fiscal-condition threshold.

The gap between them is the paper's central fiscal finding, and this shows what that gap
costs households directly rather than through the budget.

**7.2 Universal capital fund.** A stated share **ω ∈ {0.01, 0.02, 0.05, 0.10}** of
corporate equity is held collectively and pays an equal per-capita dividend at the §4.2
annuity rate. Reported at each ω.

**7.3 Broadened retirement-account ownership.** The retirement-account share of equity
(0.25) is redistributed so that ownership within it is equalised across households, run
**twice**: once with the balances illiquid (accrual basis only, no cash flow) and once
with them liquid (cash flow allowed). The pair isolates how much of the arrangement's
value is ownership and how much is access.

---

## 8. What would weaken or reverse the conclusion (g)

Each is a pre-stated sensitivity, **reported whatever it shows**.

**8.1 Lower prices raising real incomes.** A pass-through **π ∈ {0, 0.25, 0.50, 1.00}**
of the productivity gain to a consumer price index, applied to **non-debt spending only**,
since nominal debts are fixed. Real capacity rises even when nominal income does not. This
is the sensitivity most likely to move the boundary and is reported first among them.

**8.2 Reemployment at a higher retained wage share.** `R ∈ {0.568316, 0.70, 0.85}`, the
first being the measurement paper's value.

**8.3 Refinancing.** Required payments on mortgage and installment debt are recomputed at
a rate **100 and 200 basis points** below the implied current rate, with balances and
terms fixed. Credit-card minimums do not refinance.

**8.4 Household equity ownership broader than measured.** The `κ = 1.0` upper bound of
§4.3, plus a variant in which the SCF's equity over-statement against the DFA (measured at
**1.50** for all household routes) is treated as real rather than as a definitional
mismatch.

**8.5 Transfers indexed to the shift.** Social Security and other transfers grow with
total income rather than being held at the baseline scaling.

---

## 9. Plausibility bounds (h)

Checked and reported **before** any result, with violations reported first:

1. All shares in **[0, 1]**: `s`, `κ`, ownership shares, affected-debt shares, threshold
   crossing shares.
2. **Aggregate income after the shift equals the stated total**:
   `Σ φ_i (w_i' + k_i' + o_i') = (1 + g) · Σ φ_i (w_i + k_i + o_i)` to within **0.1
   percent**.
3. **The wage loss and capital gain balance**: `Σ φ_i Δ_i = s·W` and
   `Σ φ_i Γ_i = s·W·κ` to within **0.1 percent**.
4. **Household sums reconcile to the aggregates** within the tolerances measured in
   `scf_dfa_reconciliation.csv`: mortgages within **10 percent** of the Financial
   Accounts, total liabilities within **10 percent**, consumer credit **not expected to
   reconcile** (measured at 0.60) and reported as such at every use.
5. **No household's income is negative** after the shift. Households with `income ≤ 0` in
   the baseline are excluded from ratio calculations and counted.
6. **Five implicates and 999 replicate weights** are used throughout (§11); no statistic
   is reported from a single implicate.

---

## 10. What would count as an uninteresting result (j)

Stated now, before computation.

**10.1 The boundary is at or near zero growth under every case.** If `g*(s) ≈ 0`
throughout — capacity is preserved without any growth — then the shift does not bind and
there is nothing to report beyond that fact. **It will be reported as that fact.**

**10.2 The result is driven entirely by one convention.** If the boundary moves more
between the cash-flow and accrual bases (§4.2), or between `κ = 0.27` and `κ = 1.0`, than
it does across the entire `s` grid, then the exercise is measuring a definitional choice
and not an economic quantity. The measurement paper already found this pattern once: the
one-step rule moved its headline by 76 percent while every other judgement call moved it
under 10. **If that recurs here it is reported in the same form, as the single most
important fact about the statistic.**

**10.3 The direction alone.** That indebted wage-earners lose capacity when wages fall is
not a finding (§0.3). Only the **magnitude of the boundary**, its **sensitivity across the
pre-stated cases**, and the **holder mapping** can carry the contribution.

---

## 11. Estimation and inference

- **Five implicates.** Every statistic is computed within each implicate and combined by
  Rubin's rules: point estimate is the mean across implicates; total variance is
  `V_W + (1 + 1/5)·V_B`, within-implicate plus between-implicate.
- **999 replicate weights** (`wt1b1`–`wt1b999`, file `p22_rw1.dta`) give the
  within-implicate sampling variance by the SCF's own bootstrap design.
- Weights: the summary-extract `WGT` sums to the household count over **all five
  implicates** (131.31m in 2022). A single implicate carries one fifth of the weight, and
  aggregates use the full-sample sum. **This is a documented trap and was got wrong once
  while writing this specification**; the run must assert the household count before
  proceeding.
- **Stability check:** every headline quantity is recomputed on **SCF 2019** (5,777
  households). Disagreement in sign or in the boundary by more than **25 percent** is
  reported as instability, not averaged away.

---

## 12. What is fixed by this document

Specifications, grids, thresholds, allocation cases, ownership definitions, bases,
arrangements, sensitivities, bounds and the primary cell are fixed here. Any departure is
recorded in `DEVIATIONS.md` with its reason and whether it was decided before or after any
result was seen.
