# Deviations log — household condition run, 2026-09-21

Every departure from `SPECIFICATION.md` (SHA256
`476e093703da92d8eacf85332f2d6f637851b2e925b5a34bcb441d1e35f21f9b`), with its reason and
whether it was decided before or after a result was seen.

**No grid, allocation, ownership definition, basis, threshold, arrangement, sensitivity or
primary cell has been changed.**

---

## D1. Negative business equity floored at zero as an allocation weight

**Decided before any result was computed.**

§4.1 uses `bus` as part of two ownership bases. The SCF contains **2 rows of 22,975** with
negative business equity, minimum **−$300**, weighted aggregate **−$0.0004bn**.

§9 bound 1 requires ownership shares to lie in **[0,1]**, which a negative weight would
violate — it would assign a household a negative share of the capital gain. The bound
therefore forces the treatment: **negative equity is floored at zero when used as an
allocation weight.** Balances are left unaltered wherever they are reported as levels.

This is the closest pre-specified alternative and it is implied by the specification rather
than chosen. The quantity involved is four ten-thousandths of a billion dollars and moves
nothing.

---

## D2. Preconditions that are not bounds, recorded so they are not mistaken for violations

**Before any result.**

Three baseline features look like bound violations and are not:

| Feature | Value | Why it is not a violation |
|---|---|---|
| `pirtotal` above 1.0 | 374 rows, max 313.5 | Payment-to-income is a **ratio, not a share**, and §9 bound 1 does not apply to it. A household with near-zero income and any payment has an arbitrarily large PTI. |
| `bussefarminc` negative | min −$1,680,818 | Business **losses** are real income components and are kept. §9 bound 5 constrains total household income, not its components. |
| `wageinc` negative | 20 rows | Self-employment losses booked to wage income. Kept; they enter the wage-loss allocation at their reported value and cannot produce a negative total by §9 bound 5. |

Households with `income ≤ 0` (**197 rows, 0.86 percent**) are excluded from ratio
calculations and counted, exactly as §9 bound 5 requires.

---

## D3. The accrual basis collapses onto the cash-flow basis

**Decided before any result was read; consequence seen after.**

§4.2 defines the accrual basis as counting the whole capital gain as income "at a stated
annuity rate applied to the wealth increment". The shift of §2 moves an income **flow**.
Capitalising a flow at rate *a* and annuitising the resulting wealth at the same rate *a*
returns the flow. The accrual basis therefore counts the whole household-reaching gain as
income and the annuity rate cancels.

**Consequence, visible in every table: the cash-flow and accrual bases produce identical
numbers, and only κ separates them.** The specification's two-basis structure has one
degree of freedom, not two. The annuity rate bites only where a **stock** of equity is
converted into an income stream — the universal fund (§7.2) and broadened retirement
ownership (§7.3) — and it is applied there.

This was not changed. It is the arithmetic the specification implies.

---

## D4. A coding error in the capital-gain allocation, caught by bound 3

**Found before any result was read, by the §9 bound-3 check.**

`gamma` divided the per-household gain by the household weight, so the allocated capital
gain summed to about one one-thousandth of its target: bound 3 failed at a relative
deviation of 0.999. Corrected to `pot * own / Σ(own·w)`, which satisfies `Σ γᵢ wᵢ = pot`
exactly.

Bound 3 now holds at 3.57 × 10⁻¹⁶. **The bound did its job**: the error would otherwise
have produced a near-zero capital gain and a spuriously large boundary in every cell.

---

## D5. The SCF's bottom wage quintile has no wage income, so the quintile shares are
## renormalised

**Before any result was read. §3.3 affected; every quintile-allocation result is marked.**

§3.3 distributes the wage loss across quintiles in proportion to the measurement paper's
wage-bill shares, whose first element is 0.0324. **In the SCF the bottom wage quintile
contains no wage income at all** — the bottom fifth of households by wage income are
non-earners (0 of 919 with positive wage income). Q1's share cannot be placed, and bound 3
failed by exactly 3.24 percent.

The SCF and paper profiles also differ materially elsewhere (SCF Q5 0.665 against the
paper's 0.512), because the paper's quintiles are cut on a different base.

**Closest pre-specified alternative, and the one the bounds force:** renormalise the paper's
shares over quintiles with a positive wage bill. Bound 3 then holds exactly. **Results under
the quintile allocation carry this renormalisation** and should not be read as reproducing
the paper's quintile profile.

---

## D6. Bounds 3 and 5 conflict for 121 households; resolved by capping with redistribution

**Before any result was read.**

121 valid households of 4,556 have wage income exceeding total income (negative business
income). For them the wage loss can drive income below zero, violating bound 5, while
capping the loss violates bound 3.

**Resolution, forced by holding both bounds:** cap the loss at the household's
income-plus-gain and redistribute the capped excess pro rata across households with
remaining headroom, iterated to convergence. The excess is **0.0033 percent** of the target
at s = 0.25.

Both bounds then hold: bound 3 at 3.57 × 10⁻¹⁶ and bound 5 at zero violations.

**Consequence, seen later and reported in RESULTS §3:** the cap can drive a household's
post-shift income to near zero, and because §6's boundary is a maximum over households, the
boundary diverges at high s. That divergence is a property of the specification, not of the
correction — the κ = 1.0 column, where the gain keeps every household above water, stays
finite.

---

## D7. The boundary is censored beyond the pre-registered growth grid

**After results were computed. No specification changed.**

§2 fixes the growth grid at g ∈ [0, 0.20]. The boundary exceeds 0.20 for **s ≥ 0.05 in every
convention except κ = 1.0**, and for all conventions at s ≥ 0.10.

§6 defines the boundary as "the smallest g on the grid" satisfying the condition, so the
pre-registered answer where the grid is not reached is **censored**, and it is reported as
such rather than extrapolated. The uncensored **analytic** boundary — the growth that makes
the worst-affected indebted household whole — is reported alongside, clearly labelled, so
the censoring can be quantified.

The §10 comparison is made on the **grid** boundary, the object §6 defines, restricted to the
s values uncensored in every convention cell (s = 0.01 and 0.02). That restriction is stated
with the result.

---
---

# V2 DEVIATIONS — POST HOC

**Everything below concerns `SPECIFICATION_V2.md`, which is POST HOC: written after the v1
results were seen. The v1 deviations D1 to D7 continue to apply unchanged.**

## V2-D1. Households driven to non-positive net income carry an infinite restoring rate

**Decided before any v2 result was read.**

`SPECIFICATION_V2.md` §2 defines each household's restoring rate as
`income / post-shift income − 1`. For households whose post-shift income is driven to zero
or below by the §9 bound-5 cap (D6), that rate is undefined.

**Treatment: they carry `g_i = +∞`** — no finite growth restores them — and they are kept in
the debt weighting. Excluding them would understate the distribution by dropping exactly the
worst-affected debt. They are counted and reported as `share_never_restored`, which is
**0.0000 at every s except 0.25, where it is 0.0002**.

This is the treatment that preserves the v1 information rather than discarding it: v1's
maximum was driven by these households, and v2 keeps them visible at the top of the
distribution instead of letting one of them set the headline.

## V2-D2. The conditional median is the wrong statistic for evaluating an arrangement

**Found after v2 results were computed. No specification changed. This is the most
important caveat on the v2 numbers.**

`SPECIFICATION_V2.md` §3 carries the v1 arrangements over unchanged and reports their effect
on the median. **That turns out to be a selection artefact**, and the artefact runs the wrong
way: **most arrangements raise the median while genuinely helping.**

The mechanism, verified directly. At s = 0.10 the capital-tax transfer at the assembled rate:

| | Affected debt | Households affected | Median |
|---|---|---|---|
| No arrangement | $9,662.6bn | 1,962 | 0.1673 |
| Capital tax 0.086 | $7,945.7bn | 1,118 | 0.1760 |

The transfer lifts **844 households and about $1.7 trillion of debt out of the affected set
entirely** — and those are the households needing the *least* growth. Removing the
easiest-restored debt from the denominator raises the median of what remains. The same
effect drives `restored_at_10%` **down** from 0.313 to 0.171, which reads as harm and is the
opposite of what happened.

**A distribution conditional on being affected cannot measure an intervention that changes
who is affected.** Both quantities are therefore reported side by side in RESULTS_V2 §4 —
the affected-debt level, which falls and shows the arrangement working, and the conditional
median, which rises and is an artefact. **The median deltas in the arrangements table must
not be read as the arrangements' effect.**

The repair — holding the denominator fixed at the no-arrangement affected set, or reporting
the share of *all* household debt restored — was not specified in v2 and has not been
computed. Inventing it now, after seeing that the specified statistic misbehaves, is exactly
the move a post hoc specification must not make twice.

## V2-D3. The pre-stated stability criterion is partly failed

**After v2 results were read. Reported first in RESULTS_V2, as §4 of the v2 specification
requires.**

§4 fixed the criterion at 25 percent on the **median and both quartiles, each separately**,
and recorded in advance that failure of the *median* would mean the redefinition had fixed
nothing and should be abandoned.

Result: **4 of 12 statistics fail, all of them the lower quartile.**

| Statistic | Change 2022 → 2019 | Verdict |
|---|---|---|
| Median, all four s | +3.2% to +3.6% | **stable** |
| q75, all four s | +10.6% to +12.7% | **stable** |
| **q25, all four s** | **−78.4% to −79.7%** | **UNSTABLE** |

**The median passes, so the abandonment condition is not triggered and v2 is reported.** But
the criterion as written covers the quartiles too, and a third of it fails badly. The lower
quartile is the easiest-restored debt — households with large equity relative to their wage
loss — and its composition differs sharply between waves, which is unsurprising given equity
valuations between 2019 and 2022.

**Reported as a partial failure, not a pass.** The median and the upper quartile may be
carried forward; the lower quartile and anything derived from it may not.
