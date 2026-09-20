# tau_k on AI surplus, rebuilt from components

`definitions.md` first (what each published rate already contains), then `components.py`
(the components and their verification status), then `assemble.py` (assembly, variance
decomposition, map), then `base_argument.md` (which base, and the case against ours).

Rebuild: `python components.py && python assemble.py`. Figure at
`paper/figures/tau_k_map.png`.

## Gate report

### Plausibility violations

**None.** Every component range sits inside its named statutory or structural ceiling; every
share is in [0, 1]; the assembled rate lies between the lowest and highest
component-consistent values in both rent readings; the assembled maximum is below the ceiling
on a fully domestic, fully distributed, fully taxable, all-equity dollar (0.3142 under
Barkai, 0.2380 under Karabarbounis and Neiman). The one negative value that appears,
a minimum of -0.0128 under the Karabarbounis and Neiman reading, is not a violation: it is
the AMR debt-financing result, where the marginal rate on the normal return is `tau_b - tau_c`
and is negative when bondholders are taxed below the corporation. AMR state that explicitly.

### Thesis-weakening results, first

**1. The task's own premise about which parameters matter is wrong, and we tested it rather
than assuming it.** The task named expected rent share, shifted share and taxable-shareholder
share as the three most influential parameters. The first-order variance decomposition says
otherwise. Under the Barkai reading the three are **taxable-shareholder share (0.356),
deferral factor (0.261) and bondholder rate (0.153)**. The **shifted share carries 0.029**,
and the debt share carries 0.0004. Profit shifting, which is the leg of our published story
that has had the most attention, is close to irrelevant to the assembled rate. Two of the
three parameters that do matter were not in the published construction at all.

**2. Our published 0.0708 is too low, and the rebuild says so.** It omits the shareholder
layer entirely, which under AMR's own algebra is the *whole* of the effective rate on the
normal return under full expensing. The assembled rate under the same Barkai rent reading has
a 5th to 95th percentile span of **0.0865 to 0.1558**, and its minimum across the entire
swept space, 0.0578, is the only region that reaches down to 0.0708. The published figure
sits at the bottom edge of the plausible range, not in the middle of it.

**3. The verdict changes, and it changes toward "cannot be called".** The required rate is
0.1101 to 0.1373. The assembled median under Barkai is **0.1158**, which is *inside* the
required band. So the condition neither clearly fails, as the published 0.0708 implied, nor
clearly passes. Across the swept space it passes in **61 percent** of draws against the
easier labour-tax reading and **18 percent** against the harder one.

**4. The rent-share disagreement is still the thing that decides it, and the worse reading
is decisive.** Under Karabarbounis and Neiman, with a rent share near zero, the assembled
median is **0.0518** and the condition passes in **1.1 percent** of the swept space against
the easier threshold and in **none** against the harder one. The two readings must not be
averaged, and under one of them the answer is not in doubt.

**5. Four separate parameters can each cross a threshold on their own.** Holding everything
else at its range midpoint, the taxable-shareholder share alone moves the rate from 0.0960 to
0.1396, the deferral factor from 0.0991 to 0.1365, the bondholder rate from 0.1035 to 0.1320
and the shareholder rate from 0.1079 to 0.1277. Each of those intervals contains at least one
of the two thresholds. **None of these four is verified.**

### Sourced, kept separate from scenario

**Verified this session or previously in this repo, five components:**

- Federal corporate rate 0.21, 26 USC 11(b).
- **26 USC 250(a)(1), as amended by Pub. L. 119-21 of 4 July 2025.** The deduction is now
  33.34 percent of foreign-derived deduction eligible income and 40 percent of the net CFC
  tested income amount, giving effective rates of **14.0 and 12.6 percent**. 26 USC 951A has
  been recaptioned from "Global intangible low-taxed income" to "Net CFC tested income".
  Verified from Cornell LII on 2026-09-20. **The pre-2025 figures of 13.125 and 10.5 percent
  are superseded and are not used.** This is exactly the check the task asked for, and the
  descriptions had in fact moved.
- Shifted share 0.48, Torslov, Wier and Zucman, already verified in this repo. **One verified
  source, not the two the task required**, so the parameter is swept as well as marked.
- The two rent readings, Barkai 0.351 and Karabarbounis and Neiman case R at approximately
  zero, both previously verified, **never averaged**.
- The AMR expensing algebra, read in full from the paper this session.

**Scenario, swept, no point value asserted, seven components:** taxable-shareholder share,
shareholder rate, deferral factor, state effective corporate rate, debt share, bondholder
rate, shifted share. Each is listed in `lit/unverified.md` with what was sought, what
happened, and the ceiling that bounds its range. **No claim in this project depends on a
point value for any of them.** The map is the deliverable precisely because they could not be
pinned.

### Pillar Two, item 3

**NOT VERIFIED, and therefore not used.** The OECD pages returned HTTP 403 in this session
and no primary-source confirmation of the current status of the global minimum tax for
US-parented groups as of 2026 was obtained. It is recorded in `lit/unverified.md`. It appears
on the map **only as a marked reference line at 0.15**, with its status printed next to it,
and it carries no claim. The conditional statement, which is arithmetic and not a finding, is
this: 0.15 exceeds the required 0.1101 to 0.1373, so wherever a 15 percent floor genuinely
bound the AI rents the condition would pass on the rent component. Whether it binds is the
unverified part and is the whole of the question.

### What would close this

One verified source for the taxable-shareholder share and one for the deferral factor would
between them remove 62 percent of the variance in the assembled rate under the Barkai
reading. That is the highest-value hour of sourcing left in this project.
