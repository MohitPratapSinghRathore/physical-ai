# Labor backing accounts, and the capital-tax replacement condition

Two papers and the measurement pipeline behind them. Every number printed in either paper
resolves to a file in `data/release`, so any figure can be traced to an artifact and a key.

## The papers

**Labor Backing Accounts: Who Holds the Claims That Wages Pay?** Decomposes the US financial
claim stock twice over, by the income attributed to servicing each claim and by who holds,
guarantees or owes it, across thirteen claim classes from 1947 to 2025. About 52 percent of US
debt is attributed to labor income on the direct route and 60 percent once the indirect route is
counted; the federal government stands behind about 79.5 percent of directly wage-attributed
claims as holder, guarantor or debtor.

**Can Capital Taxes Replace Wage Tax Revenue? Both Sides Computed.** Assembles both sides of the
replacement condition. Which effective rate is used decides the answer: on the marginal wedge the
federal rate is 10.5 percent against the 11.0 to 13.7 percent replacement requires, and on the
annual rate it is 23.8 percent. No shortfall is established on either, which corroborates
Hötte, Theodorakopoulos and Koutroumpis (2024) by an independent route.

The manuscript sources are not tracked here, for the reason given below. The measurement
pipeline that produces every number in them is.

## What is measured, and what is a convention

The accounts observe the income composition of the parties owing each claim class and attribute
claims in proportion. **They do not observe which income actually pays a claim.** Every figure is
an attribution under that stated convention, not a measurement of servicing cash flows, and the
papers say so in the abstract, the definitions and the conclusions. The largest single judgement
is the one-step rule, which moves the headline ratio by about 15 percent, more than every other
convention together.

## Verifying a number

    python paper/gen_results_macros.py     # prints every macro name and value
    python paper/gen_tables.py             # rebuilds every table from the release data

Each printed figure in either paper is one of those macros. `data/release` holds 55 JSON and 49
CSV artifacts, one per measured object.

**Raw survey and supervisory microdata are not in this repository.** The SIPP public-use file,
the ACS extracts, the FDIC call report panel and the Federal Reserve financial accounts come from
the providers named in each paper's data section and are not ours to redistribute, so `data/raw`
is empty by design. This repository supports verification of every reported figure from the
processed artifacts; it does not by itself support a rebuild from raw microdata.

## Results that went against the project

Kept deliberately visible, because the pipeline's value depends on it.

- **A pre-registered institutional test was a null.** The accounts did not predict bank household
  credit losses out of sample. `framework/stress_scoping/` holds the pre-registration, the
  deviations log and the result.
- **A third paper does not exist.** Three pre-registered tests on a stress-test allocation
  question returned a failed novelty check, an inconclusive out-of-sample result in which the
  shortcut rule won, and then a kill. `framework/stress_scoping/RESULTS_C3.md` is the verdict and
  `REFEREE_C_REBUILD.md` records that the referee's own prescribed repairs overturned the
  paper's headline.
- **One distributional magnitude is contested.** The bottom-quintile claims-to-wages index is
  4.15 here against an independent rebuild's 1.21 to 1.64. Unreconciled, flagged wherever it
  appears, and no conclusion rests on its rank.
- **Five quantities were withdrawn** after independent rebuild rounds disagreed with them. They
  are listed with reasons in the removed-quantities table of the first paper rather than dropped
  quietly.

## On the rebuilds

Three rebuild rounds were run, each a separate run with no access to this code, working from raw
data and a published specification and scored against values sealed before the round. Round two
scored 127 quantities, 79 against sealed values, with 34 mismatches; round three matched all 32.
The blind was procedural rather than enforced and the rounds shared the raw data, so they test
the pipeline and the completeness of the specification rather than the validity of the inputs.
The claim made is that these quantities were **independently rebuilt under a reported blind
protocol**, never that they were independently verified.

## The manuscripts are not in this repository

Deliberately. A text-similarity screen cannot distinguish an author's own repository from an
external source, so a public copy of a manuscript's full text can read as near-total overlap and
trigger a desk rejection at a preprint server. Both papers' sources were removed from this
repository for that reason; they are distributed as the published preprints and, on request, as a
LaTeX source archive.

Nothing a reader needs in order to check a number is affected. The artifacts, the generators, the
pre-registrations and the rebuild records are all here, and that is what the papers' data
availability statements point to.

## Layout

    paper/           generators for the macros, tables and figures
    framework/       the measurement modules, by workstream
    data/release/    one artifact per measured object; the source of every printed number
    data/raw/        empty by design, see above
    notes/           findings, gate reports and source extractions

`PROJECT_BRIEF.md` is the original brief and is kept for the record; where it and the papers
disagree, the papers are current.
