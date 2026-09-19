# Pre-registration: the cognitive contrast

**Committed before the analysis was run.** Git history is the evidence: this file is
committed in a commit that contains no cognitive-contrast results.

Date: 2026-09-19.

## Question

Where does wage-backed household debt actually sit: with cognitively exposed workers or
with physically exposed ones?

## Registered hypothesis

> Mortgage debt, total debt and debt service concentrate in cognitively exposed households,
> and buffers are thicker there.

Directional predictions, stated in advance:

1. Mortgage DTI: **higher** for top-quintile cognitively exposed households than for
   households with no exposed worker, and higher than for embodied households.
2. Total debt to income: **higher** for cognitively exposed.
3. Liquid buffer under one month of income: **lower** share (thicker buffers) for
   cognitively exposed.
4. Share of national mortgage debt service held: **higher** for top-quintile cognitive than
   for top-quintile embodied.
5. The P1r fiscal wedge per displaced dollar: **larger** for cognitive work, because
   cognitively exposed workers earn more and face higher effective labour tax rates.

## Method, identical to A31

Same source (SIPP 2025, December reference month), same household weighting (reference
person, ERELRPE in (1,2)), same restricted sample (at least one employed member, reference
person aged 25 to 64), same adjustment set (reference-person age, household size, number of
earners, region, household income), same twelve debt measures, same buffer and asset
measures, same replicate-weight inference (Fay, rho = 0.5, 240 replicates).

Cognitive exposure is measured with the already-crosswalked Felten, Raj and Seamans AIOE and
Eloundou et al. GPT exposure, in place of embodiment P. Top quintile is employment-weighted.

## Full disclosure

Every measure examined will be reported, including nulls and wrong-signed results. No
selection.

## Interpretation fixed in advance

- If the hypothesis is CONFIRMED, the household-credit leg of the two-sided bet is primarily
  a cognitive-AI exposure, not a Physical AI one. That WEAKENS the Physical AI framing of
  the paper and must be led with.
- If the fiscal wedge is also larger for cognitive work, the fiscal channel is also
  predominantly a cognitive-AI channel, which weakens the framing further. This is the
  single most damaging possible result for the current paper and will be reported first if
  it occurs.
- If the hypothesis is REFUTED, the Physical AI framing survives on the household side and
  the paper's current structure stands.

## What this comparison is NOT

Cognitive AI exposure indices measure **task overlap**, not displacement, and not timing.
Webb, Felten and Eloundou all score what a technology could in principle touch. This
comparison is about **where wage-backed debt sits**, not about which technology arrives
first or which causes more displacement. That distinction must be stated wherever the
result is reported.

---

## AMENDMENT 1 (2026-09-19): H3, geography. Registered BEFORE running.

Added on owner instruction under the scope change (D22). **No geographic analysis of
cognitive exposure has been run at the time of this amendment.** H1, H2 and H4 below map to
predictions 1 to 5 in the original registration, which was committed before any results.

**H3. Cognitive exposure is geographically CONCENTRATED** (Gini, p90/p10 and p99/p1 of the
at-risk rate across PUMAs and counties) **and correlates with local house price levels,
unlike embodied exposure.**

Directional predictions:
- Gini and p99/p1 of the cognitive at-risk rate exceed those for all embodied work (which
  came in at county Gini 0.141, p99/p1 3.85 in A28).
- The correlation between the county cognitive at-risk rate and local house values is
  positive and materially larger than for embodied exposure.

Interpretation fixed in advance: if H3 holds, the two exposure types differ not only in
whose balance sheet they touch but in where, which would make the geographic argument a
contrast rather than a Physical AI finding. If H3 fails, embodied and cognitive exposure
share a geography and the geographic result is about employment density, not technology.

House prices: ACS median home value by PUMA from the PUMS housing file (VALP), and FHFA HPI
by county if the download succeeds. FHFA has failed twice from this environment.
