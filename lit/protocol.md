# WS0 Systematic Literature Audit: Protocol

Status: active. Registered before screening. Deviations are logged in Section 7.

Purpose: confirm, narrow, or refute the novelty statement in PROJECT_BRIEF.md Section 3.

## 1. Review question

Has any existing work treated wage-dependent liabilities (Leg W) and AI-capital-dependent
liabilities (Leg A) as two sides of a single transition-risk exposure, mapped their joint
failure across Physical AI scenarios, and derived a financial architecture per regime?

Three separable sub-questions, screened independently, because a paper may satisfy one and
not the others:

- Q1. Does the work model automation or AI displacement as a credit risk to household or
  sovereign balance sheets (Leg W as a financial exposure, not a labor outcome)?
- Q2. Does the work model AI capital expenditure as a credit or valuation exposure (Leg A)?
- Q3. Does the work hold Q1 and Q2 jointly in one exposure framework?

A paper answering Q1 and Q2 but not Q3 narrows our contribution. A paper answering Q3
triggers the kill or reshape criterion.

## 2. Databases and sources

Tier A (systematic, counted): Google Scholar, SSRN, arXiv (econ.GN, q-fin.GN, q-fin.RM),
RePEc/IDEAS, NBER working papers.
Tier B (systematic, counted): BIS, IMF, ECB, Federal Reserve Board and regional Feds,
Bank of England, OECD, FSB, NGFS.
Tier C (hand search, counted separately): reference lists of included papers (backward
snowballing) and citing articles (forward snowballing), one generation only.
Tier D (context, not counted as academic evidence): practitioner and press commentary.
Recorded because it establishes whether a framing is already in circulation, which bears on
novelty framing even when it carries no scholarly priority.

Scopus and Web of Science are NOT currently available to this project. This is a declared
limitation, logged in notes/open_questions.md. The audit is therefore reproducible but not
database-exhaustive in the strict PRISMA sense, and is reported as a structured search.

## 3. Query families

Executed as the cross product of blocks, with quoted phrases where noted.

- F1 Leg W as credit risk: (automation OR robots OR "artificial intelligence" OR AI) AND
  ("household debt" OR "mortgage default" OR "consumer credit" OR "student loan" OR
  delinquency OR "debt service")
- F2 Leg W sovereign: (automation OR AI) AND ("tax base" OR "fiscal sustainability" OR
  "payroll tax" OR "social security contributions" OR "sovereign debt")
- F3 Leg A: ("AI capex" OR "data center" OR "data centre" OR GPU OR robotics) AND
  (debt OR "private credit" OR ABS OR CMBS OR securitization OR "stranded asset")
- F4 Joint framing: ("two-sided" OR "both legs" OR "joint exposure" OR "offsetting
  exposure" OR hedge) AND (automation OR AI) AND ("financial stability" OR "bank capital")
- F5 Methodological analogue: "transition risk" AND ("stranded assets" OR "climate stress
  test" OR "scenario analysis") AND (bank OR "credit exposure")
- F6 Architecture: ("robot tax" OR "AI dividend" OR "universal basic income" financing OR
  "sovereign wealth fund" AI OR "income-contingent" OR "shared responsibility mortgage")
- F7 Macro foundations: ("so-so automation" OR "displacement effect" OR "indebted demand"
  OR "household leverage" crisis)

Date range: 2013-01-01 to 2026-09-19. Rationale: Frey and Osborne (2013) marks the start of
the modern occupational-exposure literature. Seminal earlier work enters via snowballing.
Language: English. Document types: journal article, working paper, official institution
report, conference paper. Excluded: theses, blog posts (Tier D only), news (Tier D only).

## 4. Screening

Stage 1 title and abstract. Stage 2 full text. Two-pass screening on a 10 percent random
sample for consistency; disagreements resolved by re-reading the inclusion rule.

Inclusion: the work must make a claim about a financial exposure (credit, valuation, or
fiscal), that is conditioned on an automation or AI adoption path.

Exclusion:
- E1 labor-market effects only, no financial exposure
- E2 finance only, automation is not a conditioning variable
- E3 firm-level AI adoption and productivity, no balance-sheet channel
- E4 AI applied to finance (credit scoring, algorithmic trading), which is a different topic
- E5 opinion or commentary without method or data (recorded as Tier D)

## 5. Extraction

Each included record is coded in lit/matrix.csv with: citation key, year, venue, type,
Q1/Q2/Q3 flags, method (theory, empirical, scenario, simulation, descriptive), sectors
covered, economies, whether stocks or flows are the object, policy instruments discussed,
and an explicit "gap relative to us" field.

## 6. Counts

Recorded per stage in lit/audit_report.md: identified, deduplicated, title/abstract
screened, full-text assessed, included, and reasons for full-text exclusion. A PRISMA-style
flow diagram is generated from these counts.

## 7. Deviations

Logged here with date and reason. None to date beyond the Scopus/WoS limitation in Section 2.
