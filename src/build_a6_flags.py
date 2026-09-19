"""A6: three occupation-level FLAGS, not new index factors.

The index stays two-factor. These are diagnostic flags used to report the switcher list and
the wage bill at risk with and without each group, because each names a reason the headline
exposure number may be misleading:

  driving_dominant     exposure runs through autonomous vehicles, a separate capability
                       pathway with its own regulatory clock. Lumping it into a robotics
                       capability parameter c conflates two different technologies.
  interpersonal        the task is substantially about dealing with people. Even a fully
                       capable manipulator does not obviously substitute here.
  accountability       legal or custodial responsibility for people or for outcomes with
                       legal force. Substitution is gated by liability and statute, not
                       capability.

Flags are built from O*NET Work Activities and Work Context descriptors, thresholded at the
employment-weighted 70th percentile, and from SOC major-group membership where the
descriptor evidence is not the right instrument (custodial and legal accountability).
"""
import csv, io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

WA = "db_31_0_text/Work Activities.txt"
WC = "db_31_0_text/Work Context.txt"

DRIVING = [("4.A.3.a.4", WA, "IM")]                    # Operating Vehicles, Mechanized Devices
DRIVING_CTX = [("4.C.2.a.1.f", WC, "CX")]              # In an Enclosed Vehicle or Equipment
INTERPERSONAL = [("4.C.1.a.4", WC, "CX"),              # Contact With Others
                 ("4.C.1.b.1.f", WC, "CX"),            # Deal With External Customers
                 ("4.A.4.a.4", WA, "IM"),              # Establishing and Maintaining Relationships
                 ("4.A.4.a.8", WA, "IM")]              # Performing for or Working Directly with Public
ACCOUNT_CTX = [("4.C.1.c.1", WC, "CX"),                # Health and Safety of Other Workers
               ("4.C.3.a.1", WC, "CX")]                # Consequence of Error
ACCOUNT_SOC = {"23", "33", "29"}                       # Legal, Protective Service, Healthcare Practitioners


def read_scales(z):
    t = io.TextIOWrapper(z.open("db_31_0_text/Scales Reference.txt"),
                         encoding="utf-8", errors="replace")
    r = csv.reader(t, delimiter="\t"); next(r)
    return {x[0]: (float(x[2]), float(x[3])) for x in r}


def read_vals(z, fname, wanted):
    t = io.TextIOWrapper(z.open(fname), encoding="utf-8", errors="replace")
    r = csv.reader(t, delimiter="\t"); hdr = next(r)
    iv = hdr.index("Data Value")
    out = []
    for row in r:
        if (row[1], row[3]) in wanted:
            out.append((row[0], row[1], row[3], float(row[iv])))
    return pd.DataFrame(out, columns=["onet_soc", "element", "scale", "value"])


def construct(z, scales, spec):
    wanted = {(e, s) for e, _, s in spec}
    frames = []
    for f in {f for _, f, _ in spec}:
        w = {(e, s) for e, ff, s in spec if ff == f}
        if w:
            frames.append(read_vals(z, f, w))
    d = pd.concat(frames, ignore_index=True)
    lo = d["scale"].map(lambda s: scales[s][0])
    hi = d["scale"].map(lambda s: scales[s][1])
    d["norm"] = (d["value"] - lo) / (hi - lo)
    wide = d.pivot_table(index="onet_soc", columns="element", values="norm")
    return wide.mean(axis=1, skipna=True)


def main():
    z = zipfile.ZipFile(RAW / "onet" / "db_31_0_text.zip")
    scales = read_scales(z)
    drive = construct(z, scales, DRIVING + DRIVING_CTX).rename("drive_score")
    inter = construct(z, scales, INTERPERSONAL).rename("inter_score")
    acct = construct(z, scales, ACCOUNT_CTX).rename("acct_score")
    D = pd.concat([drive, inter, acct], axis=1).reset_index()
    D["soc"] = D["onet_soc"].astype(str).str[:7]
    S = D.groupby("soc")[["drive_score", "inter_score", "acct_score"]].mean().reset_index()

    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0].copy()
    base["broad"] = base["soc"].astype(str).str[:6]
    S["broad"] = S["soc"].str[:6]
    m = base.merge(S[["soc", "drive_score", "inter_score", "acct_score"]],
                   on="soc", how="left")
    bg = S.groupby("broad")[["drive_score", "inter_score", "acct_score"]].mean()
    m = m.merge(bg, on="broad", how="left", suffixes=("", "_b"))
    for c in ["drive_score", "inter_score", "acct_score"]:
        m[c] = m[c].fillna(m[f"{c}_b"])
    m = m[m["employment"].notna() & (m["employment"] > 0)].copy()

    def wpct(x, w, q):
        o = np.argsort(x); xs, ws = np.asarray(x)[o], np.asarray(w)[o]
        return float(np.interp(q, np.cumsum(ws) / ws.sum(), xs))

    thr = {c: wpct(m[c].fillna(0), m["employment"], 0.70)
           for c in ["drive_score", "inter_score", "acct_score"]}
    m["flag_driving"] = (m["drive_score"] >= thr["drive_score"]).astype(int)
    m["flag_interpersonal"] = (m["inter_score"] >= thr["inter_score"]).astype(int)
    m["flag_accountability"] = (
        (m["acct_score"] >= thr["acct_score"])
        | m["soc"].astype(str).str[:2].isin(ACCOUNT_SOC)).astype(int)

    flags = m[["occp", "soc", "title", "embodiment_P", "structure_S_rank",
               "structure_deficit_rank", "employment", "wage_bill",
               "drive_score", "inter_score", "acct_score",
               "flag_driving", "flag_interpersonal", "flag_accountability"]]
    flags.round(4).to_csv(OUT / "a6_occupation_flags.csv", index=False)

    # ---- effect on wage bill at risk, with and without each flagged group ----
    G = grid.merge(flags[["occp", "flag_driving", "flag_interpersonal",
                          "flag_accountability"]], on="occp", how="inner")
    rows = []
    for c in [0.2, 0.5, 0.8, 1.0]:
        g = G[G["c"] == c]
        ex = g["exposed_threshold_rank"] == 1
        full = float((g.loc[ex, "wage_bill"] * g.loc[ex, "embodiment_P"]).sum() / 1e9)
        rec = {"c": c, "wagebill_at_risk_all_usd_bn": full}
        for f in ["flag_driving", "flag_interpersonal", "flag_accountability"]:
            keep = ex & (g[f] == 0)
            v = float((g.loc[keep, "wage_bill"] * g.loc[keep, "embodiment_P"]).sum() / 1e9)
            rec[f"excl_{f.replace('flag_','')}_usd_bn"] = v
            rec[f"excl_{f.replace('flag_','')}_pct_removed"] = 100 * (full - v) / full if full else 0.0
        keep_all = ex & (g["flag_driving"] == 0) & (g["flag_interpersonal"] == 0) & (g["flag_accountability"] == 0)
        v = float((g.loc[keep_all, "wage_bill"] * g.loc[keep_all, "embodiment_P"]).sum() / 1e9)
        rec["excl_all_three_usd_bn"] = v
        rec["excl_all_three_pct_removed"] = 100 * (full - v) / full if full else 0.0
        rows.append(rec)
    A6 = pd.DataFrame(rows)
    A6.round(2).to_csv(OUT / "a6_wagebill_with_without_flags.csv", index=False)

    # ---- switcher list with flags ----
    sw = flags[(flags["structure_deficit_rank"] > 0.5)
               & (flags["structure_deficit_rank"] <= 0.8)].copy()
    P_MED = float(flags["embodiment_P"].median())
    sw = sw[sw["embodiment_P"] >= P_MED].copy()
    sw["emp_x_P"] = sw["employment"] * sw["embodiment_P"]
    sw = sw.sort_values("emp_x_P", ascending=False)
    sw.round(4).to_csv(OUT / "a6_switchers_flagged.csv", index=False)
    unflagged = sw[(sw["flag_driving"] == 0) & (sw["flag_interpersonal"] == 0)
                   & (sw["flag_accountability"] == 0)]

    summary = {
        "thresholds_employment_weighted_p70": thr,
        "flag_shares_of_employment_pct": {
            f: float(100 * m.loc[m[f] == 1, "employment"].sum() / m["employment"].sum())
            for f in ["flag_driving", "flag_interpersonal", "flag_accountability"]},
        "switchers": {"n_all": int(len(sw)), "n_unflagged": int(len(unflagged)),
                      "employment_all": float(sw["employment"].sum()),
                      "employment_unflagged": float(unflagged["employment"].sum())},
    }
    (OUT / "a6_summary.json").write_text(json.dumps(summary, indent=2))

    pd.set_option("display.width", 210)
    print("=== A6 flag shares of employment ===")
    for k, v in summary["flag_shares_of_employment_pct"].items():
        print(f"  {k:24s} {v:5.1f}%   (threshold {thr.get(k.replace('flag_','')+'_score', float('nan')):.3f})"
              if False else f"  {k:24s} {v:5.1f}%")
    print("\n=== Wage bill at risk with and without each flagged group (USD bn) ===")
    print(A6.round(1).to_string(index=False))
    print(f"\n=== Switchers (deficit 0.5-0.8, P >= {P_MED:.3f}) ===")
    print(f"  all: {len(sw)} occupations, {sw['employment'].sum():,.0f} workers")
    print(f"  unflagged: {len(unflagged)} occupations, "
          f"{unflagged['employment'].sum():,.0f} workers")
    print("\n  top 15 unflagged switchers (the cleanest Physical AI cases):")
    print(unflagged.head(15)[["title", "embodiment_P", "structure_deficit_rank",
                              "employment"]].round(3).to_string(index=False,
                                                                max_colwidth=46))


if __name__ == "__main__":
    main()
