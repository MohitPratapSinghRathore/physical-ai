"""Exposure frontier figure: wage bill at risk as a function of Physical AI capability."""
import pathlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).parents[1]
OUT, FIG = ROOT / "data" / "processed", ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
F = pd.read_csv(OUT / "paei_c_frontier.csv")

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))

ax[0].plot(F["c"], F["wagebill_at_risk_usd_bn"], lw=2.2, color="#1f4e79")
ax[0].set_xlabel("Physical AI capability, c")
ax[0].set_ylabel("Wage bill at risk (USD bn)")
ax[0].set_title("Embodiment-weighted wage bill at risk", fontsize=10)
for c, lab in [(0.2, "low"), (0.5, "medium"), (0.8, "high")]:
    y = float(F.loc[F["c"] == c, "wagebill_at_risk_usd_bn"].iloc[0])
    ax[0].axvline(c, color="grey", ls=":", lw=0.9)
    ax[0].annotate(f"{lab}\n{y:,.0f}", (c, y), textcoords="offset points",
                   xytext=(5, -18), fontsize=8, color="#444")
ax[0].grid(alpha=0.25)

ax[1].plot(F["c"], F["share_embodied_work_exposed_pct"], lw=2.2, color="#1f4e79",
           label="embodied work exposed (%)")
ax[1].plot(F["c"], F["share_employment_exposed_rawS_pct"], lw=1.6, color="#b03a2e",
           ls="--", label="raw-S threshold (degenerate)")
ax[1].set_xlabel("Physical AI capability, c")
ax[1].set_ylabel("Percent")
ax[1].set_title("Rank vs raw structure scale", fontsize=10)
ax[1].legend(fontsize=8)
ax[1].grid(alpha=0.25)

fig.suptitle("Physical AI exposure frontier, United States (O*NET 31.0 x ACS PUMS 2023)",
             fontsize=11)
fig.tight_layout()
fig.savefig(FIG / "exposure_frontier.png", dpi=180)
print("wrote", FIG / "exposure_frontier.png")
