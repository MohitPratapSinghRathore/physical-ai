# The household condition: results

**Run 2026-09-21. `SPECIFICATION.md` sha256
`476e093703da92d8eacf85332f2d6f637851b2e925b5a34bcb441d1e35f21f9b`, verified unchanged at
H2 (`8f0346c`). Measured distributions, scenario arithmetic: not a forecast and not a
causal estimate.**

---

## The verdict

**The boundary exists, it is large, and it is not what should be reported.** At the
primary cell — concentrated wage loss, all ownership routes, cash-flow basis, κ = 0.27 —
returning household debt-service capacity to its unshifted baseline requires cumulative
real growth of **5.10 percent [4.78, 5.42]** for a 1-percent shift of the wage bill to
capital, and **10.74 percent [10.04, 11.45]** for a 2-percent shift. **Beyond a 5-percent
shift the boundary lies outside the pre-registered growth grid entirely** (g > 0.20), and
by s = 0.25 it is numerically unbounded.

**Three findings weigh against reporting that number as the contribution.**

First, **the §10 convention test is close to failing and the boundary is fragile by
construction.** The convention spread is 0.050 against an s-grid spread of 0.057 — the
pre-committed test returns **No**, but by 0.007. And the boundary as §6 defines it (the
growth at which *no* household's capacity is reduced) is a **maximum over households**: it
is set by the single worst-affected indebted household, which is why it explodes from 0.94
at s = 0.10 to 57 at s = 0.20 to 7.9 × 10¹⁵ at s = 0.25.

Second, **the 2019 stability check fails at every s**, by 50 to 65 percent — far outside
the 25-percent threshold §11 fixed in advance.

Third, **two of the four pre-stated sensitivities cannot move the boundary at all, for a
structural reason.** With payments fixed in nominal terms, PTI rises exactly when income
falls, so the rising test is an **income incidence test**. Refinancing (§8.3) changes
payments and therefore moves the boundary by **exactly zero** at every s and every rate
cut. The same identity makes the payment-to-income framing add nothing to the rising test
beyond income.

**What survives.** The distributional shape is robust and is the reportable object: the
share of households whose capacity falls is **84.6 percent in the bottom wealth quartile
against 23.6 percent in the top 1 percent**, and the affected debt is **55.1 percent
federally held or guaranteed** under the paper's central agency classification. §10.3
rules that direction alone is not a finding; the gradient and the holder mapping are.

---

## 1. Plausibility bounds, reported first

All bounds in `bounds.json`. **No violations.**

| Bound | Result |
|---|---|
| 1. Ownership weights non-negative (D1 flooring) | 0 violations of 15 checks |
| 2. Aggregate income identity | worst relative deviation **5.74 × 10⁻¹⁶** over 3,780 checks (tolerance 10⁻³) — **OK** |
| 3. Wage loss and capital gain balance | worst relative deviation **3.57 × 10⁻¹⁶** — **OK** |
| 5. No negative household income after the shift | **0** household-cells (valid households, $1 float tolerance) — **OK** |
| 4. Reconciliation | mortgages 0.930 and total liabilities 0.905 within 10 percent — **OK**. **Consumer credit 0.603 does NOT reconcile** and is reported as unreconciled at every use |

Bounds 2, 3 and 5 required two corrections before they held, both logged before any result
was read (D5, D6) and both forced by the bounds themselves. A third correction (D4) fixed a
coding error in the capital-gain allocation found by bound 3.

---

## 2. §10 pre-committed check — reported before any boundary

**In the pre-committed words: the convention spread does NOT exceed the effect of the whole
s grid. The answer is No.**

Compared on the **grid** boundary, the object §6 defines, over the s values where it is
uncensored in every convention cell (s = 0.01 and 0.02):

| Quantity | Value |
|---|---|
| Spread across the s grid, at the primary convention | **0.0570** |
| Spread across conventions (cash-flow vs accrual, and across κ), worst over s | **0.0500** |
| Convention spread exceeds s spread | **False** |

**The margin is 0.007 and should not be leaned on.** Two qualifications belong next to it:

- The comparison rests on **two s values**, because the boundary is censored beyond g = 0.20
  for s ≥ 0.05 in every convention except κ = 1.0.
- On the **uncensored analytic** boundary, where all seven s values are available, κ is by
  far the largest single axis: at s = 0.10 it moves the boundary from 0.942 (κ = 0.27) to
  0.374 (κ = 1.0), a change of −0.569, larger than any sensitivity in §6.

**The cash-flow and accrual bases give identical results at every cell.** This is not an
error: under the reading recorded in D3, capitalising an income flow and annuitising it at
the same rate returns the flow, so the basis distinction collapses and only κ moves. The
spec's two-basis structure therefore has one degree of freedom, not two.

Everything below is conditional on convention to the extent §10 allows, and the κ column
should be read as the widest source of variation in the table.

---

## 3. The boundary

### Primary cell, with interval

Concentrated allocation, all routes, cash-flow basis, κ = 0.27. Five implicates combined by
Rubin's rules; within-implicate variance from 200 SCF bootstrap replicate weights.

| s | Boundary | 95 percent interval |
|---|---|---|
| 0.01 | **0.0510** | [0.0478, 0.0542] |
| 0.02 | **0.1074** | [0.1004, 0.1145] |

A 1-percent shift of the wage bill to capital requires about **5 percent** cumulative real
growth to restore capacity; a 2-percent shift about **11 percent**. The relationship is
faster than linear.

### Full table, never blended across bases

`boundary_table.csv` carries all 7 × 3 × 3 × 2 × 3 = 378 cells. Grid boundary at the
primary allocation and ownership:

| s | κ = 0.27 | κ = 0.52 | κ = 1.00 | censored |
|---|---|---|---|---|
| 0.01 | 0.052 | 0.044 | 0.029 | no |
| 0.02 | 0.109 | 0.091 | 0.059 | no |
| 0.05 | — | — | 0.159 | yes except κ = 1.0 |
| 0.10–0.25 | — | — | — | **all cells beyond g = 0.20** |

Uncensored analytic boundary, same cells:

| s | κ = 0.27 | κ = 0.52 | κ = 1.00 |
|---|---|---|---|
| 0.01 | 0.051 | 0.043 | 0.028 |
| 0.02 | 0.107 | 0.089 | 0.057 |
| 0.05 | 0.320 | 0.258 | 0.157 |
| 0.10 | 0.942 | 0.694 | 0.374 |
| 0.15 | 2.678 | 1.596 | 0.690 |
| 0.20 | **57.13** | 4.562 | 1.199 |
| 0.25 | **7.9 × 10¹⁵** | 2.6 × 10¹⁵ | 2.160 |

**The blow-up is the statistic, not the economy.** §6 defines the boundary as the growth at
which the affected-debt share returns to zero, so it is a maximum over households. Once the
§9 bound-5 cap drives one household's post-shift income to near zero, the growth needed to
make that household whole diverges. The κ = 1.0 column, where the capital gain is large
enough to keep every household above water, stays finite throughout — which is the clearest
demonstration that the divergence is a property of the definition.

---

## 4. Shares of households and of debt

Primary cell, g = 0. Full table in `shares_table.csv`.

### Overall, and the s-invariance

| s | Households affected | Debt affected | Debt crossing PTI > 0.40 |
|---|---|---|---|
| 0.01 | 0.6173 | 0.5925 | 0.0000 |
| 0.05 | 0.6174 | 0.5925 | 0.0000 |
| 0.10 | 0.6176 | 0.5925 | 0.0000 |
| 0.25 | 0.6181 | 0.5928 | 0.0002 |

**The extensive margin is almost perfectly invariant to the size of the shift.** Both the
wage loss and the capital gain scale linearly in s, so *who* is affected is set by whether a
household earns more wages than it owns equity — not by how large the shift is. Only the
intensive margin (how much growth restores capacity) scales. This is a structural result and
it holds across every allocation.

**Almost no debt crosses a distress threshold.** At g = 0 and s = 0.25, only **0.02 percent**
of debt crosses PTI > 0.40; the 0.36, 0.43 and 0.50 thresholds behave the same way. The
income changes are small relative to most households' distance from the thresholds. The
distress-threshold outcome of §5.3 is therefore **uninformative in this exercise**, and that
is reported rather than dropped.

### By debt class, and the credit-card under-reporting axis shown separately

At s = 0.05, share of each class's balances owed by households whose capacity falls:

| Class | Unadjusted | UR-adjusted |
|---|---|---|
| Mortgage | 0.6075 | 0.6075 |
| Credit card | 0.6213 | 0.6213 |
| Vehicle | 0.5388 | 0.5388 |
| Education | 0.6776 | 0.6776 |
| **Total** | **0.5925** | **0.5864** |

Within-class shares are identical by construction — the under-reporting factor scales a
class uniformly. The adjustment moves the **total** by −0.006, because it reweights toward
credit cards (factor 3.734), whose affected share is above average. **The credit-card
correction is therefore small for this statistic**, which is a more reassuring result than
FEASIBILITY §0.1 anticipated, and it is reported as a separate axis rather than folded in.

### By wage quintile, wealth group and age

At s = 0.05, unadjusted:

| Wage quintile | Households | Debt |
|---|---|---|
| Q1 | 0.5308 | 0.2075 |
| Q2 | 0.6090 | 0.4322 |
| Q3 | 0.6670 | 0.5863 |
| Q4 | 0.5888 | 0.5891 |
| Q5 | 0.6905 | 0.7052 |

| Wealth group | Households | Debt |
|---|---|---|
| **p0–25** | **0.8460** | **0.7240** |
| p25–50 | 0.6807 | 0.6506 |
| p50–75 | 0.5222 | 0.5857 |
| p75–90 | 0.4295 | 0.6006 |
| p90–99 | 0.4226 | 0.5691 |
| **top 1** | **0.2364** | **0.3317** |

**The wealth gradient is the strongest and most robust result in the run.** 84.6 percent of
bottom-quartile households lose capacity against 23.6 percent of the top 1 percent, and the
gradient is monotone. It is driven by exactly the fact FEASIBILITY §0.2 recorded in advance:
the households that owe the debt are not the households that own the equity.

The wage gradient is not monotone in households (Q4 dips) but is monotone in **debt**,
rising from 0.21 to 0.71 — the top wage quintile owes most of the debt that is affected.

---

## 5. Holder mapping

Affected debt mapped through the measurement paper's holder map. At every s the affected
stock is about **$9,829bn**, and the holder composition is invariant:

| Holder | Share of affected debt |
|---|---|
| **Federal government (central classification)** | **0.5506** |
| Banks | 0.3434 |
| Other financial | 0.0871 |
| Insurers | 0.0067 |
| State and local government | 0.0055 |
| Nonfinancial business | 0.0024 |
| Households | 0.0021 |
| **Federal government (agency pools NOT federal)** | **0.0793** |

**The federal share moves from 0.551 to 0.079 between the two agency classifications.** That
is a factor of seven and it is the single largest judgement call in this section, exactly as
the measurement paper found for its own sovereign share (0.794 against 0.587). Under the
central classification the federal government holds or guarantees **more than half** of the
debt owed by households whose capacity falls; under the alternative it holds **under a
tenth**. Both are reported; neither is preferred.

---

## 6. Arrangements

Effect on the boundary and fiscal cost, primary cell. Full table in `arrangements.csv`.

**At s = 0.10 (baseline boundary 0.9424):**

| Arrangement | Parameter | Boundary | Δ | Cost ($bn) |
|---|---|---|---|---|
| Broadened retirement | **liquid** | 0.7874 | **−0.1550** | 273.6 |
| Broadened retirement | **illiquid** | 0.9424 | **0.0000** | 0.0 |
| Universal fund | ω = 0.10 | 0.8635 | −0.0789 | 133.5 |
| Universal fund | ω = 0.05 | 0.9021 | −0.0403 | 66.8 |
| Universal fund | ω = 0.02 | 0.9261 | −0.0163 | 26.7 |
| Universal fund | ω = 0.01 | 0.9342 | −0.0082 | 13.4 |
| Capital tax | required 0.137 | 0.9178 | −0.0246 | 40.5 |
| Capital tax | required 0.110 | 0.9226 | −0.0198 | 32.5 |
| Capital tax | assembled 0.086 | 0.9269 | −0.0155 | 25.4 |

**Three things follow.**

**Liquidity is the whole of the broadened-ownership arrangement.** Illiquid broadened
retirement ownership moves the boundary by **exactly zero** at every s. Ownership without
access changes no household's cash flow, so it cannot change an income test. The pair was
designed to separate ownership from access and the separation is total: **all of the value
is access, none is ownership.**

**The capital-tax transfer is the weakest instrument per dollar.** Moving from the
assembled rate (0.086) to the top of the required band (0.137) — the measurement paper's
entire fiscal gap — buys **−0.009** of boundary at s = 0.10. The gap that decides the
fiscal condition barely registers in the household condition.

**No arrangement closes the boundary.** The best, liquid broadened retirement at $273.6bn,
removes 16 percent of it.

---

## 7. Sensitivities, reported whatever they show

Full table in `sensitivities.csv`.

**At s = 0.05 (baseline 0.3202):**

| Sensitivity | Parameter | Boundary | Δ |
|---|---|---|---|
| Price pass-through | π = 1.00 | 0.1440 | **−0.1762** |
| Price pass-through | π = 0.50 | 0.1975 | −0.1227 |
| κ | counterfactual 1.00 | 0.1573 | −0.1629 |
| κ | accrual 0.52 | 0.2576 | −0.0626 |
| Equity over-statement treated as real | ×1.504 | 0.2854 | −0.0348 |
| **Indexed transfers** | — | 0.3671 | **+0.0469** |
| **Refinancing** | −100bp, −200bp | 0.3202 | **0.0000** |
| **Retained wage share** | R = 0.70, 0.85 | 0.3202 | **0.0000** |

**Price pass-through is the sensitivity most likely to close the boundary**, as §8.1
predicted, and at full pass-through it removes 55 percent of it. It does not close it.
(π = 0 and π = 0.25 return no value at s ≥ 0.05 because the fixed-point search runs on the
pre-registered g grid, which is censored at 0.20; this is a grid limit, not a result.)

**Refinancing moves nothing, structurally.** Payments are fixed in the rising test, so
changing them cannot alter who loses capacity. Reported as zero rather than omitted.

**Indexing transfers to the shift makes the boundary worse** (+0.047 at s = 0.05, +0.428 at
s = 0.10). Transfers accrue to households that hold little debt and have already lost little
wage income, so indexing them raises aggregate income without helping the binding household.
This is the only sensitivity that moves in the unhelpful direction and it is reported as
such.

**A higher retained wage share does nothing until s = 0.10**, where R = 0.85 buys −0.159.
Under the concentrated allocation a higher R means more households each losing less, which
leaves the binding household unchanged until the loss must spread widely.

---

## 8. 2019 stability check — FAILS

§11 fixes instability as a sign change or a boundary move above 25 percent.

| s | 2022 | 2019 | Change | Unstable? |
|---|---|---|---|---|
| 0.01 | 0.0510 | 0.0255 | **−49.9%** | **yes** |
| 0.02 | 0.1074 | 0.0524 | **−51.2%** | **yes** |
| 0.05 | 0.3202 | 0.1422 | **−55.6%** | **yes** |
| 0.10 | 0.9424 | 0.3314 | **−64.8%** | **yes** |

**The boundary fails the stability check at every s, by two to three times the threshold.**
The sign is unchanged and the ordering across s is preserved, but the level is roughly half
in 2019. The boundary is a max-over-households statistic, so it is sensitive to the tail of
the joint distribution of wage income, equity and debt, and that tail differs between waves.

**This is not averaged away and it is not a footnote.** Any level reported from the 2022
wave should be treated as wave-specific. The **distributional shape** — the wealth gradient
of §4 — is what should be carried forward, not the boundary's level.

---

## 9. §10 — does this run meet the definition of an uninteresting result?

Stated plainly, against the three clauses fixed in advance.

**§10.1, boundary at or near zero everywhere: NO.** The boundary is strictly positive at
every s and every convention, and large: 5 percent growth for a 1-percent shift.

**§10.2, driven entirely by one convention: NO, but narrowly.** The pre-committed test
returns False by 0.007. The honest statement is that the convention spread is **comparable
to** the effect of the whole s grid, not smaller than it in any comfortable margin, and that
κ is the single widest axis in the results.

**§10.3, direction alone: the run does not rest on direction.** The reportable content is
the wealth gradient (84.6 percent against 23.6 percent), the holder mapping (0.551 against
0.079 across agency classifications), and the liquidity-versus-ownership separation (all
value in access). None of these is a statement of direction.

**Verdict: the run does not meet §10's definition of uninteresting, but it fails §11's
stability requirement and its headline object is fragile by construction.** The
specification's boundary should not be the contribution; §4, §5 and §6 should.

---

## EXPLORATORY, NOT PRE-SPECIFIED

Three items. **None bears on the verdict.**

**E1. A robust boundary exists if the definition is relaxed.** §6 requires the affected-debt
share to return to *zero*, which is a max statistic. The growth at which the affected share
falls to 1 percent of debt, rather than zero, would be far smaller and would not diverge.
That is a different object from the one pre-registered and was not computed; it is noted
because it is the obvious repair.

**E2. The basis axis is degenerate and the spec has one fewer degree of freedom than it
appears.** Cash-flow and accrual produce identical numbers in every cell (§2). A future
specification should either define the accrual basis on a stock rather than a flow, or drop
the axis.

**E3. The affected stock is stable at about $9,829bn across the whole s grid** — 59 percent
of household debt — because of the s-invariance in §4. That number, and the holder split on
it, is arguably the most quotable quantity the run produced, and it required no boundary at
all.

---

## Appendix: files

| File | Contents |
|---|---|
| `run_verification.json` | H2 invariants and preconditions |
| `bounds.json` | §9 plausibility bounds |
| `s10.json`, `s10_convention_grid.csv` | §10 check |
| `boundary_table.csv` | all 378 boundary cells |
| `shares_table.csv` | shares by s, group and UR axis |
| `holder_mapping.csv` | §5 |
| `arrangements.csv`, `sensitivities.csv`, `stability_2019.csv` | §6, §7, §8 |
| `DEVIATIONS.md` | seven logged items |
