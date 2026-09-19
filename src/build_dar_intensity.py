"""DAR intensity: is high-Physical-AI-exposure wage income MORE leveraged than its size?

build_dar.py answers "where is the mortgage debt service?" and finds it in low-PAEI
households. That is partly mechanical: high-PAEI occupations earn less and own homes with
mortgages less often. The question that actually bears on the thesis is different:

    per dollar of wage income earned in a PAEI quintile, how much mortgage debt service
    does that dollar carry?

Two statistics:
  concentration ratio = (share of mortgage service) / (share of wage income)
      > 1 means that quintile's wage income is over-committed to mortgage debt relative
      to its size, i.e. leveraged against exactly the income Physical AI puts at risk.
  service-to-income  = mortgage service attributed to the quintile / wage income of that
      quintile, a debt-service-to-income ratio on the exposed income only.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
PCOLS = ["SERIALNO", "OCCP", "PWGTP", "WAGP", "ADJINC"]
HCOLS = ["SERIALNO", "WGTP", "TEN", "MRGP"]


def read_part(zf, fn, cols):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        return pd.concat(list(pd.read_csv(
            io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
            usecols=cols, dtype={"SERIALNO": str}, chunksize=400_000, low_memory=False)),
            ignore_index=True)


def main():
    occ = pd.read_csv(OUT / "occp_to_paei.csv")
    P = pd.concat([read_part(z, f, PCOLS) for z, f in PPART], ignore_index=True)
    H = pd.concat([read_part(z, f, HCOLS) for z, f in HPART], ignore_index=True)

    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P = P.dropna(subset=["OCCP"])
    P["OCCP"] = P["OCCP"].astype(int)
    P["WAGP"] = pd.to_numeric(P["WAGP"], errors="coerce").fillna(0.0)
    P["wage_adj"] = P["WAGP"] * pd.to_numeric(P["ADJINC"], errors="coerce") / 1e6
    P = P.merge(occ[["occp", "PAEI"]], left_on="OCCP", right_on="occp", how="left")

    W = P[P["PAEI"].notna() & (P["wage_adj"] > 0)].sort_values("PAEI")
    cum = np.cumsum(W["PWGTP"].to_numpy()) / W["PWGTP"].sum()
    qs = np.interp([0.2, 0.4, 0.6, 0.8], cum, W["PAEI"].to_numpy())
    P["paei_q"] = np.where(P["PAEI"].notna(), np.digitize(P["PAEI"].to_numpy(), qs) + 1, np.nan)

    # national wage income by quintile (population weighted)
    P["w_wt"] = P["wage_adj"] * P["PWGTP"]
    wage_q = P.dropna(subset=["paei_q"]).groupby("paei_q")["w_wt"].sum()
    wage_tot = wage_q.sum()

    # mortgage service attributed by household wage shares (as in build_dar.py)
    hh_tot = P.groupby("SERIALNO")["wage_adj"].sum().rename("hh_wage")
    byq = (P.dropna(subset=["paei_q"]).groupby(["SERIALNO", "paei_q"])["wage_adj"]
             .sum().unstack(fill_value=0.0))
    byq.columns = [f"q{int(c)}" for c in byq.columns]
    sh = byq.join(hh_tot, how="right").fillna(0.0)
    qc = [c for c in sh.columns if c.startswith("q")]
    for c in qc:
        sh[c] = np.where(sh["hh_wage"] > 0, sh[c] / sh["hh_wage"], 0.0)

    H["TEN"] = pd.to_numeric(H["TEN"], errors="coerce")
    H["MRGP"] = pd.to_numeric(H["MRGP"], errors="coerce")
    H["WGTP"] = pd.to_numeric(H["WGTP"], errors="coerce")
    M = H[(H["TEN"] == 1) & (H["MRGP"] > 0)].merge(sh[qc], left_on="SERIALNO",
                                                   right_index=True, how="left")
    M[qc] = M[qc].fillna(0.0)
    M["ann"] = M["MRGP"] * 12.0
    svc = {c: float((M["ann"] * M[c] * M["WGTP"]).sum()) for c in sorted(qc)}
    svc_tot = sum(svc.values())

    rows = []
    for i, c in enumerate(sorted(qc), start=1):
        wq = float(wage_q.get(float(i), np.nan))
        rows.append({
            "paei_quintile": c,
            "wage_income_usd_bn": wq / 1e9,
            "share_of_wage_income_pct": 100 * wq / wage_tot,
            "mortgage_service_usd_bn": svc[c] / 1e9,
            "share_of_mortgage_service_pct": 100 * svc[c] / svc_tot,
            "concentration_ratio": (svc[c] / svc_tot) / (wq / wage_tot),
            "service_to_income_pct": 100 * svc[c] / wq,
        })
    t = pd.DataFrame(rows)
    t.round(3).to_csv(OUT / "dar_intensity_us.csv", index=False)
    (OUT / "dar_intensity_summary.json").write_text(json.dumps(
        {"paei_quintile_cutpoints": [float(x) for x in qs],
         "rows": t.round(4).to_dict("records")}, indent=2))

    pd.set_option("display.width", 200)
    print("\n=== DAR intensity by PAEI quintile (US, ACS PUMS 2023) ===")
    print(t.round(2).to_string(index=False))
    print("\nconcentration_ratio > 1 means mortgage debt service is over-represented "
          "relative to that quintile's share of wage income.")


if __name__ == "__main__":
    main()
