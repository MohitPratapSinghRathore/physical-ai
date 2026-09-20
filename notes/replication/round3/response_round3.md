# Response to round three, A118

Round three rebuilt both constructions of `notes/replication_brief_v2_2_addendum.md` from the
brief and raw data alone and matched **all 32 sealed quantities** — 30 within rounding, 2
within the stated tolerance with the cause of each identified exactly. This is the response:
what was changed, where, and what it costs.

**Every finding below is an error on this project's side.** The replicator's arithmetic was
right in all four.

---

## THESIS-WEAKENING FIRST

### 1. The robustness half of the capital-tax verdict is conditional on the base of theta

This is the substantive item and it is the one that costs us something.

**What CRS R47113 actually uses.** The report was read directly for this pass (the PDF host
returns 403 to automated fetches; the congress.gov and everycrsreport.com HTML mirrors do
not). Table 5's fourth row, "Adjusted for Share of Corporate Stock Held in Taxable Form
(55% reduction)", is the row whose outputs are 4.5 and 8.5 percent. A 55 percent reduction is
a multiplier of 0.45, and CRS gives the arithmetic in its own text: the row adjusts for "the
25% share of corporate stock held by taxable individuals compared with the 30% share from
exempt shareholders". **25 / (25 + 30) = 0.4545.** Its source note cites Rosenthal and Theo
Burke, *Who's Left to Tax? US Taxation of Corporations and Their Shareholders*, NYU Tax Policy
Colloquium, 27 October 2020, for "of total equity in U.S. corporations, 25% are in taxable
accounts and 30% are in retirement assets"; the remaining roughly 45 percent is foreign-held
and, in CRS's words, not subject to tax.

**So the base is domestically held stock. The foreign slice is dropped from the denominator,
not carried as untaxed.**

**Does it measure the same object as Rosenthal and coauthors? Same numerator, different
denominator.** CRS's 25 percent *is* a Rosenthal figure, measured over total equity in US
corporations — the same base as Rosenthal and Mucciolo's 0.27 and within a point of it. The
Rosenthal family (Austin 2016: 0.242 on C corporation stock; Burke 2020: 0.25 on total equity;
Mucciolo 2024: 0.27 total, 0.28 publicly traded) is internally consistent, and CRS's numerator
belongs to it. What CRS then does, and Rosenthal does not, is renormalise onto the domestic
holder base.

| | numerator | denominator | value |
|---|---|---|---|
| Rosenthal family, and OUR theta | equity in taxable accounts | ALL US equity outstanding, foreign included | **0.24 to 0.28** |
| CRS R47113 Table 5, row 4 | the same | DOMESTICALLY held equity only | **0.4545** |

Neither is wrong. CRS's question is the rate faced by a US saver; ours is the rate on a dollar
of US AI surplus **whoever holds it**. For our object the foreign-inclusive base is right: a
foreign holder genuinely bears close to no US shareholder-level tax, and that dollar is still
part of the surplus the fiscal condition has to tax. **We keep our base. But the choice is now
visible and it is load-bearing.**

**(b) The assembly at the CRS-implied share, run as a marked sensitivity.**
`framework/tau_k/tau_k_crs_theta_sensitivity.csv`.

| | our theta, 0.24 to 0.28 | CRS-implied theta, 0.4545 |
|---|---|---|
| **Barkai central** | 0.0851 | **0.1024** |
| Barkai p05 to p95 | 0.0726 to 0.0993 | 0.0860 to 0.1231 |
| Barkai ANALYTIC min to max | 0.0563 to **0.1236** | 0.0666 to **0.1506** |
| pass share vs required 0.1101 | 0.0013 | **0.2832** |
| pass share vs required 0.1373 | 0.0000 | **0.0010** |
| **Karabarbounis-Neiman central** | 0.0150 | **0.0322** |
| Karabarbounis-Neiman pass share, either threshold | 0.0000 | 0.0000 |

**(c) The verdict IS sensitive, in one specific respect, and it is carried everywhere.**

- **What survives on either base.** The condition **fails at the centre under both rent
  readings** — 0.1024 is still below the easier 0.1101 — and fails **everywhere** in the space
  under Karabarbounis and Neiman. The headline verdict does not turn over.
- **What does not survive.** A116's stronger statement, that the analytic maximum is below the
  harder threshold so there is **no corner of the space** in which the condition closes, is
  true at our theta (0.1236 against 0.1373) and **false** at CRS's (0.1506). And the pass share
  against the easier labour-tax reading goes from under a tenth of a percent to **28 percent** —
  the difference between "arithmetically closed off" and "unlikely".

Carried into: claim **53f** in the register, **B9** of the addendum, the **A118 gate report**
in `framework/tau_k/README.md` (with the A116 gate report's items 1 and 2 amended in place),
the **dashboard** row and its generator, and a new limitation **L14**. The rule recorded with
the claim is that **"nowhere in the parameter space" must carry the base of theta in the same
sentence, wherever it appears.**

### 2. Our own check B6.2 was wrong, and our own construction failed it

B6.2 required `theta x 0.238 x deferral` to land in CRS Table 5's published **0.045 to
0.085**. Our shareholder layer is **0.0386** and across the entire swept space runs 0.0235 to
0.0526 — it cannot reach 0.085 at any point. The replicator identified the cause before
opening the seal and was right: that CRS row has already had the taxable-share adjustment
applied at 0.4545 on a foreign-excluded base, while we substitute 0.24 to 0.28 on a
foreign-inclusive one. Taking the deferral factor from row 3, *before* CRS's adjustment, is
correct as modelling and is exactly what makes the row-4 comparison invalid.

**Corrected, two tests replacing one.**

- **(a) The text figure, direct.** CRS p. 2: the overall effective capital gains tax rate on
  corporate profits is "around 3%". Our 0.0386 against **0.0315**, tested within 0.010.
  Passes. No rescaling needed — the text figure is stated on the whole of corporate profits.
- **(b) The Table 5 band, rescaled** by `theta / 0.4545`: **0.0267 to 0.0505** at theta = 0.27,
  and 0.0238 to 0.0524 across our theta range. 0.0386 is inside throughout. Passes.

**Withdrawn:** "Our construction reproduces the published figure" in
`data/raw/manual/SHAREHOLDER_PARAMS_extracted.md`, and "Two published-figure checks, both
passed" in the A116 gate report. Both were true of the text figure and false of the Table 5
band, and should never have been asserted of both at once. The word "reproduces" is gone from
every passage that referred to the band.

Both tests now run in code, in `assemble.py`, and both are in the plausibility list.

---

## Housekeeping

### 3. The shifted share's central: the TEXT is right, the code is corrected

B3 said "0.30 to 0.60, **centred on 0.48**" and cited Torslov, Wier and Zucman for the 0.48.
The generating code took the range **midpoint, 0.45**. They disagreed and the sealed file
carried the code's value.

**The text is right.** The sweep is uncertainty around one measured value — a second source
was sought and not obtained, which is why it is swept at all — not a flat interval whose
midpoint means anything. A range midpoint is an artefact of how the bounds were drawn.

Effect: the Barkai central falls **0.0864 to 0.0851**. Nothing else moves: the percentiles,
pass shares and threshold conclusions are untouched, and under Karabarbounis and Neiman
sigma = 0 kills the shifted term entirely, which is why the sealed file shows 0.015 either way.

### 4. The maximum is now analytic, not a sample extreme

The assembly is **multilinear** in all seven parameters, so its supremum and infimum over the
box sit at corners. `corner_extremes()` evaluates all 2^7 = 128.

| reading | analytic | 200,000-draw sample |
|---|---|---|
| Barkai | **0.0563 to 0.1236** | 0.0593 to 0.1166 |
| Karabarbounis-Neiman | **-0.0063 to 0.0403** | -0.0048 to 0.0385 |

The sample maximum was low by 0.007 at the top and has no stable value across seeds. Every
"no corner closes it" statement is now made against the analytic figure. The lower tail is much
less dispersed, which is why the minima agreed closely.

### 5. The Treasury labour share: the number is right, the band quoted against it was not

A6 said the Treasury backing share "runs 0.6339 to 0.6528. We publish the lower end", while
the A3 class table and every sealed value use **0.657788** — above the top of that band. The
replicator correctly established from the sealed ratios that 0.657788 is the production value.

**The band was the wrong one, not the number.** Two distinct quantities in
`framework/labor_backing/capital_gains_bound.json`:

| quantity | 2023 band | |
|---|---|---|
| labour-linked share of federal **receipts** | **0.6339 to 0.6528** | the INPUT |
| **Treasury class backing** | **0.657788 to 0.678331** | the OUTPUT, downstream of it |

"We publish the lower end" was always true — of the **second** band. A6 quoted the first.
Corrected by giving both with their scope. This is the replicator's option 1, "the band is
differently scoped", which was also their guess.

**Effect of moving to the upper end**, stated because it is small:

| | lower, 0.657788 | upper, 0.678331 | relative |
|---|---|---|---|
| 2025 debt-only direct ratio | 0.5216 | 0.5306 | +1.73 pct |
| 2025 all-claims direct ratio | 0.270271 | 0.274931 | +1.72 pct |
| sovereign union share | 0.793592 | 0.797089 | +0.44 pct |

**No conclusion moves.**

### 6. The indirect labour share is now stated, not inferrable

**0.338212** for 2025, the product of consumption's share of final demand **0.681191** and
labour's share of personal income **0.496502**, a per-year series. Added to A3 and A4. The
replicator back-solved 0.339556 from the brief's rounded "about 76 percent" and was high by
0.4 percent — entirely downstream of our omission. This was the single blocking gap in Part A.

A2 now also states what the replicator had to infer and inferred correctly: **`corporate_equity`
carries the indirect share in the all-claims numerator** while being dropped from the
debt-only construction entirely. The business-revenue-serviced set is five classes, not four.

### 7. The coefficients of variation use the sample standard deviation

`ddof = 1`. The sealed values pin it down (0.050627 and 0.094174 against 0.0506 and 0.0942);
the population convention gives 0.050283 and 0.093536, which clears the tolerance but is the
wrong choice. Now stated in A6.

---

## What was NOT changed

- **Our theta stays 0.24 to 0.28.** The base argument is made, not conceded; the CRS base runs
  as a marked sensitivity and nothing in the assembly uses it as a central value.
- **The deferral factor stays 0.412 / 0.601 / 0.790.** It comes from Table 5 **row 3**, before
  CRS's taxable-share adjustment, which is unaffected by any of this and is precisely why that
  row was chosen.
- **No sealed value was edited.** `notes/sealed/sealed_addendum_v2_2.json` is the record of
  what the code produced at A117 and stays as it is; the two quantities that moved (the Barkai
  central and the maximum) moved because the code was corrected afterwards, and the correction
  is documented rather than backfilled.
- **The replicator's two prior-bound misses** — CV(all-claims) and the Barkai p05–p95 width —
  were theirs and are not defects in the brief.
