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

**Status: draft, arithmetic checked, assumptions not yet stress-tested.** Open issues: tau_k
is an economy-wide average applied to a marginal surplus; the 1:1 mapping of displaced wage
income into taxable capital income assumes output preserved and no change in factor shares
beyond the substitution itself; g is scenario, not measured.

## P2. Hedge failure

Not yet drafted. To be written with the fiscal wedge from P1 integrated.
