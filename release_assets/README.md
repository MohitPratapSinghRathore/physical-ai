# Labor backing accounts: replication package

This package contains the code, the measured artifacts and the documentation behind
**"Labor-Backed Finance and the Fiscal Exposure to AI"**. It ships every number the paper
reports and the pipeline that produces them. It does not ship the manuscript, and it does
not redistribute any publisher's raw data.

Version 1.0.0.

## Quick start

```
pip install -r requirements.lock        # Python 3.12, exact versions
make headline                           # rebuilds the headline numbers, prints PASS or FAIL
```

## What the two rebuild levels do

**`make headline`** runs offline from the processed inputs shipped here, in under ten
minutes on a laptop. It re-executes four modules in a scratch copy, so nothing shipped is
overwritten, and compares what they produce to `data/release/`: the assembled capital tax
rate under both rent readings and both taxable-share bases, the required band, the rate
and required band on each jurisdiction, the value of g at which the fiscal condition
closes, the labor backing ratio pair on both coefficient bases, and the federal exposure
share with its creditor-or-guarantor and debtor parts. It then regenerates every value the
paper reports from `data/release/` and compares all of them, key by key, to
`replication/reported_values.csv`. That second stage covers the quantities whose own
rebuild needs raw survey data: the 1952 to 2025 series, the first-round incidence by
holder, the institution-level summary by business model and the quintile gradient.

**`make all`** rebuilds every artifact and figure from raw data, then runs the QA gates and
the plausibility audit. It requires `make fetch` and `make verify` first. Several sources
must be downloaded by hand because they refuse automated requests; `make fetch` names each
one, its landing page and where to put the file. Expect a few hours, dominated by the
survey stages.

## System requirements

Python 3.12, about 2 GB of memory for `make headline` and 16 GB for the survey stages of
`make all`, and roughly 2 GB of disk for the raw inputs. A `Dockerfile` reproduces the
environment exactly. Random seeds are fixed at 20260919 wherever a stage samples; the seed
is set in `src/config.py` and stated in each module that uses it.

## Directory map

```
data/release/        every measured artifact the paper reads, by module
data/processed/      the small derived inputs the headline rebuild needs
framework/           the accounts, the capital rate, the institutions, the revisions
src/                 fetchers, the exposure index, the engines, the verification code
paper_interface/     the scripts that turn artifacts into the paper's numbers and figures
replication/         the rebuild harness, the fetch and verify steps, reported values
docs/                the rebuild specifications and reports, source extraction notes
```

## Changing a disputed convention and seeing what moves

The one-step rule is the largest judgment in the paper: a claim serviced out of business
revenue takes zero direct backing. To see what the federal exposure share does without it,
edit `framework/labor_backing/config.py`, move the business classes to their measured
indirect share, and rerun:

```
python framework/labor_backing/build_direct.py
python framework/revision_r2/b2_headline_effect.py
```

The exposure share moves from about 79 percent to the value reported as
`StructIndirect` in `data/release/labor_backing/item3_sovereign_robustness.json`. To drop
the debtor position instead, set `INCLUDE_OBLIGOR = False` in the same file: that is the
largest structural move in the paper, and the released artifact carries it as
`obligor leg EXCLUDED`.

## The status vocabulary

Every number carries one of three statuses, and the status lives with the number.

- **measured** comes from a published source or a survey, with the series named.
- **rebuilt** was additionally reproduced by an independent computational rebuild; see
  `REBUILDS.md`.
- **scenario** is conditional arithmetic on a stated input, most often a displacement
  level, and is never a forecast.

Statuses are recorded in the artifacts themselves, in the `status` field of each JSON and
in `data/release/stated_limitations.csv`.

## Known limitations of the package

Raw data is not redistributed, so `make all` needs the fetch step and four sources that
must be downloaded by hand. The off-balance-sheet AI financing the paper reports as
unmeasured is unmeasured here too. The institution panel is rebuilt from FDIC and NCUA
files that are fetched, not shipped. `make headline` verifies reproduction of the released
artifacts; it does not verify the economic assumptions behind them, which is a different
question and is stated in the paper's limitations.

## How to cite

See `CITATION.cff`. The paper's DOI and the archive DOI are placeholders until
publication; `ZENODO_STEPS.md` sets out how they are minted.

## Contact

Set `CONTACT_NAME` and `CONTACT_EMAIL` in your environment before fetching, as the SEC and
FDIC fair-access policies require a real contact in the request header. See
`.env.example`. For questions about the package, use the contact in `CITATION.cff`.
