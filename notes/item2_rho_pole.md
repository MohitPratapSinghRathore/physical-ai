# Item 2. The pole in the extended displacement axis, and the bounded replacement

Code: `src/rho_bounded.py` (the bounded solver and the new audit bound),
`src/recompute_bounded.py` (recomputation and diff). Outputs:
`data/processed/rho_bounded_axis.csv`, `rho_bounded_dose_grid.csv`,
`rho_bounded_summary.json`, `fiscal_extended_axis_bounded.csv`,
`fiscal_extended_axis_bounded_diff.csv`, `fiscal_extended_axis_bounded_summary.json`.

## 1. The defect, confirmed, and one correction to how it was described

The replicator's algebra is right. With INT = 1.227975, SLOPE = -0.027490,
NE0 = 19.310920 and an exit share of 0.462,

    rho = (INT + SLOPE*NE0 + SLOPE*c) / (1 + SLOPE*c),   c = 100 * d_emp * 0.538

and the denominator vanishes at **d_emp = 0.676142** (the replicator reports 0.676150; the
difference is rounding of the slope). In wage-bill terms, using the ACS relative wages:

| group | relative wage | pole, as a share of the total wage bill |
|---|---|---|
| **embodied** | 0.6789 | **0.459** |
| cognitive GPT | 1.1996 | 0.811 |
| cognitive AIOE | 1.5047 | 1.017 |

**One correction to the replicator's account.** It reports that the construction "returns
rho = 4.39" at the headline dose. Our code never printed 4.39, and it is worth saying why,
because the reason is itself the defect. `src/fiscal_extended_axis.py` did not evaluate the
closed form. It ran a DAMPED iteration with `np.clip(rho, 0.0, 0.999)` INSIDE the loop. Past
the pole the iteration diverges, walks into the clip, and settles at **rho = 0**.

So the bound was being enforced, but accidentally, by a numerical device, and the value the
device produced at the boundary was then reported as though it were a solution. It is not a
solution. It is the floor of the extrapolation band, printed without the label. The most
direct evidence is `embodied_top50` at a wage-bill dose of 0.3366: the published rho is
exactly 0.0000 and the published terminal loss of 1,035.5bn is exactly the top of the band
the bounded treatment now reports. The old number was the boundary all along.

That is a worse finding than a printed 4.39 would have been. A 4.39 is visible. A silently
clipped boundary is not.

## 2. The replacement

Implemented in `solve_bounded`:

1. Solve the fixed point in closed form.
2. Accept it as a **point estimate only where it lies inside the observed range of rho**,
   which is [0.49, 0.74], the y-range of the fourteen-vintage fit (x-range 18.27 to 24.71).
3. **Clamp rho to [0, 1] everywhere.** Enforced, not incidental.
4. Where the fixed point falls outside the observed range, and wherever the denominator is
   non-positive so that no admissible fixed point exists, report **no point estimate at
   all**: report the band already defined for extrapolation, from the worst observed vintage
   **rho = 0.49 down to rho = 0**, labelled **outside the data**.

The band is not new. It is the same "floor at the lowest observed rho" mode the extended axis
already carried as one of two modes. What changes is that outside the observed range it
becomes the only output, instead of sitting beside a point estimate the data cannot support.

Three statuses are emitted: `inside`, `outside_range`, `no_solution`.

## 3. The inside-the-data boundary, which is the usable result

On the dose-response axis:

| exposure type | 5 pct | 10 pct | 25 pct | 50 pct | 75 pct |
|---|---|---|---|---|---|
| **embodied** | 0.660 | 0.613 | **band** | **none** | **none** |
| cognitive GPT | 0.677 | 0.655 | 0.562 | band | band |
| cognitive AIOE | 0.682 | 0.664 | 0.598 | band | band |

Stated plainly, and this is the sentence the paper needs:

> **A point estimate of the reemployment rate is available at the 5 and 10 percent doses for
> all three exposure types, and at the 25 percent dose for the two cognitive types only. At
> 50 percent and above no exposure type has a point estimate. The embodied group loses its
> point estimate first, at a wage-bill dose between 17 and 25 percent, because its relative
> wage of 0.679 means a given wage-bill dose displaces half again as many workers.**

The replicator's judgement that "the headline scenario can only be a cognitive one" is
correct at 25 percent and too generous at 50 percent, where the cognitive rows are outside
the observed rho range too.

## 4. What changed, quantity by quantity

Across the full extended-axis grid, 2,520 comparable cells:

| | |
|---|---|
| cells losing their point estimate | **672 of 2,520, 26.7 percent** |
| of those, the old point lies inside the new band | **568 of 672, 85 percent** |
| of those, the old point was exactly the band boundary | the embodied_top50 top dose, and the other rho = 0 rows |

Embodied results at doses of 25 percent and above, base reading, 10-year horizon,
terminal-year fiscal loss in bn:

| group | wage-bill dose | old rho | old point | **new band** | status |
|---|---|---|---|---|---|
| embodied_top30 | 0.1531 | 0.542 | 184.1 | 184.1 | **inside, unchanged** |
| embodied_top30 | 0.1837 | 0.490 | 254.2 | **253.9 to 565.3** | withdrawn |
| embodied_top30 | 0.2041 | 0.448 | 312.1 | **282.1 to 628.1** | withdrawn |
| embodied_top50 | 0.1683 | 0.519 | 215.5 | 215.5 | **inside, unchanged** |
| embodied_top50 | 0.2524 | 0.319 | 497.9 | **348.8 to 776.7** | withdrawn |
| embodied_top50 | 0.3029 | 0.093 | 834.5 | **418.6 to 931.9** | withdrawn |
| embodied_top50 | 0.3366 | **0.000** | 1,035.5 | **465.1 to 1,035.5** | withdrawn, old value was the boundary |
| embodied_top20 | all doses to 0.1362 | 0.569 to 0.693 | unchanged | unchanged | **inside throughout** |

Share of each group's doses losing the point estimate, base reading:

| group | pct of doses withdrawn |
|---|---|
| embodied_top20, cognitive_AIOE_top20 and top30, cognitive_GPT_top20 and top30 | **0** |
| both_AIOE_top20, both_GPT_top20, cognitive_AIOE_top50 | 28.6 |
| embodied_top30 | 28.6 |
| both_AIOE_top30, both_GPT_top30, cognitive_GPT_top50 | 42.9 |
| embodied_top50 | 42.9 |
| both_AIOE_top50, both_GPT_top50 | 57.1 |

**Direction of the change.** Withdrawing the point does not systematically raise or lower the
loss. The band straddles the old value in 85 percent of cases. Where the old rho had already
been clipped to zero, the old value sits at the TOP of the band, so the old figure was the
worst case reported as the central case. That is the one systematic bias, and it runs against
us: the superseded embodied figures at the largest doses overstate the fiscal loss relative
to the centre of the band.

## 5. What is withdrawn

- **Every embodied point estimate at a wage-bill dose above 0.17.** Replaced by a band,
  labelled outside the data.
- **Every point estimate for any group where the fixed point leaves [0.49, 0.74].**
- **The 50 percent headline as a point estimate for any exposure type.** At 50 percent all
  three types are outside the observed rho range; the embodied type has no fixed point at
  all, the denominator being negative.
- **Any statement of the form "at a 50 percent dose the reemployment rate is X".** There is
  no such X in this data.

Nothing is withdrawn that cannot be replaced by a band, so nothing is lost outright. What is
lost is the false precision.

## 6. The bound is now in the audit

`src/verify/plausibility_audit.py` gains the check **rho in [0, 1], it is a rate**, applied
to every rho column on the superseded axis, the bounded axis, the bounded scenario axis and
the bounded dose grid, plus a diagnostic that counts breaches of the RAW fixed point, which
are expected past the pole and must be caught and banded rather than printed.

The audit goes from **43 checks to 53**. Violations stay at **4**, all of them the superseded
rows deliberately retained to show what the rule caught. The raw fixed point breaches [0, 1]
in **6 of 101** scenario-axis rows and **2 of 13** dose-grid rows; both are caught.

This is the second time a bound has found something a tolerance could not. The replicator had
no code access and found it from the formula alone.
