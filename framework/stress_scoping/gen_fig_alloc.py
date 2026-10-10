"""Figure for the allocation paper: how the two rules diverge as severity rises.

Greyscale-safe, Type 42 fonts, same house style as the other two papers.

Run:  python framework/stress_scoping/gen_fig_alloc.py
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "paper" / "figures"

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "serif", "font.size": 9,
    "axes.linewidth": 0.7, "axes.edgecolor": "0.2",
    "axes.grid": True, "grid.color": "0.85", "grid.linewidth": 0.5,
    "legend.frameon": False, "figure.dpi": 200, "savefig.bbox": "tight",
})


def main():
    B = json.loads((HERE / "robustness.json").read_text())
    S = B["by_severity"]
    x = [r["severity_multiplier"] for r in S]
    pro = [r["breach_prorata"] for r in S]
    spec = [r["breach_specific"] for r in S]
    jac = [r["jaccard"] for r in S]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.3, 5.0), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(x, pro, color="0.10", lw=1.8, marker="o", ms=4,
             label="pro rata allocation")
    ax1.plot(x, spec, color="0.45", lw=1.5, ls="--", marker="s", ms=4,
             label="institution-specific allocation")
    ax1.set_yscale("log")
    ax1.set_ylabel("Banks below the leverage minimum")
    ax1.legend(loc="upper left", fontsize=8)
    ax1.axvline(1.0, color="0.7", lw=0.8, ls=":")
    ax1.text(1.03, ax1.get_ylim()[0] * 1.6, "base case", fontsize=7, color="0.4")

    ax2.plot(x, jac, color="0.10", lw=1.5, marker="o", ms=4)
    ax2.set_ylabel("Overlap (Jaccard)")
    ax2.set_xlabel("Severity multiplier on every category loss")
    ax2.set_ylim(0, 1)
    ax2.axvline(1.0, color="0.7", lw=0.8, ls=":")

    fig.tight_layout()
    fig.savefig(OUT / "fig_alloc_severity.pdf")
    fig.savefig(OUT / "fig_alloc_severity.png")
    print("wrote fig_alloc_severity.pdf")
    d = (OUT / "fig_alloc_severity.pdf").read_bytes()
    print("Type3 present:", b"Type3" in d, " FontFile:", b"FontFile" in d)


if __name__ == "__main__":
    main()
