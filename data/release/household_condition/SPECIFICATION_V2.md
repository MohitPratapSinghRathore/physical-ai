# Specification V2 — the boundary redefined

# ⚠ POST HOC. WRITTEN AFTER V1 RESULTS WERE SEEN.

**This is not a pre-registration. It is a redefinition of one object, proposed after the
v1 run was complete and its results were known.** Every result produced under it is post
hoc and is labelled **V2, POST HOC** wherever it appears — in `RESULTS_V2.md`, in
`OWNER_SUMMARY.md`, in every table and in every commit message. It carries none of the
evidentiary standing of `SPECIFICATION.md`
(sha256 `476e093703da92d8eacf85332f2d6f637851b2e925b5a34bcb441d1e35f21f9b`), which was
committed before any data was seen and which remains the pre-specified record.

Written and committed at H4 **before anything under it was computed.** That ordering is the
only discipline available to a post hoc specification and it is not a substitute for
pre-registration.

---

## 1. Why v1's boundary has to be replaced

`SPECIFICATION.md` §6 defines the boundary as the growth factor at which the share of debt
owed by households with reduced capacity **returns to its baseline value, which is zero**.
Requiring *every* affected household to be made whole makes the statistic a **maximum over
households**:

    g*(s) = max over affected indebted households i of [ income_i / net_income_i − 1 ]

**It is therefore set by one observation.** The v1 run showed what that does. At the primary
cell the boundary runs 0.051, 0.107, 0.320, 0.942, 2.678, **57.13**, **7.9 × 10¹⁵** across
the s grid. The last two values are a single household whose post-shift income approaches
zero, not a statement about the household sector. The κ = 1.0 column stays finite throughout,
which confirms the divergence is a property of the definition rather than of the economy.

It also failed the pre-registered 2019 stability check at every s, by 50 to 65 percent — which
is what a maximum does when the tail of a joint distribution differs between waves.

**v1's boundary is not wrong. It answers a question nobody asked**: how much growth would be
needed so that not one indebted household anywhere is worse off. V2 asks the question the
exercise was for.

---

## 2. The v2 object

For each household *i* whose capacity falls, define its **own restoring growth rate**:

    g_i = income_i / (income_i − Δ_i + Γ_i) − 1

the growth that returns household *i* alone to its pre-shift income. Households whose
capacity does not fall have no restoring rate and are excluded.

**The reported object is the DEBT-WEIGHTED distribution of g_i across affected households**,
weighted by each household's total debt balance times its survey weight. Debt weighting, not
household weighting, because the question is about claims: a dollar of debt owed by a
household needing 40 percent growth is the thing at risk, not the household count.

**Reported statistics, fixed here:**

| Statistic | Definition |
|---|---|
| **Median** | debt-weighted 50th percentile of g_i — **the headline** |
| **Quartiles** | debt-weighted 25th and 75th percentiles |
| **p90** | debt-weighted 90th percentile |
| **Restored at g = 0.05** | share of affected debt whose g_i ≤ 0.05 |
| **Restored at g = 0.10** | share of affected debt whose g_i ≤ 0.10 |
| **Restored at g = 0.20** | share of affected debt whose g_i ≤ 0.20 |

The three restored-shares are the inverse reading of the same distribution and are reported
because they are the form a reader can act on: *at 10 percent growth, this much of the
affected debt is back where it started.*

**v1's maximum is reported alongside as the p100 of the same distribution**, so the two
versions sit on one scale and the reader can see exactly what the maximum was doing.

---

## 3. What is NOT changed

Everything else is v1, unaltered:

- **The shift and its grids.** s ∈ {0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25}; growth enters
  only through g_i, which is continuous and needs no grid, so the **censoring problem of v1
  disappears** — g_i is always defined for an affected household with positive net income.
- **The three wage-loss allocations**: proportional, concentrated at R = 0.568316 under the
  nine exposure-and-pay cases, quintile (carrying the D5 renormalisation).
- **The three ownership definitions**: direct, direct + business, all routes.
- **The two bases and three κ values**: cash-flow (κ = 0.27), accrual (κ = 0.52),
  counterfactual (κ = 1.00). D3 stands — the bases collapse onto each other and that is
  reported again.
- **The primary cell**: concentrated / all routes / cash-flow / κ = 0.27.
- **The arrangements** of §7: capital-tax transfer at 0.086 and the required band 0.110–0.137;
  universal fund at ω ∈ {0.01, 0.02, 0.05, 0.10}; broadened retirement ownership, liquid and
  illiquid.
- **The plausibility bounds** of §9 and the corrections D1, D4, D5, D6 that the bounds forced.
- **Five implicates by Rubin's rules; 999 replicate weights.**
- **Status vocabulary**: measured distributions, scenario arithmetic.

**No new case, threshold, arrangement, ownership definition or sensitivity is introduced.**
V2 changes one thing: how the boundary is summarised.

---

## 4. Stability criterion, stated before the run

**Same as v1: 25 percent.** Applied to the **median and both quartiles**, each separately.

A statistic is **unstable** if its 2019 value differs from its 2022 value by more than
25 percent, or changes sign. The check is reported **first**, before the distribution, as in
v1.

**Pre-stated expectation, recorded so it cannot be claimed afterwards:** the median should be
considerably more stable than v1's maximum, because a median is not set by the tail. **If the
median also fails at 25 percent, v2 has not fixed anything and the redefinition should be
abandoned rather than reported.** That is the honest test of whether this redefinition was
worth making.

---

## 5. What would count as an uninteresting result

Stated before computing, as in v1 §10.

**5.1 The median is at or near zero.** If the debt-weighted median restoring rate is
negligible — say under 1 percent growth — then the affected debt is affected only trivially
and there is nothing to report beyond that fact.

**5.2 The distribution is degenerate.** If the interquartile range is a small fraction of the
median, the distribution adds nothing over a point estimate and v2's apparatus is
unnecessary; the honest report is that a single number would have done.

**5.3 The median is driven by convention as much as by s.** The v1 §10 test returned *No* by
0.007, which was uncomfortably narrow. **The same comparison is repeated on the median**: if
the spread of the median across conventions (cash-flow vs accrual, and across κ) exceeds its
spread across the whole s grid, then the redefinition has inherited v1's problem and it is
reported in v1's pre-committed words.

**5.4 The median fails the stability check.** See §4: this voids the redefinition.

---

## 6. Deviations discipline

Identical to v1. Any departure from this document is logged in `DEVIATIONS.md` under a **V2**
heading, with its reason and whether it was decided before or after a v2 result was seen.
The v1 deviations D1 to D7 continue to apply unchanged.

**One standing instruction:** because v2 is post hoc, any result that flatters the exercise
relative to v1 is to be reported with the fact that the definition was changed after seeing
v1 stated in the same sentence. The improvement may be real; it is not evidence, because the
definition was chosen with knowledge of what it would fix.
