"""The capital tax rate exposure, moved into the main text.

WHY THIS EXISTS. IMF SDN/2024/002 puts the advanced-economy average tax rate on capital
income at roughly 0.20 to 0.22 and the US somewhat below that but still well above this
project's OPERATIVE effective rate of 0.0708. The required rate to close the fiscal condition
is 0.110 to 0.137. So the condition FAILS at our rate and PASSES at theirs, and the whole
verdict turns on which rate is the right one.

That cannot sit in a footnote. This module restates the condition as an explicit function of
tau_k, locates both rates on it, and computes the one number that makes the disagreement
tractable: the share of the AI surplus that would have to bear the higher rate for the
condition to pass.

No new estimation. Every input is read from data/processed/replication_r_sensitivity.json,
which is unchanged.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
FIG = ROOT / "paper" / "figures"

# The two rates, and what each one is a rate ON. This distinction is the whole argument.
OPERATIVE = 0.0708          # ours: the effective rate on the AI SURPLUS
IMF_AE_LOW, IMF_AE_HIGH = 0.20, 0.22   # IMF SDN/2024/002 Figure 14, advanced economies
SOURCED_HIGH = 0.20351      # our own sourced maximum, built independently


def main():
    S = json.loads((OUT / "replication_r_sensitivity.json").read_text())
    base = S["ours_observed_rho_and_our_omega"]
    R = base["R"]
    req = base["required_tau_k"]
    req_lo, req_hi = min(req.values()), max(req.values())

    # ---- the condition as a function of tau_k.
    # The condition passes when tau_k >= the required rate, which is itself a function of R
    # and tau_l. tau_l * (1 - R) is the labour revenue lost; tau_k must cover it.
    rows = []
    for name, tl in [("AMR_0.255", 0.255), ("bottom_up_0.301", 0.301),
                     ("bottom_up_0.318", 0.318)]:
        r = req[name]
        for tk in np.round(np.arange(0.00, 0.2601, 0.005), 4):
            rows.append({"tau_l_reading": name, "tau_l": tl, "R": R,
                         "required_tau_k": r, "tau_k": float(tk),
                         "condition_passes": bool(tk >= r),
                         "margin": float(tk - r)})
    C = pd.DataFrame(rows)
    C.to_csv(OUT / "tau_k_condition_curve.csv", index=False)

    # ---- the mixture: what share of the AI surplus must bear the higher rate
    mix = []
    for hi_name, tau_hi in [("IMF advanced economy low, 0.20", IMF_AE_LOW),
                            ("IMF advanced economy high, 0.22", IMF_AE_HIGH),
                            ("our own sourced maximum, 0.20351", SOURCED_HIGH)]:
        for rq_name, rq in [("required low", req_lo), ("required high", req_hi)]:
            s = (rq - OPERATIVE) / (tau_hi - OPERATIVE)
            mix.append({"higher_rate": hi_name, "tau_high": tau_hi,
                        "required": rq_name, "required_tau_k": rq,
                        "share_of_AI_surplus_at_higher_rate": round(s, 4)})
    M = pd.DataFrame(mix)
    M.to_csv(OUT / "tau_k_mixture_share.csv", index=False)

    summ = {
        "R": R,
        "operative_tau_k_ours": OPERATIVE,
        "operative_is_a_rate_on": "the AI SURPLUS, after expensing exempts the normal return "
                                  "and after a share of rents is shifted abroad",
        "imf_measured_range": [IMF_AE_LOW, IMF_AE_HIGH],
        "imf_is_a_rate_on": "all capital income, economy-wide, INCLUDING personal-level taxes "
                            "on dividends and realised capital gains",
        "our_sourced_maximum": SOURCED_HIGH,
        "required_tau_k_range": [round(req_lo, 6), round(req_hi, 6)],
        "condition_at_operative": "FAILS",
        "condition_at_imf_measured": "PASSES",
        "condition_at_our_sourced_maximum": "PASSES",
        "share_of_AI_surplus_needed_at_0.20": [
            round((req_lo - OPERATIVE) / (IMF_AE_LOW - OPERATIVE), 4),
            round((req_hi - OPERATIVE) / (IMF_AE_LOW - OPERATIVE), 4)],
        "share_of_AI_surplus_needed_at_0.22": [
            round((req_lo - OPERATIVE) / (IMF_AE_HIGH - OPERATIVE), 4),
            round((req_hi - OPERATIVE) / (IMF_AE_HIGH - OPERATIVE), 4)],
        "headline": "The fiscal condition is NOT a verdict under current law. It is a "
                    "function of tau_k with a threshold at 0.110 to 0.137, and the two "
                    "defensible measurements of tau_k fall on opposite sides of it.",
    }
    (OUT / "tau_k_exposure_summary.json").write_text(json.dumps(summ, indent=2))

    # ---- the figure
    FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    tk = np.linspace(0, 0.26, 400)
    ax.axhspan(req_lo, req_hi, color="#c0703b", alpha=0.18, zorder=0)
    ax.axhline(req_lo, color="#943126", lw=1.4, ls="--")
    ax.axhline(req_hi, color="#943126", lw=1.4, ls="--")
    ax.plot(tk, tk, color="#1f4e79", lw=2, label="tau_k available")
    ax.axvspan(IMF_AE_LOW, IMF_AE_HIGH, color="#2e7d32", alpha=0.15, zorder=0)
    ax.axvline(OPERATIVE, color="#943126", lw=2)
    ax.axvline(SOURCED_HIGH, color="#666", lw=1.2, ls=":")
    ax.annotate(f"OURS, on the AI surplus\n{OPERATIVE}\nCONDITION FAILS",
                xy=(OPERATIVE, 0.232), xytext=(0.083, 0.225), fontsize=8.5,
                color="#943126", va="top")
    ax.annotate(f"IMF measured, economy-wide\n{IMF_AE_LOW} to {IMF_AE_HIGH}\nCONDITION PASSES",
                xy=(0.21, 0.232), xytext=(0.152, 0.225), fontsize=8.5,
                color="#2e7d32", va="top")
    ax.annotate(f"required to close the condition\n{req_lo:.3f} to {req_hi:.3f}",
                xy=(0.012, req_hi), xytext=(0.012, 0.162), fontsize=8.5, color="#943126")
    ax.set_xlabel("effective tax rate on capital, tau_k")
    ax.set_ylabel("rate required to close the fiscal condition")
    ax.set_title("The fiscal condition is a function of tau_k, and the two defensible\n"
                 "measurements of tau_k fall on opposite sides of the threshold",
                 fontsize=10.5, loc="left")
    ax.set_xlim(0, 0.26)
    ax.set_ylim(0, 0.26)
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "fig_tau_k_condition.png", dpi=160)

    pd.set_option("display.width", 200)
    print("THE CONDITION AS A FUNCTION OF tau_k")
    print(f"  R = {R:.6f}")
    print(f"  required tau_k          {req_lo:.6f} to {req_hi:.6f}")
    print(f"  OURS, on the AI surplus {OPERATIVE}            -> FAILS")
    print(f"  our sourced maximum     {SOURCED_HIGH}        -> PASSES")
    print(f"  IMF measured, AE        {IMF_AE_LOW} to {IMF_AE_HIGH}     -> PASSES")
    print()
    print("SHARE OF THE AI SURPLUS THAT MUST BEAR THE HIGHER RATE")
    print(M.to_string(index=False))
    print()
    print("figure written to paper/figures/fig_tau_k_condition.png")


if __name__ == "__main__":
    main()
