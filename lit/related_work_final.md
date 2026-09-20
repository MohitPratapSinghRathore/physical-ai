# Related work, boundary redrawn. Final analysis session, 2026-09-20

Supersedes the boundary in `lit/related_work_labour_backing.md` for the rows changed here.
That file's eleven-row table and its verification-level scheme stand; this file records what
moved.

## Verification levels, unchanged

**F** full text read directly in this environment. **B** bibliographic record verified, full
text not readable from here. **U** not verified; goes to `lit/unverified.md` and carries no
dependent claim.

## What moved

| work | was | now | why |
|---|---|---|---|
| Price and Suresh 2026 (RAND) | B | **F** | full text obtained and read in this session, retained at `data/raw/manual/RAND_RRA4980-1_PriceSuresh2026.pdf` |
| Korinek and Lockwood | B, superseded title | **B, corrected** | NBER WP 34873, DOI 10.3386/w34873, February 2026. Now in `references.bib` |
| CBO 2024 | proposed addition | **U** | `cbo.gov` returns HTTP 403 on every route. Does not enter `references.bib` |
| IMF Notes 2026/002 | B | **B, unchanged** | full text still unreachable and the owner's copy is not on this machine. **Boundary NOT redrawn from full text; the row below says so** |
| Manning and others 2026 | "thesis-weakening" | **overlap, not contradiction** | corrected below |

---

## 1. Price and Suresh (2026), RAND RR-A4980-1. Read in full

**What it measures.** US federal revenue under AI labour substitution, using the RAND von
Furstenberg Family Budget Model. Two cases: a near-term case in which **10 percent of the
workforce is replaced**, simulated over 2025 to 2035, and a long-term case in which all
existing jobs are displaced, handled as a framework rather than a simulation.

**Its two axes**, and the earlier audit described the second one loosely:

1. **Whether displaced workers find new remunerated tasks.** This IS our rho.
2. **Whether AI is priced monopolistically or at cost.** This is **NOT** our tau_k. It sits
   one step UPSTREAM of tau_k: it determines whether a taxable surplus exists at all. Priced
   monopolistically, displaced wages become corporate profit. Priced at cost, the surplus
   accrues to consumers as deflation and is untaxable. Our tau_k asks what share of an
   existing surplus the state can take; their pricing axis asks whether there is one.
   **Correcting this sharpens rather than weakens the priority retirement**: they have a
   mechanism we do not model at all.

**What it measures that we also measure, and the agreement is close.**

| | RAND | ours |
|---|---|---|
| federal revenue from individual or payroll taxes, 2024 | **84 percent** | labour-linked upper bound **77.7 percent** |
| federal revenue **due directly to labour** | **about 66 percent** | labour-linked central **63.4 percent** |

**Two independently constructed measures of the same object agree to within 2.6 percentage
points.** Ours is built bottom-up from the SOI wage share of AGI applied to federal personal
current taxes, plus social insurance contributions in full, over federal current receipts.
Theirs is RAND's own decomposition inside their budget model. Neither saw the other. **This
is the strongest external corroboration the fiscal half of this project has, and it should be
reported as such.**

**A second, sharper corroboration.** RAND's key finding on the corporate side:

> "the revenue from corporate income taxes would not be able to offset the revenue from
> displaced labor **unless the corporate tax rates were roughly doubled to be at parity with
> labor tax rates**."

Our break-even result, reached from a completely different direction: the operative effective
capital tax rate is **0.0708** and the rate required to close the condition is **0.110 to
0.137**, which is **1.55 to 1.94 times the operative rate**. "Roughly doubled" and "1.55 to
1.94 times" are the same answer. RAND reached it inside a macro model; we reached it from
sourced effective rates and a retained wage share. **Report the agreement, and report that it
is agreement about a magnitude, not about a mechanism we discovered.**

**What RAND only asserts, or does not address at all.** The report contains **no household
debt, no mortgage analysis, no bank balance sheets, no credit losses and no financial
stability content**. A text search of the full report returns "mortgage" once, inside a
modelling note about interest rate types, and every "bank" hit is a Federal Reserve Bank of
St. Louis data citation. Its policy options are named and not sized: change the tax code,
stabilise nominal demand, plan income support, regulate concentrated AI systems. The report
says explicitly that they are "illustrative".

**One methodological point that matters for our case B.** RAND holds output constant by
construction: "we adjust the total factor productivity so that the net change in output
associated with replacing human labor is zero." Their entire simulation is therefore the
analogue of **our case A, output preserved**. **Our case B, output falling, has no RAND
counterpart**, and case B is where the required capital tax rate reaches 0.650. That is a
genuine extension, and it is the only part of the taxation argument that is ours alone.

### The boundary

| | RAND | this project |
|---|---|---|
| unit | macro, budget model | household microdata plus the claim stock |
| the fiscal mechanism | **theirs, published first** | not ours, and not presented as ours |
| labour-linked receipts share | 84 pct and 66 pct | 77.7 pct and 63.4 pct, **independent agreement** |
| corporate tax cannot offset | "roughly doubled" | 1.55 to 1.94 times operative, **independent agreement** |
| output falling | not modelled | **ours**, case B |
| **who holds the claims** | **absent** | **ours**: the holder map, 0.794 of the wage leg on the state |
| household balance sheets, mortgages, cards, autos, student loans | **absent** | **ours** |
| GSE and FHA split, bank capital, supervisory benchmark | **absent** | **ours** |
| trust fund arithmetic against the 2026 Trustees tables | **absent** | **ours** |
| the AI leg and the two-sided bet | **absent** | **ours** |

**One sentence for the paper:** RAND established that AI labour displacement is a federal
revenue event and sized it inside a macro model; this paper measures **whose balance sheets
the claims sit on** and what happens to them, which RAND does not attempt.

---

## 2. Manning, Aguirre, Muro and Methkupally (2026). CORRECTED: overlap, not contradiction

**The previous entry was wrong in its framing**, and the correction matters because the
previous entry told the paper to treat its own buffer work as under threat.

The previous entry read: "THIS IS THESIS-WEAKENING AND IS REPORTED AS SUCH. It cuts against
the implicit direction of our household buffer work."

**It does not cut against it.** Manning and others find AI exposure and *adaptive capacity*
positively correlated: 26.5m of the 37.1m workers in the top exposure quartile are in
occupations with above-median adaptive capacity, where adaptive capacity is an index of
savings, age, local labour market density and skill transferability.

That is the **same finding as ours, on a different object.** Our claim 145 already says
buffers are **not monotonic in pay**, and our pay-control result (claim 139) already says
that neither exposure-type contrast survives controlling for pay. A positive correlation
between exposure and adaptive capacity is what you get when the exposed group is
higher-paid, which is exactly what our cognitive groups are: ACS relative wages of 1.20 (GPT)
and 1.50 (AIOE) against 0.68 for embodied.

**So this is overlap and corroboration, not contradiction.** The correct statement:

> Manning and others reach, from an occupation-level adaptive capacity index, the conclusion
> this project reaches from household microdata: AI exposure is concentrated among
> better-placed workers, and exposure alone does not identify vulnerability.

**What remains ours is the pay-level buffer finding**, which their index cannot produce:
adaptive capacity is an occupation-level construct, so it cannot show that the relationship
between buffers and exposure runs through **pay level** and disappears when pay is
controlled. That is a household-level result requiring household-level buffers and balances,
and it is the finding to lead with. Their index is an input we should cite rather than
rebuild.

**The hiring-freeze blind spot (claims 80, 93, 94) is unaffected either way.** It is a
statement about never-hired entrants, who are outside both their sample frame and ours, and
it stays a deduction. It remains cautioned for that reason and not because of Manning.

---

## 3. IMF Notes 2026/002. Boundary NOT redrawn

**Stated plainly because the alternative is to assert a reading we do not have.** The full
text is unreachable from this environment (`imf.org` returns HTTP 403, the eLibrary route
returns 404) and the owner's copy is not on this machine. The row below is unchanged from
the previous audit, at verification level B, resting on the bibliographic record and the
publisher abstract only.

| | |
|---|---|
| what it is | scenario planning exercise, five-year horizon, two diffusion trajectories, baseline and runaway |
| what it claims | transition dynamics strain fiscal frameworks through erosion of labour tax bases and rising social spending, particularly where social insurance is employment-linked; capital income taxes should be strengthened |
| overlap | the employment-linked social insurance point is our trust fund result (claims 120, 161, 190). **Our audience is this institution and it has already published the framing** |
| what remains ours, AT LEVEL B | our trust fund arithmetic is measured fund by fund against the 2026 Trustees tables with depletion dates; the note is a scenario exercise without that arithmetic |

**This boundary must be re-checked against the full text before submission.** It is the one
row in the table where a claim about what a competitor does NOT do rests on an abstract.

---

## 4. The connected work, named as such

Three of these are not competitors to be distinguished from. They are **connected work that
establishes the framing this paper builds on**, and the paper should say so in those words
rather than hedging:

- **IMF Notes 2026/002** established the fiscal-strain framing at an institution.
- **Ieong and others (2026), Windfall Trust** established the four-channel tax-risk
  accounting, including the international leakage channel that is our open-economy case.
- **Korinek and Lockwood (2026)** established the optimal-taxation treatment, which our
  fiscal framing sits inside.

Together with **Price and Suresh (2026)** and **Casas and Torres (2024)**, they mean the
fiscal mechanism is established literature. **This paper's contribution is the liability
side: who holds the claims, and what a displacement dose does to them.**

---

## 5. What remains a stated limitation

The systematic PRISMA-protocol search **for the labour backing question specifically** has
not been run. The novelty statement for that ratio is "none located", not "none exists".
Recorded as limitation L3 in the gate report and carried into the paper's limitations
section. The related-work audit has already retired one priority claim on the fiscal
mechanism after a non-systematic search found prior work; the same could happen here.
