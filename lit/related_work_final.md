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
| IMF Note 2026/002 | B | **F, read in full** | owner placed it. Boundary redrawn. Kill criterion assessed and NOT triggered, but it is the closest approach located |
| **IMF SDN/2024/002** | not in the audit | **F, read in full** | NEW ROW. Corroborates our sourced tau_k maximum, raises a vulnerability in our operative rate, and supplies measured social-protection effects |
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

## 3. IMF Note 2026/002 (Barhoumi and others). READ IN FULL, boundary redrawn

**Upgraded from verification level B to F.** Retained at
`data/raw/manual/IMF_Note_2026_002_AI_Scenario_Planning.pdf`. This is the row the previous
audit could only describe from an abstract, and reading it changes the boundary in both
directions.

**What it is.** A synthesis of a two-day IMF workshop (10 to 11 December 2025) co-organised
with the Economics of Transformative AI Initiative at the University of Virginia (Anton
Korinek), plus a closed-door scenario-planning exercise on day two with about 30 IMF staff and
15 external experts, under the Chatham House Rule. **The scenarios were developed in
collaboration with the Windfall Trust**, which connects two rows of this table that the
previous audit treated as independent.

**Its two scenarios.** A shared assumption that AI attains human expert-level capability
within five years and, by the early 2030s, "the technical capacity to perform most cognitive
and physical tasks ... supported by its integration into robotics". The scenarios differ only
in diffusion speed: **baseline diffusion** (slow, frictions and pushback) and **runaway
diffusion** (rapid, minimal regulatory constraint). **The shared assumption covers PHYSICAL
tasks and robotics**, so this is not a cognitive-only exercise, which the abstract did not
make clear.

### 3.1 The overlap is much larger than the previous audit recorded

The previous row said the overlap was the employment-linked social insurance point. That
understated it. **The Note states the wage-leg credit mechanism directly:**

> "In the runaway scenario, **large-scale job losses weaken household balance sheets and raise
> default risks, putting pressure on banking systems with high exposure to consumer credit**."

> "Sharp declines in household and firm income during periods of rapid adoption **weaken debt
> servicing capacity, transmitting adjustment pressures into banking losses and tighter credit
> conditions**."

That is this project's first-round and second-round mechanism, asserted. It also states the
tau_k result qualitatively: "Shifting taxation from labor to capital through higher corporate
income taxes **may only partially offset these losses** given capital mobility, market
concentration, and international tax competition."

### 3.2 THE KILL CRITERION: assessed, NOT triggered, and the closest approach yet located

`PROJECT_BRIEF.md` WS0 carries a standing instruction: **"if any paper already combines both
legs in one exposure framework, stop and report to the owner with a proposed repositioning."**
This Note forces that assessment, because **both legs appear in the same paragraph**:

| leg | the Note's words |
|---|---|
| **Leg W** | "large-scale job losses weaken household balance sheets and raise default risks, putting pressure on banking systems with high exposure to consumer credit" |
| **Leg A** | "elevated leverage to finance AI-related investment, coupled with rapid capital obsolescence risks, increases uncertainty around future earnings and asset valuations" |

and it closes that paragraph with a sentence close to our partial-success logic:

> "These risks are especially acute during the transition, when **displacement costs are
> concentrated among incumbent workers and borrowers, whereas productivity gains accrue
> primarily to new entrants and AI-intensive firms**."

**The assessment, stated conservatively.** The criterion is **not triggered**, for four
reasons, each checkable against the text:

1. The two exposures are listed as **separate items on a risk list**, not as two sides of one
   position.
2. There is **no holder map**. The Note never asks who holds each leg, and never identifies an
   institution holding both.
3. There is **no hedge-failure proposition**. It does not state that a holder of both is
   hedged at the extremes and unhedged in partial success, which is our centerpiece.
4. **Nothing is measured.** No level, no share, no dose. It is a qualitative workshop
   synthesis and says so.

**But it is closer than anything previously located, and closer than the previous audit knew,
so it is reported first rather than buried.** The distributional sentence above asserts, in
one line, the asymmetry our dose-response table measures. **Our contribution narrows
accordingly: we measure what this Note asserts.** That is a smaller claim than "we identified
the two-sided bet", and the paper must make the smaller claim.

### 3.3 What is ours, stated against the full text

The Note names the data gap it cannot fill, and it is our paper:

> "a key priority could be to **close data gaps** and strengthen diagnostic capabilities ...
> systematically tracking **indicators of AI diffusion, sectoral concentration, and labor
> market exposure** ... improved **measurement** of AI adoption and usage, combined with better
> data on **task-level impacts and investment flows**."

> "Fiscal analysis could incorporate **scenarios with persistent declines in labor income
> share**."

> a precondition for supervision is "improved **data collection on financial institutions'
> exposures to AI-sensitive sectors**".

| | IMF Note 2026/002 | this project |
|---|---|---|
| method | workshop synthesis, Chatham House Rule, no model | microdata plus the claim stock, one-command rebuild |
| the wage-leg credit mechanism | **asserted** | **measured**, by dose and by holder |
| the AI-leg leverage mechanism | **asserted** | **measured and bounded from below**, nine named filers |
| who holds each leg | **absent** | **ours**: 0.794 of the wage leg, 0.010 of the AI leg |
| hedge failure as a proposition | **absent** | **ours** |
| numbers of any kind | **none** | the whole paper |
| supervisory stress scenario | recommended in general terms | **ours**: severity against the Fed 2026 severely adverse, by loan category |
| trust fund arithmetic | "employment-linked social insurance becomes less effective" | **ours**: fund by fund against the 2026 Trustees tables, with depletion dates |

**One sentence for the paper:** the IMF's own scenario exercise identifies both exposures and
calls for exactly the measurement this paper supplies; it does not combine them into a single
holder-level position, and it produces no numbers.

---

## 3A. IMF Staff Discussion Note SDN/2024/002 (Brollo and others). NEW ROW, read in full

**Not in the previous audit at all.** "Broadening the Gains from Generative AI: The Role of
Fiscal Policies", June 2024, ISBN 979-8-40027-717-7, retained at
`data/raw/manual/IMF_SDN_2024_002_Generative_AI_Fiscal_Policies.pdf`. Level **F**.

This is the substantive fiscal companion to the 2026 Note, and it bears on three things in
this project.

**(a) It corroborates the top of our sourced capital tax range, from a different
construction.** Its Figure 14 puts the advanced-economy average tax rate on capital income at
roughly **0.20 to 0.22** in recent years, built from the Bachas and others (2022)
macro-historical database, with property and wealth taxes excluded "to better reflect taxes
affecting firms' automation decisions". **Our sourced maximum is 0.20351**, constructed
entirely differently as `0.351 x 0.21 + 0.649 x 0.20` on a rent-share decomposition. Two
unrelated constructions land on the same number.

**(b) It raises a vulnerability in our OPERATIVE rate, and this is reported against
ourselves.** The same series put the **US** average tax rate on capital well above our
operative effective rate of **0.0708**. The two are different objects: ours is the effective
rate on the **AI surplus** after profit shifting (Torslov, Wier and Zucman's 48 percent haven
share) and after the rent decomposition; theirs is an economy-wide average on all capital
income including personal-level taxes. **But a referee will put these side by side, and the
paper must pre-empt it:** the fiscal condition fails at 0.0708 and would be closer to closing
at the IMF's measured rate. The correct defence is the definitional one, stated up front, not
silence. **This is a new and real exposure in the paper's central fiscal result and it is
recorded as such.**

**(c) It independently confirms a project input on the US tax code.** Our tau_k decomposition
cites 26 USC 168(k). The SDN identifies the **United States among the ten economies whose
corporate tax bias most favours labour-saving assets** (Figure 10), naming the Tax Cuts and
Jobs Act's full expensing of acquired software and computer hardware from 2018 as the cause.
An IMF measurement of METR differentials reaches the same conclusion as our statutory reading.

**(d) It supplies MEASURED evidence for social-protection instruments, which our architecture
previously had only as precedent.** From Brollo (2024), IMF Working Paper 2024/095, on US
commuting zones:

- States with more generous unemployment insurance saw a decline in wages from robotisation
  **about two-thirds smaller** than other states, with the effect concentrated among workers
  **without a college degree**. Employment effects did not depend on UI generosity.
- **One additional robot per thousand workers raised the poverty rate by 0.3 percentage
  points**, a 3 percent increase, and most of that was attenuated where social assistance was
  more generous.
- Maximum UI benefit duration is usually **under 12 months**; the US at 26 weeks in most
  states is **on the low side of the OECD**.

**(e) It sets the literature's position on taxing AI, which our architecture must match.**
"**A specific tax on gen AI is therefore not recommended**", because the base is hard to
define, assets can be relabelled, and AI location is mobile. Instead: reconsider capital
allowances that favour labour-displacing assets, and strengthen **general** capital income
taxation. **This creates a live disagreement the paper should name rather than smooth over:**
Falk and Tsoukalas (2026) conclude a Pigouvian automation tax is the instrument that works;
the IMF concludes a specific AI tax is not implementable; Costinot and Werning's optimal robot
tax of 1 to 3.7 percent of the robot price sits between them. **Our contribution is none of
those verdicts: it is the calibrated break-even rate that says what any such instrument would
have to raise.**

### The boundary

| | SDN/2024/002 | this project |
|---|---|---|
| unit | cross-country, 74 to 85 economies, METRs and ATRs | one country, measured to the claim |
| capital tax rates | **measured, and we agree at the top of the range** | ours is the rate on the AI surplus specifically |
| social protection effects | **measured, and we should cite rather than rebuild** | ours is the obligation side they do not touch |
| household debt, mortgages, holders | **absent** | **ours** |
| the AI leg | **absent** | **ours** |

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
