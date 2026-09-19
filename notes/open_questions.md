# Open questions and blocked sources

Owner decisions are marked DECISION NEEDED. Everything else is a work item.

Last updated: 2026-09-19.

---

## DECISION NEEDED

### Q1. RESOLVED 2026-09-19: SEC EDGAR access

SEC returns HTTP 403 to this environment: "Your Request Originates from an Undeclared
Automated Tool". SEC's fair-access policy asks automated users to declare themselves with a
contact address in the User-Agent header. A generic browser user-agent string does work,
but sending one would misrepresent the client to a financial regulator's data service, and
that is not a trade worth making for this paper (decision D8).

This blocks WS1 Leg A Tier 2 entirely. No Leg A number exists yet.

Options:
1. Supply a contact email to declare in the User-Agent. This is the normal, intended route
   and is what SEC asks for. It publishes that address to SEC in request logs.
2. Use a project-specific address rather than a personal one.
3. Download filings manually and drop them in `data/raw/sec/`.
4. Use a commercial data provider instead.

RESOLVED: the owner supplied `team@oviguide.in` as the declared contact address. It is set
in `src/fetch_sec.py` and Leg A Tier 2 is built (findings B4). Tiers 1 and 2b remain open.

### Q2. CLOSED: repository ownership

The repository lives under `MohitPratapSinghRathore`. Owner decision 2026-09-19: leave it
there. Noted so that the Zenodo DOI and replication package inherit that identity
deliberately rather than by accident.

### Q3. Co-author recruitment (brief Section 8.7)

The brief asks for candidate names with macro-finance or central bank credentials, found
during WS0. Candidates will be logged here as WS0 proceeds. None recorded yet: the audit
has completed only the first query batch.

---

## Blocked or paywalled sources

| Source | Status | Blocks | Workaround |
|---|---|---|---|
| SEC EDGAR XBRL | RESOLVED, contact address declared | - | - |
| BLS OES | HTTP 403 to this environment | employment and wage weights for PAEI | ACS PUMS used instead; OES still wanted for occupation-level wage bills |
| IFR World Robotics | paid | robot stock and shipments, WS1 | ask owner whether to purchase |
| Scopus / Web of Science | subscription | strict PRISMA coverage in WS0 | audit currently documented as a structured search, declared as a limitation |
| Preqin | paid | private credit to AI infrastructure, Leg A Tier 2b | BIS aggregates as a labelled estimate |
| Census API | free key required | nothing | bulk PUMS files used, no key needed |

---

## Work items, in priority order

1. **Consumer credit DAR.** The mortgage result (findings A4) came back flat. The brief's
   concentration hypothesis is most likely to survive on consumer credit, auto loans and
   rent arrears, where low-wage high-PAEI workers actually sit. ACS PUMS cannot see these.
   Needs SCF (public, free) or credit-bureau microdata. This is the single highest-value
   next test in the project.

2. **PAEI validation against existing indices.** Correlate PAEI against Frey-Osborne,
   Webb, Felten et al. and Eloundou et al. If PAEI is highly correlated with an existing
   cognitive-AI measure, its claim to be measuring something new fails. Expected and
   required result: low or negative correlation with cognitive-AI exposure measures. This
   test must be run before the index is published, not after.

3. **PAEI expert validation.** The brief's WS7 sketch calls for human validation. At
   minimum: a blind review of the top and bottom 30 occupations by two people with
   robotics or industrial-engineering background, plus a documented sensitivity analysis
   over element selection and over the S midpoint normalisation (decision D6).

4. **tau * s threshold.** Not touched this session. The brief flags it as the result most
   worth getting right (Section 8.3). Derivation must be checked, assumptions stated, and
   the open-economy leakage case written out.

5. **Leg A Tiers 1 and 2b.** Tier 2 is built. Tier 1 (GPU-backed lending, data-centre ABS
   and CMBS) and Tier 2b (off-balance-sheet SPV debt, from BIS and private-credit
   aggregates) are what the kill criterion actually needs. Until they exist the 2.14
   percent ratio is a lower bound and must not be reported as the answer.

6. **Holder map (WS2)**, not started. Note that findings A5 raises its value: if mortgage
   exposure cannot be diversified by occupation, the question of which institutions hold
   that undiversifiable exposure becomes the central empirical object of the paper.

7. **Stock version of DAR.** PUMS gives debt service, not balances. SCF gives balances.

8. **Other economies.** Everything so far is United States only. The euro area via HFCS is
   the natural second case, and HFCS has both occupation and debt, so it can carry a DAR
   replication that PUMS cannot.

---

## Methodological questions not yet resolved

- MRGP includes escrowed property taxes and insurance where the respondent reports them in
  that field, so mortgage "debt service" is overstated by an unknown amount. SMOCP and
  TAXAMT are in the data and could bound this. Not yet done.
- PAEI aggregation from O*NET-SOC to 6-digit SOC is an unweighted mean across detail
  occupations, because employment weights at O*NET detail level require OES, which is
  blocked. This should be revisited if OES becomes available.
- Attributing household mortgage service by each earner's share of household wage income
  assumes debt service is shared in proportion to earnings. Alternatives (primary earner
  only, equal split) should be run as a sensitivity.
- The index treats a point-in-time occupation as the unit of exposure. It says nothing
  about when displacement occurs, and the paper must not let the reader infer a timeline
  from it.
