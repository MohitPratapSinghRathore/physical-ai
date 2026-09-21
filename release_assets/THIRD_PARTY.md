# Third-party material and terms

No raw input is redistributed in this package. `DATA_SOURCES.md` gives the publisher, the
identifier, the vintage, the access date and a checksum for each one, so a replicator can
obtain the same bytes under the publisher's own terms.

| publisher | material | terms as we read them | in this package |
|---|---|---|---|
| Federal Reserve Board | Financial Accounts (Z.1), Distributional Financial Accounts, DFAST results | US Government work, public domain | derived artifacts only |
| US Census Bureau | SIPP, ACS PUMS | US Government work, public domain | derived artifacts only |
| Bureau of Labor Statistics | Worker Displacement Survey, employment projections | US Government work, public domain | derived artifacts only |
| O*NET Resource Center | O*NET database | CC BY 4.0, attribution required | derived indices only, attributed |
| Internal Revenue Service | Statistics of Income tables | US Government work, public domain | derived shares only |
| FHFA | House Price Index | US Government work; FHFA asks that the index be attributed and not presented as official | one elasticity input, attributed; no index values redistributed |
| SEC EDGAR | Company filings, Enterprise 10-Ks | Public filings; fair-access policy governs automated requests | extracted figures only |
| FDIC, NCUA | Institution panels | US Government work, public domain | not shipped; fetched by the user |
| Federal Reserve Bank of New York | Household Debt and Credit report aggregates | Published aggregates, reuse with attribution; the underlying Consumer Credit Panel is licensed from Equifax and is not redistributable | only published report aggregates are used, as benchmark totals, attributed; no panel microdata is present |
| Bank for International Settlements | Quarterly Review commentary | BIS terms permit citation with attribution; redistribution of the text is not permitted | cited, not reproduced |
| Congressional Research Service, Congressional Budget Office | R47113, Taxing Capital Income | US Government works | short quotations and table references only, in `docs/source_extractions/` |

## Flagged for the owner

- **New York Fed Consumer Credit Panel.** Only the published report aggregates are used,
  as benchmark totals for survey balances. No panel microdata is present, so the Equifax
  licence restriction is not engaged. Basis for including the benchmark: it is published in
  a public report and is attributed.
- **FHFA House Price Index.** One elasticity input is derived from it. No index series is
  redistributed.
- **BIS.** Commentary is cited, never reproduced beyond a short quotation.
- **O*NET.** CC BY 4.0 requires attribution wherever derived indices appear; the
  attribution is in `DATA_SOURCES.md` and in the module that builds the index.
