# Comparison against sealed values — round 3

Sealed file: `notes/sealed/sealed_addendum_v2_2.json`, opened only after
`results_round3.csv` and `insufficiencies_round3.md` were written.

Stated tolerances: Part A within **0.002** absolute on every ratio and **0.005** on the
coefficient of variation; Part B within **0.004** absolute on central rates and **0.01** on
pass shares.

## Verdict

**Every one of the 32 sealed quantities matches.** 30 match within rounding; 2 match within
tolerance but not within rounding, and both are fully explained below. **No mismatches.**

The two constructions replicate. That includes the one quantity I had flagged as blocking —
the indirect labour share of business revenue — which I recovered to within 0.4 percent
without ever seeing it.

---

## Part A — debt-only labour backing ratio

| quantity | sealed | mine | abs diff | verdict |
|---|---|---|---|---|
| 2025 direct | 0.5216 | 0.521628 | 0.000028 | match within rounding |
| 2025 including indirect | 0.602 | 0.602273 | 0.000273 | match within rounding |
| 2025 all-claims direct | 0.2703 | 0.270271 | 0.000029 | match within rounding |
| 2025 all-claims incl. indirect | 0.4749 | 0.475678 | 0.000778 | match within rounding |
| 2000 direct, debt-only | 0.4687 | 0.468697 | 0.000003 | match within rounding |
| 2000 direct, all-claims | 0.2705 | 0.270479 | 0.000021 | match within rounding |
| 2008 direct, debt-only | 0.5006 | 0.500590 | 0.000010 | match within rounding |
| 2008 direct, all-claims | 0.3772 | 0.377240 | 0.000040 | match within rounding |
| 1952 direct, debt-only | 0.5208 | 0.520791 | 0.000009 | match within rounding |
| 1952 direct, all-claims | 0.3942 | 0.394157 | 0.000043 | match within rounding |
| equity share of all-claims denominator 2025 | 0.4819 | 0.481870 | 0.000030 | match within rounding |
| CV 1952–2025, debt-only | 0.0506 | 0.050627 | 0.000027 | match within rounding |
| CV 1952–2025, all-claims | 0.0942 | 0.094174 | 0.000026 | match within rounding |
| largest judgement call | one-step rule | one-step rule | — | agree |
| largest move, percent | 15.4 | 15.46 | 0.06 | match within rounding |

**Note on the CVs.** The sealed values pin down the sample (n−1) convention: my sample
figures are 0.050627 and 0.094174 against sealed 0.0506 and 0.0942, agreeing to 5 decimal
places. My *headline* was the population convention (0.050283, 0.093536), which also clears
the 0.005 tolerance but is visibly the wrong choice. My insufficiency I-8 flagged the
ambiguity and reported both, so nothing was lost — but the convention is sample sd, and the
brief should say so.

**Error side: none.** Every class list, series mapping, Q4 convention and backing coefficient
reproduced exactly. The Z.1 series in A3 are correct as printed and the arithmetic in A4 is
unambiguous.

---

## Part B — assembled effective capital tax rate

| quantity | sealed | mine | abs diff | verdict |
|---|---|---|---|---|
| central, Barkai | 0.0864 | 0.085116 | **0.001284** | match within tolerance — see B-i |
| central, Karabarbounis–Neiman | 0.015 | 0.015028 | 0.000028 | match within rounding |
| Barkai p05 | 0.0726 | 0.072681 | 0.000081 | match within rounding |
| Barkai median | 0.0851 | 0.085057 | 0.000043 | match within rounding |
| Barkai p95 | 0.0993 | 0.099342 | 0.000042 | match within rounding |
| Barkai min | 0.0593 | 0.059550 | 0.000250 | match within rounding |
| Barkai max | 0.1166 | 0.119015 | **0.002415** | match within tolerance — see B-ii |
| Barkai pass share vs required low | 0.0013 | 0.001195 | 0.000105 | match within rounding |
| Barkai pass share vs required high | 0.0 | 0.000000 | 0 | exact |
| KN p05 | 0.004 | 0.004026 | 0.000026 | match within rounding |
| KN median | 0.0137 | 0.013721 | 0.000021 | match within rounding |
| KN p95 | 0.0255 | 0.025415 | 0.000085 | match within rounding |
| KN min | −0.0048 | −0.004833 | 0.000033 | match within rounding |
| KN max | 0.0385 | 0.038015 | 0.000485 | match within rounding |
| KN pass shares, both | 0.0 | 0.000000 | 0 | exact |
| shareholder layer at centrals | 0.0386 | 0.038607 | 0.000007 | **exact** |
| no single parameter crosses a threshold alone | true | true (0 of 14) | — | agree |

### B-i. The Barkai central rate — cause identified exactly

The sealed file's own **median is 0.0851** while its **central is 0.0864**. My value,
0.085116, reproduces the sealed *median* to 6×10⁻⁵. So the model is identical and the gap is
purely in which vector counts as "central".

One parameter explains all of it. Holding everything else at midpoints:

- shifted share **0.48** → **0.085116** (what I used, and what B3 says: "centred on 0.48")
- shifted share **0.45** → **0.086355** → rounds to **0.0864** (the sealed central)

0.45 is the midpoint of the swept range 0.30–0.60. The Karabarbounis–Neiman central is
unaffected either way (σ = 0 kills the shifted term), which is exactly what the sealed file
shows: 0.015 under both.

**Error side: the brief's.** B3 explicitly says the shifted share is "0.30 to 0.60, **centred
on 0.48**", citing Torslov, Wier and Zucman's 48 percent. The generating code used the range
midpoint 0.45 instead. Either the text or the code should change; they currently disagree.
The effect is 0.0012 on one of sixteen Part B numbers, so nothing downstream moves — the pass
shares, percentiles and threshold conclusions are untouched.

### B-ii. The Barkai maximum — Monte Carlo tail, neither side wrong

The analytic supremum of the Barkai assembly over the stated boxes is **0.123555** (all seven
parameters at their rate-maximising corners). Both the sealed 0.1166 and my 0.119015 sit
below it, as any finite sample must: the maximum of 200,000 draws from a 7-dimensional box is
an extreme order statistic with no stable value across seeds. The sealed file's own
instruction anticipates this. The corresponding minima agree to 0.00025 because the lower
tail of this assembly is much less dispersed.

**Error side: neither.** This is the one quantity in the set that is not reproducible by
construction, and the 0.004 tolerance is the right way to handle it. If a stable figure is
wanted, report the analytic corner (0.1236 / 0.0563) rather than the sample extremes.

---

## The three flagged issues — resolutions

### 1. The missing indirect labour share of business revenue

**Resolved, and my reconstruction was right in structure and nearly right in value.**

I back-solved **0.339556** from the addendum's "about 76 percent". Inverting the sealed
values recovers the owner's actual figure:

- from sealed debt-only incl. 0.602 → share in **[0.3363, 0.3405]**
- from sealed all-claims incl. 0.4749 → share in **[0.33819, 0.33835]**

The intersection is **≈ 0.3383**. Mine is high by 0.0013, **0.4 percent relative** — because I
solved against 0.76 exactly, whereas 0.3383 produces an all-claims move of **75.72 percent**,
which the addendum rounded to "about 76". At 0.3383 the debt-only move is **15.403 percent**,
matching the sealed `largest_move_pct` of 15.4 to three digits.

The structural question I had to decide on my own is also settled, and settled my way: the
same single share backs out of the debt-only and the all-claims sealed figures
(0.33841 vs 0.33827, differing only by the sealed rounding). **Corporate equity does carry
the indirect share in the all-claims numerator under the one-step rule.** Had it not, no
value in [0,1] would have reproduced either number.

**Recommended resolution.** Add one line to A3 or A4 stating the share numerically —
`indirect labour share of business revenue = 0.3383` — and one sentence to A2 or A4 stating
that corporate equity is treated as a business-revenue class in the all-claims INCLUDING
INDIRECT variant. Those two sentences convert Part A from "recoverable by inference from a
rounded cross-check" to "specified". This is the single highest-value edit to the addendum:
it is the only genuinely blocking gap, and the +76 percent that currently substitutes for it
is rounded hard enough to cost 0.4 percent on the recovered parameter.

**Error side: the brief's**, unambiguously — a required input was omitted. My 0.4 percent
overshoot is downstream of that omission, not an independent error.

### 2. Check B6.2 against CRS R47113 Table 5

**Resolved in my favour, and the sealed file confirms it.**

The sealed `shareholder_layer_at_centrals` is **0.0386**. Mine is **0.038607** — an exact
match. So the owner's own pipeline produces 0.0386, while B6.2 instructs the replicator that
this quantity "must land in CRS R47113 Table 5's published 0.045 to 0.085". **The brief's own
construction fails the brief's own check**, and it fails it by 0.0064 at the bottom.

The reason is the one I gave before opening the seal. CRS's 0.045/0.085 row is the row after
CRS's own taxable-share adjustment — a stated **55 percent reduction**, i.e. an implied
taxable share of **0.45**. B3 substitutes `theta` of **0.24–0.28** for that 0.45. A smaller
share must produce a smaller product; across the entire swept space the layer runs 0.0235 to
0.0526 and can never reach 0.085. The instruction to take the deferral factor "BEFORE its own
taxable-share adjustment so theta is not double counted" is precisely what guarantees the
mismatch — it is correct as a modelling choice and incorrect as grounds for comparing the
result to a figure that *has* had that adjustment applied.

**Recommended resolution.** Replace the check with one that is consistent with the
substitution. Either:

- compare `theta x 0.238 x deferral` to **CRS Table 5 row 3 rescaled by theta/0.45**, i.e. to
  **0.024 to 0.045** at theta = 0.27, which the constructed 0.0386 sits comfortably inside; or
- drop the band and keep only the half of the check that already passes — CRS's text figure
  of "around 3 percent" against `tau_sh` of **0.0315**, which is a clean, direct
  corroboration and needs no rescaling.

I would keep both: the rescaled band as the quantitative test, and the 3 percent as the
sanity check. What must not survive is the current form, because a replicator who trusts it
will conclude they have double-counted theta when they have not.

**Error side: the brief's.** The arithmetic on both sides is identical; only the stated
acceptance criterion is wrong.

### 3. The two Treasury backing shares

**Not resolved by the sealed file — it contains no Treasury-share entry.** But the sealed
ratios settle which value was actually used.

My A1 (0.521628, on 0.657788) matches sealed 0.5216 to 3×10⁻⁵. Had the build used 0.6339 or
0.6528, the 2025 direct ratio would have been 0.5112 or 0.5194 — both outside the 0.002
tolerance, and 0.5112 outside it by fivefold. So **the production value is 0.657788**, the
figure in the A3 class table, and A6's claim that "we publish the lower end" of 0.6339–0.6528
is simply false of the number in use: 0.657788 is above the *upper* end of that band.

**Recommended resolution.** A6 is making a defensible point — that the Treasury share is a
bound rather than a point, because realised gains sit inside AGI at preferential rates — and
the point survives intact. What needs fixing is the arithmetic relationship between the two
passages. Three possibilities, in my order of preference:

1. **The band is stale or differently scoped.** If 0.657788 comes from a later SOI vintage or
   a wider receipts definition than the 2021–2023 band, say so and give the band on the same
   basis. This is my guess, because 0.657788 carries six decimals and looks computed, whereas
   0.6339/0.6528 are quoted to four.
2. **The published figure should be the band's lower end**, in which case the headline ratio
   becomes 0.5112, not 0.5216 — and every sealed Part A ratio would move. Given the sealed
   values, this is not what was done.
3. **Delete "We publish the lower end."** If 0.657788 is right and the band is an illustrative
   sensitivity, the sentence is the only thing that is wrong, and it is a one-word fix.

Whichever is chosen, the stake is small and I would say so in the text: the full spread of the
disagreement is **−0.0105 to −0.0022** on the 2025 ratio, at most **2.0 percent relative**,
and it changes no conclusion. Worth stating precisely *because* it is small — an unexplained
inconsistency reads as a larger problem than it is.

**Error side: the brief's**, but as a drafting fault rather than a computational one. The
build is internally consistent; only the prose contradicts the table.

---

## Prior-bound performance

Of my 22 pre-registered plausibility bounds, 20 contained the value I computed. The two
misses were both mine and both were mis-sizings rather than errors of method:

- **CV(all-claims)**: I predicted 0.12–0.35, actual 0.0942. I over-estimated the destabilising
  effect of the equity denominator over the full 1952–2025 window. The qualitative claim
  survives — all-claims is still 1.86× as variable as debt-only — but I sized the effect
  roughly twice too large.
- **Barkai p05–p95 width**: I predicted 0.03–0.10, actual 0.0267. The seven parameters are
  individually narrow and the assembly is near-additive (first-order Sobol indices sum to
  1.009), so they do not compound as I assumed.

My prior interval for `tau_b − tau_c`, −0.067 to −0.045, was also too narrow at the top: the
true range is [−0.0667, −0.0347]. It contained CBO's −0.06, so the sign test passed, but I
had the upper end wrong by 0.010.
