# Thesis sentence, PROVISIONAL, for owner approval

Item 5 of the closing session. **Not to be used until the owner approves it, and
`paper/outline.md` is not touched before then.**

**AMENDED AGAIN 2026-09-20 (final analysis session, A103 and the closing pass), AWAITING
OWNER APPROVAL.** Four changes, each marked in place below:

1. **The holder gap is promoted to the opening clause.** The sovereign share is the paper's
   central object and the sentence should lead with it rather than reach it.
2. **"77 to 92 percent" is replaced by a by-dose statement reported both ways.** The federal
   share is not one range and it is not monotone: narrow reading 0.785 to 0.870 at the 10
   percent dose rising to 0.855 to 0.925 at 50 and falling back at 75; conservatorship reading
   8 to 10 points higher. See `notes/item3b_gse_classification.md`.
3. **The inside-the-data boundary is stated in the sentence itself.** At a 50 percent dose no
   exposure type has a reemployment-rate point estimate, so everything there is a band.
4. **The capital tax verdict is now conditional on the rate, not on "current law".** The
   condition STRADDLES the threshold once the rate is assembled from components, 0.087 to
   0.156 against a required 0.110 to 0.137; the earlier operative rate and the IMF's rate are
   the two edges of that disagreement and both are
   correctly computed on different bases. See `notes/tau_k_exposure.md`.
5. **The priority claim on the fiscal mechanism is gone from the wording.** RAND, the IMF
   (both the 2024 SDN and the 2026 Note), the Windfall Trust, Korinek and Lockwood, and Casas
   and Torres all have it. What is ours is the measured liability side.

## The sentence, matched to the seven-claim order. AWAITING OWNER APPROVAL.

Amended to follow the claim order, to carry the union wording, and to end on the organising
conclusion rather than on the method boundary.

> In the United States, about **52 percent of all debt is serviced directly out of wages**,
> and the federal government is exposed, as holder, guarantor or debtor, on about **four
> fifths** of those claims: roughly a third as creditor or guarantor, through mortgage
> guarantees and student loans, and about **55 percent as the debtor** on Treasury debt
> serviced from income and payroll taxes. It holds about **one percent** of the claims on AI
> capital. So displacement is a fiscal event before it is a financial one: at ten percent of
> wages displaced, the only level inside observed data, the federal government bears roughly
> **80 to 90 percent** of first-round losses while the banking system barely moves, and when
> automation works through non-hiring rather than layoffs the losses shift onto younger
> borrowers while **the fiscal loss is unchanged**. Banks are reached mainly at larger
> displacement and mostly indirectly, through falling spending, house prices and business
> credit rather than displaced borrowers' own loans, which is why **household relief does not
> protect bank capital**: forbearance, income-driven repayment and wage insurance together
> remove under a tenth of bank losses. Whether the budget can absorb the loss depends on
> which capital tax rate reaches AI profits: the condition needs about **11 to 14 percent**,
> AI capital after expensing and profit shifting bears about **7**, and capital economy-wide
> bears **20 to 22**, so between a quarter and a half of AI profits would need to be taxed at
> the ordinary rate. **And if AI fails instead, the state still loses: a bust costs 569 to
> 955bn in capital gains and corporate receipts while barely touching wages. The state loses
> in both directions, through different tax bases, so the same capital tax rate is being
> asked to do two opposite jobs.**

## The one-line version

> The state is the residual claimant on labour income and holds almost none of the capital
> that would replace it, so it loses whether AI succeeds or fails, and the one instrument
> that could hedge either is the same rate pulled in opposite directions.

**Note on the previous one-liner.** The earlier closing clause, "the terms on which a
sovereign borrows decide whether that is an accounting problem or a crisis", **rested on
scenario arithmetic**, not measurement: the emerging-market debt path and the 376.7 percent
baseline are projections. It is dropped from the headline version and kept in section 9.

---

## SUPERSEDED VERSION, retained to show what moved

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
