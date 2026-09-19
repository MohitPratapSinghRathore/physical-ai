# Propositions

Working file. Statements here are drafts to be checked, not established results.

## P1. The fiscal tau*s condition

**Setup.** Automation displaces a wage bill dW. Let

    tau_l  effective tax rate on labour income
    tau_k  effective tax rate on the capital income that replaces it
    g      added public outlays per dollar of displaced wage bill
    s      additional taxable surplus generated per dollar of displaced wage bill

**Condition.** The public budget is unchanged by the displacement if and only if

    tau_k * s * dW  >=  tau_l * dW  +  g * dW

that is

    **s  >=  (tau_l + g) / tau_k**

**Calibration** (Acemoglu, Manera and Restrepo 2020, Brookings Papers 2020(1), 231-300,
read from the published PDF): tau_l = 0.255; tau_k = 0.10 on net capital income; tau_k =
0.05 on equipment and software after the 2017 reform.

| g | s required at tau_k = 0.10 | s required at tau_k = 0.05 |
|---|---|---|
| 0 | 2.55 | 5.10 |
| 0.10 | 3.55 | 7.10 |
| 0.25 | 5.05 | 10.10 |

**Reading.** Output-neutral automation (s = 1) always worsens the public budget, by
(tau_l - tau_k) per dollar displaced, which is 15.5 cents at the 10 percent capital rate and
20.5 cents at the equipment rate. Fiscal neutrality requires a surplus multiple of at least
2.55, and 5.10 if the surplus accrues to equipment and software.

**Relation to the brief's threshold.** PROJECT_BRIEF.md Section 2.3 states the condition for
full income replacement as tau * s >= 1. That is the REDISTRIBUTION condition: can the
government, having taxed the surplus, replace displaced income. P1 is the prior FISCAL
condition: can the government collect as much as it loses. P1 is strictly harder whenever
tau_k < tau_l, and the gap is the tax wedge between labour and capital. **The brief's
threshold understates the constraint by assuming the revenue arrives.**

**SUPERSEDED 2026-09-19 by P1r below. The statement above is wrong in framing: it presents s >= 2.55 as a threshold, but under output neutrality s <= 1 by construction, so the condition is unattainable rather than demanding. Kept as the record of the error.**

**Status: draft, arithmetic checked.** Open issues: tau_k
is an economy-wide average applied to a marginal surplus; the 1:1 mapping of displaced wage
income into taxable capital income assumes output preserved and no change in factor shares
beyond the substitution itself; g is scenario, not measured.

## P2. Hedge failure

Not yet drafted. To be written with the fiscal wedge from P1 integrated.


---

## P1r. The fiscal condition, restated and repaired

**Setup.** Displace one dollar of wage bill. A robot performs the same task at all-in cost
c_r against wage w, so the cost saving is s = 1 - c_r/w, with 0 < s <= 1. Let tau_l be the
effective labour tax rate, tau_k the rate on the capital income that replaces it, tau_r the
rate on robot-producer income, m the imported share of robot capital, g added public outlays
per dollar displaced, rho the reemployment share and omega the wage ratio on reemployment.

**General condition for fiscal neutrality:**

    tau_k*s + tau_l*rho*omega + tau_r*(1-m)*(1-s)  >=  tau_l + g*(1-rho)

**Proposition P1r (infeasibility under output neutrality).** With rho = 0 and m = 1 the
condition is tau_k*s >= tau_l + g. Since s <= 1, it cannot hold whenever tau_k < tau_l + g.
At tau_l = 0.255 and tau_k = 0.10 it fails for every g >= 0.

*Therefore output-neutral automation is never fiscally neutral. There is no break-even
value of the robot cost ratio s. (This is a statement about s, NOT about adoption speed:
speed determines how fast the loss accrues, not its size per displaced dollar.) The public
loss per dollar displaced is*

    L(s) = tau_l + g - tau_k*s,  with  tau_l + g - tau_k <= L <= tau_l + g

*and fiscal neutrality requires additional taxable output y >= (tau_l + g)/tau_k - s, at
best (tau_l + g - tau_k)/tau_k.*

**Corollary 1 (closed economy).** With m = 0 and tau_r = tau_k the s terms cancel and the
condition becomes tau_k + tau_l*rho*omega >= tau_l + g*(1-rho), independent of s. **The
loss per displaced dollar is independent of the ROBOT COST RATIO s under uniform capital
taxation. This says nothing about adoption speed**, which governs how fast the loss accrues,
not its size per dollar. (Corrected 2026-09-19; an earlier version said adoption speed was
irrelevant, which does not follow.) Only the tax wedge and the reemployment margin set the
size of the per-dollar loss. Break-even reemployment share rho* = (1 - tau_k/tau_l)/omega. At omega = 0.75 and tau_k =
0.10 this is 0.810 to 0.914, and it is INFEASIBLE (above 1) at the 5 percent equipment rate.
But allowing for the robot sector's own labour share, 0.337 for NAICS 333 machinery
(NBER-CES), a third of robot spending is wages taxed at tau_l, and rho* falls to 0.537 in
the central case and is feasible everywhere. See A34.

**Corollary 2 (imported capital, the emerging-market case).** With m = 1 the robot cost is
untaxed domestically and only the surplus is taxable. Near the adoption margin the entire
labour tax base is lost with essentially no offsetting domestic base: -0.250 per dollar
displaced at AMR rates with rho = 0, s = 0.05.

**Relation to the brief.** PROJECT_BRIEF.md Section 2.3 states tau*s >= 1 as the condition
for full income replacement. That is the REDISTRIBUTION condition and sits downstream: it
asks whether collected revenue can replace lost income, taking collection as given. P1r asks
whether revenue is collected at all, and is binding first.

**Calibration sources.** tau_l 0.255 and tau_k 0.10 (0.05 equipment and software): Acemoglu,
Manera and Restrepo, Brookings Papers 2020(1), 231-300. Bottom-up tau_l 0.301 to 0.318:
NIPA and IRS SOI, this repository. omega 0.75 (0.65 to 0.82): Jacobson, LaLonde and
Sullivan, AER 83(4), 1993, 685-709. **rho is stipulated, not sourced.**

**Novelty, narrowly.** The mechanism is stated qualitatively by the IMF (SDN/2024/002),
including the developing-economy exposure. We have not identified a source that writes the
closed-form per-dollar condition with retained streams, states the infeasibility result, or
reduces the closed-economy case to a calibrated break-even reemployment share. This is a
formalisation and calibration claim, not a discovery claim.
