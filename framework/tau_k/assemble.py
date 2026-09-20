"""ASSEMBLE TAU_K, DECOMPOSE ITS VARIANCE, AND DRAW THE MAP. Items 4 and 5.

THE ASSEMBLY, layer by layer, on a marginal dollar of US AI surplus.

  RENT component. The dollar is booked domestically with probability (1 - shifted), and
  abroad otherwise.
      entity rate, domestic = fed_cit + state_eff x (1 - fed_cit)
          state corporate tax is deductible against the federal base, so it adds
          s x (1 - 0.21), not s.
      entity rate, foreign  = the CURRENT preferential rate, 26 USC 250(a)(1)(B) at a 40
          percent deduction, which is 12.6 percent on net CFC tested income. This is a
          VERIFIED 2025 change and replaces the superseded 10.5 percent GILTI figure.
      The shareholder layer then applies to what is left:
          tau_rent = tau_entity + (1 - tau_entity) x tau_sh
      with tau_sh = theta_taxable x shareholder_rate x deferral_factor.

  NORMAL-RETURN component, under 100 percent expensing, 26 USC 168(k). This is taken
  directly from the Acemoglu, Manera and Restrepo algebra, not assumed:
      C-corporation, equity financed:  tau = tau_sh          (the entity tax washes out)
      C-corporation, debt financed:    tau = tau_b - tau_c   (NEGATIVE where bondholders
                                       face a lower rate than the corporation)
      so   tau_normal = (1 - debt) x tau_sh + debt x (tau_b - fed_cit).

  tau_k = sigma x tau_rent + (1 - sigma) x tau_normal, with sigma one of the TWO rent
  readings, never their average.

WHY THE MAP AND NOT A NUMBER. Seven of the twelve components could not be verified from a
primary source in this session, and they include every parameter of the shareholder layer.
Asserting a point would be asserting those seven. So the deliverable is the surface and the
threshold contour drawn across it, with the previously published points marked on it.

PLAUSIBILITY, checked in code and printed first:
  no component above its statutory or structural ceiling;
  every share in [0, 1];
  the assembled rate between the lowest and highest component-consistent values;
  the assembled rate never above the statutory ceiling on a fully domestic, fully
  distributed, fully taxable dollar.
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402
import pandas as pd                      # noqa: E402

import components as K                   # noqa: E402

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "paper" / "figures"

OPERATIVE = 0.0708        # the project published rate, entity-level only
IMF_LO, IMF_HI = 0.20, 0.22
PILLAR_TWO = 0.15

RNG = np.random.default_rng(20260920)
N = 200_000


def tau_sh(theta, rate, defer):
    return theta * rate * defer


def assemble(sigma, shifted, theta, sh_rate, defer, state, debt, bond):
    ts = tau_sh(theta, sh_rate, defer)
    ent_dom = K.V_FED_CIT + state * (1 - K.V_FED_CIT)
    ent = (1 - shifted) * ent_dom + shifted * K.V_CFC_RATE
    tau_rent = ent + (1 - ent) * ts
    tau_normal = (1 - debt) * ts + debt * (bond - K.V_FED_CIT)
    return sigma * tau_rent + (1 - sigma) * tau_normal, tau_rent, tau_normal


def draw(n, sourced=True):
    """Sample the parameter space. The two SOURCED parameters are drawn over their
    published ranges; passing sourced=False restores the superseded blind sweep so the
    effect of sourcing them is visible as a sensitivity."""
    r = {k: RNG.uniform(*K.U[k]["range"], n) for k in K.U}
    if sourced:
        r["theta_taxable"] = RNG.uniform(K.THETA_TAXABLE["low"],
                                         K.THETA_TAXABLE["high"], n)
        r["deferral_factor"] = RNG.uniform(K.DEFERRAL_FACTOR["low"],
                                           K.DEFERRAL_FACTOR["high"], n)
    else:
        r["theta_taxable"] = RNG.uniform(*K.SUPERSEDED_SWEEP["theta_taxable"], n)
        r["deferral_factor"] = RNG.uniform(*K.SUPERSEDED_SWEEP["deferral_factor"], n)
    return r


def ranges(sourced=True):
    d = {k: K.U[k]["range"] for k in K.U}
    if sourced:
        d["theta_taxable"] = [K.THETA_TAXABLE["low"], K.THETA_TAXABLE["high"]]
        d["deferral_factor"] = [K.DEFERRAL_FACTOR["low"], K.DEFERRAL_FACTOR["high"]]
    else:
        d.update(K.SUPERSEDED_SWEEP)
    return d


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    S = json.loads((PROC / "replication_r_sensitivity.json").read_text())
    req = S["ours_observed_rho_and_our_omega"]["required_tau_k"]
    req_lo, req_hi = min(req.values()), max(req.values())

    viol = []
    RNG_ALL = ranges(True)
    # ---- plausibility on the component ranges themselves
    for k, lohi in RNG_ALL.items():
        lo, hi = lohi
        if not (0.0 <= lo <= hi):
            viol.append(f"{k}: range not ordered or negative")
        if hi > K.CEILINGS[k] + 1e-12:
            viol.append(f"{k}: upper {hi} exceeds ceiling {K.CEILINGS[k]}")

    d = draw(N)
    out_rows = []
    per_reading = {}
    for name, sigma in K.RENT_READINGS.items():
        tk, tr, tn = assemble(sigma, d["shifted_share"], d["theta_taxable"],
                              d["shareholder_rate"], d["deferral_factor"],
                              d["state_cit_effective"], d["debt_share"],
                              d["bondholder_rate"])
        per_reading[name] = {"tau_k": tk, "draws": d}
        # ceiling: fully domestic, fully distributed, fully taxable, all-equity dollar
        ceil = sigma * (0.21 + 0.095 * 0.79
                        + (1 - (0.21 + 0.095 * 0.79)) * 0.238) + (1 - sigma) * 0.238
        if tk.max() > ceil + 1e-9:
            viol.append(f"{name}: assembled max {tk.max():.4f} above ceiling {ceil:.4f}")
        if tk.min() < -1.0:
            viol.append(f"{name}: assembled min implausibly negative")
        out_rows.append({
            "rent_reading": name, "sigma_rent": sigma,
            "tau_k_p05": round(float(np.percentile(tk, 5)), 4),
            "tau_k_median": round(float(np.median(tk)), 4),
            "tau_k_p95": round(float(np.percentile(tk, 95)), 4),
            "tau_k_min": round(float(tk.min()), 4),
            "tau_k_max": round(float(tk.max()), 4),
            "component_ceiling": round(float(ceil), 4),
            "pass_share_vs_required_low": round(float((tk >= req_lo).mean()), 4),
            "pass_share_vs_required_high": round(float((tk >= req_hi).mean()), 4),
        })
    T = pd.DataFrame(out_rows)
    T.to_csv(HERE / "tau_k_assembled.csv", index=False)

    # ---- VARIANCE DECOMPOSITION, first-order, by binned conditional expectation.
    # Confirms which parameters actually move tau_k, rather than assuming the three.
    vd_rows = []
    for name, sigma in K.RENT_READINGS.items():
        tk = per_reading[name]["tau_k"]
        tot = float(tk.var())
        for p in RNG_ALL:
            x = d[p]
            b = np.clip(((x - x.min()) / (x.max() - x.min() + 1e-12) * 20).astype(int), 0, 19)
            m = np.array([tk[b == j].mean() if (b == j).any() else np.nan
                          for j in range(20)])
            w = np.array([(b == j).mean() for j in range(20)])
            ok = ~np.isnan(m)
            cond = float(np.average((m[ok] - tk.mean()) ** 2, weights=w[ok]))
            vd_rows.append({"rent_reading": name, "parameter": p,
                            "first_order_index": round(cond / tot, 4) if tot > 0 else 0.0})
    V = pd.DataFrame(vd_rows)
    V = V.sort_values(["rent_reading", "first_order_index"], ascending=[True, False])
    V.to_csv(HERE / "tau_k_variance_decomposition.csv", index=False)

    top3 = {r: list(V[V.rent_reading == r].parameter.head(3)) for r in K.RENT_READINGS}

    # ---- THE MAP. Barkai reading, the two most influential parameters on the axes,
    # every other unverified parameter held at its range midpoint and named as such.
    name = "Barkai"
    sigma = K.RENT_READINGS[name]
    ax_names = top3[name][:2]
    mid = {k: float(np.mean(v)) for k, v in RNG_ALL.items()}
    mid["theta_taxable"] = K.THETA_TAXABLE["central"]
    mid["deferral_factor"] = K.DEFERRAL_FACTOR["central"]
    g = 120
    A = np.linspace(*RNG_ALL[ax_names[0]], g)
    B = np.linspace(*RNG_ALL[ax_names[1]], g)
    GA, GB = np.meshgrid(A, B)
    kw = dict(mid)
    kw[ax_names[0]] = GA
    kw[ax_names[1]] = GB
    Z, _, _ = assemble(sigma, kw["shifted_share"], kw["theta_taxable"],
                       kw["shareholder_rate"], kw["deferral_factor"],
                       kw["state_cit_effective"], kw["debt_share"], kw["bondholder_rate"])

    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    im = ax.contourf(GA, GB, Z, levels=18, cmap="viridis")
    fig.colorbar(im, ax=ax, label="assembled marginal tau_k on AI surplus")
    for lev, col, lab in [(req_lo, "white", f"required {req_lo:.3f}"),
                          (req_hi, "white", f"required {req_hi:.3f}"),
                          (PILLAR_TWO, "orange", "15 pct minimum")]:
        if Z.min() <= lev <= Z.max():
            cs = ax.contour(GA, GB, Z, levels=[lev], colors=col,
                            linewidths=2.0, linestyles="--")
            ax.clabel(cs, fmt={lev: lab}, fontsize=8)
    SRC = {"theta_taxable", "deferral_factor"}
    lab = lambda n: n + ("  (SOURCED range)" if n in SRC else "  (NOT VERIFIED, swept)")
    ax.set_xlabel(lab(ax_names[0]))
    ax.set_ylabel(lab(ax_names[1]))
    ax.set_title("tau_k on AI surplus, assembled from components, Barkai rent reading\n"
                 "other unverified parameters at range midpoints; dashed lines are the "
                 "fiscal condition threshold", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "tau_k_map.png", dpi=160)
    plt.close(fig)

    marked = {
        "published operative rate, entity level only": OPERATIVE,
        "assembled median, Barkai reading":
            float(np.median(per_reading["Barkai"]["tau_k"])),
        "assembled median, Karabarbounis-Neiman reading":
            float(np.median(per_reading["Karabarbounis_Neiman_case_R"]["tau_k"])),
        "IMF SDN/2024/002 economy-wide average, low": IMF_LO,
        "IMF SDN/2024/002 economy-wide average, high": IMF_HI,
        "OECD Pillar Two headline minimum, status NOT verified": PILLAR_TWO,
        "required, AMR labour reading": req_lo,
        "required, bottom-up labour reading": req_hi,
    }

    # ---- which single parameter moves the verdict across the line, and by how much
    movers = []
    tkB = per_reading["Barkai"]["tau_k"]
    for p in RNG_ALL:
        lo, hi = RNG_ALL[p]
        kwl, kwh = dict(mid), dict(mid)
        kwl[p], kwh[p] = lo, hi
        zl, _, _ = assemble(sigma, kwl["shifted_share"], kwl["theta_taxable"],
                            kwl["shareholder_rate"], kwl["deferral_factor"],
                            kwl["state_cit_effective"], kwl["debt_share"],
                            kwl["bondholder_rate"])
        zh, _, _ = assemble(sigma, kwh["shifted_share"], kwh["theta_taxable"],
                            kwh["shareholder_rate"], kwh["deferral_factor"],
                            kwh["state_cit_effective"], kwh["debt_share"],
                            kwh["bondholder_rate"])
        crosses = (min(zl, zh) < req_lo <= max(zl, zh)) or \
                  (min(zl, zh) < req_hi <= max(zl, zh))
        movers.append({"parameter": p, "tau_k_at_range_low": round(float(zl), 4),
                       "tau_k_at_range_high": round(float(zh), 4),
                       "swing": round(abs(float(zh - zl)), 4),
                       "crosses_a_threshold_alone": bool(crosses)})
    M = pd.DataFrame(movers).sort_values("swing", ascending=False)
    M.to_csv(HERE / "tau_k_movers.csv", index=False)

    # ---- the assembled CENTRAL rate, at the sourced central values
    central_rows = []
    for name, sigma in K.RENT_READINGS.items():
        kw = dict(mid)
        c, cr, cn = assemble(sigma, kw["shifted_share"], kw["theta_taxable"],
                             kw["shareholder_rate"], kw["deferral_factor"],
                             kw["state_cit_effective"], kw["debt_share"],
                             kw["bondholder_rate"])
        central_rows.append({"rent_reading": name, "tau_k_central": round(float(c), 4),
                             "tau_rent": round(float(cr), 4),
                             "tau_normal": round(float(cn), 4),
                             "passes_vs_required_low": bool(c >= req_lo),
                             "passes_vs_required_high": bool(c >= req_hi)})

    # ---- PLAUSIBILITY on the shareholder layer against the published figure
    sh = mid["theta_taxable"] * 0.238 * mid["deferral_factor"]
    if not (0.02 <= sh <= 0.09):
        viol.append(f"shareholder layer {sh:.4f} outside the CRS R47113 Table 5 published "
                    f"band of 0.03 to 0.085")

    # ---- SENSITIVITY: what the superseded blind sweep gave
    d_old = draw(N, sourced=False)
    old_rows = []
    for name, sigma in K.RENT_READINGS.items():
        tk_old, _, _ = assemble(sigma, d_old["shifted_share"], d_old["theta_taxable"],
                                d_old["shareholder_rate"], d_old["deferral_factor"],
                                d_old["state_cit_effective"], d_old["debt_share"],
                                d_old["bondholder_rate"])
        old_rows.append({"rent_reading": name,
                         "tau_k_p05": round(float(np.percentile(tk_old, 5)), 4),
                         "tau_k_median": round(float(np.median(tk_old)), 4),
                         "tau_k_p95": round(float(np.percentile(tk_old, 95)), 4),
                         "pass_share_vs_required_low": round(float((tk_old >= req_lo).mean()), 4),
                         "pass_share_vs_required_high": round(float((tk_old >= req_hi).mean()), 4)})

    summary = {
        "status": "ASSEMBLED FROM COMPONENTS. Five components VERIFIED, seven NOT VERIFIED "
                  "and swept. Reported as a MAP, not a point.",
        "plausibility_violations": viol,
        "required_tau_k": {"low": req_lo, "high": req_hi, "by_labour_reading": req},
        "assembled_SOURCED": out_rows,
        "assembled_CENTRAL_at_sourced_centrals": central_rows,
        "shareholder_layer_at_centrals": round(float(sh), 4),
        "SUPERSEDED_blind_sweep_for_comparison": old_rows,
        "sourced_parameters": {"theta_taxable": K.THETA_TAXABLE,
                               "deferral_factor": K.DEFERRAL_FACTOR},
        "variance_decomposition_top3": top3,
        "map_axes": ax_names,
        "map_other_parameters": "held at range midpoints, which are NOT estimates",
        "marked_points": {k: round(v, 4) for k, v in marked.items()},
        "single_parameter_movers": movers,
        "headline": "",
    }
    b = T[T.rent_reading == "Barkai"].iloc[0]
    cb = [r for r in central_rows if r["rent_reading"] == "Barkai"][0]
    summary["headline"] = (
        f"Under the Barkai rent reading the assembled marginal rate spans "
        f"{b.tau_k_p05:.3f} to {b.tau_k_p95:.3f} across the unverified components, against a "
        f"required {req_lo:.3f} to {req_hi:.3f}. The condition passes in "
        f"{100*b.pass_share_vs_required_low:.0f} percent of the swept space against the "
        f"easier threshold and {100*b.pass_share_vs_required_high:.0f} percent against the "
        f"harder one. The published 0.0708 sits below that span because it omits the "
        f"shareholder layer entirely.")
    (HERE / "tau_k_assembled.json").write_text(json.dumps(summary, indent=2))

    pd.set_option("display.width", 200)
    print("PLAUSIBILITY:", "NO VIOLATIONS" if not viol else viol)
    print("\nASSEMBLED tau_k, two rent readings, never averaged")
    print(T.to_string(index=False))
    print(f"\nrequired: {req_lo:.4f} to {req_hi:.4f}")
    print("\nVARIANCE DECOMPOSITION, first order")
    print(V.to_string(index=False))
    print("\nSINGLE-PARAMETER MOVERS, Barkai reading, others at midpoint")
    print(M.to_string(index=False))
    print("\nMARKED POINTS")
    for k, v in marked.items():
        print(f"  {v:7.4f}   {k}")
    print("\n" + summary["headline"])


if __name__ == "__main__":
    main()
