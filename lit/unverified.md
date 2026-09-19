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
