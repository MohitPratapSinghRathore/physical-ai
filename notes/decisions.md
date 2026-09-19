# Decisions

Architectural and methodological decisions, with the tradeoff. Per PROJECT_BRIEF.md Rule 7,
decisions are made here and only escalated when irreversible or thesis-changing.

---

## D1. Series metadata is fetched, never asserted (2026-09-19)

Every FRED series is pulled together with its published title, units, frequency, seasonal
adjustment, source and last-updated date, stored in data/raw/fred/_manifest.json, and unit
scaling in the build is driven by the fetched units string.

Why: the first draft of src/sources.py hard-coded units from memory and got CMDEBT wrong
(millions, not billions), which would have understated US household debt by a factor of
1000. It also mislabelled four series, two of which (W019..., A576...) were the wrong
series entirely and one of which was discontinued.

Tradeoff: two HTTP requests per series instead of one, and the build fails if FRED changes
its page markup. Accepted: a silently wrong unit is far more costly than a loud failure.

## D2. Labor-tax dependence uses federal CURRENT RECEIPTS as the denominator (2026-09-19)

NIPA classifies contributions for government social insurance outside "current tax
receipts". Dividing labor-linked receipts by current TAX receipts yields 125 percent, which
is impossible and was caught for that reason.

Decision: denominator is federal current receipts (FGRECPT). Numerator is federal personal
current taxes (A074RC1Q027SBEA) plus federal contributions for government social insurance
(W780RC1Q027SBEA), both federal-only.

Tradeoff: excludes state and local labor taxation, so 77.7 percent understates the
all-government labor dependence. An all-government version is a later extension; the
federal figure is the one tied to the federal debt stock in Leg W, so it is the right
match for the thesis.

## D3. Leg W household and sovereign components are reported separately (2026-09-19)

The combined "Leg W broad" figure (186.1 percent of GDP) is a memo line only.

Why: household debt and federal debt are claims on the wage bill through different
mechanisms, held by different sectors, with different default and restructuring
technologies. Summing them implies a consolidation that does not exist and would invite a
referee to dismiss the headline number.

Tradeoff: a less dramatic headline. Accepted, per brief Section 8.8 (restraint).

## D4. Leg A definition gains a Tier 2b for off-balance-sheet financing (2026-09-19)

The brief's Tier 2 is hyperscaler capex from filings, split by funding source. BIS QR March
2026 documents that data-centre debt is commonly held in SPVs with the hyperscaler as
minority equity plus a long-term lease, deliberately off the hyperscaler balance sheet.

Decision: add Tier 2b, off-balance-sheet and SPV-financed data-centre debt, sourced from
BIS and private-credit aggregates, labelled as estimates with method shown. Filings-based
Tier 2 is reported as a LOWER BOUND, never as the measure.

Tradeoff: Tier 2b cannot meet the same evidentiary standard as filings data. Mitigated by
reporting all tiers separately and never blending an estimate into a hard-data total.

Consequence for the WS1 kill criterion: it must be evaluated on Tier 1 + Tier 2 + Tier 2b.
Evaluating it on filings alone would return a false "lopsided" verdict, because the
structures exist precisely to keep that debt out of the filings.

## D5. The exposure index is pulled forward from WS7 into the main paper (2026-09-19)

The brief defers occupational exposure work to WS7 as an optional sequel, and designates
the sizing table plus holder map as the paper's citable artifact.

Decision: build the Physical AI Exposure Index (PAEI) now, in the main paper.

Why:
- The brief's own Section 7.4 requires "one original quantitative artifact". The sizing
  table is an aggregation of existing official statistics; it is useful but it is not new
  measurement, and it is the kind of table that is superseded the moment an official body
  publishes its own.
- PAEI is new measurement. No existing index scores exposure to PHYSICAL AI specifically;
  the established measures (Frey-Osborne, Felten et al., Webb, Eloundou et al.) score
  cognitive or generic automation exposure.
- It is what makes the central hypothesis testable. The claim that Physical AI exposure
  concentrates in mid-income, high debt-to-income households is currently Tier 2
  ("our hypotheses, unverified") and cannot move to Tier 1 without an exposure measure to
  join to household debt microdata.
- Without it the paper is a taxonomy plus a threshold. With it the paper has an object
  other researchers must cite and can extend.

Tradeoff: scope growth in a paper already targeting 9,000-11,000 words, and the index
invites methodological attack that a pure framework paper would avoid. Accepted: the attack
surface is the point, because a measure that cannot be attacked cannot be used.

## D6. PAEI is multiplicative in two orthogonal factors, not an additive score (2026-09-19)

PAEI = P * S, P = embodiment intensity, S = environmental structure.

Why multiplicative: a robot displaces a task only if the task needs a body AND the
environment is structured enough to act in. Either condition failing means no exposure. An
additive index would score a high-embodiment, low-structure job (emergency plumber) as
highly exposed, which is the single most common error in this literature and is exactly
what Moravec's paradox predicts against.

Validation that this is not cosmetic: electricians score higher embodiment than team
assemblers (0.679 vs 0.551) but lower PAEI (0.256 vs 0.322). Correlation between P and S
across 911 occupations is -0.06, so the factors are close to orthogonal and the second
factor is doing real work.

Tradeoff: multiplicative form makes the index harder to decompose in regressions, and the
midpoint rescaling of S (enablers equal to frictions maps to 0.5) is a normalisation choice
that must be justified and sensitivity-tested. Both P and S are therefore published
alongside PAEI in data/processed/paei_onet.csv so others can re-aggregate.

## D7. Normalisation uses O*NET published scale anchors, not min-max (2026-09-19)

Each element is mapped to [0,1] using the minimum and maximum from O*NET's
Scales Reference.txt, not the observed range across occupations.

Why: min-max normalisation makes the index a purely relative ranking that silently changes
whenever O*NET adds or revises occupations, destroying comparability across releases. The
brief commits to annual updates of the artifact (Section 8.2), which requires a measure
that is stable across vintages.

Tradeoff: the index does not use the full [0,1] range (observed PAEI runs 0.02 to 0.43),
which looks less striking. Accepted; comparability matters more than presentation.

## D8. SEC filings are not accessed with a spoofed browser user-agent (2026-09-19)

SEC returns 403 to this environment with the message "Your Request Originates from an
Undeclared Automated Tool". A standard browser user-agent string succeeds.

Decision: do not do that. SEC's fair-access policy asks automated users to declare
themselves with a contact address. Escalated to the owner instead, as open question Q1.

Tradeoff: WS1 Tier 2 is blocked this session. Accepted; misrepresenting the client to a
regulator's data service to build a paper about financial regulation is not a trade worth
making, and a referee who learned of it would be entitled to distrust the whole pipeline.
