# Validation pilot: data feasibility and episode selection

**Session 1 of 2. Feasibility and pre-registration only.** No outcome variable for any
candidate shock period was downloaded, opened or plotted in this session. Everything
below is either a predictor dated before the shock, a treatment-side variable, or a
reachability check that did not retrieve data.

Produced 2026-09-20 on branch `validation-pilot`. Nothing here is promoted to standing.

---

## 0. The finding that matters most, first

**The class-level labour backing coefficients add almost nothing to a bank-level measure
beyond what loan composition already says.** This was testable before any outcome and it
has been tested, on 6,637 banks at 2014-06-30.

The coefficients in `claim_class_rules.csv` are near-binary: every household-serviced
class sits between 0.727 and 0.883, and every business-serviced class is 0.0 by rule.
A weighted sum of loan shares with those weights is therefore close to an affine function
of one number, the household-serviced share of the book.

| Regression of the construct on plain loan-composition shares | R² |
|---|---|
| **Composition leg alone** (loan shares × class coefficients) | **0.899** |
| Full bank labour backing (composition leg × county wage share) | 0.515 |
| Full measure on composition + county wage share + interactions | **0.939** |

Read the first and third rows together. The composition leg is 90 percent reproducible
from call-report loan shares alone. And a rival researcher who never opens the labour
backing accounts — who takes only FDIC loan shares and the BEA county wage share and
interacts them — reproduces **94 percent of the variance** of the labour backing measure.
The accounts' distinctive contribution to this construct is the residual 6 percent.

**Consequence for the design.** Whatever predictive power the bank measure turns out to
have will come overwhelmingly from the *geography* leg — the deposit-weighted county wage
share — and not from the labour backing coefficients. The geography leg is orthogonal to
the composition leg (correlation 0.011) and is genuinely new relative to loan composition,
but it is not new relative to the broader literature: it is a local-labour-exposure
control, and local labour exposure is a standard thing to condition on.

This does not sink the exercise. It sharply narrows what a positive result could mean,
and the pre-registration has been written to isolate the two legs so that a win for the
geography leg is never reported as a win for the accounts. See PREREGISTRATION.md §4.

**Second weakening finding.** BEA suppresses county mining earnings for small counties:
only **1,789 of 3,113 counties** have usable mining data in 2013. QCEW has the same
disclosure suppression. Exposure is therefore measured with error, and the error is
correlated with county size. This is a real limit on the oil design, not a nuisance.

---

## 1. Data feasibility by source

Verified live from this environment on 2026-09-20 unless marked otherwise.

### Bank level

| Source | Series / endpoint | Coverage | Status |
|---|---|---|---|
| FDIC BankFind `/financials` | Call-report derived: `ASSET DEP EQ SC SCMUNI LNLSGR LNLSNET LNRECONS LNRENRES LNREMULT LNRERES LNRELOC LNREAG LNCI LNAG LNCRCD LNAUTO LNCONOTH BRO RBC1AAJ RBCT1J` | quarterly, 1992– ; 6,738 institutions at 2014Q2 | **Fetched** (pre-shock quarter only). No key. Paginates at 10,000. |
| FDIC BankFind `/sod` | Summary of Deposits: `CERT STCNTYBR DEPSUMBR YEAR` | annual, June 30, 1994– ; 94,725 branch rows for 2014 | **Fetched.** `STCNTYBR` is the 5-digit county FIPS, which is what makes the geography leg possible. |
| FDIC BankFind `/failures` | failure and assistance transactions | 1934– | Reachable (HTTP 200). **Not retrieved — outcome.** |
| Charge-offs / NPL | `NTLNLSQ`, `NCLNLSQ`, `P3ASSET`, `P9ASSET`, `NPERFV` on `/financials` | quarterly | Fields exist on the same endpoint. **Not retrieved — outcome.** |

Vintage note: the `/financials` index is stamped `risview_20260819`, the `/sod` index
`sod_20260918`. Call report data is restated; the run session must record the index
stamp with the pull so the extract is reproducible.

### County level

| Source | Series | Coverage | Status |
|---|---|---|---|
| BEA Regional **CAINC4** | Personal income by source: personal income (10), wages (50), proprietors' (70), dividends/interest/rent (46), transfers (47) | **1969–2024**, all counties | **Fetched.** Drives the wage share of personal income. |
| BEA Regional **CAINC5N** | Earnings by 2-digit NAICS industry by county, incl. mining (200), oil and gas extraction (201) | **2001–2024**, all counties | **Fetched.** This is the full shift-share ingredient set and it covers every candidate episode from 2001 on. |
| BLS **QCEW** | county × industry employment and wages, annual singlefile | 1990– ; 77 MB/year | Reachable (HTTP 200, 76,869,588 bytes). Not needed if CAINC5N suffices; QCEW is the higher-frequency fallback and the standard Bartik source. |
| BLS **LAUS** county unemployment | `laucnty*.txt` | 1990– | **BLOCKED: HTTP 403** to this environment, including with a browser user-agent. bls.gov blocks non-browser retrieval of these static files. **Owner must fetch.** |
| FHFA county house price index | `hpi_at_bdl_county.csv` | annual, 1975– | **BLOCKED: HTTP 404** at the documented paths; FHFA reorganised its download URLs. The metro quarterly file resolves (HTTP 200). **Owner must fetch the county file.** |
| Federal Reserve **Enhanced Financial Accounts**, household DTI by county | EFA county-level debt-to-income | landing page reachable | Distributed as a page with per-table links, not a single stable CSV. **Owner should confirm the county DTI table and its start date**; the series is county-level from roughly 1999 via the FRBNY/Equifax CCP underpinnings, but the EFA public county cut is narrower. |
| NY Fed Household Debt and Credit, **state** delinquency | `area_report_by_year.xlsx` | state, 2003– | Reachable (HTTP 200). **Not retrieved — outcome.** |
| CFPB Mortgage Performance Trends, **county** delinquency | 30-89 and 90+ day rates | county, **2008–** | Outcome series; start date 2008 means it **covers the oil episode and 2020 but not 2001 and not the run-up to 2007**. Not retrieved. |

### Must be fetched by the owner

**Updated 2026-09-20, after the owner's handoff and Amendment 1. Two of the three original
blockers are closed.**

1. ~~BLS LAUS county unemployment~~ — **CLOSED 2026-09-21.** Owner-fetched
   `la.data.64.County`, `la.series` and `la.area`, staged in `data/raw/validation/laus/`
   with checksums recorded in SESSION2_PLAN §1. Built pre-shock only: **3,220 counties**
   carry a 2013 annual unemployment rate (p10 4.19, median 7.20, p90 10.90), and
   **98.6 percent** of 2014 SOD branch rows match a LAUS county, giving a deposit-weighted
   rate for **6,623 banks**. BLS still returns HTTP 403 to this environment, so these three
   files cannot be re-fetched here if lost.
2. ~~FHFA county annual HPI~~ — **CLOSED.** Owner-fetched `hpi_at_county.xlsx`, SHA256
   verified against the handoff. 1975–2025, 2,796 counties; 2,757 carry both 2011 and 2013
   values, so the pre-shock control covers 2,757 of 3,113 counties. See PREREGISTRATION §12.8.
3. ~~Federal Reserve EFA county household DTI~~ — **CLOSED.** The
   `federalreserve.gov/releases/z1/dataviz/download/zips/household-debt.zip` path works
   from this environment even though the `/releases/efa/` landing page did not. Coverage
   verified from the file bytes: **1999Q1–2025Q4 quarterly, 3,139 counties in 2013Q4.**
   The owner's warning is confirmed — values are **interval bounds, not point estimates**,
   in nine roughly equal-count bins, so the variable is handled as an ordinal rank and
   never as bin midpoints. See PREREGISTRATION §12.7.

**Nothing is blocked. All inputs for the run are in place.**

---

## 2. Candidate episodes

Wage-bill shock measured as the change in county earnings over base-year personal income.
Exposure is the 2013 mining share of county earnings; "exposed" means above 10 percent,
which is 246 counties. Treatment side only.

| Episode | Window | National wage-bill change | Cross-county SD | Exposed counties, median change | Rest, median | Gap | corr(exposure, change) |
|---|---|---|---|---|---|---|---|
| 2001 recession | 2001–2003 | +1.96% | 7.90 | +4.08% | +4.67% | −0.60pp | −0.04 |
| Financial crisis | 2007–2010 | −0.25% | 5.49 | +6.62% | +2.11% | **+4.51pp** | +0.27 |
| **Oil collapse** | **2014–2016** | +4.19% | 5.98 | **−8.12%** | **+1.43%** | **−9.55pp** | **−0.47** |
| Pandemic | 2019–2020 | +0.74% | 4.54 | −1.16% | +1.62% | −2.78pp | −0.27 |

Bank counts by deposit-weighted 2014 mining exposure: **1,266** banks above 2 percent,
**842** above 5 percent, **461** above 10 percent, out of 6,666 with branch data.

### Recommendation: primary = 2014–2016 oil collapse. Confirmed, not assumed.

The prior was that the oil collapse is cleanest because house prices and national credit
conditions were stable. The evidence supports it, and adds a reason the prior did not
state:

- **The shock is large and sharply targeted.** A 9.55 percentage point gap in the
  earnings change between exposed and unexposed counties, against a *positive* national
  backdrop of +4.19 percent. The shock is local by construction, which is exactly what a
  cross-sectional design needs. No other episode comes close on this contrast.
- **The national backdrop is genuinely benign.** Because aggregate wages were rising, a
  national-level confound cannot generate the cross-sectional variation. In 2007–2010 and
  2020 the aggregate is moving too, and separating local from national is much harder.
- **The crisis episode is actively disqualified, not merely confounded.** Exposed counties
  did *better* than the rest through 2007–2010 (+4.51pp) — the shale boom ran through the
  financial crisis. Mining exposure in that window is a proxy for being insulated from the
  crisis, so the instrument would have the wrong sign for the wrong reason.
- **2001 has essentially no mining signal** (gap −0.60pp, correlation −0.04). It cannot
  identify anything through this exposure measure, and CFPB county delinquency does not
  reach back to it anyway.

### Held-out: 2020 pandemic oil component, plus a within-episode geographic hold-out

2020 carries a real, separately-caused oil shock (gap −2.78pp, correlation −0.27) with a
different macro environment and a different policy response. That makes it a genuine
out-of-sample test of the same construct rather than a re-run. Its weakness is severe and
must be stated: the CARES Act, PPP and expanded unemployment insurance broke the normal
link from income loss to credit loss, so a null in 2020 is weaker evidence against the
hypothesis than a null within the oil episode.

For that reason the hold-out is **two-layered**, and both layers are fixed now:

- **Layer 1, geographic, inside the primary episode.** Train on all states except
  Texas, North Dakota, Oklahoma, New Mexico, Wyoming, Alaska, Louisiana, West Virginia;
  test on those eight. This holds out the bulk of the exposure and is the harder test.
- **Layer 2, episode.** 2020, construct rebuilt on 2019 pre-shock data.

The primary confirmatory test is Layer 1. Layer 2 is reported alongside and is not
allowed to rescue a Layer 1 failure.

---

## 3. Pre-shock correlation of bank labour backing with each conventional control

n = 6,637 banks, 2014-06-30. Labour backing mean 0.165, SD 0.094.
Full table in `preshock_correlations.csv`; decomposition in `construct_decomposition.csv`.

| Conventional control | corr with full measure | corr with composition leg only |
|---|---|---|
| County wage share (geography leg) | **0.598** | 0.011 |
| Household share of book | **0.582** | **0.765** |
| 1-4 family residential share | 0.542 | 0.715 |
| Agricultural share | −0.465 | −0.440 |
| C&I share | −0.324 | −0.524 |
| Deposits / assets | −0.255 | −0.153 |
| Log assets | 0.182 | −0.003 |
| Tier 1 leverage ratio | 0.168 | 0.135 |
| Consumer share | 0.166 | 0.212 |
| CRE share | −0.141 | −0.367 |
| Construction share | −0.112 | −0.215 |
| Securities share | 0.106 | 0.235 |
| Loans / assets | −0.103 | −0.222 |
| CRE concentration (supervisory) | −0.100 | −0.274 |
| Brokered / deposits | 0.056 | −0.072 |

No single conventional control exceeds 0.60 in absolute correlation with the full
measure, so it is **not** pairwise collinear with any one of them. The problem is joint,
not pairwise, and it is in the third row of the table in §0: the composition leg is 0.899
explained by the composition shares together.

---

## 4. Files produced

| File | Contents |
|---|---|
| `fetch_preshock.py` | Pulls FDIC financials 2014Q2, FDIC SOD 2014, BEA CAINC4 |
| `build_constructs.py` | Builds both legs, conventional controls, correlation table, collinearity verdict |
| `decompose_construct.py` | The nested-R² test, and episode wage-shock spread |
| `episode_diagnostics.py` | Mining exposure, exposed-vs-rest contrast, bank exposure counts |
| `preshock_correlations.csv` | §3 table |
| `preshock_collinearity.json` | §0 verdict, machine readable |
| `construct_decomposition.csv` | Nested R² ladder |
| `episode_shock_spread.csv`, `episode_exposure_contrast.csv` | §2 tables |
| `data/raw/validation/preshock_panel_2014.csv` | The 6,637-bank pre-shock panel |

### Added by Amendment 1 (2026-09-20)

| File | Contents |
|---|---|
| `build_debtor_wage_shares.py` | ACS 2009–2013 5-year PUMS → wage share of household income by tenure group, PUMA then county, housing-unit weighted |
| `build_debtor_construct.py` | Bank-level debtor-specific measure and the test against the rival |
| `suppression_analysis.py` | BEA mining `(D)` suppression: state residuals, bounds, effect on the exposed-bank sample |
| `puma_debtor_wage_shares_2013.csv`, `county_debtor_wage_shares_2013.csv` | The debtor-specific wage shares with cell counts |
| `debtor_construct_decomposition.csv`, `debtor_construct_verdict.json` | §12.4 tables |
| `suppression_state_residual.csv` | §12.6 state residuals |

**Headline from Amendment 1, in one line:** the debtor-specific refinement does carry
content the rival lacks (rival alone explains 0.640 of it), but a rival holding loan shares
and the population wage share still reproduces 0.917, so the accounts' distinctive content
roughly doubles from 6.1 to 11.2 percent of variance and remains about one ninth.
