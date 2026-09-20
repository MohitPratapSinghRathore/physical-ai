# One entry point. `make all` rebuilds every table and figure from raw data.
#
# The ordering below is the real dependency order and is not alphabetical. Later targets
# read CSVs written by earlier ones, so running a stage on its own only works if the stage
# before it has been run at least once.
#
# COST WARNING. `make stress` simulates displacement household by household across the full
# scenario grid and takes roughly 25 minutes wall clock. Run the stages one at a time:
# running two ACS stages concurrently has exhausted memory on a 16GB machine and killed a
# run mid-way.

PY := ./.venv/Scripts/python.exe

.PHONY: all fetch build exposure household geography stress paper sources owner chain verify replication release clean

all: fetch build exposure household geography stress chain verify replication release sources

# ---------------------------------------------------------------------------
# 1. Raw data
# ---------------------------------------------------------------------------
fetch:
	$(PY) src/fetch_fred.py
	$(PY) src/fetch_sec.py
	@echo "NOTE: O*NET, PUMS, SIPP and the Census crosswalks are large one-time downloads."
	@echo "      See data/SOURCES.md for URLs; src/fetch_bulk.sh re-fetches them."
	@echo "NOTE: files in data/raw/manual/ are placed by hand and are listed in SOURCES.md."

# ---------------------------------------------------------------------------
# 2. Aggregate legs and the exposure index
# ---------------------------------------------------------------------------
build:
	$(PY) src/build_legw.py
	$(PY) src/build_lega.py

exposure:
	$(PY) src/build_paei.py
	$(PY) src/build_paei_c.py
	$(PY) src/build_a6_flags.py
	$(PY) src/build_pathways.py

# ---------------------------------------------------------------------------
# 3. Household balance sheet, share-based. RETAINED FOR THE RECORD ONLY.
#
# These produce the share-attributed figures that A39 showed to be an aggregation artifact
# and that the owner retired as a method. They are still built because src/stress/
# run_compare.py reports them beside the engine figures, and because the superseded numbers
# in notes/findings.md must stay reproducible.
# ---------------------------------------------------------------------------
household:
	$(PY) src/build_dar.py
	$(PY) src/build_dar_intensity.py
	$(PY) src/sipp_buffers_v2.py
	$(PY) src/sipp_v2_ci.py
	$(PY) src/cognitive_contrast.py
	$(PY) src/overlap_shares.py
	$(PY) src/shares_and_proportionality.py
	$(PY) src/vehicle_proportionality.py

# ---------------------------------------------------------------------------
# 4. Geography. Writes paper/figures/fig_concentration_breadth_scale.png
# ---------------------------------------------------------------------------
geography:
	$(PY) src/h3_geography.py
	$(PY) src/geo_breadth_scale.py

# ---------------------------------------------------------------------------
# 5. Household stress engine. This is the method every "at risk" number now routes through.
#    Strictly sequential: see the memory warning at the top of this file.
# ---------------------------------------------------------------------------
stress:
	$(PY) src/stress/run_acs.py
	$(PY) src/stress/run_compare.py
	$(PY) src/stress/run_sipp.py
	$(PY) src/stress/reconcile_acs_sipp.py

# ---------------------------------------------------------------------------
# 6. Fiscal
# ---------------------------------------------------------------------------
fiscal:
	$(PY) src/p1_repairs.py
	$(PY) src/p1r_fixes.py

# ---------------------------------------------------------------------------
# 7. Owner-placed sources, then the fiscal and credit chain that depends on them.
#
# ORDER IS LOAD BEARING. owner_files.py writes data/processed/owner_sources.json, which
# capacity.py reads for the trust fund denominators, reserves and depletion dates and which
# fiscal_extended_axis.py reads for the same denominators. capacity.py also publishes
# national_wage_bill_bn, THE single wage bill base every dose is converted to dollars on,
# and consistency.py and second_round.py read it from there. Running any of these out of
# order silently reuses a stale base.
# ---------------------------------------------------------------------------
owner:
	$(PY) src/owner_files.py
	$(PY) src/capacity.py

chain: owner
	$(PY) src/fiscal_extended_axis.py
	$(PY) src/benchmark_and_cap.py
	$(PY) src/under_reporting_impact.py
	$(PY) src/trust_fund_and_benchmark.py
	$(PY) src/consistency.py
	$(PY) src/dose_response.py
	$(PY) src/second_round.py
	$(PY) src/order_of_stress.py
	$(PY) src/thresholds.py

# ---------------------------------------------------------------------------
# 8. Verification, sealing and release. Run AFTER chain, never before.
# ---------------------------------------------------------------------------
verify:
	$(PY) src/verify/hand_check_credit.py
	$(PY) src/verify/independent_recompute.py
	$(PY) src/verify/plausibility_audit.py

replication:
	$(PY) src/slack_window_check.py
	$(PY) src/replication_round1_response.py

release: chain
	$(PY) src/seal.py
	$(PY) src/make_release.py

sources:
	$(PY) src/gen_sources.py

clean:
	rm -f data/processed/*.csv data/processed/*.json
	rm -f data/processed/stress/*.csv data/processed/stress/*.json
	rm -f paper/figures/*.png paper/figures/*.pdf
