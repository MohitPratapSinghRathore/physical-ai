# One page for the owner

**2026-09-21. Household condition. Branch `household-condition`, not merged.
Measured distributions, scenario arithmetic — not a forecast, not a causal estimate.**

> **Read this line first.** Everything in sections 1 to 5 below is **v1: pre-specified**,
> fixed before any data was seen. Section 6 is **v2: POST HOC**, a redefinition of one
> statistic made *after* the v1 results were known. The v2 numbers look better. That is not
> evidence, because the definition was chosen knowing what it would fix.

## 1. What was computed  *(v1, pre-specified)*

Take the Survey of Consumer Finances 2022 — 4,595 households, five implicates, 131 million
weighted. Move a share of the national wage bill to capital income. Hold every existing debt
and required payment fixed in nominal terms, because contracts do not move when factor shares
do. Then ask three things: whose ability to service debt falls, how much growth would undo
it, and which arrangements would move that.

Everything was specified in advance and the specification's hash was verified unchanged
before a single number was produced.

## 2. What was found  *(v1, pre-specified)*

**A boundary exists and it is large.** A 1-percent shift of the wage bill to capital needs
about **5 percent** cumulative real growth to restore household debt-service capacity;
2 percent needs about **11 percent**. Past a 5-percent shift the answer runs off the
pre-registered growth grid entirely.

**Who loses is sharply unequal, and this is the robust result.** Capacity falls for
**84.6 percent** of households in the bottom wealth quartile and **23.6 percent** of the top
1 percent, monotonically in between. The reason was known before the run: the households that
owe the debt are not the households that own the equity, and **47 percent of US corporate
equity sits with foreign, nonprofit and government holders whose income never reaches any
household at all.**

**Of the debt owed by households whose capacity falls — about $9.8 trillion, 59 percent of
household debt — the federal government holds or guarantees 55 percent** under the
measurement paper's central classification. Under the alternative agency treatment it holds
under 8 percent. That factor-of-seven swing is the largest judgement call in the exercise.

**Among the arrangements, only access matters.** Broadening retirement-account ownership
*with* liquidity moves the boundary; broadening it *without* liquidity moves it by **exactly
zero**. Ownership that cannot be spent cannot service debt. The capital-tax transfer is the
weakest instrument per dollar: moving from the paper's assembled rate to the top of its
required band — the whole fiscal gap — buys almost nothing here.

## 3. How much of it is convention  *(v1, pre-specified)*

**More than is comfortable.** The pre-committed test asked whether the convention spread
exceeds the effect of the entire shift grid. It answers **No — by 0.007.** That is a pass on
the letter and a warning in substance.

Two specific problems:

- **The boundary is a maximum over households.** The specification asks for the growth at
  which *no* household's capacity is reduced, so one household sets the answer. It explodes
  from 0.94 to 57 to 7.9 × 10¹⁵ across the top of the shift grid. That is the statistic
  misbehaving, not the economy.
- **The 2019 wave gives a boundary half the size**, failing the stability test at every
  shift size by two to three times the threshold fixed in advance.

Also worth knowing: the specification's two capital-income bases turn out to be the same
thing arithmetically, so it has one degree of freedom where it appeared to have two. And
refinancing moves the boundary by exactly zero, because with payments fixed the test reduces
to an income test.

## 4. What it would and would not support in a paper  *(v1)*

**Would support:** the distributional incidence. The wealth gradient, the $9.8 trillion
affected stock, the holder mapping under both classifications, and the
liquidity-versus-ownership separation are stable, interpretable and not obtainable from the
aggregate accounts. The liquidity finding in particular is a clean policy-relevant result:
universal-capital-fund proposals that vest ownership without access do nothing for debt
service.

**Would not support:** the boundary as a headline number. It fails its own stability check,
it is defined as a maximum, and its level is wave-specific. Any paper should report the
incidence and treat the growth threshold as an illustrative scaling, not a finding — or
redefine it on a share of debt rather than on every household, which is the obvious repair
and was not pre-registered.

The novelty position from the feasibility session is unchanged: Bartscher, Kuhn, Schularick
and Steins already stress-test SCF debt-service capacity, so the contribution is the
factor-share shock, the incidence, and the holder mapping — not the machinery.

## 5. How it relates to the measurement paper's fiscal boundary  *(v1)*

The fiscal condition asks whether the tax system can recoup from capital what labour stops
paying: `τ_k · g ≥ τ_l · (1 − R)`. The paper finds it fails, with an assembled rate of 0.086
against a required 0.110 to 0.137.

The household condition is the same question one layer down, and **it answers worse.** The
fiscal gap is a gap between two rates that a legislature could in principle close. The
household gap is structural: the capital income simply does not arrive at the households that
owe the debt, because 47 percent of it leaves the household sector and another 25 percent is
locked in retirement vehicles. Closing the paper's entire fiscal gap — moving τ_k from 0.086
to 0.137 — shifts the household boundary by less than one percentage point of growth.

**That is the connection worth stating: the fiscal condition can be fixed with a rate; the
household condition cannot.** It is an ownership-and-access problem, and the run's own
arrangements show that only the access half moves anything.


---
---

## 6. V2 — POST HOC. The boundary redefined after the results were seen

**This section is not pre-specified.** After the v1 run, the boundary was redefined and
written into `SPECIFICATION_V2.md`, committed before anything under it was computed. That
ordering is the only discipline a post hoc specification can offer, and it is not a
substitute for pre-registration.

**What changed.** v1 asked how much growth would restore *every* affected household — a
maximum over households, so one observation set it. v2 asks, for each affected household,
what growth would restore *that household*, and reports the **debt-weighted distribution**:
median, quartiles, 90th percentile, and the share of affected debt restored at 5, 10 and 20
percent growth. Nothing else changed — same shift sizes, same cases, same ownership
definitions, same κ values, same arrangements.

**What v2 shows.** The median dollar of affected debt needs **7.6 percent** growth at a
5-percent shift and **16.6 percent** at a 10-percent shift. At a 5-percent shift, **99 percent
of affected debt is restored by 10 percent growth**. The corresponding v1 numbers were 32 and
94 percent, and at a 20-percent shift v1 reported **5,713 percent** where the median is 39.7
— because one household needed that much.

**Three honest qualifications.**

1. **The improvement was the point.** A median is not set by a tail; that it behaves better
   than a maximum is nearly a property of the statistic, not a discovery about households.
2. **A third of the stability test still fails.** The median is stable across waves to 3.6
   percent and the upper quartile to 12.7, but the **lower quartile moves by −79 percent** at
   every shift size. The median and upper quartile can be carried forward; the lower quartile
   cannot.
3. **v2 cannot measure the arrangements, and this is the sharpest finding of the exercise.**
   A distribution conditional on being affected cannot evaluate an intervention that changes
   *who* is affected. Most arrangements remove about **$1.7 trillion** of debt from the
   affected set — genuinely helping — while *raising* the median, because the debt they
   remove is the easiest to restore. Any reading of the median deltas as the arrangements'
   effect is wrong.

**What this means for a paper.** v1's boundary should not be the headline; the incidence
(section 2) should. If a growth threshold is reported at all, the v2 median is the defensible
form — labelled post hoc, with the stability failure stated, and **not** used to rank
arrangements. The two findings that survive both versions unchanged are the wealth gradient
and that **ownership without liquidity does exactly nothing**: illiquid broadened ownership
moves every statistic in both versions by precisely zero.
