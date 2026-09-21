# Replication package for "Labor-Backed Finance and the Fiscal Exposure to AI".
#
# Two levels of rebuild:
#   make headline   from the shipped processed inputs, rebuilds the headline numbers and
#                   compares each to data/release/. Offline. Target under ten minutes.
#   make all        from raw data, after `make fetch` and `make verify`, rebuilds every
#                   artifact and figure, then runs the gates and the plausibility audit.
#
# PY can be overridden:  make headline PY=python3

PY ?= python

.PHONY: help headline all fetch verify figures gates audit dictionary anon named clean

help:
	@echo "make headline   rebuild the headline numbers and compare to data/release"
	@echo "make fetch      download the raw inputs that allow automated access"
	@echo "make verify     check raw inputs against data/CHECKSUMS.sha256"
	@echo "make all        full rebuild from raw data (needs make fetch first)"
	@echo "make gates      run the QA gates over the released artifacts"
	@echo "make audit      run the plausibility audit"
	@echo "make anon       build the anonymous archive variant"
	@echo "make named      build the named archive variant"

headline:
	$(PY) replication/headline.py

fetch:
	$(PY) replication/fetch_raw.py

verify:
	$(PY) replication/verify_raw.py

all: verify
	$(PY) framework/labor_backing/build_direct.py
	$(PY) framework/labor_backing/build_indirect.py
	$(PY) framework/labor_backing/build_debt_only.py
	$(PY) framework/labor_backing/build_sensitivity.py
	$(PY) framework/labor_backing/item3_sovereign_robustness.py
	$(PY) framework/tau_k/components.py
	$(PY) framework/tau_k/assemble.py
	$(PY) framework/revision_r1/a1_pass_through.py
	$(PY) framework/revision_r1/a2_cashflow_bridge.py
	$(PY) framework/revision_r1/a3_relief_feedback.py
	$(PY) framework/revision_r2/b1_bridge_table.py
	$(PY) framework/revision_r2/b2_backing_basis.py
	$(PY) framework/revision_r2/b2_headline_effect.py
	$(PY) framework/revision_r2/c_jurisdiction_boundary.py
	$(PY) framework/institutions/apply_losses.py
	$(PY) framework/ai_bust/b1_tiers.py
	$(MAKE) figures gates audit

figures:
	$(PY) paper_interface/gen_results_macros.py
	$(PY) paper_interface/gen_figures.py

# The manuscript-side gates need the LaTeX source, which this package does not ship.
# What can be checked here is the arithmetic and the bounds.
gates:
	$(PY) replication/headline.py
	$(PY) src/verify/plausibility_audit.py

audit:
	$(PY) src/verify/plausibility_audit.py

dictionary:
	$(PY) replication/make_dictionary.py

anon:
	$(PY) replication/make_variant.py --variant anon

named:
	$(PY) replication/make_variant.py --variant named

clean:
	rm -rf build dist
