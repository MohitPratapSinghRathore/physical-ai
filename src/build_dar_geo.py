"""Step 3 (Part B): geographic DAR at PUMA level, with replicate-weight standard errors.

For each 2020 PUMA and each capability level c:
    wage_at_risk      embodiment-weighted wage bill in exposed occupations
    mortgage_at_risk  annual mortgage outlay of mortgage-holding households, attributed by
                      the share of household wage income earned in exposed occupations
    rent_at_risk      the same for gross rent
each as a level and as a share of the local total.

B5: no point estimate without an interval. Standard errors use the ACS successive-difference
replication formula over the 80 replicate weights:

    SE(theta) = sqrt( (4/80) * sum_r (theta_r - theta)^2 )

B2 note on the column whitelist. This module reads ACS PUMS only and touches no HMDA data,
so no HMDA outcome variable can leak into it. The PUMS whitelist is enforced below via
usecols. The HMDA whitelist lives in the loader that is currently blocked (open question Q4).

PAEI version is read from paei_c_summary.json and written into every output row, so revising
the index requires no change here.

Implementation note: everything is accumulated with vectorised groupby into (area x
replicate) matrices. An earlier version looped per household in Python and did not finish.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

KEY_C = [0.0, 0.2, 0.3, 0.5, 0.8, 1.0]
NREP = 80
PWT = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, NREP + 1)]
HWT = ["WGTP"] + [f"WGTP{i}" for i in range(1, NREP + 1)]
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]


def chunks(zf, fn, cols, size=250_000):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype={"SERIALNO": str},
                              chunksize=size, low_memory=False):
            yield ch


class Acc:
    """Accumulate (area x replicate) sums across streamed chunks."""

    def __init__(self):
        self.parts = []

    def add(self, keys, mat):
        df = pd.DataFrame(mat)
        df["__k"] = keys
        self.parts.append(df.groupby("__k", sort=False).sum())

    def result(self):
        if not self.parts:
            return pd.DataFrame()
        return pd.concat(self.parts).groupby(level=0).sum()


def se_rows(M):
    """M: (n areas, 1+NREP). Returns point estimate and replication SE per row."""
    pt = M[:, 0]
    rep = M[:, 1:]
    return pt, np.sqrt((4.0 / NREP) * ((rep - pt[:, None]) ** 2).sum(axis=1))


def main():
    ver = json.loads((OUT / "paei_c_summary.json").read_text())["paei_c_version"]
    grid = pd.read_csv(OUT / "paei_c.csv")
    Pmap = (grid[grid["c"] == 0.0].drop_duplicates("occp")
            .set_index("occp")["embodiment_P"].to_dict())
    expo = {c: (grid[np.isclose(grid["c"], c)].drop_duplicates("occp")
                .set_index("occp")["exposed_threshold_rank"].to_dict()) for c in KEY_C}

    # ---------- pass 1: household share of wage income in exposed occupations ----------
    print("pass 1: household exposed wage shares ...")
    p1 = []
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["SERIALNO", "OCCP", "WAGP", "ADJINC"]):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
            Pv = occ.map(Pmap)
            keep = (wage > 0) & Pv.notna()
            if not keep.any():
                continue
            d = pd.DataFrame({"SERIALNO": ch.loc[keep, "SERIALNO"],
                              "wage": wage[keep]})
            for c in KEY_C:
                m = occ[keep].map(expo[c]).fillna(0).astype(float)
                d[f"e{c}"] = wage[keep] * Pv[keep] * m
            p1.append(d.groupby("SERIALNO", sort=False).sum())
    HH = pd.concat(p1).groupby(level=0).sum()
    for c in KEY_C:
        HH[f"share{c}"] = np.where(HH["wage"] > 0, HH[f"e{c}"] / HH["wage"], 0.0)
    HH = HH[[f"share{c}" for c in KEY_C]]
    print(f"  households with wage income: {len(HH):,}")

    # ---------- pass 2: wage bill at risk by PUMA ----------
    print("pass 2: wage bill at risk by PUMA ...")
    accs = {"total": Acc(), **{f"risk{c}": Acc() for c in KEY_C}}
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["STATE", "PUMA", "OCCP", "WAGP", "ADJINC"] + PWT):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6).to_numpy()
            keys = (ch["STATE"].astype(int).astype(str).str.zfill(2).to_numpy()
                    + ch["PUMA"].astype(int).astype(str).str.zfill(5).to_numpy())
            W = ch[PWT].to_numpy(float)
            Pv = occ.map(Pmap).fillna(0.0).to_numpy()
            accs["total"].add(keys, wage[:, None] * W)
            for c in KEY_C:
                m = occ.map(expo[c]).fillna(0).astype(float).to_numpy()
                accs[f"risk{c}"].add(keys, (wage * Pv * m)[:, None] * W)

    # ---------- pass 3: housing obligations at risk ----------
    print("pass 3: mortgage and rent at risk by PUMA ...")
    hacc = {"mort_total": Acc(), "rent_total": Acc(),
            **{f"mort{c}": Acc() for c in KEY_C}, **{f"rent{c}": Acc() for c in KEY_C}}
    for zf, fn in HPART:
        for ch in chunks(zf, fn, ["SERIALNO", "STATE", "PUMA", "TEN", "MRGP", "GRNTP",
                                  "ADJHSG"] + HWT):
            for col in ["TEN", "MRGP", "GRNTP", "ADJHSG"]:
                ch[col] = pd.to_numeric(ch[col], errors="coerce")
            a = (ch["ADJHSG"] / 1e6).to_numpy()
            mort = np.nan_to_num(np.where(ch["TEN"] == 1, ch["MRGP"] * 12 * a, 0.0))
            rent = np.nan_to_num(np.where(ch["TEN"] == 3, ch["GRNTP"] * 12 * a, 0.0))
            keys = (ch["STATE"].astype(int).astype(str).str.zfill(2).to_numpy()
                    + ch["PUMA"].astype(int).astype(str).str.zfill(5).to_numpy())
            W = ch[HWT].to_numpy(float)
            hacc["mort_total"].add(keys, mort[:, None] * W)
            hacc["rent_total"].add(keys, rent[:, None] * W)
            sh = ch[["SERIALNO"]].join(HH, on="SERIALNO")
            for c in KEY_C:
                s = sh[f"share{c}"].fillna(0.0).to_numpy()
                hacc[f"mort{c}"].add(keys, (mort * s)[:, None] * W)
                hacc[f"rent{c}"].add(keys, (rent * s)[:, None] * W)

    # ---------- assemble ----------
    print("assembling ...")
    res = {k: v.result() for k, v in {**accs, **hacc}.items()}
    areas = sorted(set().union(*[set(v.index) for v in res.values() if len(v)]))
    idx = pd.Index(areas, name="puma_id")

    def mat(name):
        d = res[name].reindex(idx).fillna(0.0)
        return d.to_numpy(float)

    wt_pt, _ = se_rows(mat("total"))
    mt_pt, _ = se_rows(mat("mort_total"))
    rt_pt, _ = se_rows(mat("rent_total"))

    rows = []
    for c in KEY_C:
        wr_pt, wr_se = se_rows(mat(f"risk{c}"))
        mr_pt, mr_se = se_rows(mat(f"mort{c}"))
        rr_pt, rr_se = se_rows(mat(f"rent{c}"))
        rows.append(pd.DataFrame({
            "puma_id": idx, "state": [a[:2] for a in idx], "puma": [a[2:] for a in idx],
            "c": c, "paei_c_version": ver,
            "wage_bill": wt_pt, "wage_at_risk": wr_pt, "wage_at_risk_se": wr_se,
            "wage_at_risk_share": np.divide(wr_pt, wt_pt, out=np.full_like(wr_pt, np.nan),
                                            where=wt_pt > 0),
            "mortgage_total": mt_pt, "mortgage_at_risk": mr_pt,
            "mortgage_at_risk_se": mr_se,
            "mortgage_at_risk_share": np.divide(mr_pt, mt_pt,
                                                out=np.full_like(mr_pt, np.nan),
                                                where=mt_pt > 0),
            "rent_total": rt_pt, "rent_at_risk": rr_pt, "rent_at_risk_se": rr_se,
            "rent_at_risk_share": np.divide(rr_pt, rt_pt, out=np.full_like(rr_pt, np.nan),
                                            where=rt_pt > 0),
        }))
    D = pd.concat(rows, ignore_index=True)
    D.to_csv(OUT / "dar_geo_puma.csv", index=False)

    nat = []
    for c in KEY_C:
        d = D[D["c"] == c]
        # national SE: sum replicates across areas first, then apply the formula
        wr = mat(f"risk{c}").sum(axis=0)
        mr = mat(f"mort{c}").sum(axis=0)
        rr = mat(f"rent{c}").sum(axis=0)
        f = lambda v: float(np.sqrt((4.0 / NREP) * ((v[1:] - v[0]) ** 2).sum()))
        nat.append({
            "c": c, "paei_c_version": ver, "n_pumas": int(d["puma_id"].nunique()),
            "wage_at_risk_usd_bn": wr[0] / 1e9, "wage_at_risk_se_usd_bn": f(wr) / 1e9,
            "wage_at_risk_share": wr[0] / d["wage_bill"].sum(),
            "mortgage_at_risk_usd_bn": mr[0] / 1e9, "mortgage_at_risk_se_usd_bn": f(mr) / 1e9,
            "mortgage_at_risk_share": mr[0] / d["mortgage_total"].sum(),
            "rent_at_risk_usd_bn": rr[0] / 1e9, "rent_at_risk_se_usd_bn": f(rr) / 1e9,
            "rent_at_risk_share": rr[0] / d["rent_total"].sum(),
        })
    N = pd.DataFrame(nat)
    N.round(4).to_csv(OUT / "dar_geo_national.csv", index=False)

    pd.set_option("display.width", 220)
    print(f"\nPAEI_C_VERSION = {ver}; PUMAs = {D['puma_id'].nunique()}")
    print("\n=== National totals by c, with replication SEs (USD bn) ===")
    print(N[["c", "wage_at_risk_usd_bn", "wage_at_risk_se_usd_bn", "wage_at_risk_share",
             "mortgage_at_risk_usd_bn", "mortgage_at_risk_se_usd_bn",
             "mortgage_at_risk_share", "rent_at_risk_usd_bn", "rent_at_risk_se_usd_bn",
             "rent_at_risk_share"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
