# Architecture section: build specification

NOT YET BUILT. Gated on owner approval of a thesis statement (Part 2 output). Sequenced
after thesis approval and before the outline rewrite (item H).

## Output

`framework/architecture.md`, as a table, one row per instrument.

| Column | Content |
|---|---|
| Measured mechanism | the specific measured finding the instrument responds to |
| Evidence file | path in this repository |
| Institution that must act | the body with the authority |
| Instrument | the policy or contractual device |
| Type | tax, flow, stock, contract, buffer, or ownership |
| Precedent | real-world precedent with a VERIFIED citation |
| Trigger indicator | observable, with its data source |
| Binds in | which adoption scenarios it binds in |

## Rules, binding

1. **No instrument without a measured mechanism**, or an explicitly labelled scenario
   assumption. An instrument that answers nothing we measured does not go in the table.
2. **No instrument aimed at a channel the data showed to be small.** This rules out general
   mortgage relief and general unsecured-credit instruments for embodied households:
   A31 showed embodied households are LESS indebted on seven of twelve debt measures, and
   the unsecured concentration is null. Vehicle credit for the DRIVING pathway survives
   this rule (A31, adjusted +13.39, t = 3.50); nothing else in household credit does.
3. For each of the five scenarios, state the **minimum sufficient set** and say explicitly
   **which instruments are unnecessary** in that scenario.
4. For the partial-success scenario, show from P1r **why surplus-financed instruments fail**
   there (the surplus s is small near the adoption margin, so anything financed out of
   tau_k * s raises almost nothing) and **which instruments do not depend on surplus**.
5. Every trigger must be defined precisely enough to be **computed from public data today**,
   and its **current value must be computed** and shown.

## Candidate triggers already computable in this repository

- payroll tax at stake as a share of OASDI payroll income (fiscal_channel_scenarios.csv)
- reemployment share against rho* (p1r_rho_star_labour_share.csv); rho itself needs the BLS
  Displaced Worker Survey, currently blocked
- county at-risk-rate dispersion, p99/p1 (geo_groups_concentration.csv)
- share of embodied households under one month of liquid buffer (sipp_v2_ci.csv)
- vehicle debt to income for the driving pathway (sipp_v2_adjusted.csv)
- Leg A self-funding ratio by firm (legA_tier2.csv)
