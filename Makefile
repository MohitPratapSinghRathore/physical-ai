# One entry point. `make all` rebuilds every table from raw data.
PY := ./.venv/Scripts/python.exe

.PHONY: all fetch build clean sources

all: fetch build sources

fetch:
	$(PY) src/fetch_fred.py
	@echo "NOTE: src/fetch_sec.py is blocked (HTTP 403). See notes/open_questions.md Q1."
	@echo "NOTE: O*NET, PUMS and the Census crosswalk are large one-time downloads."
	@echo "      See data/SOURCES.md for URLs; src/fetch_bulk.sh re-fetches them."

build:
	$(PY) src/build_legw.py
	$(PY) src/build_paei.py
	$(PY) src/build_dar.py
	$(PY) src/build_dar_intensity.py

sources:
	$(PY) src/gen_sources.py

clean:
	rm -f data/processed/*.csv data/processed/*.json
