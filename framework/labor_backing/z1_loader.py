"""Z.1 Financial Accounts loader.

Reads the Federal Reserve's own Z.1 CSV package and exposes any FL/LM level series
by its Z.1 series code. One download, every claim class and every holder sector,
annual from 1945. This avoids the per-series FRED route, which is rate limited and
which mirrors the same underlying series anyway.

SOURCE: https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip
PROVENANCE: the extracted series actually used are written to z1_extract.csv next to
this file, with the release date, so the build is reproducible without the zip.
"""
import io, json, pathlib, zipfile, re
import numpy as np
import pandas as pd
import requests

HERE = pathlib.Path(__file__).parent
URL = "https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip"
UA = {"User-Agent": "physical-ai research (team@oviguide.in)"}
CACHE = HERE / "_z1_cache.zip"


def _zip():
    if not CACHE.exists():
        r = requests.get(URL, timeout=600, headers=UA)
        r.raise_for_status()
        CACHE.write_bytes(r.content)
    return zipfile.ZipFile(CACHE)


def load_all():
    """code -> pandas Series indexed by period string, for every FL/LM level series."""
    z = _zip()
    out = {}
    for f in z.namelist():
        if not (f.startswith("csv/") and f.endswith(".csv")):
            continue
        txt = z.read(f).decode("utf8", errors="replace")
        try:
            df = pd.read_csv(io.StringIO(txt), dtype=str)
        except Exception:
            continue
        if df.empty or df.columns[0] != "date":
            continue
        idx = df["date"].astype(str)
        for c in df.columns[1:]:
            code = c.strip()
            if not re.match(r"^(FL|LM)\d", code):
                continue
            s = pd.to_numeric(df[c].replace("ND", np.nan), errors="coerce")
            s.index = idx
            s = s.dropna()
            if len(s) == 0:
                continue
            if code not in out or len(s) > len(out[code]):
                out[code] = s
    return out


def annual(series):
    """Annual end-of-year level, in millions of dollars, indexed by int year.

    Q4 for quarterly series, the annual observation for annual series."""
    v = {}
    for k, x in series.items():
        k = str(k)
        if ":Q" in k:
            y, q = k.split(":Q")
            if q != "4":
                continue
            v[int(y)] = x
        else:
            m = re.match(r"^(\d{4})", k)
            if m:
                v.setdefault(int(m.group(1)), x)
    return pd.Series(v).sort_index()


if __name__ == "__main__":
    a = load_all()
    print(f"{len(a)} level series loaded")
    for c in ["FL153165105", "FL413065105", "FL313065105", "FL763065105"]:
        hit = [k for k in a if k.startswith(c)]
        print(c, hit[:3], (annual(a[hit[0]]).tail(2).to_dict() if hit else None))


def catalog():
    """code (no frequency suffix) -> the Federal Reserve's own description."""
    z = _zip()
    out = {}
    for f in z.namelist():
        if not (f.startswith("data_dictionary/") and f.endswith(".txt")):
            continue
        for line in z.read(f).decode("utf8", errors="replace").splitlines():
            p = line.split("\t")
            if len(p) < 2:
                continue
            code = p[0].split(".")[0]
            if re.match(r"^(FL|LM)\d", code):
                out.setdefault(code, p[1].strip())
    return out


def find(pattern, cat=None):
    cat = cat or catalog()
    rx = re.compile(pattern, re.I)
    return {k: v for k, v in cat.items() if rx.search(v)}
