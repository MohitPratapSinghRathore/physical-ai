# The household condition: results, V2

# ⚠ V2 — POST HOC. DEFINITION CHANGED AFTER V1 RESULTS WERE SEEN.

**Every number in this document is post hoc.** The boundary was redefined in
`SPECIFICATION_V2.md` (sha256 `cabd85ea…f50078`, committed at H4 `13ed331` before anything
here was computed) **after** the v1 run was complete and its results were known. This
carries none of the evidentiary standing of `SPECIFICATION.md`, which was fixed before any
data was seen and whose results are in `RESULTS.md`.

**The v2 numbers are better than v1's. That is not evidence, because the definition was
chosen with knowledge of what it would fix.**

Measured distributions, scenario arithmetic. Not a forecast, not a causal estimate.

---

## Verdict

**The redefinition works on its own terms and fails a third of its own stability test.**

The debt-weighted median restoring rate is **7.64 percent [7.29, 7.99]** at a 5-percent
shift and **16.55 percent [15.73, 17.36]** at a 10-percent shift — against v1 maxima of 32.0
and 94.2 percent for the same cells. At a 20-percent shift the median is 0.397 against v1's
**57.13**, a factor of 144. The statistic no longer diverges, is never censored, and passes
the convention test by a factor of six where v1 passed by 0.007.

**But the pre-stated stability criterion is partly failed.** The median is stable to within
3.6 percent across waves and the upper quartile to within 12.7 percent; **the lower quartile
moves by −78 to −80 percent** and fails at every s. §4 of the v2 specification made median
failure the abandonment condition — that is not triggered — but the criterion covered the
quartiles too, and a third of it fails.

**And the arrangements section of v2 is unusable as written.** A distribution conditional on
being affected cannot measure an intervention that changes who is affected. Most arrangements
*raise* the median while removing $1.7 trillion of debt from the affected set. See §4.

---

## 1. Stability check, reported first

§4 of the v2 specification: 25 percent, on the median and both quartiles, each separately.

| Statistic | 2022 | 2019 | Change | Verdict |
|---|---|---|---|---|
| Median, s = 0.01 | 0.0144 | 0.0149 | +3.2% | stable |
| Median, s = 0.02 | 0.0292 | 0.0302 | +3.2% | stable |
| Median, s = 0.05 | 0.0764 | 0.0790 | +3.4% | stable |
| Median, s = 0.10 | 0.1655 | 0.1715 | +3.6% | stable |
| q75, s = 0.01 | 0.0162 | 0.0179 | +10.6% | stable |
| q75, s = 0.02 | 0.0329 | 0.0364 | +10.8% | stable |
| q75, s = 0.05 | 0.0864 | 0.0963 | +11.5% | stable |
| q75, s = 0.10 | 0.1892 | 0.2131 | +12.7% | stable |
| **q25, s = 0.01** | 0.0064 | 0.0014 | **−78.4%** | **UNSTABLE** |
| **q25, s = 0.02** | 0.0128 | 0.0028 | **−78.5%** | **UNSTABLE** |
| **q25, s = 0.05** | 0.0327 | 0.0069 | **−78.9%** | **UNSTABLE** |
| **q25, s = 0.10** | 0.0677 | 0.0138 | **−79.7%** | **UNSTABLE** |

**FAIL on 4 of 12 statistics, all of them the lower quartile.**

The median's stability is a genuine improvement over v1's maximum, which failed at every s by
50 to 65 percent — **and the improvement was the point of the redefinition, so it should be
discounted accordingly.** A median is not set by a tail; that it is more stable than a
maximum is close to a property of the statistic rather than a discovery about the data.

The lower quartile is the easiest-restored debt: households holding large equity relative to
their wage loss. Its composition differs sharply between 2019 and 2022, which is
unsurprising given what equity valuations did between those waves. **The median and upper
quartile may be carried forward; the lower quartile may not.**

---

## 2. The debt-weighted distribution of the restoring rate

Primary cell: concentrated allocation, all ownership routes, cash-flow basis, κ = 0.27.
Five implicates by Rubin's rules. Full surface in `v2_distribution.csv`.

| s | q25 | **median** | q75 | p90 | **p100 = v1's boundary** | IQR/median | @5% | @10% | @20% |
|---|---|---|---|---|---|---|---|---|---|
| 0.01 | 0.0064 | **0.0144** | 0.0162 | 0.0165 | 0.0510 | 0.68 | 1.000 | 1.000 | 1.000 |
| 0.02 | 0.0128 | **0.0292** | 0.0329 | 0.0336 | 0.1074 | 0.69 | 0.997 | 1.000 | 1.000 |
| 0.05 | 0.0327 | **0.0764** | 0.0864 | 0.0886 | 0.3202 | 0.70 | 0.325 | 0.994 | 1.000 |
| 0.10 | 0.0677 | **0.1655** | 0.1892 | 0.1943 | 0.9424 | 0.73 | 0.234 | 0.313 | 0.987 |
| 0.15 | 0.1051 | **0.2706** | 0.3134 | 0.3229 | 2.678 | 0.77 | 0.212 | 0.245 | 0.369 |
| 0.20 | 0.1452 | **0.3966** | 0.4666 | 0.4824 | **57.13** | 0.81 | 0.204 | 0.228 | 0.296 |
| 0.25 | 0.1869 | **0.5503** | 0.6602 | 0.6857 | **∞** | 0.86 | 0.197 | 0.217 | 0.259 |

Median with interval (Rubin plus 200 bootstrap replicate weights):

| s | Median | 95 percent interval |
|---|---|---|
| 0.05 | **0.0764** | [0.0729, 0.0799] |
| 0.10 | **0.1655** | [0.1573, 0.1736] |

**What the p100 column shows.** Putting v1's boundary in the same table as its own p100 is
the clearest statement of what was wrong with it. At s = 0.20 the median household-dollar of
affected debt needs 39.7 percent growth; the worst single dollar needs 5,713 percent. v1
reported the second number.

**The distribution is not degenerate** (§5.2): the interquartile range runs 0.68 to 0.86 of
the median, so a point estimate would have lost real information.

**The restored shares are the readable form.** At a 5-percent shift, **99.4 percent of
affected debt is restored by 10 percent growth**. At a 10-percent shift only 31.3 percent is,
but 98.7 percent is restored by 20 percent growth. **Beyond s = 0.15 the distribution's tail
thickens sharply**: at s = 0.25, 20 percent growth restores only 25.9 percent of affected
debt. The share that no finite growth restores is 0.0000 everywhere except s = 0.25, where it
is 0.0002 (V2-D1).

---

## 3. §5.3 convention test on the median

| Quantity | v2 (median) | v1 (maximum) |
|---|---|---|
| Spread across the s grid | **0.5359** | 0.0570 |
| Spread across conventions, worst over s | **0.0879** | 0.0500 |
| Convention exceeds s | **False** | False |
| **Margin** | **6.1× — comfortable** | **0.007 — narrow** |

**v2 passes decisively where v1 passed by a hair.** The median responds to the size of the
shift six times more than it responds to the convention, and it is defined at every s rather
than censored beyond 0.02. This is the clearest respect in which the redefinition is an
improvement, and it is a real one — but it is also partly mechanical, because v1's s-spread
was compressed by censoring at exactly the values where the convention spread was measured.

As in v1, the cash-flow and accrual bases produce identical numbers (D3 stands): the
specification has one degree of freedom where it appears to have two, and κ is the only axis
that moves anything.

---

## 4. Arrangements — and why the v2 statistic cannot measure them

**This section reports a failure of the v2 specification, not a result about arrangements.**

§3 of the v2 specification carried the v1 arrangements over and asked for their effect on the
median. **That is a selection artefact.** At s = 0.10:

| Arrangement | Affected debt | Δ affected debt | Median | Δ median | Cost |
|---|---|---|---|---|---|
| **None** | $9,829.1bn | — | 0.1655 | — | — |
| Broadened retirement, **illiquid** | 9,829.1 | **0.0** | 0.1655 | **+0.0000** | 0.0 |
| Broadened retirement, **liquid** | 8,042.9 | **−1,786.2** | 0.1569 | −0.0086 | 273.6 |
| Capital tax, assembled 0.086 | 8,111.7 | −1,717.4 | 0.1747 | **+0.0092** | 25.4 |
| Capital tax, required 0.110 | 8,106.7 | −1,722.5 | 0.1743 | **+0.0088** | 32.5 |
| Capital tax, required 0.137 | 8,105.5 | −1,723.7 | 0.1738 | **+0.0083** | 40.5 |
| Universal fund, ω = 0.01 | 8,112.6 | −1,716.5 | 0.1755 | **+0.0100** | 13.4 |
| Universal fund, ω = 0.10 | 8,078.3 | −1,750.9 | 0.1672 | **+0.0018** | 133.5 |

**Every arrangement except the illiquid one removes about $1.7 trillion of debt from the
affected set, and most of them raise the median while doing it.** The transfer lifts the
households needing the *least* growth out of the affected set; removing the easiest-restored
debt from the denominator raises the median of what remains. The `restored_at_10%` statistic
moves the same wrong way, falling from 0.313 to 0.171.

**The median deltas in this table must not be read as the arrangements' effect.** The
affected-debt column is the honest one, and it says every cash arrangement helps by roughly
the same amount — about $1.7tn — nearly regardless of its cost, from $13.4bn to $273.6bn.

**Two things survive from v1 unchanged.** Illiquid broadened ownership moves **exactly
nothing** on both the affected-debt level and the median: ownership without access cannot
service debt. And the capital-tax transfer remains weak — moving across the measurement
paper's entire fiscal gap, from 0.086 to 0.137, changes the affected debt by $6bn out of
$9,829bn.

The repair (fixing the denominator, or reporting the share of *all* household debt restored)
was not specified in v2 and has **not** been computed. Inventing a third statistic after
watching the second one misbehave is the move a post hoc specification must not make twice.
See DEVIATIONS V2-D2.

---

## 5. §5 — does v2 meet its own definition of an uninteresting result?

| Clause | Test | Result |
|---|---|---|
| **5.1** Median at or near zero | median < 1 percent? | **No.** 1.44 percent at s = 0.01, rising to 55 percent at s = 0.25. |
| **5.2** Degenerate distribution | IQR a small fraction of the median? | **No.** IQR/median runs 0.68 to 0.86. |
| **5.3** Convention-driven | convention spread > s spread? | **No**, and by a factor of 6.1. |
| **5.4** Stability failure | median fails at 25 percent? | **No** for the median (3.6 percent). **Yes for the lower quartile** (−79 percent). |

**v2 does not meet its own abandonment condition. It does partly fail its own stability
criterion, and its arrangements section does not measure what it was meant to.**

---

## 6. What changed between v1 and v2, in one table

| | v1 (pre-specified) | v2 (post hoc) |
|---|---|---|
| Object | maximum over households | debt-weighted distribution |
| Headline at s = 0.05 | 0.3202 | **0.0764** median |
| Headline at s = 0.20 | **57.13** | **0.3966** median |
| Behaviour at s = 0.25 | diverges (7.9 × 10¹⁵) | finite (0.5503) |
| Censoring | beyond grid for s ≥ 0.05 | none |
| Stability (median/max) | **fails at every s**, −50 to −65 percent | **passes**, +3.2 to +3.6 percent |
| Stability (quartiles) | not applicable | **q25 fails**, −79 percent |
| Convention test margin | No, by 0.007 | No, by a factor of 6.1 |
| Arrangements measurable | yes | **no** — selection artefact |

**The redefinition fixed the fragility and introduced a different problem.** It should be
described that way, and the fact that it was chosen after seeing v1 should be stated in the
same sentence as any claim that it is better.

---

## Appendix: files

| File | Contents |
|---|---|
| `SPECIFICATION_V2.md` | the post hoc definition, committed at H4 before computing |
| `run_v2.py` | the v2 run |
| `v2_stability.csv` | §1 |
| `v2_distribution.csv`, `v2_results.json` | §2, §3, §5 |
| `v2_arrangements.csv`, `v2_arrangements_with_denominator.csv` | §4 |
| `DEVIATIONS.md` | V2-D1 to V2-D3, after the v1 log |
