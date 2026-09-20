# tau_k on AI surplus, rebuilt from components

`definitions.md` first (what each published rate already contains), then `components.py`
(the components and their verification status), then `labor_component.py` (item 2(g)), then
`assemble.py` (assembly, variance decomposition, map), then `base_argument.md` (which base,
and the case against ours).

Rebuild: `python components.py && python labor_component.py && python assemble.py`. Figure at
`paper/figures/tau_k_map.png`. The A115 source extraction, with tables and page references,
is in `data/raw/manual/SHAREHOLDER_PARAMS_extracted.md`.

## Gate report, A115

### Plausibility violations

**None.** Every component range sits inside its named statutory or structural ceiling; every
share is in [0, 1]; the assembled rate lies between the lowest and highest
component-consistent values under both rent readings; the assembled maximum is below the
ceiling on a fully domestic, fully distributed, fully taxable, all-equity dollar. The one
negative value, a minimum of -0.0121 under the Karabarbounis and Neiman reading, is AMR's own
debt-financing result, `tau_b - tau_c`, which is negative when bondholders are taxed below
the corporation.

**One new check, and it is the one that matters.** The assembled shareholder layer at the
sourced central values is `0.27 x 0.238 x 0.601 = 0.0386`. CRS R47113 Table 5 publishes
**0.045** for no-dividend stock and **0.085** for dividend stock after the same adjustments,
and its summary text puts the overall effective capital gains rate on corporate profits at
**"around 3 percent"**. **Our construction reproduces the published figure**, which is the
test a rebuilt component has to pass and which the blind sweep could not have passed or
failed.

### Thesis-weakening results, first

**1. Sourcing the two parameters moves the verdict, and it moves it toward FAILING.** The
required rate is 0.1101 to 0.1373. Under the Barkai rent reading the assembled rate at the
**sourced central values is 0.0994, which is BELOW the requirement**, and the 5th to 95th
percentile span is **0.079 to 0.120**. The condition passes in **17.6 percent** of the
remaining space against the easier labour-tax reading and **0.13 percent** against the harder
one. Under Karabarbounis and Neiman the central is **0.0352** and it passes nowhere.

**2. The A113 verdict of "cannot be called" does not stand. It tightens, and it resolves
against the thesis-friendly reading.** A113's blind sweep gave a Barkai median of 0.1159,
inside the required band, passing in 61 percent of the space. Sourcing the two parameters
moves the median down by **0.018** and the pass rate from **61 percent to 18 percent**. The
honest statement is no longer "it straddles". It is **"it fails at the central value under
both rent readings, and passes only in the corner of the space where the bondholder rate is
at its ceiling."**

**3. Both corrections pushed the same way, and the holder share did most of it.** Holding
everything else at midpoints, correcting the taxable-shareholder share from the blind
midpoint of 0.40 to the sourced 0.27 costs **0.0142**; correcting the deferral factor from
0.70 to 0.601 costs a further **0.0062**; together **0.0183**. **Who holds the equity is the
larger of the two**, and it moved the rate down because the published share is near the
bottom of what we had been sweeping.

**4. The reason is that most US corporate equity is outside the shareholder tax base
entirely.** Rosenthal and Mucciolo put 2022 holdings at **42 percent foreign** and **25
percent in retirement accounts** (IRAs 11, defined benefit 7, defined contribution 7), with
nonprofits 4, life insurance separate accounts 2 and government 1, leaving **27 percent
taxable**, down from 79 percent in 1965. A shareholder-level tax reaches roughly a quarter of
the equity it appears to apply to.

**5. And roughly half of the gains on that quarter are never taxed.** CBO 2014 has **46.9
percent of capital gains held until the owner's death** and therefore untaxed through step-up
in basis; CRS applies a 50 percent reduction for the same reason. Two separate datasets, one
conclusion.

**6. The variance decomposition has been reshaped, and it must not be misread.** The
remaining first-order indices under Barkai are **bondholder rate 0.442, deferral factor
0.127, state corporate rate 0.105, shifted share 0.085, shareholder rate 0.064, debt share
0.013, taxable-shareholder share 0.007**. The taxable-shareholder share now carries almost
none of the *variance* **because it has been pinned to a four-point range**, not because it
does not matter: it is simultaneously the **largest single mover of the level** (finding 3)
and the **smallest remaining source of uncertainty**. Those are different questions and this
report answers both.

**7. Only one parameter can still cross a threshold on its own**, and it is the bondholder
rate, which moves the rate from 0.0852 to 0.1137 across its range. It is unsourced. That is
now the single highest-value item left.

**8. Profit shifting still is not the story.** It carries 0.085 of the variance and moves the
rate by 0.0124 across a range from 0.30 to 0.60, against 0.0183 from the two shareholder
parameters combined.

### Sourced, kept separate from scenario

**Verified, seven components.** Federal corporate rate 0.21 (26 USC 11(b)); 26 USC 250(a)(1)
as amended by Pub. L. 119-21 of 4 July 2025, giving **14.0 and 12.6 percent** effective, with
26 USC 951A recaptioned from GILTI to "net CFC tested income" and the pre-2025 13.125 and
10.5 superseded; the shifted share 0.48 (Torslov, Wier and Zucman, one source only, so still
swept); the two rent readings, Barkai 0.351 and Karabarbounis and Neiman at approximately
zero, **never averaged**; the AMR expensing algebra; and, **new in A115**, the
**taxable-shareholder share 0.24 to 0.28, central 0.27** (Rosenthal and Austin 2016 Table 2;
Rosenthal and Burke 2020; Rosenthal and Mucciolo 2024 Tables 5 and 7) and the **deferral
factor 0.412 to 0.790, central 0.601** (CRS R47113 Table 5, cross-checked at 0.488 from CBO
2014 Tables A-3 and A-4).

**Scenario, swept, no point asserted, five components:** shareholder rate, state effective
corporate rate, debt share, bondholder rate, shifted share, plus the two capex parameters of
item 2(g), which affect nothing in the assembly. All are in `lit/unverified.md`.

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

The **bondholder rate**, alone, carries 44 percent of the remaining variance and is the only
parameter that can still cross a threshold by itself. It is the next hour of sourcing.
