# Related work: the labour backing ratio, the fiscal mechanism and the stress-test framing

**PROVISIONAL. Produced 2026-09-20 in the labour backing session.** This table exists
because the owner's own search located a set of works that overlap this project more
closely than `lit/audit_report.md` recorded. **It narrows several of this project's
novelty claims and one of them it retires.** That is reported first, per hard rule 5.

## Verification status, stated per item and not in aggregate

No citation below is asserted without a check. Three levels are used and every row carries
one:

| Level | Meaning |
|---|---|
| **F** | Publisher page or full text read directly from this environment on 2026-09-20 |
| **B** | Bibliographic record verified (title, authors, venue, identifier) but the full text was NOT readable from here. The publisher blocked the request or only a record was reachable |
| **U** | Not verified. Goes to `lit/unverified.md` and carries no dependent claim |

**Nothing here is level U.** Two publishers, RAND and the IMF e-library, return HTTP 403
to this environment, so their rows are level B and their content is described from the
publisher's own abstract as surfaced by search, never from a paraphrase of a paraphrase.

---

## The table

| # | Work | Level | Method and data | What it claims | Overlap with us | What remains ours |
|---|---|---|---|---|---|---|
| 1 | **Chen, Xupeng (2026), "Abundant Intelligence and Deficient Demand: A Macro-Financial Stress Test of Rapid AI Adoption", arXiv 2603.09209, 10 March 2026** | F | Theoretical model plus calibrated simulation on FRED and BLS. Eleven testable predictions | A distribution-and-contract mismatch: AI abundance with demand deficiency. Three mechanisms: a displacement spiral, "ghost GDP", and intermediation collapse. High earners drive 47 to 65 percent of US consumption and are most exposed, so transmission runs **into private credit and mortgage markets** | **THE LARGEST OVERLAP IN THE SET, and it is with our SECOND-ROUND module.** Displacement reduces labour income, which reduces demand, which transmits to mortgage and private credit. That is claim 154 and claim 158. It also anticipates our top-quintile result (claim 144) | Our second round is **measured against a named supervisory benchmark** (the Fed 2026 severely adverse scenario) and decomposed by **holder**. Chen has no holder map, no GSE or FHA split, no trust fund arithmetic, and no claim-stock measurement. The 9:1 second-to-first-round ratio is ours |
| 2 | **Falk, Brett Hemenway and Tsoukalas, Gerry (2026), "The AI Layoff Trap", arXiv 2603.20617, 21 March 2026** | F | Economic model of firm automation decisions under a demand externality | Each firm captures the full cost saving from automation but bears only a fraction of the demand loss, so competition produces excessive automation. **Wage adjustment, free entry, capital income taxes, worker equity, UBI, upskilling and bargaining all fail to resolve it. A Pigouvian automation tax can** | **Directly relevant to the amended claim 168 and to item 0a of this session.** They reach by theory the conclusion we reached by arithmetic: a capital income tax is not the instrument. Their result is stronger than ours, being general rather than calibrated | Ours is a **calibrated break-even rate on sourced effective rates** (case A 0.125 to 0.301, case B 0.182 to 0.650) against an operative rate of 0.0708, not an impossibility theorem. The two are complements: they say the instrument is wrong in principle, we say it is unavailable in fact |
| 3 | **Price, Carter C. and Suresh, Akshaya (2026), "Federal Revenue When AI Replaces Labor: An Examination of Economic Scenarios with Highly Capable Artificial Intelligence", RAND, RR-A4980-1** | B | Scenario simulation of US federal revenue | 84 percent of 2024 federal revenue came from individual or payroll taxes, both collected on worker income, so federal revenue is highly vulnerable to labour-displacing AI. Varies **whether displaced workers are reemployed** and **how AI is priced**, monopolistically or at cost | **THIS RETIRES OUR PRIORITY CLAIM ON THE FISCAL MECHANISM.** Their two axes are our rho (reemployment) and our tau_k (how much surplus is taxable). Their 84 percent is our labour-linked receipts share. The mechanism is not ours and must not be presented as ours | The **financial-stability half**: household balance sheets, the holder map, the GSE and FHA split, bank capital, and the claim-stock measurement. Publisher blocked, so this row is level B and the boundary should be re-checked against the full text before the paper is submitted |
| 4 | **Ieong, Trish; Saputra, Akbar; Maniar, Anuja and Cheng, Deric (2026), "Mapping Tax Risks From Labour-Displacing AI", Windfall Trust, 13 May 2026** | F | Scenario-based fiscal accounting for an "average OECD country". Two parameters: labour market disruption (low, medium, high) and domestic value capture (high, low) | Four channels: (i) labour is taxed more heavily than capital, so displacement shifts revenue to a lower-taxed base; (ii) international tax leakage when earnings are replaced by non-resident AI capital income; (iii) consumer surplus is untaxable; (iv) spending rises | Channel (i) is our tau_l against tau_k. Channel (ii) is our profit-shifting result (claims 54 and 55) and our open-economy India contrast. **The fiscal mechanism is independently established here too** | Confirmed directly from the publisher page: it **does not address household debt, mortgages, bank balance sheets, financial institution exposures or financial stability at all**. The entire second half of our paper is outside it. Also ours: a single-country measurement rather than an OECD average |
| 5 | **Korinek, Anton and Lockwood, Lee M. (2026), "Public Finance in the Age of AI: A Primer", Brookings working paper, 8 January 2026; NBER Working Paper 34873** | B | Optimal taxation theory across two stages of AI transformation | Labour-income-based tax systems erode exactly when redistribution is most needed. Consumption taxation may become the primary instrument and differential commodity taxation regains relevance | Our fiscal framing sits inside theirs. **Note also a citation-hygiene item: the repository carries `KorinekLockwood2025_public_finance_AI.pdf` and this is the superseded title.** `paper/references.bib` must be updated to the January 2026 Brookings and NBER 34873 version | Ours is measurement, not optimal taxation. We produce an operative effective rate and a break-even rate; they produce an instrument ranking |
| 6 | **Casas, Pablo and Torres, José L. (2024), "Government size and automation", International Tax and Public Finance 31(3), 780 to 807** | B | General equilibrium model of automation and government size | Automation shifts the tax base from labour to capital and changes the sustainable size of government | Establishes the base-shift mechanism in the peer-reviewed literature two years before this project. Our contribution cannot be "noticing that automation erodes the labour tax base" | The dose-response calibration and everything on the liability side |
| 7 | **Manning, Sam; Aguirre, Tomás; Muro, Mark and Methkupally, Shriya (2026), "Measuring US workers' capacity to adapt to AI-driven job displacement", Brookings, January 2026; related NBER Working Paper 34705** | B | Occupation-level adaptive capacity index combining AI exposure with savings, age, labour market density and skill transferability | **AI exposure and adaptive capacity are POSITIVELY correlated**: 26.5m of the 37.1m workers in the top exposure quartile are in occupations with above-median adaptive capacity | **THIS IS THESIS-WEAKENING AND IS REPORTED AS SUCH.** It cuts against the implicit direction of our household buffer work and is the external counterpart of our own claim 145 (buffers are not monotonic in pay) and our pay-control result (claim 139). It also overlaps our use of liquid buffers directly | Ours measures **obligations** (debt service, balances, loss given default) rather than **adaptability**, and routes them to holders. Their index is an input we do not have and should cite rather than rebuild |
| 8 | **International Monetary Fund (2026), "Global Economic and Financial Implications of Artificial Intelligence: Lessons from a Scenario Planning Exercise", IMF Notes 2026/002** | B | Scenario planning exercise, five-year horizon, two diffusion trajectories (baseline and runaway) | Transition dynamics strain fiscal frameworks through erosion of labour tax bases and rising social spending, particularly where social insurance is employment-linked. Capital income taxes should be strengthened | **Our audience is this institution and it has already published the framing.** The employment-linked social insurance point is our trust fund result (claims 120, 161, 190) | Our trust fund arithmetic is **measured against the 2026 Trustees tables**, fund by fund, with depletion dates. The IMF note is a scenario exercise without that arithmetic |
| 9 | **Congressional Budget Office (2024), "Artificial Intelligence and Its Potential Effects on the Economy and the Federal Budget", December 2024** | B | CBO budget analysis | AI's potential effects on the economy and the federal budget | Located during this search and NOT previously in the audit. A US-specific official fiscal analysis predating this project | To be read before submission. Flagged as an audit gap |
| 10 | **Federal Reserve Board, Household Debt Service and Financial Obligations Ratios (DSR); and the Enhanced Financial Accounts, including the Distributional Financial Accounts** | F | Published statistical programme | Debt service as a share of disposable income; distributional balance sheets by wealth percentile | **This is the closest thing to our ratio that exists and it is the reason the novelty gate is narrow.** The DSR denominator is ALL income, explicitly including capital income, with no labour decomposition. The DFA distributes balance sheets by wealth percentile but not by income TYPE | The labour decomposition itself, and the extension beyond the household sector to Treasury, municipal, multifamily and agency claims. **The DFA is used as an input to B11 and B12 in this session rather than treated as a competitor** |
| 11 | **Lustig, Hanno; Van Nieuwerburgh, Stijn and Verdelhan, Adrien (2013), "The Wealth-Consumption Ratio", Review of Asset Pricing Studies 3(1), 38 to 94; NBER Working Paper 13896 (2008)** | B | Exponentially affine stochastic discount factor estimated on bond yields and stock returns | The wealth-consumption ratio is high and most US household wealth is HUMAN wealth. Long-term bond markets, not stock markets, drive total wealth fluctuations | The **mirror image** of our ratio, as `feasibility.md` section 1(a) already recorded. They price labour income as an ASSET. We measure the share of the LIABILITY side serviced out of it | The liability-side direction. A high human-wealth economy can have a low labour backing ratio and the reverse, so the two are not substitutes |

---

## What this does to the novelty claims, restated as narrowly as the table requires

The old formulation, "no published work links occupational AI exposure to household
balance-sheet outcomes" (claim 85, provisional, non-systematic search), **is no longer
adequate.** It was true as written and is now misleading by omission, because it says
nothing about the fiscal half, which several of these works cover directly and better.

**RETIRED as a priority claim.**

- **The fiscal mechanism.** That wage-based public finance makes labour displacement a
  revenue event is established in Casas and Torres (2024), Korinek and Lockwood (2026),
  Price and Suresh (2026), the Windfall Trust (2026) and the IMF (2026). **This project
  did not discover it and must not imply that it did.** What the project adds is a
  calibrated US measurement with an operative effective rate and a break-even rate.

**NARROWED.**

- **The stress-test framing.** Chen (2026) is explicitly a macro-financial stress test of
  rapid AI adoption and reaches private credit and mortgages. The framing is not ours.
  What remains ours is severity expressed against the **Federal Reserve's own 2026
  severely adverse scenario**, loss rates by loan category, and the decomposition by
  holder, which is what a stress-test designer actually needs and which none of these
  works provides.
- **The capital tax verdict.** Falk and Tsoukalas (2026) reach it in theory first. Ours is
  the calibration, and after this session's item 0a it is a narrower claim than it was.

**SURVIVING, and they are narrower than the paper's current framing.**

1. **The labour backing ratio itself**, a system-wide decomposition of the claim stock by
   the income TYPE that services it. Nothing in this table computes it. The Fed DSR is the
   nearest and its denominator is undifferentiated income.
2. **The holder map of labour-backed claims**, and the finding that the federal government
   holds, guarantees or owes about four fifths of them.
3. **The two-sided bet by holder** (B11), and the payoff table across AI outcomes (B12).
   No work in this table puts the wage leg and the AI leg on one holder axis.
4. **The hiring-freeze blind spot** (claims 80, 93, 94). Brynjolfsson, Chandar and Chen
   (2026) measure the entry-level effect; the deduction that it is invisible to the
   Displaced Worker Survey and to every dashboard indicator is still ours. **But see the
   caution below.**
5. **The early-warning dashboard.** Still ours as an artifact. **The claim of priority is
   weak** and should be dropped: an indicator list is not a research contribution, and the
   IMF note and the Windfall Trust report both effectively propose monitoring.

## Cautions on the two claims that look strongest

- **The hiring-freeze blind spot** rests on our own deduction plus one external paper. It
  has not been tested against the Manning and others adaptive-capacity work, which reaches
  the opposite-signed conclusion about who can absorb displacement. Treat it as
  provisional until that comparison is done.
- **The labour backing ratio novelty gate remains the one in `feasibility.md`**: the search
  is now systematic for this question but a statistic this simple may exist inside a
  central bank without being published. A direct approach to the Federal Reserve Financial
  Accounts team is still the right next step and has not been made.

## Sources

- https://arxiv.org/abs/2603.09209
- https://arxiv.org/abs/2603.20617
- https://www.rand.org/pubs/research_reports/RRA4980-1.html
- https://windfalltrust.org/publications/mapping-tax-risks-from-labour-displacing-ai
- https://www.brookings.edu/wp-content/uploads/2026/01/Korinek-Lockwood-FINAL-for-website.pdf
- https://www.nber.org/papers/w34873
- https://ideas.repec.org/a/aiy/jnljtr/v4y2018i1p6-26.html (search route to Casas and Torres; the record itself is International Tax and Public Finance 31(3), 780 to 807)
- https://www.brookings.edu/articles/measuring-us-workers-capacity-to-adapt-to-ai-driven-job-displacement/
- https://www.nber.org/papers/w34705
- https://www.elibrary.imf.org/view/journals/068/2026/002/article-A001-en.xml
- https://cbo.gov/system/files/2024-12/60774-AI-fed-budget.pdf
- https://www.federalreserve.gov/releases/efa/efa-distributional-financial-accounts.htm
- https://academic.oup.com/raps/article-abstract/3/1/38/1575308
