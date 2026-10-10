# Session 2, the run: one page

Runs only after PREREGISTRATION.md **including Amendments 1 (§12), 2 (§13) and 3 (§14)**
is committed. That is done, on this branch, at V4.

**All inputs are now in place. There is no outstanding owner fetch.**

---

## 1. Complete input inventory

Everything lives under `data/raw/validation/`, which is **gitignored** by the repo's
existing convention (re-downloadable caches are not committed). The fetch scripts
regenerate everything except the owner-fetched files, which cannot be re-fetched from this
environment.

### Owner-fetched — irreplaceable from here, do not delete

| File | Location | SHA256 | Note |
|---|---|---|---|
| `la.data.64.County` | `data/raw/validation/laus/` | `7e5a532f…f01c9858` | 321 MB. All years; the build reads **pre-shock only**. |
| `la.series` | `data/raw/validation/laus/` | `2b11e414…97db77a4` | Supplied as `LA.SERIES`; renamed to lower case to match the loader. |
| `la.area` | `data/raw/validation/laus/` | `7f1dcbd6…dce1fc45` | |
| `hpi_at_county.xlsx` | `data/raw/validation/fhfa/` | `534e9fd3…df79afd1` | Verified against the owner's handoff. |

BLS returns HTTP 403 to this environment on both `www.bls.gov` and `download.bls.gov`, so
if the LAUS files are lost they must be fetched by the owner again.

### Fetched by script

| File | Location | Source |
|---|---|---|
| `fdic_financials_20140630.csv` | `data/raw/validation/` | `fetch_preshock.py`; index `risview_20260819` |
| `fdic_sod_2014.csv` | `data/raw/validation/` | `fetch_preshock.py`; index `sod_20260918` |
| `CAINC4.zip`, `bea_cainc4_all_areas.csv` | `data/raw/validation/` | BEA county income by source, 1969–2024 |
| `CAINC5N.zip` | `data/raw/validation/` | BEA county earnings by NAICS, 2001–2024 |
| `qcew_2013_annual.zip` | `data/raw/validation/` | 73 MB; mining establishment counts for the §12.6 imputation |
| `pums2013/csv_hus.zip`, `pums2013/csv_pus.zip` | `data/raw/validation/pums2013/` | ACS 2009–2013 5-year, 3.3 GB. **Not** the repo's 2023 PUMS, which is post-shock |
| `crosswalk/2010_tract_to_2010_puma.txt` | `data/raw/validation/crosswalk/` | Census |
| `crosswalk/Gaz_tracts_national.zip` | `data/raw/validation/crosswalk/` | Tract gazetteer, `HU10` allocation weights |
| `efa/household-debt.zip` | `data/raw/validation/efa/` | Fed EFA county debt, 1999Q1–2025Q4, interval-valued (§12.7) |

### Derived, rebuilt by the scripts in `framework/validation/`

`preshock_panel_2014.csv`, `preshock_debtor_panel_2014.csv`, `amendment2_panel.csv`,
`bank_mining_exposure_2014.csv`, `bank_exposure_suppression_variants.csv`,
`bank_unemployment_2013.csv`, `outcome_denominators_2014.csv`,
`puma2010_to_county_afact_hu.csv`.

### Not yet fetched, by design

**The outcome files.** FDIC `/financials` for 2014Q3–2018Q4 and `/failures`. These are
opened at step 8 and not before.

---

## 2. Order of operations — outcome files opened LAST

Steps 1 to 7 touch no outcome. **Step 8 is the first step that opens one.** Nothing in
steps 1 to 7 may be revised after step 8 begins.

| # | Step | Opens an outcome? | Runtime |
|---|---|---|---|
| 1 | Rebuild the pre-shock panel: `fetch_preshock.py`, `build_constructs.py`, `build_debtor_wage_shares.py`, `build_debtor_construct.py` | no | 40 min |
| 2 | `build_laus.py`; merge FHFA (2,757 counties) and the EFA **rank** (§12.7) into the county frame | no | 20 min |
| 3 | Mining-exposure imputation (§12.6): state residual allocated by QCEW establishment counts; build the disclosed-only and zero variants | no | 20 min |
| 4 | `outcome_denominators.py`: fix the §14.1 and §14.2 sample rules; freeze the qualifying bank lists | no | 5 min |
| 5 | Leave-one-out Bartik instrument from CAINC5N 2-digit shares; first-stage F; Rotemberg weights | no | 30 min |
| 6 | `amendment2_gap.py`: Gap, predicted loss, MDE grid | no | 10 min |
| 7 | **Freeze.** Commit everything above. Record the FDIC index stamps. **Re-verify the engine SHA256 against §13.4 and record it (§14.6).** | no | 10 min |
| — | — | — | — |
| 8 | **Pull outcomes.** `/financials` 2014Q3–2018Q4 for `NTRERES NTCRCD NTAUTO NTCONOTH NTCI NTRENRES NTRECONS NTLNLSQ P9RERES NARERES P9CI NACI NACRCD RBC1AAJ ROA LNLSGR`, plus `/failures`. Apply the §14.4 YTD-differencing rule for `NTCONOTH` and `NTRENRES` | **yes** | 25–40 min |
| 9 | Fit the **Gap-form specification (§13.3)** on the §14.1 primary outcome, **training set only**; then M1/M2/M3 and S1–S5 | yes | 35 min |
| 10 | Business-loan contrast (§14.2) and the rest of the secondary family | yes | 25 min |
| 11 | Structural calibration test (§13.4), bands per §14.5: rival-ω and debtor-ω, `s_lo`/`s_mid`/`s_hi`, non-linear dose-grid robustness | yes | 25 min |
| 12 | AKM exposure-robust SEs; 2011–2013 placebo | yes | 30 min |
| 13 | **Single pass** over the Layer 1 held-out set; then Layer 2 (2020). Compute the **realised design effect and realised MDE**, apply the §13.3 power rule before any interpretation | yes | 25 min |
| 14 | Romano–Wolf over the §14.2 secondary family, 10,000 bootstrap reps | yes | 40–60 min |
| 15 | Specification curve: three suppression handlings, cell-size thresholds, footprint thresholds, the `energy_adjacent_CI` robustness row | yes | 40 min |
| 16 | Write RESULTS.md against §13.3, §14.2 and §14.5; fill the deviations log | yes | 60 min |

**Total: roughly 7 to 8 hours of wall clock**, about 3.5 of it compute. Steps 8 and 14
dominate and both run unattended.

For Layer 2 (2020) the ACS must be rebuilt pre-shock for that episode — the 2015–2019
5-year PUMS on 2010 PUMA geography, which the existing crosswalk already matches. Budget a
further **40 minutes** if Layer 2 is run.

---

## 3. Discipline for the run

- **Steps 1–7 are frozen before step 8 opens an outcome.** If a pre-shock bug is found
  after step 8, the fix and the fact that it was made with outcomes visible both go in the
  deviations log.
- The held-out set is touched **once**, at step 13. If a bug is found afterwards, the fix
  is applied and the double consumption is logged — never a quiet re-run.
- The **Gap coefficient θ (§13.3) is the estimand.** M1/M2/M3 are reported alternatives and
  M3−M2 is the same test. The conventional controls must be in every Gap specification —
  without them θ is a mortgage-share coefficient under another name (§13.2).
- **The business-loan contrast is reported next to the primary in every table.** If the Gap
  predicts business-loan charge-offs as strongly as household ones, the household result is
  reported as a general local-distress effect and **not** as evidence for the accounts
  (§14.2).
- A null on θ is classified **"no effect"** or **"underpowered"** by the realised MDE
  (§13.3). With the primary sample at 5,938 the MDE is 0.079 at ICC 0.05 and 0.108 at ICC
  0.10 — so the branch is genuinely live, and it is chosen by the number, never after the
  fact.
- The §13.4 structural test answers a **different question** and cannot substitute for θ.
  Its rival-ω and debtor-ω variants correlate 0.946. Band 2 of §14.5 **cannot attribute**
  the gap between prediction and realisation to second-round transmission.
- `energy_adjacent_CI` stays out of the baseline; it correlates 0.840 with the treatment.
- Bin midpoints are never used as continuous EFA values (§12.7).
- Never sum year-to-date charge-off fields across quarters (§14.4).

---

## 4. Expected outcome

The most likely result remains the §12.5 middle verdict — **"local labour exposure predicts
losses; the labour backing accounts add nothing beyond it."**

Amendment 3 does not change that expectation but does change what a positive result would
be worth. Confining the outcome to household classes removes the most likely source of a
spurious positive, and the business-loan contrast gives a pre-stated way to detect one that
survives. A Gap effect on household charge-offs, absent on business charge-offs, with the
realised MDE below 0.10, would be a genuine finding. The same effect present on both would
not be, and the plan now says so in advance.

The structural test is expected to land in band 2 — **"direction supported; realised losses
exceed first-round predictions by a factor"** — and that band explicitly cannot distinguish
second-round transmission from omitted channels.

Session 2 should still be resourced as a null-writing exercise, and will have succeeded if
the verdict is stated cleanly, the power branch is chosen by the realised MDE, the
business-loan contrast is reported beside the primary, and no band-2 slope is written up as
confirmation of a mechanism it cannot identify.
