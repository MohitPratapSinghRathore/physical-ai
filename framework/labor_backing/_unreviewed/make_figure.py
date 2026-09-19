"""B4/B7 figure: the direct labour backing ratio, 1952 to the latest year.

PROVISIONAL. Writes only inside framework/labor_backing/.
"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = pathlib.Path(__file__).parent


def main():
    r = list(csv.DictReader(open(OUT / "ratio_time_series.csv")))
    y = [int(x["year"]) for x in r]
    f = lambda k: [float(x[k]) for x in r]

    fig, ax = plt.subplots(2, 1, figsize=(8.5, 8.0), sharex=True,
                           gridspec_kw={"height_ratios": [2, 1]})

    ax[0].fill_between(y, f("ratio_lower"), f("ratio_upper"), alpha=0.18, color="#3b6ea5",
                       label="lower to upper variant")
    ax[0].plot(y, f("ratio_central"), lw=2.2, color="#1f3f63", label="direct ratio, central")
    ax[0].plot(y, f("ratio_central_tv"), lw=1.2, ls=":", color="#1f3f63",
               label="central, time-varying wage share of AGI proxy")
    ax[0].plot(y, f("ratio_frozen_shares"), lw=1.1, ls="--", color="#b1660b",
               label="claim composition only (receipt shares frozen at latest)")
    ax[0].plot(y, f("ratio_frozen_weights"), lw=1.1, ls="-.", color="#7a2f2f",
               label="receipt shares only (claim composition frozen at latest)")
    ax[0].set_ylabel("share of the nonfinancial debt stock\ndirectly backed by labour income")
    ax[0].set_title("The direct labour backing ratio, United States, 1952 to 2025\n"
                    "PROVISIONAL. First-round servicing only. Business claims are zero by rule.",
                    fontsize=11, loc="left")
    ax[0].legend(fontsize=8, loc="lower right", framealpha=0.9)
    ax[0].grid(alpha=0.25)
    ax[0].set_ylim(0.2, 0.7)

    ax[1].plot(y, f("share_federal"), lw=1.8, color="#1f3f63", label="federal debt")
    ax[1].plot(y, f("share_home_mortgage"), lw=1.4, color="#b1660b", label="home mortgages")
    ax[1].plot(y, f("share_business_other"), lw=1.4, color="#4b7a4b", label="other business debt")
    ax[1].plot(y, f("fed_labour_linked_share"), lw=1.6, ls="--", color="#7a2f2f",
               label="labour-linked share of federal receipts")
    ax[1].set_ylabel("share")
    ax[1].set_xlabel("year")
    ax[1].legend(fontsize=8, ncol=2, framealpha=0.9)
    ax[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(OUT / "fig_labour_backing_ratio.png", dpi=170)
    print("wrote", OUT / "fig_labour_backing_ratio.png")


if __name__ == "__main__":
    main()
