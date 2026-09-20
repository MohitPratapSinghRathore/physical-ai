# Places the brief was insufficient to reproduce a number

Ordered by how much they block. "Blocking" means no value can be produced without inventing
the missing definition; "underdetermined" means I produced a value but it rests on a choice
the brief left open.

## Blocking

1. **Embodiment P (sections 6, and every group split that uses it).** The brief defers the
   whole construction to `notes/paei_c_method.md`, which was not supplied. I substituted my
   own O*NET 31.0 index (mean Importance over elements 1.A.2 psychomotor and 1.A.3 physical
   abilities). Every `cap_contrast.*.embodied` and every `pay_control.*` value therefore rests
   on my index, not theirs, and cannot be treated as a replication.

2. **Section 5, household first-round losses.** The brief gives the loss formula, the default
   uplifts and the LGD ranges, but never says how a dose expressed as a share of the total
   wage bill is converted into a set of displaced households in SIPP. Without that mapping the
   exposure-at-default sum is undefined. Not computed.

3. **Section 7, incidence.** The three cases (incumbents, entrants, sourced mix) are named but
   none is defined, and the "sourced mix" has no source attached. Not computed.

4. **Section 10, sovereign share.** Needs section 5 plus GSE capital, GSE pre-provision pre-tax
   earnings, FHA book size, and CRT and PMI attachment points. None are given and DFAST 2026
   Tables 4 and 9 are referenced without a retrievable locator. Not computed. The one
   component I could verify independently is the 97.3 percent federal student share, which I
   reproduce at 97.28 percent.

5. **Section 11, second round.** The five input ranges are given, but the model that maps them
   to a bank loss is not. There is no stated demand-to-revenue mapping, no house-price-to-loss
   mapping, and the three "loss mapping beyond the Fed's severity" options (linear, capped,
   convex) are named without functional forms. Not computed.

## Underdetermined (value produced, choice documented)

6. **Section 1, vintage window.** "One observation per DWS vintage" sets no start date. I used
   all 15 vintages I could source to a primary BLS release (1998-2026). The brief's own remark
   that the circular unemployment-rate fit gives the higher R-squared is true only on a
   post-2008 window, so I also report the 2008-2026 fit.

7. **Section 1, "speed limit".** Used in the error table ("about 2.5 times too large") but
   never defined. The slope ratio between the two specifications is 1.11, not 2.5, so I cannot
   confirm or refute the claim.

8. **Section 2, omega.** Described only as "a blended counterfactual from the DWS earnings
   question". The DWS reports a median earnings ratio and a share earning at least as much;
   the blend weights are not given. I used 0.90 with a 0.85-0.97 range.

9. **Section 2 and 3, the three readings of tau_l.** The brief says there are three and states
   none. I chose 0.153, 0.25 and 0.35. This single gap drives my contradiction of the brief's
   headline result in section 2.

10. **Section 2, tau_k components.** Barkai, Torslov-Wier-Zucman, Auerbach and
    Acemoglu-Manera-Restrepo are named as sources, but no extracted value is given for
    sigma_rent, the domestic share, or tau_normal. Reproducing sigma_rent from Barkai is a
    separate replication in itself.

11. **Section 3, trust fund denominators.** "The fund's own payroll income" is the correct
    denominator but its value is never stated for either OASDI or HI.

12. **Section 3, who is displaced.** The dose is a share of the total wage bill, but the
    under-cap share needed for the OASDI loss depends on which workers are displaced. I used
    the cognitive AIOE group's share.

13. **Section 4, "working core".** Never defined. I used households with positive summed
    member earnings in month 12. My resulting inflation band (6.4 to 19.3 percent) does not
    match the brief's stated 14 to 26 percent, and no age restriction I tried matched it
    across all four books, so their subsample is narrower and differently shaped than mine.

14. **Section 4, MVLOAS vintage.** The brief instructs using FRED MVLOAS for the auto
    aggregate, but that series was discontinued after 2024Q4 while every other input is 2026.
    I used the last available observation and flagged the mismatch.

15. **Section 6, group definitions.** "Exposure group" is never defined. Section 3 warns that
    a top quintile is a moving denominator, but that warning is about the dose axis, not about
    group construction. I used the top employment-weighted quintile of each index.

16. **Section 6, which Eloundou measure.** The replication package supplies alpha, beta and
    gamma under both human and model labels. The brief says only "GPT exposure". I used
    human-labelled beta.

17. **Section 6, wage vintage against the cap.** The brief applies the 2026 cap of $184,500 to
    ACS 2023 wages without saying whether to inflate them. I did not inflate, per the literal
    instruction, which understates the share above the cap.

18. **ACS SOC aggregation.** ACS SOCP codes are broad or wildcarded (for example `5191XX`)
    while both exposure indices are detailed six-digit SOC. The brief never says how to
    aggregate. I used OES May 2021 employment-weighted means within each matched prefix.

19. **Section 12, case B stability.** The formulas are given but the ratio B/A has the case A
    fiscal loss in its denominator, which approaches zero at my lowest tau_l. My reported
    range (-3.18 to 3.97) is therefore not a usable number, and the case B break-even tau_k
    exceeds 1 at the top of the mpc grid, which is not plausible as a tax rate. Both are
    symptoms of the missing tau_l, not of the formulas.

20. **Section 13, the regimes.** "Each regime" implies several, but only one (r = 9 percent
    against g = 3 percent, labelled emerging market) is ever specified. I computed that one.

21. **Section 13, the starting ratio.** The brief states 121.4 percent. FRED GFDEBTN over GDP
    gives 122.59 percent at 2026Q1. Their figure is reproduced exactly at their start, so the
    gap is a vintage or debt-concept choice (total public debt against debt held by the
    public) that the brief does not pin down.
