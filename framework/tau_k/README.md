# tau_k on AI surplus, rebuilt from components

`definitions.md` first (what each published rate already contains), then `components.py`
(the components and their verification status), then `labor_component.py` (item 2(g)), then
`assemble.py` (assembly, variance decomposition, map), then `base_argument.md` (which base,
and the case against ours).

Rebuild: `python components.py && python labor_component.py && python assemble.py`. Figure at
`paper/figures/tau_k_map.png`. The A115 source extraction, with tables and page references,
is in `notes/sources/SHAREHOLDER_PARAMS_extracted.md`.

## Gate report, A118. THESIS-WEAKENING FIRST.

**1. The strongest robustness statement this module makes is SENSITIVE to the base of theta,
and it does not survive CRS's base.** A116 said there is "no corner of the space left in
which it closes" against the harder labour-tax reading. That is true at our theta, where the
ANALYTIC maximum under Barkai is **0.1236** against a required 0.1373. It is **false** at the
taxable share CRS R47113 itself implies, 25/(25+30) = **0.4545**, where the analytic maximum
is **0.1506** and clears the harder threshold, and the pass share against the easier reading
rises from **0.0013 to 0.2832**. The centre still fails under both rent readings (Barkai
0.1024 against 0.1101; Karabarbounis and Neiman 0.0322) and the condition still fails
everywhere under Karabarbounis and Neiman. But **"nowhere in the parameter space" is now a
statement that must carry the base of theta in the same sentence.** Full run in
`tau_k_crs_theta_sensitivity.csv`; the base argument is in
`notes/sources/SHAREHOLDER_PARAMS_extracted.md` section 3.

**2. Our own published cross-check was wrong, and our construction failed it.** B6.2 of the
addendum required the shareholder layer to land in CRS Table 5's published 0.045 to 0.085.
Our layer is 0.0386 and cannot reach 0.085 anywhere in the swept space, because that CRS row
has already had CRS's own taxable-share adjustment applied at 0.4545 over a foreign-excluded
base while we substitute 0.24 to 0.28 over a foreign-inclusive one. The check is corrected to
the rescaled band **0.0267 to 0.0505**, which the construction passes, plus the "around 3
percent" text figure against 0.0315, which it also passes. **The claim that the construction
"reproduces the published figure" is WITHDRAWN** wherever it referred to the Table 5 band.

**3. The Barkai central moves from 0.0864 to 0.0851.** Through A117 the code took the
shifted share's RANGE MIDPOINT, 0.45, while B3 of the brief said "centred on 0.48" and cited
Torslov, Wier and Zucman for it. The text is right: the sweep is uncertainty around one
measured value, not a flat interval. The code is corrected. Nothing downstream moves - the
percentiles, pass shares and threshold conclusions are untouched, and under Karabarbounis and
Neiman sigma = 0 kills the term entirely.

**4. The reported maximum is now ANALYTIC, not a sample extreme.** The assembly is multilinear
in all seven parameters, so its supremum and infimum sit at corners of the box. Evaluating all
128 gives **0.0563 to 0.1236** under Barkai and **-0.0063 to 0.0403** under Karabarbounis and
Neiman. The 200,000-draw sample gave 0.0593 to 0.1166, low by 0.007 at the top; a sample
maximum from a 7-dimensional box has no stable value across seeds and should never have been
the reported figure.

### Round-three replication, 2026-09-20

An instance that did not write the code rebuilt both constructions from the addendum alone.
**All 32 sealed quantities matched**, 30 within rounding and 2 within tolerance, both
explained. The four items above are what that round found; every one is an error on this
project's side, not the replicator's. Comparison in
`notes/replication/round3/comparison_round3.md`.

---

## Gate report, A116

### Plausibility violations

**None.** Every component range sits inside its ceiling; every share is in [0, 1]; the
assembled rate lies between the lowest and highest component-consistent values under both
rent readings; the assembled maximum is below the ceiling on a fully domestic, fully
distributed, fully taxable, all-equity dollar.

**Two published-figure checks. AMENDED A118: the first passed only on one of its two legs
and its band was wrongly scoped. See the A118 gate report above.**

1. The shareholder layer at the sourced centrals is `0.27 x 0.238 x 0.601 = 0.0386`.
   **CORROBORATED** against CRS R47113's text figure of about 3 percent (0.0315).
   **NOT corroborated against Table 5's published 0.045 to 0.085 as printed** - that row is
   on CRS's foreign-excluded base at an implied taxable share of 0.4545, and 0.0386 cannot
   reach it. Rescaled to our theta the band is 0.0267 to 0.0505 and 0.0386 sits inside.
2. **New in A116, the sign test.** AMR debt-financed normal return is `tau_b - tau_c`. At the
   sourced bondholder range that is **-0.0667 to -0.0347**, and **CBO 2014 Table 2 measures
   the effective marginal rate on C-corporation debt-financed investment at -0.06**, which
   sits inside it. AMR predicted the sign, CBO measured the magnitude, and our assembly
   reproduces both from components.

### Thesis-weakening results, first

**1. The verdict does not change. It hardens, and it is now robust to every remaining
parameter** - subject, as of A118, to the base of theta, per item 1 of the A118 gate report.
Required 0.1101 to 0.1373. Under the Barkai rent reading the assembled rate at
the sourced centrals is **0.0851** (**0.0864** through A117, on the superseded shifted-share
midpoint), median 0.0851, 5th to 95th percentile **0.073 to 0.099**.
Under Karabarbounis and Neiman it is **0.0150**. The condition passes in **0.85 percent** of
the remaining space against the easier labour-tax reading and **in none of it** against the
harder one.

**2. Against the harder labour-tax reading the condition cannot pass anywhere in the
parameter space - AT OUR THETA.** The ANALYTIC maximum under Barkai, over all 128 corners of
the box, is **0.1236**, below the 0.1373 required. That is a stronger statement than a low
pass share: there is no corner of the space left in which it closes. **A118 qualifies it: at
the CRS-implied theta of 0.4545 the analytic maximum is 0.1506 and the statement fails.** It
must not be quoted without the base of theta attached.

**3. No single parameter can cross a threshold on its own any more.** In A113 four could; in
A115 one could, the bondholder rate; in A116 **none can**. The largest single swing left is
the debt share at 0.0213, against thresholds 0.024 and 0.051 away from the central.

**4. The bondholder rate was the last parameter capable of rescuing the condition, and
sourcing it removed that possibility.** The blind sweep put it at 0.15 to 0.37 with a
midpoint of 0.26. The sourced range is **0.143 to 0.175**, whose entire mass sits at or below
the old lower bound. Correcting it costs **0.0131** on the assembled rate and collapses that
parameter own swing from 0.0286 to **0.0042**.

**5. The reason is the one that governed the shareholder layer: most of the instrument is
outside the individual income tax.** CBO 2014 Table A-3 puts **32.8 percent of C corporation
debt in nontaxable accounts and 14.9 percent temporarily deferred**, leaving 52.3 fully
taxable, and Table A-4 puts the marginal rate on interest for those holders at **27.4
percent**, well below the 43.4 top statutory rate. The Fed 2026Q2 holder map corroborates the
direction: **the rest of the world holds 28.7 percent** of corporate and foreign bonds and
**households and nonprofits hold 1.1 percent directly**, with nonprofits alone accounting for
all of that, so taxable household exposure is almost entirely indirect through mutual funds
and life insurance, which is exactly what CBO looks through.

**6. Cumulatively, sourcing has moved the rate by 0.0314.** A113 all-blind midpoints gave
0.1178, inside the required band. A116 all-sourced centrals give **0.0864**, clearly below
it. All three corrections pushed the same way. **None of that came from new modelling; it
came from looking up parameters that were already published.**

**7. The variance decomposition has been reshaped again, and again it must be read alongside
the level.** Remaining first-order indices under Barkai: **debt share 0.369, deferral factor
0.195, state corporate rate 0.162, shifted share 0.127, shareholder rate 0.102, bondholder
rate 0.014, taxable-shareholder share 0.012**. The bondholder rate fell from 0.442 to 0.014
**because it is now pinned**, not because it stopped mattering: it is the second largest
mover of the level in this pass. The largest remaining uncertainty is the **debt share of AI
capital spending**, which is unsourced.

**8. Profit shifting is now fifth by variance and fourth by swing.** It has been overtaken by
three parameters that our published construction did not contain at all.

### Sourced, kept separate from scenario

**Verified, eight components.** Federal corporate rate 0.21 (26 USC 11(b)); 26 USC 250(a)(1)
as amended by Pub. L. 119-21 of 4 July 2025, giving **14.0 and 12.6 percent** effective, with
26 USC 951A recaptioned from GILTI to "net CFC tested income" and the pre-2025 13.125 and
10.5 superseded; the shifted share 0.48 (Torslov, Wier and Zucman, one source only, so still
swept); the two rent readings, Barkai 0.351 and Karabarbounis and Neiman at approximately
zero, **never averaged**; the AMR expensing algebra; and, **new in A115**, the
**taxable-shareholder share 0.24 to 0.28, central 0.27** (Rosenthal and Austin 2016 Table 2;
Rosenthal and Burke 2020; Rosenthal and Mucciolo 2024 Tables 5 and 7) and the **deferral
factor 0.412 to 0.790, central 0.601** (CRS R47113 Table 5, cross-checked at 0.488 from CBO
2014 Tables A-3 and A-4); and, **new in A116**, the **bondholder rate 0.143 to 0.175, central
0.159** (CBO 2014 Table A-3 for the 52.3 percent fully taxable share of C corporation debt,
Table A-4 for the 27.4 percent marginal rate on interest, corroborated by a Fed Z.1 holder
map at 2026Q2 and cross-checked against CBO Table 2 measured -6 percent).

**Scenario, swept, no point asserted, four components:** shareholder rate, state effective
corporate rate, **debt share** and shifted share, plus the two capex parameters of item 2(g),
which affect nothing in the assembly. All are in `lit/unverified.md`.

**One measure deliberately not used.** CBO 2014 Table A-3 reports 57.2 percent of C
corporation equity as "fully taxable". That is the distribution of the **marginal dollar of
saving by tax status in 2007**, not the holder share of the outstanding **stock**. The two
answer different questions and are **not averaged**; our construction needs the holder share.

### Pillar Two

Unchanged from A113: **NOT VERIFIED** (OECD returned HTTP 403), used nowhere, present only as
a marked line at 0.15 with its status printed. The conditional arithmetic still holds and is
now more relevant, not less: 0.15 exceeds the required 0.1101 to 0.1373, and the assembled
rate does not, so a binding 15 percent floor is one of the few things in this analysis that
would close the condition on the rent component. Whether it binds is the unverified part.

### What would close this

Nothing in the parameter space now closes the condition against the harder labour-tax
reading. The largest remaining uncertainty is the **debt share of AI capital spending** at
0.369 of the variance, and Module B reading of the nine filers own books is that the
financing is predominantly equity, which is the low end of its range and the **unfavourable**
end for the condition. Sourcing it would most likely harden the verdict, not soften it.

The live question is therefore no longer a parameter. It is the **base**: whether a marginal
flow rate is the right object at all, against an average rate on the existing stock. That
argument is in `base_argument.md` and nothing here settles it.
