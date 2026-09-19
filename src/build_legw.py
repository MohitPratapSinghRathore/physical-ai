"""Build the US Leg W panel. All units normalised to USD billions using FRED-reported units."""
import json, pathlib, sys
import pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))

ROOT = pathlib.Path(__file__).parents[1]
RAW = ROOT / "data" / "raw" / "fred"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
MAN = json.loads((RAW / "_manifest.json").read_text())

SCALE = {"Millions of U.S. Dollars": 1e-3, "Millions of Dollars": 1e-3,
         "Billions of Dollars": 1.0, "Billions of US Dollars": 1.0}

def load(sid):
    df = pd.read_csv(RAW / f"{sid}.csv")
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    u = MAN[sid]["units"]
    df["value"] *= SCALE.get(u, 1.0)          # -> USD bn where monetary
    df["units_out"] = "USD bn" if u in SCALE else u
    return df.dropna(subset=["value"]).set_index("date")["value"], df["units_out"].iloc[0]

def latest(s, asof=None):
    s = s[s.index <= asof] if asof else s
    return s.index[-1], s.iloc[-1]

def main():
    panel, meta = {}, {}
    for sid in MAN:
        s, u = load(sid)
        panel[sid] = s
        d, v = latest(s)
        meta[sid] = {"date": d.date().isoformat(), "value": v, "units": u,
                     "title": MAN[sid]["title"], "leg": MAN[sid]["leg"]}
    wide = pd.DataFrame(panel).sort_index()
    wide.to_csv(OUT / "us_panel.csv")

    g = lambda k: meta[k]["value"]
    gdp = g("GDP")
    rows = []
    add = lambda comp, sid, tier: rows.append(
        {"economy": "US", "leg": "W", "component": comp, "series": sid,
         "value_usd_bn": round(g(sid), 1), "pct_gdp": round(100 * g(sid) / gdp, 1),
         "asof": meta[sid]["date"], "tier": tier, "source_title": meta[sid]["title"]})

    add("Household debt, total (Z.1)", "CMDEBT", "1")
    add("of which: home mortgages 1-4 family", "HHMSDODNS", "1")
    add("of which: consumer credit", "CCLBSHNO", "1")
    add("of which: federal student loans held", "FGCCSAQ027S", "1")
    add("Federal public debt, total", "GFDEBTN", "1")
    add("Wage and salary accruals (annual rate)", "WASCUR", "flow")
    add("Compensation of employees (annual rate)", "COE", "flow")
    add("Personal current taxes, federal (annual rate)", "A074RC1Q027SBEA", "flow")
    add("Social insurance contributions, federal (annual rate)", "W780RC1Q027SBEA", "flow")
    add("Federal current tax receipts (annual rate)", "W006RC1Q027SBEA", "flow")
    add("Corporate profits before tax (annual rate)", "A053RC1Q027SBEA", "flow")
    add("GDP (annual rate)", "GDP", "denom")

    t = pd.DataFrame(rows)
    t.to_csv(OUT / "legW_us.csv", index=False)

    # --- derived: labor-tax dependence of the sovereign leg ---
    # Federal labor-linked receipts: personal current taxes + federal social insurance
    # contributions. NIPA books contributions OUTSIDE "current tax receipts", so the
    # denominator must be federal CURRENT RECEIPTS, not current tax receipts.
    labor_tax = g("A074RC1Q027SBEA") + g("W780RC1Q027SBEA")
    fed_tax = g("W006RC1Q027SBEA")
    fed_rec = g("FGRECPT")
    derived = {
        "asof_gdp": meta["GDP"]["date"],
        "gdp_usd_bn": round(gdp, 1),
        "hh_debt_usd_bn": round(g("CMDEBT"), 1),
        "hh_debt_pct_gdp": round(100 * g("CMDEBT") / gdp, 1),
        "fed_debt_usd_bn": round(g("GFDEBTN"), 1),
        "fed_debt_pct_gdp": round(100 * g("GFDEBTN") / gdp, 1),
        "legW_broad_usd_bn": round(g("CMDEBT") + g("GFDEBTN"), 1),
        "legW_broad_pct_gdp": round(100 * (g("CMDEBT") + g("GFDEBTN")) / gdp, 1),
        "labor_tax_usd_bn": round(labor_tax, 1),
        "fed_personal_current_taxes_usd_bn": round(g("A074RC1Q027SBEA"), 1),
        "fed_social_insurance_contrib_usd_bn": round(g("W780RC1Q027SBEA"), 1),
        "fed_labor_linked_receipts_usd_bn": round(labor_tax, 1),
        "labor_share_of_fed_current_receipts_pct": round(100 * labor_tax / fed_rec, 1),
        "fed_current_receipts_usd_bn": round(fed_rec, 1),
        "fed_current_tax_receipts_usd_bn": round(fed_tax, 1),
        "wage_bill_usd_bn": round(g("WASCUR"), 1),
        "compensation_usd_bn": round(g("COE"), 1),
        "wage_share_gdi_pct": round(g("W270RE1A156NBEA"), 1),
        "corp_profits_before_tax_usd_bn": round(g("A053RC1Q027SBEA"), 1),
        "hh_debt_service_pct_dpi": round(g("TDSP"), 2),
        "hh_debt_to_gdp_bis_ratio": round(g("HDTGPDUSQ163N"), 1),
        "nonfin_corp_debt_usd_bn": round(g("TCMILBSNNCB"), 1),
    }
    (OUT / "legW_us_derived.json").write_text(json.dumps(derived, indent=2))
    (OUT / "us_series_meta.json").write_text(json.dumps(meta, indent=2))

    print(t.to_string(index=False, max_colwidth=44))
    print()
    for k, v in derived.items():
        print(f"  {k:46s} {v}")

if __name__ == "__main__":
    main()
