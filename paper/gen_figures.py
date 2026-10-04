"""Generate paper/figures/*.pdf from data/release only.

Six figures, greyscale-safe: no colour carries information, series are separated
by line style, marker and hatch. Every value comes from a released artifact.

Run:  python paper/gen_figures.py
"""
import csv
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import PercentFormatter  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    # Type 42 (TrueType), not matplotlib's default Type 3. Type 3 subsets render
    # unreliably outside desktop PDF readers -- which is why figures came back
    # "not loading" in review -- and most journals reject Type 3 outright.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "serif",
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.edgecolor": "0.2",
    "axes.grid": True,
    "grid.color": "0.85",
    "grid.linewidth": 0.5,
    "legend.frameon": False,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
})

GREY = ["0.15", "0.45", "0.70", "0.88"]
HATCH = ["", "///", "...", "xxx"]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def finish(fig, name):
    path = OUT / name
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=140)
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def fig_series():
    do = {r["year"]: r for r in
          rows("data/release/labor_backing/debt_only_ratio_timeseries.csv")}
    dr = [r for r in rows("data/release/labor_backing/direct_ratio_timeseries.csv")
          if r["year"] in do]
    years = [int(r["year"]) for r in dr]
    union = [float(r["sovereign_share_union"]) for r in dr]
    held = [float(r["sovereign_share_of_labour_backed"]) for r in dr]
    obl = [float(r["sovereign_obligor_bn"]) / float(r["labour_backed_bn"]) for r in dr]
    debt_only = [float(do[r["year"]]["DEBT_ONLY_ratio_direct"]) for r in dr]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.3, 5.2), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(years, union, color="0.10", lw=1.8, label="Federal exposure, union of the three roles")
    ax1.plot(years, held, color="0.40", lw=1.2, ls="--", label="as creditor or guarantor")
    ax1.plot(years, obl, color="0.40", lw=1.2, ls=":", label="as debtor")
    ax1.set_ylabel("Share of directly wage-backed claims")
    ax1.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax1.set_ylim(0, 0.95)
    ax1.legend(loc="upper left", fontsize=8)

    ax2.plot(years, debt_only, color="0.10", lw=1.5,
             label="Debt-only labor backing ratio")
    ax2.set_ylabel("Share of debt")
    ax2.set_xlabel("Year")
    ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax2.set_ylim(0, 0.75)
    ax2.legend(loc="lower left", fontsize=8)
    for ax in (ax1, ax2):
        ax.set_xlim(min(years), max(years))
    finish(fig, "fig1_series.pdf")


HOLDER_NAME = {"federal_government": "Federal government", "banks": "Banks",
               "rest_of_world": "Rest of the world", "other_financial": "Other financial",
               "households": "Households", "state_local_government": "State and local",
               "insurers": "Insurers", "pensions": "Pension funds",
               "nonfinancial_business": "Nonfinancial business",
               "residual_unallocated": "Unallocated"}


def fig_holders():
    rs = rows("data/release/ai_bust/b4_payoff_by_holder.csv")
    rs = sorted(rs, key=lambda r: float(r["wage_leg_share"]))
    names = [HOLDER_NAME[r["holder"]] for r in rs]
    wage = [float(r["wage_leg_share"]) for r in rs]
    ai = [float(r["ai_leg_share"]) for r in rs]
    y = range(len(rs))
    fig, ax = plt.subplots(figsize=(6.3, 3.6))
    h = 0.38
    ax.barh([i + h / 2 for i in y], wage, height=h, color="0.25",
            edgecolor="black", lw=0.5, label="Wage side")
    ax.barh([i - h / 2 for i in y], ai, height=h, color="0.85",
            edgecolor="black", lw=0.5, hatch="///", label="AI side, lower bound")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names)
    ax.set_xlabel("Share of the claims on that side")
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(axis="y", visible=False)
    finish(fig, "fig2_holders.pdf")


def fig_tau_k():
    tk = load("data/release/tau_k/tau_k_assembled.json")
    req = tk["required_tau_k"]["by_labour_reading"]
    ours = {r["rent_reading"]: r for r in tk["assembled_CENTRAL_at_sourced_centrals"]}
    oursweep = {r["rent_reading"]: r for r in tk["assembled_SOURCED"]}
    crs = {r["rent_reading"]: r for r in tk["MARKED_SENSITIVITY_at_CRS_implied_theta"]}
    labels = ["First rent reading,\nall equity", "Second rent reading,\nall equity",
              "First rent reading,\ndomestic stock", "Second rent reading,\ndomestic stock"]
    B, K = "Barkai", "Karabarbounis_Neiman_case_R"
    central = [ours[B]["tau_k_central"], ours[K]["tau_k_central"],
               crs[B]["tau_k_central"], crs[K]["tau_k_central"]]
    lo = [oursweep[B]["tau_k_p05"], oursweep[K]["tau_k_p05"],
          crs[B]["tau_k_p05"], crs[K]["tau_k_p05"]]
    hi = [oursweep[B]["tau_k_p95"], oursweep[K]["tau_k_p95"],
          crs[B]["tau_k_p95"], crs[K]["tau_k_p95"]]
    err = [[c - l for c, l in zip(central, lo)], [h - c for c, h in zip(central, hi)]]

    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    x = range(4)
    ax.bar(x, central, width=0.55, color=["0.25", "0.55", "0.25", "0.55"],
           edgecolor="black", lw=0.6,
           hatch=["", "", "///", "///"])
    ax.errorbar(x, central, yerr=err, fmt="none", ecolor="black", capsize=3, lw=0.8)
    ax.axhspan(req["AMR_0.255"], req["bottom_up_0.318"], color="0.80", alpha=0.6, zorder=0)
    ax.axhline(req["AMR_0.255"], color="black", lw=0.9, ls="--")
    ax.axhline(req["bottom_up_0.318"], color="black", lw=0.9, ls="--")
    ax.text(3.45, (req["AMR_0.255"] + req["bottom_up_0.318"]) / 2,
            "required\nband", ha="left", va="center", fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Effective marginal rate on the income that shifts")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_ylim(0, 0.16)
    ax.set_xlim(-0.6, 3.4)
    ax.grid(axis="x", visible=False)
    finish(fig, "fig3_capital_tax.pdf")


def fig_federal_share():
    rs = rows("data/release/incidence/federal_share_by_dose.csv")
    x = [100 * float(r["dose_share_of_total_wage_bill"]) for r in rs]
    nl = [float(r["narrow_low"]) for r in rs]
    nh = [float(r["narrow_high"]) for r in rs]
    cl = [float(r["conservatorship_low"]) for r in rs]
    ch = [float(r["conservatorship_high"]) for r in rs]
    inside = [r["inside_observed_data_range"].lower().startswith("t") for r in rs]
    boundary = max(v for v, i in zip(x, inside) if i)

    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.fill_between(x, cl, ch, color="0.80", edgecolor="black", lw=0.5, hatch="///",
                    label="Conservatorship reading")
    ax.fill_between(x, nl, nh, color="0.45", edgecolor="black", lw=0.5,
                    label="Narrow reading")
    ax.axvline(boundary, color="black", lw=1.0, ls=":")
    ax.text(boundary + 1, 0.72, "outside the observed data $\\rightarrow$",
            fontsize=8, va="center")
    ax.set_xlabel("Share of the wage bill displaced (per cent)")
    ax.set_ylabel("Federal share of the first-round loss")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_ylim(0.7, 1.0)
    ax.set_xlim(min(x), max(x))
    ax.legend(loc="lower right", fontsize=8)
    finish(fig, "fig4_federal_share.pdf")


def fig_breach():
    rs = [r for r in rows("data/release/institutions/a2_distribution_by_class.csv")
          if r["cut"] == "model"]
    idx = {(r["dose"], r["business_model"]): r for r in rs}
    models = ["card-heavy", "credit union", "auto-heavy", "C and I heavy",
              "commercial real estate heavy", "diversified", "mortgage portfolio lender"]
    label = {"card-heavy": "Card-heavy", "credit union": "Credit unions",
             "auto-heavy": "Auto-heavy", "C and I heavy": "Commercial\nand industrial",
             "commercial real estate heavy": "Commercial\nreal estate",
             "diversified": "Diversified", "mortgage portfolio lender": "Mortgage\nportfolio"}
    doses = ["0.1", "0.25", "0.5"]
    dlab = ["10 per cent", "25 per cent", "50 per cent"]
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    w = 0.26
    for j, (d, lab) in enumerate(zip(doses, dlab)):
        vals = [float(idx[(d, m)]["pct_assets_breaching"]) for m in models]
        ax.bar([i + (j - 1) * w for i in range(len(models))], vals, width=w,
               color=GREY[j], edgecolor="black", lw=0.5, hatch=HATCH[j], label=lab)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels([label[m] for m in models], fontsize=7.5)
    ax.set_ylabel("Share of the class's assets in breach (per cent)")
    ax.legend(title="Wage bill displaced", fontsize=8, title_fontsize=8)
    ax.grid(axis="x", visible=False)
    finish(fig, "fig5_breach.pdf")


def fig_boundary():
    """The fiscal balance over the retained wage share and the pass-through coefficient."""
    import numpy as np
    c = load("data/release/revision_r2/c_jurisdiction_boundary.json")
    juris = c["C1_jurisdiction"]
    Rs = np.linspace(0.0, 1.0, 201)
    gs = np.linspace(0.25, 4.0, 201)
    RR, GG = np.meshgrid(Rs, gs)

    fig, ax = plt.subplots(figsize=(6.3, 4.0))
    styles = {("federal only", "easier"): ("0.10", "-"),
              ("federal only", "harder"): ("0.10", "--"),
              ("all government", "easier"): ("0.45", "-."),
              ("all government", "harder"): ("0.45", ":")}
    for name, d in juris.items():
        tk = d["assembled_tau_k"]
        for reading, key in (("easier", "labor_tax_easier"), ("harder", "labor_tax_harder")):
            bal = tk * GG - d[key] * (1 - RR)
            colour, ls = styles[(name, reading)]
            ax.contour(RR, GG, bal, levels=[0.0], colors=colour, linestyles=ls,
                       linewidths=1.4)
            ax.plot([], [], color=colour, ls=ls, lw=1.4,
                    label=f"{name}, {reading} labor tax reading")
    # the region the paper's conclusion occupies, on the headline federal-only easier reading
    fed = juris["federal only"]
    fails = fed["assembled_tau_k"] * GG - fed["labor_tax_easier"] * (1 - RR) < 0
    ax.contourf(RR, GG, fails.astype(float), levels=[0.5, 1.5], colors=["0.92"], zorder=0)
    ax.axhline(1.0, color="0.55", lw=0.9)
    ax.text(0.98, 1.08, "output preserved: $g \\leq 1$", fontsize=8, color="0.35",
            ha="right")
    Rv = float(c["retained_wage_share_R"])
    ax.axvline(Rv, color="0.55", lw=0.9)
    ax.text(Rv + 0.012, 0.35, "measured $R$", fontsize=8, color="0.35")
    ax.text(0.10, 0.55, "the condition fails", fontsize=9, color="0.25")
    ax.text(0.06, 3.55, "the condition closes", fontsize=9, color="0.25")
    ax.set_xlabel("Retained wage share $R$")
    ax.set_ylabel("Taxable capital income per displaced wage dollar, $g$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.25, 4.0)
    ax.legend(loc="upper right", fontsize=7.5)
    finish(fig, "fig6_boundary.pdf")


if __name__ == "__main__":
    fig_series()
    fig_holders()
    fig_tau_k()
    fig_federal_share()
    fig_breach()
    fig_boundary()
