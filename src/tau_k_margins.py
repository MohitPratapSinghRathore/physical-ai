"""Amendments C and D: margins on the post-2017 fiscal result, and the depreciation regime
actually in force in 2026.

AMENDMENT D. CURRENT LAW, verified against the statute itself.

Source: 26 U.S.C. 168(k), read from the Legal Information Institute's text of the current
code on 2026-09-19.

    168(k)(1)(A) provides a first-year allowance equal to ONE HUNDRED PERCENT of the
    adjusted basis of qualified property.

    168(k)(6), the phase-down schedule that stepped the allowance down from 100 percent
    through 80, 60, 40 and 20 percent, is shown as REPEALED by Pub. L. 119-21, title VII,
    section 70301(b)(1)(B), July 4, 2025, 139 Stat. 189. Paragraph (8) is repealed by the
    same provision.

    168(k)(2)(A)(i) defines qualified property to include property with a recovery period of
    20 years or less and computer software under 167(f)(1)(B), which is exactly the
    equipment-and-software category AMR measure.

CONCLUSION, and it is more specific than "nothing changed": full immediate expensing for
equipment and software is in force in 2026 and the phase-down is gone from the statute. The
regime that produced AMR's post-2017 effective rate of 0.05 lapsed during the phase-down
years and was restored in July 2025. AMR's 0.05 is therefore the RIGHT value for the 2026
point, and it is retained for that reason rather than by default.

THE ONE PLACE THIS BITES. The 2024 DWS vintage sits inside the phase-down window, when the
allowance was 60 percent rather than 100. A partial allowance raises the effective rate on
the normal return above 0.05, toward the 2010s value of 0.10. This project has NO measured
effective rate for the phase-down years and will not interpolate one, so the 2024 point
retains 0.05 and carries this flag. It does not change any conclusion: the 2024 point fails
the condition at 0.05 and would fail by less at a higher rate, but the 2026 point, which
carries the conclusions, is on solid ground.

AMENDMENT C. MARGINS.

For every cell, margin = available tau_k minus required tau_k, with and without outlays.
Cells within 0.01 of flipping are listed, together with the change in R that would flip them.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
G_CASES = {"none_0.00": 0.0, "modest_0.10": 0.10, "full_0.25": 0.25}

CURRENT_LAW = {
    "statute": "26 U.S.C. 168(k)",
    "source": "Legal Information Institute text of the current code",
    "retrieved": "2026-09-19",
    "allowance_2026": 1.00,
    "phase_down_paragraph_6": "REPEALED by Pub. L. 119-21, title VII, sec. 70301(b)(1)(B), "
                              "July 4, 2025, 139 Stat. 189",
    "qualified_property_covers": "recovery period 20 years or less; computer software under "
                                 "167(f)(1)(B)",
    "tau_normal_2026_retained": 0.05,
    "reason": "Full expensing is in force, which is the regime AMR measured at 0.05. "
              "Retained because it is correct for 2026, not by default.",
    "caveat": "The 2024 vintage sits in the phase-down window (60 percent allowance) where "
              "the effective rate on the normal return would be above 0.05. No measured "
              "value exists for those years and none is interpolated.",
}


def required_R(tau_l, tau_k, g, rho, s=1.0):
    return 1.0 - (tau_k * s) / tau_l + g * (1.0 - rho) / tau_l


def main():
    T = pd.read_csv(OUT / "tau_k_second_pass.csv")
    rws = json.loads((OUT / "retained_wage_share_summary.json").read_text())
    R26, rho26 = rws["R_2026_central"], rws["rho_2026"]

    post = T[(T.tau_normal_case == "post_TCJA_0.05") & (T.sourced)].copy()
    rows = []
    for _, r in post.iterrows():
        for gn, g in G_CASES.items():
            # required tau_k such that R >= 1 - tau_k/tau_l + g(1-rho)/tau_l
            for ln, tl in TAU_L.items():
                need = (1 - R26) * tl + g * (1 - rho26)
                rows.append({
                    "sigma_case": r.sigma_case, "domestic_case": r.domestic_case,
                    "tau_k_available": r.tau_k, "tau_l": ln, "g": gn,
                    "tau_k_required": need,
                    "margin": r.tau_k - need,
                    "passes": r.tau_k >= need,
                    "R_required_at_this_tau_k": required_R(tl, r.tau_k, g, rho26),
                    "R_gap": R26 - required_R(tl, r.tau_k, g, rho26)})
    M = pd.DataFrame(rows)
    M.round(5).to_csv(OUT / "tau_k_margins_post2017.csv", index=False)
    (OUT / "current_law_168k.json").write_text(json.dumps(CURRENT_LAW, indent=2))

    pd.set_option("display.width", 250)
    print("=== AMENDMENT D: depreciation regime in force, 2026 ===")
    for k, v in CURRENT_LAW.items():
        print(f"  {k}: {v}")

    print("\n=== AMENDMENT C: MARGINS on every post-2017 cell (margin = available minus required) ===")
    for gn in G_CASES:
        s = M[M.g == gn]
        print(f"\n-- outlays g = {gn}: {int(s.passes.sum())} of {len(s)} cells pass, "
              f"best margin {s.margin.max():+.4f} --")
        piv = s.pivot_table(index=["sigma_case", "domestic_case"], columns="tau_l",
                            values="margin")
        print(piv.round(4).to_string())

    print("\n=== cells WITHIN 0.01 of flipping (either direction), any g ===")
    close = M[M.margin.abs() <= 0.01].sort_values("margin")
    if len(close) == 0:
        print("  NONE. Every cell is further than 0.01 from the threshold.")
        n = M.reindex(M.margin.abs().sort_values().index).head(4)
        print("  closest four:")
        for _, r in n.iterrows():
            print(f"    {r.sigma_case:16s} {r.domestic_case:24s} tau_l {r.tau_l:16s} "
                  f"g {r.g:12s} margin {r.margin:+.4f}")
    else:
        for _, r in close.iterrows():
            print(f"  {r.sigma_case:16s} {r.domestic_case:24s} tau_l {r.tau_l:16s} "
                  f"g {r.g:12s} margin {r.margin:+.4f}")

    print("\n=== what change in R would flip each post-2017 cell, g = none ===")
    s = M[M.g == "none_0.00"].copy()
    s["R_needed"] = R26 - s["R_gap"]
    s["delta_R_to_flip"] = s["R_needed"] - R26
    top = s.reindex(s.delta_R_to_flip.abs().sort_values().index).head(8)
    for _, r in top.iterrows():
        need_rho = r.R_needed / rws["omegas"]["counterfactual_blended_central"]
        feas = "ATTAINABLE" if need_rho <= 0.74 else "NEVER OBSERVED (max rho 0.74)"
        print(f"  {r.sigma_case:16s} {r.domestic_case:24s} tau_l {r.tau_l:16s} "
              f"needs R {r.R_needed:.4f} (rho {need_rho:.3f})  "
              f"delta {r.delta_R_to_flip:+.4f}  {feas}")

    print(f"\n  observed R = {R26:.4f}, rho = {rho26:.4f}; "
          f"highest rho ever observed in the 14 vintages = 0.740")


if __name__ == "__main__":
    main()
