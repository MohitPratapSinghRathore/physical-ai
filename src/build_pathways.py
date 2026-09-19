"""Item 3: pathway decomposition. Now the paper's primary structure (D18).

Three pathways, each with its own technology, its own clock, and its own gate:

  MANIPULATION   general-purpose physical manipulation robotics. The residual after the
                 other two are removed. This is the pathway PAEI was built for.
  DRIVING        exposure running through autonomous vehicles on public roads. A separate
                 capability pathway with its own regulatory clock and an observable
                 deployment record.

                 DEFINED BY SOC, NOT BY DESCRIPTOR. The A6 descriptor flag was built on
                 O*NET "Operating Vehicles, Mechanized Devices, or Equipment", which
                 captures forklifts, power tools and construction plant, so it wrongly
                 flagged electricians, carpenters, construction labourers and agricultural
                 workers as driving-exposed. Driving is therefore SOC major group 53-3,
                 Motor Vehicle Operators: truck and driver/sales workers, taxi drivers,
                 school and transit bus drivers, shuttle drivers and chauffeurs, ambulance
                 drivers. 6 occupations, 6.04 million workers. The descriptor version is
                 retained as a sensitivity in a6_occupation_flags.csv.
  GATED          accountability or interpersonally gated work. Substitution is constrained
                 by liability, statute and the interpersonal content of the job, not by
                 manipulation capability.

Pathways are made MUTUALLY EXCLUSIVE by priority: driving, then gated, then manipulation.
The priority is a reporting choice, not a claim: an occupation that both drives and carries
custodial accountability is assigned to driving because the driving clock is the one with
observable public evidence. Overlap counts are reported so the choice can be undone.

Scope: occupations at or above the median embodiment P. Below that, exposure runs through
cognitive AI and is out of scope for this paper.

Each pathway is reported with employment, wage bill, embodiment-weighted wage bill, and the
mortgage and rent debt service attributable to it through household wage shares.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
PATHS = ["driving", "gated", "manipulation"]


def chunks(zf, fn, cols, size=300_000):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype={"SERIALNO": str},
                              chunksize=size, low_memory=False):
            yield ch


def main():
    fl = pd.read_csv(OUT / "a6_occupation_flags.csv")
    fl = fl[fl["employment"].notna() & (fl["employment"] > 0)].copy()
    P_MED = float(fl["embodiment_P"].median())
    fl["in_scope"] = fl["embodiment_P"] >= P_MED

    fl["soc"] = fl["soc"].astype(str)
    fl["is_driving"] = fl["soc"].str.startswith("53-3")
    fl["pathway"] = np.select(
        [~fl["in_scope"],
         fl["is_driving"],
         (fl["flag_accountability"] == 1) | (fl["flag_interpersonal"] == 1)],
        ["out_of_scope", "driving", "gated"], default="manipulation")

    overlap = {
        "driving_definition": "SOC 53-3 Motor Vehicle Operators",
        "driving_and_gated": int((fl["is_driving"] & fl["in_scope"]
                                  & ((fl["flag_accountability"] == 1)
                                     | (fl["flag_interpersonal"] == 1))).sum()),
        "driving_occupations_in_scope": int((fl["is_driving"] & fl["in_scope"]).sum()),
        "driving_occupations_out_of_scope_low_P": int(
            (fl["is_driving"] & ~fl["in_scope"]).sum()),
        "descriptor_flag_would_have_included": int(
            ((fl["flag_driving"] == 1) & fl["in_scope"] & ~fl["is_driving"]).sum()),
        "P_median_scope_gate": P_MED,
    }
    fl.to_csv(OUT / "pathway_assignment.csv", index=False)
    pmap = dict(zip(fl["occp"], fl["pathway"]))
    Pmap = dict(zip(fl["occp"], fl["embodiment_P"]))

    # ---- person pass: household wage shares by pathway, plus owner-operator sizing ----
    print("person pass ...")
    parts, cow_rows = [], []
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["SERIALNO", "OCCP", "WAGP", "ADJINC", "PWGTP", "COW"]):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
            pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
            path = occ.map(pmap)
            Pv = occ.map(Pmap)
            d = pd.DataFrame({"SERIALNO": ch["SERIALNO"], "wage": wage,
                              "path": path, "P": Pv})
            d = d[d["wage"] > 0]
            if len(d):
                piv = d.assign(v=d["wage"] * d["P"].fillna(0.0))
                w = piv.pivot_table(index="SERIALNO", columns="path", values="v",
                                    aggfunc="sum")
                w["__tot"] = d.groupby("SERIALNO")["wage"].sum()
                parts.append(w)
            cow_rows.append(pd.DataFrame({
                "occp": occ, "path": path, "cow": pd.to_numeric(ch["COW"], errors="coerce"),
                "pw": pw, "wage": wage}))
    HH = pd.concat(parts).groupby(level=0).sum()
    for p in PATHS:
        if p not in HH.columns:
            HH[p] = 0.0
        HH[f"share_{p}"] = np.where(HH["__tot"] > 0, HH[p].fillna(0.0) / HH["__tot"], 0.0)
    HH = HH[[f"share_{p}" for p in PATHS]]

    # ---- owner-operator drivers ----
    C = pd.concat(cow_rows, ignore_index=True)
    C = C[C["occp"].notna()]
    drv = C[C["path"] == "driving"]
    selfemp = drv[drv["cow"].isin([6, 7])]
    oo = {
        "driving_employment": float(drv["pw"].sum()),
        "driving_self_employed_employment": float(selfemp["pw"].sum()),
        "driving_self_employed_pct": float(100 * selfemp["pw"].sum() / drv["pw"].sum())
        if drv["pw"].sum() else np.nan,
        "driving_self_employed_wage_bill_usd_bn":
            float((selfemp["wage"] * selfemp["pw"]).sum() / 1e9),
        "cow_codes_used": "6 = self-employed not incorporated, 7 = self-employed incorporated",
    }
    trk = C[C["occp"].isin([9130])]  # Driver/sales workers and truck drivers
    if len(trk):
        t_self = trk[trk["cow"].isin([6, 7])]
        oo["truck_occp9130_employment"] = float(trk["pw"].sum())
        oo["truck_occp9130_self_employed"] = float(t_self["pw"].sum())
        oo["truck_occp9130_self_employed_pct"] = float(
            100 * t_self["pw"].sum() / trk["pw"].sum()) if trk["pw"].sum() else np.nan

    # ---- household pass ----
    print("household pass ...")
    hparts = []
    for zf, fn in HPART:
        for ch in chunks(zf, fn, ["SERIALNO", "WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG"]):
            for c in ["WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG"]:
                ch[c] = pd.to_numeric(ch[c], errors="coerce")
            a = ch["ADJHSG"] / 1e6
            ch["mort"] = np.nan_to_num(np.where(ch["TEN"] == 1, ch["MRGP"] * 12 * a, 0.0))
            ch["rent"] = np.nan_to_num(np.where(ch["TEN"] == 3, ch["GRNTP"] * 12 * a, 0.0))
            hparts.append(ch[["SERIALNO", "WGTP", "mort", "rent"]])
    H = pd.concat(hparts, ignore_index=True).join(HH, on="SERIALNO")
    for p in PATHS:
        H[f"share_{p}"] = H[f"share_{p}"].fillna(0.0)

    # ---- assemble ----
    rows = []
    tot_mort = float((H["mort"] * H["WGTP"]).sum())
    tot_rent = float((H["rent"] * H["WGTP"]).sum())
    for p in PATHS:
        sel = fl[fl["pathway"] == p]
        emp = float(sel["employment"].sum())
        wb = float(sel["wage_bill"].sum())
        pwb = float((sel["wage_bill"] * sel["embodiment_P"]).sum())
        m = float((H["mort"] * H[f"share_{p}"] * H["WGTP"]).sum())
        r = float((H["rent"] * H[f"share_{p}"] * H["WGTP"]).sum())
        rows.append({"pathway": p, "n_occupations": int(len(sel)),
                     "employment": emp, "wage_bill_usd_bn": wb / 1e9,
                     "embodiment_weighted_wage_bill_usd_bn": pwb / 1e9,
                     "mortgage_at_risk_usd_bn": m / 1e9,
                     "mortgage_share_of_national_pct": 100 * m / tot_mort,
                     "rent_at_risk_usd_bn": r / 1e9,
                     "rent_share_of_national_pct": 100 * r / tot_rent})
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "pathway_totals.csv", index=False)

    top = {}
    for p in PATHS:
        sel = fl[fl["pathway"] == p].copy()
        sel["empP"] = sel["employment"] * sel["embodiment_P"]
        top[p] = sel.nlargest(10, "empP")[["title", "embodiment_P", "employment",
                                           "wage_bill"]].round(3).to_dict("records")
    (OUT / "pathway_summary.json").write_text(json.dumps(
        {"overlap": overlap, "owner_operators": oo,
         "totals": T.round(4).to_dict("records"), "top_occupations": top}, indent=2))

    pd.set_option("display.width", 220)
    print(f"\nscope gate: P >= {P_MED:.3f}; out of scope occupations: "
          f"{int((fl['pathway'] == 'out_of_scope').sum())}")
    print(f"overlap driving AND gated (assigned to driving): {overlap['driving_and_gated']}")
    print("\n=== PATHWAY TOTALS ===")
    print(T.round(2).to_string(index=False))
    print("\n=== Owner-operator / self-employed in the driving pathway ===")
    for k, v in oo.items():
        print(f"  {k:44s} {v if isinstance(v, str) else round(v, 2)}")
    for p in PATHS:
        print(f"\n-- top occupations, {p} --")
        print(pd.DataFrame(top[p])[["title", "embodiment_P", "employment"]]
              .to_string(index=False, max_colwidth=46))


if __name__ == "__main__":
    main()
