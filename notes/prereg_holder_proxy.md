# Pre-registration: mortgage holder proxy by exposure type (item 4)

**Committed before the analysis was run.** No holder-proxy result exists at this commit.
The FHFA 2025 conforming loan limit file was downloaded in the same session but had not been
joined to any exposure data when this was written.

Date: 2026-09-19.

## Registered hypothesis

> Embodied mortgage exposure sits predominantly in agency, FHA and VA eligible loans.
> Cognitive exposure has a materially higher jumbo share.

Directional predictions:
1. The share of mortgaged owner households whose implied loan exceeds the county one-unit
   conforming limit is **higher for cognitive-exposed than for embodied-exposed** households.
2. The share in low-home-value markets, where FHA and VA lending is concentrated, is
   **higher for embodied** households.
3. Combined with Z.1 holder shares, embodied mortgage exposure therefore lands
   disproportionately on **GSE and agency pools plus Ginnie Mae (FHA/VA)**, and cognitive
   exposure disproportionately on **bank portfolios**, which is where jumbo lending is held.

## Method

- PUMS 2023 mortgaged owner households (TEN == 1) with VALP, by exposure class from the
  four-way split (cognitive only, embodied only, both, neither).
- Implied original loan = VALP x LTV, over a STATED RANGE of LTV at origination
  (0.80 central; 0.70 and 0.90 as bounds). Current VALP is not the origination value, so
  this is a proxy and is labelled as one.
- County one-unit conforming limit from FHFA 2025 (HERA-based, flat file). PUMA to county
  via the tract-based allocation already in the repository.
- Jumbo proxy = implied loan above the county limit.
- Low-value market proxy = county median home value in the bottom tercile nationally.
- Z.1 holder shares applied to give exposure by holder class, with bounds.

## What this proxy CANNOT do, stated in advance

- PUMS has no loan balance, no origination date, no LTV, and no lender. VALP is a
  self-reported CURRENT value, so the implied loan is wrong for every household
  individually and is only usable in distribution.
- No public data links borrower occupation to loan holder. This is a proxy built from the
  joint distribution of occupation, home value and county, not an observation of who holds
  whose mortgage. It must be labelled as a proxy everywhere it appears.
- FHA and VA shares by county were NOT obtained; the low-value-market proxy stands in for
  them and is weaker.

## Interpretation fixed in advance

- If confirmed, embodied mortgage exposure is effectively sovereign (agency and Ginnie Mae),
  which changes who absorbs it and is a major finding either way.
- If refuted, the two exposure types share holder composition and the holder map adds
  nothing to the comparative thesis.
