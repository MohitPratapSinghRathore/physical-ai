# Thesis sentence, PROVISIONAL, for owner approval

Item 5 of the closing session. **Not to be used until the owner approves it, and
`paper/outline.md` is not touched before then.**

**AMENDED 2026-09-20 (labour backing session, item 0a), AWAITING OWNER APPROVAL.** The
break-even capital tax rates are corrected to the post-replication-repair values and the
capital tax paragraph is softened, because the correction WEAKENS the claim that the
instrument is unavailable. Three things changed and each is marked in place:
1. The fiscal condition fails at the OPERATIVE tau_k of 0.0708 in every cell, in both
   cases. That part is measured and independently replicated.
2. At the doses inside the observed data range a capital tax near the top of observed
   effective rates would break even. The blanket "no reading of the literature" claim is
   withdrawn.
3. Ownership-based instruments are described as growing in importance WITH THE DOSE rather
   than as strictly necessary.

---

## The sentence

> **AI-driven labour displacement is first a fiscal event and only second a banking event.**
> The state is the first-round absorber of lost wages, through income and payroll taxes, the
> payroll-funded trust funds, its mortgage guarantees and the student loan book it owns
> outright: it bears **77 to 92 percent** of first-round losses at every dose. The banking
> system is the second-round absorber, reached through consumer spending, house prices and
> business credit rather than through displaced borrowers defaulting on their own loans:
> roughly **nine tenths** of bank losses at large displacement arrive by that route. Whether
> the fiscal absorber holds turns on the effective tax rate on AI capital and on whether
> income reaches households some other way, and **at the operative effective rate of 0.0708
> it does not hold at any dose.** How far out of reach the repair is depends on the dose: at
> moderate displacement a capital tax near the top of observed effective rates would break
> even, while at large displacement the required rate, up to about **0.30 in case A and 0.65
> in case B**, exceeds any effective rate ever observed. **So instruments that deliver income
> through ownership or through direct claims on AI capital grow in importance with the dose,
> rather than being strictly necessary at every dose.** **And
> the United States case does not generalise:** an issuer that cannot borrow freely in its own
> currency faces the same shock on a debt path that is already unstable without it.

## The one-line version

> Wage-based public finance makes the state the residual claimant on labour income, so
> displacement lands on the sovereign first and on the banks second, and the terms on which a
> sovereign borrows decide whether that is an accounting problem or a crisis.

---

## What is MEASURED

| Component | Claims | Basis |
|---|---|---|
| The state bears 77 to 92 percent of first-round losses | 157 | Measured balances, measured tax rates, a sourced holder decomposition and a verified federal student loan share of 97.3 percent |
| 97.3 percent of the student loan book is a federal asset | 156 | FRED FGCCSAQ027S against the NY Fed total |
| The mortgage holder split: GSE 51.1, FHA 12.6, bank 11.5, residual 24.9 percent | 147 | Read from the Enterprises' own 2025 Forms 10-K, except FHA which is a flagged proxy |
| First-round household credit losses | 86, 126, 127 | ACS and SIPP microdata, corrected under-reporting factors, exposure at default times loss given default |
| The fiscal condition fails on current parameters | fiscal block, A-series | R = 0.568 against a required 0.72 at the sourced tau_k. **REPLICATED: an instance that did not write the code confirmed the failure at every reading of tau_l, under its own R of 0.6233 as well as ours (claim 183, R-confirmed-direction)** |
| The break-even capital tax rate exceeds the OPERATIVE rate of 0.0708 in every cell, in both cases | 168 amended, 179 | Case A break-even runs 0.125 to 0.301 and case B 0.182 to 0.650 across the dose grid. **Measured arithmetic on the corrected bases** |
| Displacement low in the wage distribution is a payroll tax event, high in it an income tax event | 143 | ACS wages, statutory payroll rates, an IRS SOI marginal income tax schedule |
| Exposure type is a pay proxy in three independent tests | 139, 140, 146 | Reweighting on wage deciles, two datasets, two cognitive indices, and a 2,462-PUMA cross section |
| Household buffers are not monotonic in pay | 145 | SIPP, thinnest in the second quintile |

## What is SCENARIO

| Component | Claims | Why it is scenario |
|---|---|---|
| Nine tenths of bank losses arrive through the second round | 154, 155 | Built on a derived MPC, an income-to-house-price elasticity, an Okun coefficient and an extrapolation of the Fed's loss rates beyond its own severity. The 9:1 ratio is robust in direction across the sourced ranges; the LEVEL moves by a factor of nine |
| The demand shortfall and its severity against the Fed scenario | 150 | Depends on the MPC gap, which explains 95 percent of its variance |
| "A demand event first, the opposite of 2008" | 150 | **SURVIVES ONLY CONDITIONALLY.** True at every Harter-Dreiman elasticity, false at an elasticity of 1.5, which the modern survey says is the more likely region |
| Debt paths | 152 | Stated r and g. Reported as increments over a no-displacement baseline after the level version turned out to be mostly baseline compounding |
| The policy response removes 85 percent of the loss | 160 | Case A arithmetic. **The 56 to 86 percent break-even range is WITHDRAWN (claim 167, R-failed). Corrected: case A 0.125 to 0.301, case B 0.182 to 0.650** |
| Whether a capital tax could break even AT A GIVEN DOSE | 168 amended | **SCENARIO, because the dose is.** At 5 and 10 percent of the wage bill, the only doses fully inside the observed data range, case A break-even is 0.125 to 0.143, at or below the sourced maximum of 0.204. At 50 percent it is 0.301 in case A and 0.650 in case B, outside anything observed |
| Any dose above 10 percent of the total wage bill | 135 | Outside the observed data range for at least one exposure type |

## What the sentence deliberately does NOT claim

- **It does not claim displacement will happen, or at what speed.** The labour model is frozen
  as a scenario generator and its speed limit is a range, not a number.
- **It does not claim cognitive and embodied exposure stress different balance sheets.** That
  comparative thesis did not survive the pay control.
- **It does not claim banks are safe.** It claims the first-round channel they would naturally
  model is roughly a tenth of the exposure, which is the opposite of reassuring.
- **It does not claim the fiscal condition can be repaired by a capital tax at the tax code
  as it stands.** The break-even rate exceeds the operative effective rate of 0.0708 in
  every cell in both cases. It does NOT claim more than that. On the corrected grid the
  break-even rate is at or below the top of the SOURCED effective range in 10 of 15 case A
  cells and 5 of 15 case B cells, so the earlier statement that no reading of the corporate
  tax literature makes the instrument available is withdrawn. **This weakens the thesis and
  is stated first for that reason.** What survives is a statement about the tax code in
  force, not about what is economically conceivable.
- **It does not claim ownership-based instruments are strictly necessary.** Their importance
  rises with the dose. At the doses inside the observed data range a capital tax could
  break even; at large doses it could not, and then only instruments that deliver income
  through ownership or direct claims on AI capital close the gap.
- **It does not claim the trust funds can be repaired this way at any dose.** Replacement
  income financed from a capital tax is not covered wages, so it does not reach the
  payroll-funded funds at all. That is a design choice, not a law of nature (claim 161).

## The known weak points, named before a reviewer names them

1. **The second-round module is the load-bearing part of the sentence and it is the least
   measured part.** Its ratio is robust; its level is not.
2. **The cognitive exposure indices measure task overlap, not displacement or timing.** Every
   cognitive scenario is a dose, not a forecast.
3. **The emerging-market contrast is arithmetic on stated parameters**, not an estimate for
   any particular country.
4. **The federal share is sensitive to the holder decomposition**, one quarter of which is a
   residual and one eighth of which is a flagged FHA proxy.
