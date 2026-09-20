# Unverified and partially verified references

Per PROJECT_BRIEF.md Rule 1, anything not fully verified lives here and does not enter
references.bib until it is.

## Partially verified

### BIS Quarterly Review, March 2026: "Financing the AI infrastructure boom"

- Title VERIFIED: "Financing the AI infrastructure boom: on- and off-balance sheet borrowing"
- Publication VERIFIED: BIS Quarterly Review, March 2026
- Date VERIFIED: 16 March 2026
- URL VERIFIED: https://www.bis.org/publ/qtrpdf/r_qt2603u.htm
- Substantive claims VERIFIED verbatim (SPV structures, minority stake, long-term leases,
  "shadow borrowing"), see notes/findings.md A9
- **AUTHORS NOT YET VERIFIED.** BIS Quarterly Review features are individually authored but
  the author names were not present in the fetched page content. Must be read from the PDF
  before this enters references.bib.

Dependent claims currently in the repository: findings A2, decision D4, notes/sizing_method.md.
These rest on the substantive content, which is verified, not on the author list.

## Unverified

None outstanding.

## Verified and corrected

### Bayraktar (2026), arXiv 2605.05127

PROJECT_BRIEF.md Section 3 cited this as "The Demand Externality of Automation". That is a
superseded v1 title. Verified current record:

- Title: "Automation, Income Incidence, and Capital Accumulation in Incomplete Markets"
- Author: Erhan Bayraktar (single author)
- Submitted: 6 May 2026
- arXiv: 2605.05127
- Classifications: econ.GN, math.OC

Do not cite the superseded title.

## Not verified, recorded so it is not used by accident

### Morgan Stanley projection of private-credit data-centre financing

- Claim as encountered: private credit will provide a further 800 billion USD of data-centre
  financing over the next two years.
- Encountered in: a web search result summary, 2026-09-19, while verifying the Chicago Fed
  Leg A article.
- Status: NOT VERIFIED. No primary Morgan Stanley publication was located or read, no date,
  no author, no methodology. The figure is a secondary restatement.
- Use: NONE. It is mentioned in findings A45 only as a named reason why the Chicago Fed
  bank-channel figure is a LOWER BOUND on Leg A, and no arithmetic anywhere in this
  repository uses it.

### BLS Displaced Worker Survey, reemployment rate (rho) -- RESOLVED 2026-09-19

- Status: NO LONGER BLOCKED and NO LONGER UNVERIFIED. BLS became reachable from this
  environment and the release was read directly. rho = 0.6616 and omega = 0.9554 (range
  0.9050 to 1.0103) are sourced in data/SOURCES.md with table numbers, reference period and
  every derivation assumption, and computed in src/bls_dws.py.
- This entry is kept only so the earlier "blocked" statements in findings A41 and A45 can be
  traced to their resolution.

## FHA Mutual Mortgage Insurance Fund, FY2025 (added 2026-09-20)

**NOT VERIFIED AGAINST THE PUBLISHER.** hud.gov returns HTTP 403 to this environment on
every route tried, including the annual report PDF and the HUD press release. The figures
below come from secondary reporting of the FY2025 FHA Annual Report to Congress and are
used in the analysis as a FLAGGED PROXY, never cited in the bibliography.

- MMI Fund capital ratio FY2025: **11.47 percent**, against a statutory minimum of 2 percent
- Insurance in force: about **1.647 trillion dollars**
- Economic net worth: about **188.9 billion dollars**

**A discrepancy in the secondary sources, resolved arithmetically.** One outlet reports
economic net worth of 118.87bn and another 188.87bn. The capital ratio times insurance in
force is 0.1147 x 1,647bn = 188.9bn, so 118.87 is a transposition and 188.87 is the
internally consistent figure. This is a consistency check, not a verification.

**The exact document is the FHA Annual Report to Congress on the Financial Status of the
MMI Fund, FY2025, and the accompanying Annual Actuarial Review.** If the owner places
either in `data/raw/manual/`, the flag is removed and the figure is cited.

---

## Added in the final analysis session, 2026-09-20

### Congressional Budget Office (2024), "Artificial Intelligence and Its Potential Effects on the Economy and the Federal Budget", December 2024

- **NOT VERIFIED FROM THIS ENVIRONMENT.** `cbo.gov` returns HTTP 403 on every route
  attempted, including the publication page and the direct PDF path; the block is a
  DataDome bot challenge rather than a missing page. Crossref has no record, which is
  expected: CBO reports carry no DOI.
- It was named as a bibliography gap and located by title in a secondary search only.
  **It does NOT enter `paper/references.bib` and no claim in this project depends on it.**
- Recorded in the related-work table at verification level U, not B.
- To clear: read the PDF from a network that CBO does not block, confirm the title, the
  publication number and the December 2024 date, then move the entry into
  `references.bib` and upgrade the related-work row.

### IMF Note 2026/002 (Barhoumi and others). CLEARED 2026-09-20

**RESOLVED.** The owner placed the PDF at
`data/raw/manual/IMF_Note_2026_002_AI_Scenario_Planning.pdf`. It has been read in full, the
related-work boundary has been redrawn in `lit/related_work_final.md` section 3, and the entry
is now in `paper/references.bib` as `Barhoumi2026`. Verification level **F**.

The owner also placed **IMF SDN/2024/002 (Brollo and others, June 2024)**, which was not in
the audit at all. Read in full, added as `Brollo2024`, boundary in
`lit/related_work_final.md` section 3A.

**Neither is unverified any longer. The only remaining item in this file is CBO (2024).**

---

## A113: the tau_k components. Seven parameters and one institutional status.

Added 2026-09-20 during the component rebuild of the effective capital tax rate on AI
surplus (`framework/tau_k/`). **Every item below was sought from a primary source in that
session and not obtained. None of them carries a dependent claim.** They are swept over
ranges bounded by statute or by structure, and the bound is named in
`framework/tau_k/components.py`. The map in `paper/figures/tau_k_map.png` exists because
these could not be pinned.

| parameter | range swept | bound on the range | what was sought and what happened |
|---|---|---|---|
| shareholder rate on dividends and realised gains | 0.15 to 0.238 | statutory ceiling: 20 percent top long-term rate plus the 3.8 percent net investment income tax | a sourced average realised rate across the holder distribution |
| state effective corporate income tax rate | 0.00 to 0.095 | state statutory rates run from zero to the high single digits | a verified apportioned effective rate |
| marginal debt share of AI capital spending | 0.00 to 0.40 | a share; zero is the all-equity structure reported on the nine filers' own books in Module B | a verified marginal debt share |
| bondholder marginal rate | 0.15 to 0.37 | ordinary income treatment, so the top ordinary rate is the ceiling | a sourced average bondholder rate |
| shifted share of rents | 0.30 to 0.60 | a share, centred on the one verified value | **the task required two or more verified sources.** Torslov, Wier and Zucman at 0.48 is verified in this repo. A second was sought from Clausing (NBER w28442) and from Garcia-Bernardo, Jansky and Zucman (NBER w30086, title verified as "Did the Tax Cuts and Jobs Act Reduce Profit Shifting by US Multinational Companies?", abstract not retrievable). Neither abstract could be read. **The single verified value is therefore not used as a point; the parameter is swept** |

**OECD Pillar Two, the 15 percent global minimum, current status for US-parented groups as
of 2026. NOT VERIFIED.** The OECD topic and BEPS pages returned HTTP 403 in this session. No
primary source confirming whether the minimum currently binds on US-parented groups, or on
AI rents specifically, was obtained. **It is used nowhere in the assembly.** It appears on
the map as a marked reference line at 0.15 with its status printed beside it. The only
statement made about it is arithmetic and conditional: 0.15 exceeds the required 0.1101 to
0.1373, so wherever such a floor genuinely bound, the condition would pass on the rent
component. Whether it binds is the unverified part.

**To clear any of these**: obtain the primary source, replace the swept range with a point
and a range in `components.py`, rerun `assemble.py`, and move the row out of this file. The
two worth doing first are the taxable-shareholder share and the deferral factor, which
between them carry 62 percent of the first-order variance in the assembled rate.

### A114 addendum: item 2(g), the labour component of AI capital spending

Two further parameters, sought and not obtained, swept and carrying no dependent claim.

| parameter | range swept | bound on the range | what was sought and what happened |
|---|---|---|---|
| labour share of AI capital spending | 0.20 to 0.55 | a share of value added, [0,1]; bounded below by capital-intensive semiconductor fabrication and above by labour-intensive construction and software, with the truth a weighted mix that must lie between | BEA GDP-by-industry compensation shares for computer and electronic product manufacturing, software publishing and nonresidential construction. BEA iTable requires an interactive query; the FRED CSV endpoint timed out on every series attempted |
| import share of AI capital spending | 0.25 to 0.70 | a share, [0,1]; bounded below by the predominantly offshore fabrication of advanced logic and memory, above by the necessarily domestic data centre construction, power interconnection and integration labour | Census foreign-trade exhibit 8, advanced technology products, returned HTTP 404. No primary substitute obtained |

**Neither is used in the assembled rate.** Item 2(g) contributes zero to tau_k for a
structural reason that does not depend on either value: the compensation in question is
already inside the wage bill and inside the retained wage share R, so crediting it to tau_k
would double count it. See `framework/tau_k/labor_component.py`. The two parameters are used
only to size the import leakage, which is reported as a scenario.

### A115: two of the A113 items are CLEARED

**The taxable-shareholder share and the deferral factor are no longer unverified.** The owner
supplied the source documents and both were read and recorded. They have been removed from
the A113 table above and now carry dependent claims.

| parameter | sourced range | source |
|---|---|---|
| taxable-shareholder share of US corporate equity | **0.24 to 0.28, central 0.27** | Rosenthal and Austin, Tax Notes, 16 May 2016, p. 923, Table 2 (0.242, C corporation stock, 2015); Rosenthal and Burke 2020 via CRS R47113 note 9 (0.25); Rosenthal and Mucciolo, Tax Notes Federal 183(1), 1 April 2024, Table 5 (0.27 total US equity, 2022) and Table 7 (0.28 publicly traded) |
| deferral factor on capital gains | **0.412 to 0.790, central 0.601** | CRS R47113 Table 5, third row, before its taxable-share adjustment so theta is not double counted. Cross-checked at 0.488 from CBO 2014 Tables A-3 and A-4 (46.9 percent of gains held until death and untaxed) |

Full extraction, with the method and the holder breakdown, is in
`notes/sources/SHAREHOLDER_PARAMS_extracted.md`. **The four source PDFs were supplied in
session and are named there for placement on disk.**

### A116: the bondholder rate is CLEARED

**Sourced at 0.143 to 0.175, central 0.159.** CBO 2014 Table A-3 (C corporation debt: 52.3
percent fully taxable, 14.9 temporarily deferred, 32.8 nontaxable, from Fed Flow of Funds
data for 2007) times Table A-4 (marginal rate on interest income 27.4 percent, 2006 SOI
Public Use File), with the upper bound adding the deferred tranche at CBO own nonqualified
annuity rate. Cross-checked against CBO Table 2 measured -6 percent effective rate on
C-corporation debt-financed investment, and corroborated by a Fed Z.1 holder map at 2026Q2.
Extraction in `data/raw/manual/BONDHOLDER_RATE_extracted.md`; holder map in
`framework/tau_k/z1_bond_holders.json`.

**What remains unverified and now matters most: the DEBT SHARE of AI capital spending**,
swept over 0.00 to 0.40, carrying **37 percent** of the residual variance. **No single
parameter, including this one, can now cross the fiscal threshold alone.** Module B reading
of the nine filers own books points to the low, all-equity end, which is the end unfavourable
to the condition, so clearing it would probably harden the verdict rather than soften it.
