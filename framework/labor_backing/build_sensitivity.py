"""B9 support: sensitivity of the headline to every named judgement call, and the two
time series charts. PROVISIONAL.

Each judgement call is varied ONE AT A TIME against the central case, so the reported
move is that call's own contribution and not a joint effect. The full range is then the
min and max of the one-at-a-time grid, which UNDERSTATES the true range if the calls
interact. That understatement is stated rather than hidden.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import config as C


def main():
    summ = json.loads((HERE / "direct_ratio_latest.json").read_text())
    ind = json.loads((HERE / "indirect_extension.json").read_text())
    cls = pd.read_csv(HERE / "claim_class_rules.csv").set_index("claim_class")
    T = pd.read_csv(HERE / "direct_ratio_timeseries.csv")
    H = pd.read_csv(HERE / "holder_matrix_latest.csv")

    lvl = cls["level_bn"].to_dict()
    base = {k: v["backing"] for k, v in summ["by_class"].items()}
    total = float(summ["total_claims_bn"])

    def ratio(b):
        return sum(lvl[k] * b[k] for k in lvl) / total

    central = ratio(base)

    calls = [
        ("mortgage backing: ACS service 0.8402 (central) vs SIPP balances 0.8205",
         {"home_mortgage": 0.8205}),
        ("mortgage backing: ACS service vs the superseded A38 definition 0.80305",
         {"home_mortgage": 0.80305}),
        ("rent backing: engine core 0.7275 (central) vs the A38 definition 0.69913",
         {"multifamily_mortgage": 0.69913}),
        ("federal receipts: SOI-split central vs the 77.7 percent upper bound",
         {"treasury": 0.7768}),
        ("state and local: wage-split central vs all personal current taxes",
         {"state_local_debt": float(cls.loc["state_local_debt", "labour_backing_share"])
          / 0.66754 if cls.loc["state_local_debt", "labour_backing_share"] > 0 else 0.0}),
        ("other consumer: blend (central) vs the card share alone",
         {"other_consumer": base["credit_card"]}),
        ("THE ONE-STEP RULE: business classes zero (central) vs the B2 indirect share",
         {k: ind["indirect_labour_backing_of_business_revenue"]
          for k in ind["business_revenue_serviced_classes"]}),
        ("commercial mortgage treated like multifamily rather than zero",
         {"commercial_mortgage": base["multifamily_mortgage"]}),
    ]

    rows = [dict(judgement_call="CENTRAL CASE", ratio=round(central, 6),
                 move_from_central=0.0, move_pct=0.0)]
    for name, override in calls:
        b = dict(base)
        b.update(override)
        r = ratio(b)
        rows.append(dict(judgement_call=name, ratio=round(r, 6),
                         move_from_central=round(r - central, 6),
                         move_pct=round(100 * (r / central - 1), 2)))
    S = pd.DataFrame(rows)
    S["abs_move"] = S["move_from_central"].abs()
    S = pd.concat([S.iloc[:1], S.iloc[1:].sort_values("abs_move", ascending=False)])
    S.drop(columns="abs_move").to_csv(HERE / "sensitivity.csv", index=False)

    # holder judgement calls
    fed = float(H[H.holder == "federal_government"]["labour_backed_bn"].sum())
    lb_tot = float(H["labour_backed_bn"].sum())
    sov = summ["sovereign_exposure"]
    pools_only = float(H[(H.holder == "federal_government")
                         & (H.claim_class.isin(["home_mortgage", "multifamily_mortgage"]))]
                       ["labour_backed_bn"].sum())
    hrows = [
        dict(judgement_call="CENTRAL: agency pools, GSEs and the central bank all federal",
             federal_share_of_labour_backed=round(fed / lb_tot, 6),
             sovereign_union_share=sov["share_union"]),
        dict(judgement_call="agency pools NOT federal (guarantee ignored, investors bear it)",
             federal_share_of_labour_backed=round((fed - pools_only) / lb_tot, 6),
             sovereign_union_share=round(
                 (sov["labour_backed_sovereign_exposure_bn"] - pools_only) / lb_tot, 6)),
        dict(judgement_call="obligor leg EXCLUDED (holder and guarantor only)",
             federal_share_of_labour_backed=round(fed / lb_tot, 6),
             sovereign_union_share=sov["share_held_or_guaranteed"]),
    ]
    HS = pd.DataFrame(hrows)
    HS.to_csv(HERE / "sensitivity_holder.csv", index=False)

    lo, hi = S["ratio"].min(), S["ratio"].max()
    out = dict(
        status="PROVISIONAL, one-at-a-time sensitivity",
        central_ratio=round(central, 6),
        range_low=round(float(lo), 6), range_high=round(float(hi), 6),
        largest_single_call=S.iloc[1]["judgement_call"] if len(S) > 1 else None,
        largest_single_move_pct=float(S.iloc[1]["move_pct"]) if len(S) > 1 else None,
        sovereign_union_central=sov["share_union"],
        sovereign_union_range=[float(HS["sovereign_union_share"].min()),
                               float(HS["sovereign_union_share"].max())],
        caveat="ONE AT A TIME. The stated range UNDERSTATES the true range if the calls "
               "interact, and the one-step rule interacts with everything.")
    (HERE / "sensitivity.json").write_text(json.dumps(out, indent=1))

    # ---------------- the two charts
    fig, ax = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True)
    ax[0].plot(T["year"], T["direct_labour_backing_ratio"], lw=2, color="#1f4e79")
    ax[0].axhline(central, ls=":", lw=1, color="#888")
    ax[0].set_ylabel("direct labour backing ratio")
    ax[0].set_title("The direct labour backing ratio and the sovereign share of it, "
                    f"{int(T.year.min())} to {int(T.year.max())}\n"
                    "PROVISIONAL, first round only, business-revenue classes zero by rule",
                    fontsize=10, loc="left")
    ax[0].grid(alpha=.25)
    ax[1].plot(T["year"], T["sovereign_share_union"], lw=2, color="#943126",
               label="union: held, guaranteed or owed")
    ax[1].plot(T["year"], T["sovereign_share_of_labour_backed"], lw=1.6, ls="--",
               color="#c0703b", label="held or guaranteed only")
    ax[1].set_ylabel("federal share of labour-backed claims")
    ax[1].set_xlabel("year")
    ax[1].legend(fontsize=8, frameon=False)
    ax[1].grid(alpha=.25)
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(HERE / "fig_labour_backing_two_panel.png", dpi=160)

    print(S.drop(columns="abs_move").to_string(index=False))
    print()
    print(HS.to_string(index=False))
    print(f"\ncentral {central:.4f}, one-at-a-time range {lo:.4f} to {hi:.4f}")


if __name__ == "__main__":
    main()
