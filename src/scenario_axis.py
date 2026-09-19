"""Scenario axis: re-express every scenario as a share of the TOTAL US wage bill.

THE PROBLEM. Every scenario in this project has been stated as a share of the EXPOSED wage
bill, where "exposed" means the top quintile of an index. That is a moving denominator: the
top quintile of Felten AIOE is 13.2 percent of employment and the top quintile of embodiment
P is 20.1, so "90 percent of exposed" means very different things across constructs and is
not comparable across them. It also caps the reachable displacement well below the level the
owner's hypothesis concerns.

THE FIX, in two parts.

1. Every scenario is now reported with the share of the TOTAL wage bill it displaces, beside
   the share-of-exposed figure. That is the comparable axis.

2. The grid is extended with BROADER exposure definitions, the top 30 and top 50 percent of
   each index by employment and the union of both types, so that displacement of 25, 50 and
   75 percent of the total wage bill is reachable. Everything beyond the observed range is
   labelled as such; broadening the definition does not make the extrapolation safe, it only
   makes it expressible.

A NOTE ON WHAT BROADENING MEANS. A63 and A65 showed that measured concentration falls
monotonically with group breadth, so a "top 50 percent" group is not a more aggressive
version of the top quintile; it is a different and much weaker claim about who is exposed.
The broad definitions are here to reach the owner's majority-displacement hypothesis on a
comparable axis, not because the exposure measure supports them equally at every breadth.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))

BREADTHS = [0.20, 0.30, 0.50]
SCORES = {"cognitive_AIOE": "aioe", "cognitive_GPT": "gpt", "embodied": "embodiment_P"}


def build():
    from src.stress import scenarios as SC
    h3 = SC._h3()
    B, _ = h3.build_groups()
    grid = pd.read_csv(OUT / "paei_c.csv")
    wb = grid[grid["c"] == 0.0][["occp", "wage_bill"]].drop_duplicates("occp")
    B = B.merge(wb, on="occp", how="left")
    B = B[B["employment"].notna() & (B["employment"] > 0)].copy()
    total_wb = float(B["wage_bill"].sum())
    total_emp = float(B["employment"].sum())

    groups = {}
    for name, col in SCORES.items():
        d = B.dropna(subset=[col]).sort_values(col)
        cum = np.cumsum(d["employment"].to_numpy()) / d["employment"].sum()
        for br in BREADTHS:
            cut = np.interp(1 - br, cum, d[col].to_numpy())
            groups[f"{name}_top{int(br*100)}"] = set(B.loc[B[col] >= cut, "occp"])
    # unions of the two types at each breadth
    for br in BREADTHS:
        b = int(br * 100)
        groups[f"both_AIOE_top{b}"] = (groups[f"cognitive_AIOE_top{b}"]
                                       | groups[f"embodied_top{b}"])
        groups[f"both_GPT_top{b}"] = (groups[f"cognitive_GPT_top{b}"]
                                      | groups[f"embodied_top{b}"])

    rows = []
    for g, s in groups.items():
        sub = B[B["occp"].isin(s)]
        rows.append({"group": g,
                     "n_occupations": len(s),
                     "employment": float(sub["employment"].sum()),
                     "employment_share": float(sub["employment"].sum() / total_emp),
                     "wage_bill_bn": float(sub["wage_bill"].sum()) / 1e9,
                     "wage_bill_share": float(sub["wage_bill"].sum() / total_wb)})
    G = pd.DataFrame(rows).sort_values("wage_bill_share")
    return G, total_wb, total_emp


def main():
    G, total_wb, total_emp = build()
    G.round(5).to_csv(OUT / "scenario_axis_groups.csv", index=False)

    pd.set_option("display.width", 220)
    print(f"=== total wage bill {total_wb/1e9:,.1f}bn, total employment "
          f"{total_emp:,.0f} ===")
    print("\n=== EXPOSURE GROUPS: employment share against WAGE BILL share ===")
    print(G[["group", "n_occupations", "employment_share",
             "wage_bill_bn", "wage_bill_share"]].round(4).to_string(index=False))

    # every scenario level, expressed on the total wage bill axis
    LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 1.00]
    rows = []
    for _, g in G.iterrows():
        for lv in LEVELS:
            rows.append({"group": g["group"], "level_of_exposed": lv,
                         "share_of_TOTAL_wage_bill": lv * g["wage_bill_share"],
                         "share_of_TOTAL_employment": lv * g["employment_share"]})
    S = pd.DataFrame(rows)
    S.round(5).to_csv(OUT / "scenario_axis_levels.csv", index=False)

    print("\n=== SHARE OF THE TOTAL WAGE BILL DISPLACED, by group and level ===")
    piv = S.pivot_table(index="group", columns="level_of_exposed",
                        values="share_of_TOTAL_wage_bill") * 100
    print(piv.round(1).to_string())

    print("\n=== WHICH COMBINATIONS REACH 25, 50 AND 75 PERCENT OF THE TOTAL WAGE BILL ===")
    for target in (0.25, 0.50, 0.75):
        hit = S[(S.share_of_TOTAL_wage_bill >= target - 0.03) &
                (S.share_of_TOTAL_wage_bill <= target + 0.03)]
        print(f"\n  target {target:.0%}:")
        if len(hit) == 0:
            print("    NOT REACHABLE with any group and level in the grid")
        for _, h in hit.sort_values("share_of_TOTAL_wage_bill").iterrows():
            print(f"    {h.group:26s} at {h.level_of_exposed:.0%} of exposed "
                  f"-> {h.share_of_TOTAL_wage_bill:.1%} of the total wage bill")

    maxreach = S.share_of_TOTAL_wage_bill.max()
    print(f"\n  maximum reachable: {maxreach:.1%} of the total wage bill "
          f"({S.loc[S.share_of_TOTAL_wage_bill.idxmax(),'group']} at 100 percent)")

    (OUT / "scenario_axis_summary.json").write_text(json.dumps({
        "total_wage_bill_bn": total_wb / 1e9, "total_employment": total_emp,
        "groups": G.round(5).to_dict("records"),
        "max_reachable_share_of_total_wage_bill": float(maxreach),
        "note": "Broadening the exposure definition makes majority displacement "
                "EXPRESSIBLE, not safe. Measured concentration falls monotonically with "
                "breadth (A63, A65), so a top-50 group is a weaker claim about who is "
                "exposed, not a more aggressive one.",
    }, indent=2))


if __name__ == "__main__":
    main()
