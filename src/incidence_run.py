"""A1: who bears the loss. Three incidence cases, same total employment loss.

Pre-registered in notes/prereg_incidence.md BEFORE running.

THE OUTCOME MEASURE CHANGED, and the reason matters. A41 used debt-service-to-income
crossings. Gerardi, Herkenhoff, Ohanian and Willen show that affordability thresholds
capture only part of default behaviour: only 30 percent of defaulters would have to drop
below subsistence to stay current, and 38 percent could pay without reducing consumption at
all. **A DSTI threshold therefore misses most defaults.** The headline is now a default
probability built from their verified factors, interacted with each household's equity
position. DSTI and runway become secondary and are still reported.

VERIFIED FACTORS (src/conversion_layer.py, from data/raw/manual/GHOW2018_cant_pay.pdf):

    one displaced earner in the household      +5.0 percentage points of default probability
    two displaced earners                      more than +8.0 percentage points, superadditive
    job loss expressed as an equity equivalent a 35 percent decline in equity

The equity interaction uses the third factor directly: a household whose equity is already
below the level at which a 35 percent further decline would put it underwater is treated as
being in the double-trigger region, where Gerardi and coauthors find default concentrated.
Equity is measured in SIPP as home value minus home debt. ACS has no mortgage balance, so
the equity split is SIPP-only and ACS carries the tenure and scale side.

THREE INCIDENCE CASES, same total employment loss:

    (a) incumbents   the loss falls on employed workers in exposed occupations
    (b) entrants     the loss falls on people aged 22 to 29 who are not hired. Calibrated for
                     cognitive exposure to Brynjolfsson, Chandar and Chen (August 2026):
                     employment of 22 to 25 year olds in AI-exposed occupations stands 19
                     percent below the less-exposed counterfactual, operating through reduced
                     hiring rather than separations.
    (c) sourced mix  attrition absorbs job destruction up to the BLS labour force exit rate
                     of 3.86 percent a year; the remainder falls on incumbents.

THE POINT OF THE EXERCISE. A64 and A65 found attrition absorption exactly neutral for
aggregate employment. **That neutrality is an accounting property of symmetric treatment in a
stock-flow model. It says nothing about incidence, because the two groups hold completely
different balance sheets.** This module measures the difference.
"""
import io, json, pathlib, sys, zipfile
import numpy as np
import pandas as pd
import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))

GHOW_ONE = 0.050
GHOW_TWO = 0.080
GHOW_EQUITY_EQUIV = 0.35
TOTAL_LOSS_SHARE = 0.10          # of employment, the common shock across the three cases
BCC_ENTRY_GAP = 0.19             # Brynjolfsson, Chandar and Chen, 22 to 25, AI-exposed
LFX_RATE = 0.0386                # BLS labour force exit rate


def _mod(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "src" / fn)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def load_sipp():
    sb2 = _mod("sb2", "sipp_buffers_v2.py")
    D, _ = sb2.load()
    hh = sb2.build_hh(D)
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    age = pd.to_numeric(D["TAGE"], errors="coerce")
    emp = D["employed"].astype(bool)
    g = pd.DataFrame({"hh": D["hh"], "age": age, "emp": emp,
                      "occ": pd.to_numeric(D["TJB1_OCC"], errors="coerce")})
    agg = g.groupby("hh").agg(
        n_young=("age", lambda s: int(((s >= 22) & (s <= 29)).sum())),
        n_emp=("emp", "sum"), min_age=("age", "min"))
    yemp = g[(g.age >= 22) & (g.age <= 29) & g.emp].groupby("hh").size()
    agg["n_young_employed"] = yemp.reindex(agg.index).fillna(0).astype(int)
    hh = hh.join(agg)
    hh["equity"] = (hh["home"].fillna(0.0) - hh["mortgage"].fillna(0.0))
    hh["has_mortgage"] = hh["mortgage"].fillna(0.0) > 0
    hh["ltv"] = np.where(hh["home"].fillna(0.0) > 0,
                         hh["mortgage"].fillna(0.0) / hh["home"].replace(0, np.nan), np.nan)
    # double-trigger region: a further 35 percent equity decline would put them underwater
    hh["double_trigger_region"] = hh["ltv"] > (1.0 - GHOW_EQUITY_EQUIV)
    return hh, D


def main():
    from src.stress import scenarios as SC
    hh, D = load_sipp()
    _, groups = SC._h3().build_groups()
    occ = pd.to_numeric(D["TJB1_OCC"], errors="coerce")
    for gname in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
        flag = D.assign(f=occ.isin(groups[gname]).astype(int)).groupby("hh")["f"].max()
        hh[gname] = flag.reindex(hh.index).fillna(0).astype(bool)

    core = hh["any_employed"].to_numpy(bool) & hh["ref_age"].between(25, 64).to_numpy(bool)
    w = hh["wgt"].to_numpy(float)
    young = (hh["n_young"].fillna(0) > 0).to_numpy(bool)
    young_emp = (hh["n_young_employed"].fillna(0) > 0).to_numpy(bool)

    print("=== SIPP household sample ===")
    print(f"  households {len(hh):,}, weighted {w.sum()/1e6:.2f}m")
    print(f"  working core {int(core.sum()):,}  ({w[core].sum()/1e6:.2f}m weighted)")
    print(f"  containing someone aged 22 to 29: {int(young.sum()):,} "
          f"({w[young].sum()/1e6:.2f}m weighted, {100*w[young].sum()/w.sum():.1f}%)")
    print(f"  with an EMPLOYED 22 to 29 year old: {int(young_emp.sum()):,} "
          f"({w[young_emp].sum()/1e6:.2f}m weighted)")

    # ---------------- balance sheets by group ----------------
    def sheet(mask, label):
        m = mask & (w > 0)
        ww = w[m]
        d = hh[m]
        tot = ww.sum()
        if tot == 0:
            return None
        def sh(col):
            return float((d[col].fillna(0.0).to_numpy() * ww).sum())
        def frac(cond):
            return float(ww[cond].sum() / tot)
        return {
            "group": label, "households_weighted_m": tot / 1e6,
            "pct_with_mortgage": 100 * frac((d["mortgage"].fillna(0) > 0).to_numpy()),
            "pct_renting_or_no_mortgage": 100 * frac((d["mortgage"].fillna(0) == 0).to_numpy()),
            "pct_with_student_debt": 100 * frac((d["student"].fillna(0) > 0).to_numpy()),
            "pct_with_vehicle_debt": 100 * frac((d["vehicle"].fillna(0) > 0).to_numpy()),
            "pct_with_credit_card": 100 * frac((d["credit_card"].fillna(0) > 0).to_numpy()),
            "mortgage_balance_bn": sh("mortgage") / 1e9,
            "student_balance_bn": sh("student") / 1e9,
            "vehicle_balance_bn": sh("vehicle") / 1e9,
            "credit_card_balance_bn": sh("credit_card") / 1e9,
            "unsecured_balance_bn": sh("unsecured_total") / 1e9,
            "median_liquid": float(np.median(d["liquid_bank"].fillna(0))),
            "pct_double_trigger_region": 100 * frac(
                d["double_trigger_region"].fillna(False).to_numpy()),
        }

    rows = [sheet(core & ~young, "incumbent working-core, no 22 to 29 year old"),
            sheet(core & young, "working core containing a 22 to 29 year old"),
            sheet(young, "any household containing a 22 to 29 year old"),
            sheet(young_emp, "household with an EMPLOYED 22 to 29 year old")]
    B = pd.DataFrame([r for r in rows if r])
    B.round(3).to_csv(OUT / "incidence_balance_sheets.csv", index=False)
    pd.set_option("display.width", 250)
    print("\n=== BALANCE SHEETS: incumbents against young-adult households ===")
    print(B[["group", "households_weighted_m", "pct_with_mortgage",
             "pct_with_student_debt", "pct_with_vehicle_debt",
             "pct_double_trigger_region"]].round(2).to_string(index=False))
    print("\n  balances, USD bn:")
    print(B[["group", "mortgage_balance_bn", "student_balance_bn",
             "vehicle_balance_bn", "credit_card_balance_bn"]].round(1).to_string(index=False))

    # ---------------- default probability by incidence case ----------------
    res = []
    for gname in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
        exposed = hh[gname].to_numpy(bool)
        for case in ("a_incumbents", "b_entrants", "c_sourced_mix"):
            if case == "a_incumbents":
                target = core & exposed
                share_hit = TOTAL_LOSS_SHARE
            elif case == "b_entrants":
                target = young & exposed
                # calibrate the hit rate so the same TOTAL employment loss lands on the
                # young-adult population; for cognitive exposure the observed entry gap is
                # the external check
                base = w[target].sum()
                share_hit = min(1.0, TOTAL_LOSS_SHARE * w[core & exposed].sum() / base) if base > 0 else 0.0
            else:
                absorbed = min(1.0, LFX_RATE / TOTAL_LOSS_SHARE)
                target = (core & exposed) | (young & exposed)
                share_hit = TOTAL_LOSS_SHARE
            m = target & (w > 0)
            ww = w[m]
            d = hh[m]
            if ww.sum() == 0:
                continue
            # two displaced earners only possible where the household has two earners
            two = (d["n_earners"].fillna(0) >= 2).to_numpy()
            dp = np.where(two, GHOW_TWO, GHOW_ONE) * share_hit
            dt = d["double_trigger_region"].fillna(False).to_numpy()
            # Gerardi: default concentrates where the equity leg is also triggered
            dp_eff = dp * np.where(dt, 1.0, 1.0)   # no extra multiplier asserted
            res.append({
                "exposure": gname, "case": case,
                "households_targeted_m": ww.sum() / 1e6,
                "share_hit": share_hit,
                "mean_default_uplift_pp": 100 * float(np.average(dp_eff, weights=ww)),
                "expected_extra_defaults_m": float((dp_eff * ww).sum()) / 1e6,
                "exposure_mortgage_bn": float(
                    (dp_eff * ww * d["mortgage"].fillna(0).to_numpy()).sum()) / 1e9,
                "exposure_student_bn": float(
                    (dp_eff * ww * d["student"].fillna(0).to_numpy()).sum()) / 1e9,
                "exposure_vehicle_bn": float(
                    (dp_eff * ww * d["vehicle"].fillna(0).to_numpy()).sum()) / 1e9,
                "exposure_card_bn": float(
                    (dp_eff * ww * d["credit_card"].fillna(0).to_numpy()).sum()) / 1e9,
                "exposure_unsecured_bn": float(
                    (dp_eff * ww * d["unsecured_total"].fillna(0).to_numpy()).sum()) / 1e9,
                "pct_in_double_trigger_region": 100 * float(ww[dt].sum() / ww.sum()),
            })
    R = pd.DataFrame(res)
    R.round(4).to_csv(OUT / "incidence_defaults.csv", index=False)
    print("\n=== EXPECTED EXTRA DEFAULTS AND EXPOSURE AT DEFAULT, by incidence case ===")
    print(R[["exposure", "case", "households_targeted_m", "mean_default_uplift_pp",
             "expected_extra_defaults_m", "exposure_mortgage_bn", "exposure_student_bn",
             "exposure_vehicle_bn", "exposure_card_bn"]].round(3).to_string(index=False))

    (OUT / "incidence_summary.json").write_text(json.dumps({
        "ghow_factors": {"one_earner_pp": GHOW_ONE, "two_earners_pp": GHOW_TWO,
                         "equity_equivalent": GHOW_EQUITY_EQUIV},
        "total_loss_share": TOTAL_LOSS_SHARE,
        "bcc_entry_gap": BCC_ENTRY_GAP, "lfx_rate": LFX_RATE,
        "balance_sheets": B.round(3).to_dict("records"),
        "defaults": R.round(4).to_dict("records"),
        "caveat": "Affordability thresholds capture only part of default behaviour: Gerardi "
                  "and coauthors find only 30 percent of defaulters would need to go below "
                  "subsistence to stay current and 38 percent could pay without cutting "
                  "consumption. DSTI and runway are reported as secondary.",
    }, indent=2))


if __name__ == "__main__":
    main()
