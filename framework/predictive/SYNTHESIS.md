# What labour backing does, and what it does not do

**Written for the owner, and as a candidate section for the measurement paper.
2026-09-26. Branch `predictive-panel`, not merged. Placing any of this in the
manuscript is the owner's call — nothing here edits it.**

---

## Why this document exists

Ten claims about labour backing have now been tested across six branches, most under a
hashed pre-registration with numeric kill thresholds fixed before the data was opened.
The results have been recorded branch by branch and never assembled. Assembled, they show
a pattern sharper than any single test:

> **Every claim that labour backing predicts or prices a risk has failed. Every claim that
> it measures the composition and incidence of a claim stock has held.**

That is not nine nulls in a row, which is how I described it in the `P3` commit message and
which is loose. It is a clean split along a line, and the line is informative.

## The record

| # | Claim tested | Branch / commit | Verdict |
|---|---|---|---|
| 1 | Bank labour backing predicts credit losses after the 2014–16 oil shock | `validation-pilot` `acaf6ba` | **Null**, powered (MDE 0.031 vs 0.10 threshold), then **voided by its own placebo** |
| 2 | The manuscript's credit engine has the structural slope claimed | `validation-pilot` `acaf6ba` | **Inconclusive**; predicted-loss term has no out-of-sample power |
| 3 | Bank labour backing predicts household charge-offs, 2001–2024 | `predictive-panel` `ec4511d` | **Null**; ranking gets *worse* in 13/13 years |
| 4 | Euro-area sovereign share matches the US figure | `paper2-absorption` | **Fail**: 10.9pp against a 15pp criterion |
| 5 | The two-phase absorption story carries a second paper | `paper2-absorption` | **Fail**: a section (4.5), not a paper |
| 6 | The state's guarantee position rotated rather than grew | `paper2-absorption` `07a6332` | **Withdrawn**: a denominator artefact; reverses on household credit |
| 7 | The state exited household credit intermediation | `paper2-absorption` `07a6332` | **Killed**: published annually in the President's Budget (OMB) |
| 8 | Labour backing formalises into a leverage / pricing theory | `regulatory-gap` `4b5be45` | **3 of 4 fail**; labour leverage *reverses* (Λ_L 2.50 < Λ_K 3.53). One survives as framing only |
| 9 | Labour-backed claims get a regulatory treatment gap | `regulatory-gap` `4b5be45` | **Narrow survivor**, twice narrowed; Acharya (2011) has the guarantee–risk-weight link |
| 10 | A household debt-service boundary exists and is unequal | `household-condition` `4e0507b` | **Holds** as measurement; novelty criterion survived |

Rows 1, 2, 3, 6, 7 and 8 are the risk-and-prediction claims. All are dead. Rows 9 and 10
are composition-and-incidence claims and both stand, 9 narrowly.

## What holds

Each of these is an accounting statement about **who holds, owes or guarantees what**. None
forecasts anything.

- **Sovereign concentration: 79.4%** of the labour-backed claim stock is held, guaranteed or
  owed by the federal government, and that share roughly **doubled**.
- **47% of US corporate equity** sits with foreign, nonprofit and government holders whose
  income never reaches any household.
- **The incidence gradient: 84.6%** of bottom-wealth-quartile households lose debt-service
  capacity under a wage-to-capital shift, against **23.6%** of the top 1%, monotone in
  between.
- **Ownership without liquidity does exactly nothing** — broadening retirement-account
  ownership without access moves the boundary by **zero**.
- **The fiscal gap is real**: τ_k assembled at 0.086 against 0.110–0.137 required.

## Why the risk claims fail, and why that is not embarrassing

The reason is visible in the construct's own algebra, and it was recoverable from the
pilot before the large panel confirmed it.

**The class coefficients are near-binary.** About 0.80 on every household class, 0.0 on
every business class. So at the level of an intermediary, labour backing is very close to a
relabelling of *how much household lending you do*. The pilot measured this directly: the
bank-level measure is **94% reproducible** by someone who never opens the accounts. The
predictive panel measured it again from the other side: regressing `LB` on the seven
loan-share controls gives **R² = 0.517**.

A construct that is half to mostly a repackaging of loan mix cannot add risk information to
a model that already contains loan mix. It did not, in either test, and in the large panel
it subtracted.

**The Gap was the honest attempt to escape this** — the difference between the wage
dependence of a county's *debtors* and of its *population*, which genuinely is not in the
loan mix. It was tested twice and is null both times: coefficient −0.0165 with the wrong
sign against a 0.10 threshold in the pilot, and +0.00180 with a 0/13 ranking record in the
panel.

## The position this supports

Labour backing is **distributional accounting, not risk measurement**. It answers *whose
income stands behind this claim, and who ends up holding it* — and on that question it
produces facts nobody had assembled. It does not answer *which intermediary takes the
loss*, and ten tests now say it should not be asked to.

That is a defensible and publishable position. It is also a **stronger** claim than
silence, because the nulls are pre-registered, powered and recorded rather than absent.

## What the manuscript should therefore not say

1. Nothing implying a supervisor could use the accounts to forecast who loses money when
   labour income falls. The pilot's own conclusion, unchanged by anything since.
2. No leverage or pricing framing built on labour backing. Labour leverage runs the wrong
   way (Λ_L 2.50 against Λ_K 3.53).
3. No "the state exited" or "the position rotated" language. Both were withdrawn — one to
   OMB's own annual table, one to a denominator artefact.
4. The classification gap is **the stock of agency-guaranteed claims**, never the value of
   an implicit guarantee.
5. Every reported share needs its numerator *and* denominator growth beside it. That is the
   lesson of row 6, where a share looked flat only because Treasury issuance inflated what
   it was divided by.

## What is still open

- The **euro-area holder leg** at the same standard as the US. It failed as a comparison at
  10.9pp against a 15pp criterion, but it failed as a *criterion*, not as a measurement.
- The **factor-of-seven agency-classification swing** in row 10 (55% versus under 8% of the
  debt owed by households whose capacity falls). That is the largest unresolved judgement
  call anywhere in this work and it is a measurement question, which is the category that
  has been working.

Both are composition questions. On the record above, that is where to spend effort.
