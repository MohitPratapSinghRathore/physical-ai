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

### BLS Displaced Worker Survey, reemployment rate (rho)

- Needed for: P1r break-even comparison, and to replace the gridded rho in
  src/stress/scenarios.py with an observed value.
- Status: BLOCKED. Every BLS endpoint returns HTTP 403 to this environment.
- Consequence: rho is gridded at 0.50, 0.65 and 0.80 throughout and is never asserted as
  observed. No claim in this repository depends on a particular value of rho.
