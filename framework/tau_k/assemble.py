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


# THETA AS CRS R47113 ITSELF IMPLIES IT. Table 5's taxable-form row is a "55 percent
# reduction", i.e. a multiplier of 0.45. CRS's own text gives the arithmetic: "the 25% share
# of corporate stock held by taxable individuals compared with the 30% share from exempt
# shareholders", so the implied share is 25 / (25 + 30) = 0.454545. That denominator is
# DOMESTICALLY HELD stock: the roughly 45 percent held by foreigners is dropped from the base
# rather than counted as untaxed. Our theta of 0.24 to 0.28 is the same numerator over ALL
# equity outstanding, foreign included. Same source family (CRS cites Rosenthal and Burke
# 2020), different base. Run here as a MARKED SENSITIVITY, not as an alternative estimate:
# our object is a rate on a dollar of US AI surplus whoever holds it, so the foreign-inclusive
# base is the right one for the assembly.
THETA_CRS_IMPLIED = 25.0 / 55.0        # 0.454545


def corner_extremes(sigma, box):
    """The assembly is MULTILINEAR in all seven parameters, so its supremum and infimum over
    a box are attained at corners. Evaluate all 2^7 and return them. This replaces the
    Monte Carlo sample max, which is an extreme order statistic with no stable value across
    seeds and is not reproducible by construction."""
    names = ["shifted_share", "theta_taxable", "shareholder_rate", "deferral_factor",
             "state_cit_effective", "debt_share", "bondholder_rate"]
    grids = np.meshgrid(*[np.array(box[n], dtype=float) for n in names], indexing="ij")
    g = dict(zip(names, grids))
    z, _, _ = assemble(sigma, g["shifted_share"], g["theta_taxable"], g["shareholder_rate"],
                       g["deferral_factor"], g["state_cit_effective"], g["debt_share"],
                       g["bondholder_rate"])
    return float(z.min()), float(z.max())


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
        r["bondholder_rate"] = RNG.uniform(K.BONDHOLDER_RATE["low"],
                                           K.BONDHOLDER_RATE["high"], n)
        r["debt_share"] = RNG.uniform(K.DEBT_SHARE["low"], K.DEBT_SHARE["high"], n)
    else:
        r["theta_taxable"] = RNG.uniform(*K.SUPERSEDED_SWEEP["theta_taxable"], n)
        r["deferral_factor"] = RNG.uniform(*K.SUPERSEDED_SWEEP["deferral_factor"], n)
        r["bondholder_rate"] = RNG.uniform(*K.SUPERSEDED_SWEEP["bondholder_rate"], n)
        r["debt_share"] = RNG.uniform(*K.SUPERSEDED_SWEEP["debt_share"], n)
    return r


def ranges(sourced=True):
    d = {k: K.U[k]["range"] for k in K.U}
    if sourced:
        d["theta_taxable"] = [K.THETA_TAXABLE["low"], K.THETA_TAXABLE["high"]]
        d["deferral_factor"] = [K.DEFERRAL_FACTOR["low"], K.DEFERRAL_FACTOR["high"]]
        d["bondholder_rate"] = [K.BONDHOLDER_RATE["low"], K.BONDHOLDER_RATE["high"]]
        d["debt_share"] = [K.DEBT_SHARE["low"], K.DEBT_SHARE["high"]]
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
        # The ANALYTIC extremes over the box. Reported in place of the sample extremes:
        # the assembly is multilinear, so its true supremum and infimum sit at corners, and
        # the max of 200,000 draws from a 7-dimensional box is an extreme order statistic
        # with no stable value across seeds.
        cmin, cmax = corner_extremes(sigma, RNG_ALL)
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
            "tau_k_min_sample": round(float(tk.min()), 4),
            "tau_k_max_sample": round(float(tk.max()), 4),
            "tau_k_min_ANALYTIC": round(cmin, 4),
            "tau_k_max_ANALYTIC": round(cmax, 4),
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
    # THE SHIFTED SHARE'S CENTRAL IS THE SOURCED VALUE, NOT THE RANGE MIDPOINT. B3 of the
    # brief says "0.30 to 0.60, centred on 0.48" and cites Torslov, Wier and Zucman for the
    # 0.48; the sweep is uncertainty AROUND that one verified value, not a flat interval
    # whose midpoint means anything. Through A117 this line took the range midpoint 0.45,
    # so text and code disagreed. The TEXT is right and the code is corrected here. Effect:
    # the Barkai central falls from 0.0864 to 0.0851. Nothing else moves -- under
    # Karabarbounis and Neiman sigma is zero, which kills the shifted term entirely.
    mid["shifted_share"] = K.V_SHIFTED
    mid["theta_taxable"] = K.THETA_TAXABLE["central"]
    mid["deferral_factor"] = K.DEFERRAL_FACTOR["central"]
    mid["bondholder_rate"] = K.BONDHOLDER_RATE["central"]
    mid["debt_share"] = K.DEBT_SHARE["central"]
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
    SRC = {"theta_taxable", "deferral_factor", "bondholder_rate", "debt_share"}
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

    # ---- PLAUSIBILITY on the shareholder layer against the published figures. CORRECTED
    # in A118. CRS R47113 Table 5's 0.045 to 0.085 row has ALREADY had CRS's own taxable-share
    # adjustment applied, at an implied share of 25/(25+30) = 0.4545 over DOMESTICALLY HELD
    # stock. Our theta is the same numerator over ALL equity outstanding, foreign included.
    # Comparing our 0.0386 to the unadjusted band was comparing two different bases, and our
    # own construction failed our own check by 0.0064 at the bottom. The band is rescaled by
    # theta / 0.4545, and the "around 3 percent" text figure is kept as a direct test against
    # tau_sh, which needs no rescaling.
    sh = mid["theta_taxable"] * 0.238 * mid["deferral_factor"]
    crs_lo = 0.045 * mid["theta_taxable"] / THETA_CRS_IMPLIED
    crs_hi = 0.085 * mid["theta_taxable"] / THETA_CRS_IMPLIED
    if not (crs_lo <= sh <= crs_hi):
        viol.append(f"shareholder layer {sh:.4f} outside CRS R47113 Table 5's 0.045 to 0.085 "
                    f"rescaled to our theta, {crs_lo:.4f} to {crs_hi:.4f}")
    tau_sh_crs_text = 0.0315     # CRS R47113 p. 2, "around 3 percent"
    if abs(sh - tau_sh_crs_text) > 0.010:
        viol.append(f"shareholder layer {sh:.4f} more than 0.010 from CRS R47113's text "
                    f"figure of around 3 percent ({tau_sh_crs_text})")

    # ---- SIGN TEST: AMR's debt-financed normal return must be NEGATIVE across the
    # sourced bondholder range, and CBO 2014 Table 2 measures the corresponding ETR at -0.06.
    dn_lo = K.BONDHOLDER_RATE["low"] - K.V_FED_CIT
    dn_hi = K.BONDHOLDER_RATE["high"] - K.V_FED_CIT
    if dn_hi >= 0:
        viol.append(f"AMR debt-financed normal return {dn_hi:.4f} is not negative, against "
                    f"CBO 2014 Table 2 measuring the C-corp debt-financed ETR at -0.06")

    # ---- MARKED SENSITIVITY, NEW IN A118: the assembly at the taxable share CRS R47113
    # ITSELF implies, 25/(25+30) = 0.4545. Not an alternative estimate of our theta -- CRS's
    # denominator drops foreign holders, ours keeps them, and ours is the right base for a
    # rate on a dollar of US AI surplus whoever holds it. Run so the reader can see exactly
    # what the base difference is worth, because it is the largest single adjustment left in
    # this module and it moves the assembled rate TOWARD the threshold.
    d_crs = dict(d)
    d_crs["theta_taxable"] = np.full(N, THETA_CRS_IMPLIED)
    box_crs = dict(RNG_ALL)
    box_crs["theta_taxable"] = [THETA_CRS_IMPLIED, THETA_CRS_IMPLIED]
    crs_rows = []
    for name, sigma in K.RENT_READINGS.items():
        tk_c, _, _ = assemble(sigma, d_crs["shifted_share"], d_crs["theta_taxable"],
                              d_crs["shareholder_rate"], d_crs["deferral_factor"],
                              d_crs["state_cit_effective"], d_crs["debt_share"],
                              d_crs["bondholder_rate"])
        kwc = dict(mid)
        kwc["theta_taxable"] = THETA_CRS_IMPLIED
        cc, _, _ = assemble(sigma, kwc["shifted_share"], kwc["theta_taxable"],
                            kwc["shareholder_rate"], kwc["deferral_factor"],
                            kwc["state_cit_effective"], kwc["debt_share"],
                            kwc["bondholder_rate"])
        cmin_c, cmax_c = corner_extremes(sigma, box_crs)
        crs_rows.append({
            "rent_reading": name, "theta_taxable": round(THETA_CRS_IMPLIED, 4),
            "tau_k_central": round(float(cc), 4),
            "tau_k_p05": round(float(np.percentile(tk_c, 5)), 4),
            "tau_k_median": round(float(np.median(tk_c)), 4),
            "tau_k_p95": round(float(np.percentile(tk_c, 95)), 4),
            "tau_k_min_ANALYTIC": round(cmin_c, 4),
            "tau_k_max_ANALYTIC": round(cmax_c, 4),
            "pass_share_vs_required_low": round(float((tk_c >= req_lo).mean()), 4),
            "pass_share_vs_required_high": round(float((tk_c >= req_hi).mean()), 4),
            "central_passes_vs_required_low": bool(cc >= req_lo),
            "central_passes_vs_required_high": bool(cc >= req_hi),
        })
    CRS = pd.DataFrame(crs_rows)
    CRS.to_csv(HERE / "tau_k_crs_theta_sensitivity.csv", index=False)

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
        "shareholder_layer_checks": {
            "CRS_R47113_Table_5_band_as_published": [0.045, 0.085],
            "CRS_implied_taxable_share": round(THETA_CRS_IMPLIED, 4),
            "CRS_implied_share_basis": "25 / (25 + 30), CRS's own arithmetic, over "
                                       "DOMESTICALLY HELD stock; the roughly 45 percent "
                                       "foreign-held slice is dropped from the base, not "
                                       "carried as untaxed. Our theta is the same numerator "
                                       "over ALL equity outstanding. Same source family "
                                       "(CRS cites Rosenthal and Burke 2020), different base.",
            "band_rescaled_to_our_theta": [round(crs_lo, 4), round(crs_hi, 4)],
            "CRS_text_figure_around_3_percent": tau_sh_crs_text,
            "verdict": "PASSES the rescaled band and the text figure. It does NOT reproduce "
                       "the published 0.045 to 0.085, and must not be described as doing so.",
        },
        "MARKED_SENSITIVITY_at_CRS_implied_theta": crs_rows,
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
    print("\nMARKED SENSITIVITY: theta at the CRS R47113 implied 0.4545 "
          "(foreign-EXCLUDED base)")
    print(CRS.to_string(index=False))

    print("\nMARKED POINTS")
    for k, v in marked.items():
        print(f"  {v:7.4f}   {k}")
    print("\n" + summary["headline"])


if __name__ == "__main__":
    main()
