# Session 3: the holder leg by programme, and the section-versus-paper decision

> # ⚠ RESULT (b) WITHDRAWN, 2026-09-25
>
> **`framework/paper3_scoping/K4_RESULT.md` shows the "rotation" below is an artefact of the
> labour-backed denominator.** On a household-credit denominator the GSE and agency complex
> **rises +0.1255** over 2007–2025 rather than falling 0.0446, and the holder leg rises
> **+0.2028** rather than being flat. The holder leg grew **2.71× in levels**. Nothing
> rotated; Treasury debt grew 5.60× and inflated the denominator underneath it.
>
> **Withdrawn:** result (b), the rotation, and the session 3 recommendation that rested on it.
> **Survives:** result (a), the guarantee phase being the GSE complex; and the two-phase
> structure **when stated as growth relative to the denominator** — phase 1 holder ×84.6
> against a stock growing ×20.0, phase 2 obligor ×5.92 against a stock growing ×2.56.
> The decision in §4 stands but for weaker reasons: Section 4.5 now carries the U-shape and
> the two-phase structure, and not the rotation.

**2026-09-22. `PROSPECTUS.md` §7 session 3. No new kills; the stop rule stands.**

---

## 1. An artefact caught before it was reported

The first run split sectors 40 (GSEs) and 41 (agency and GSE pools) and produced what looked
like a dramatic programme shift:

| Year | Pools (41) | GSE retained (40) | **Combined** |
|---|---|---|---|
| 2009 | 0.2425 | 0.0303 | **0.2727** |
| 2010 | **0.0498** | **0.2196** | **0.2694** |

**That is the FAS 166/167 consolidation**, which moved GSE securitisation trusts on balance
sheet in 2010. The separate series jump violently; the combined series is smooth. Reporting
sector 40 and 41 separately would have reported an accounting reclassification as an economic
event.

**Sectors 40 and 41 are therefore combined throughout as one programme, `gse_agency_guarantee`.**

**Limitation, stated not worked around:** Ginnie Mae sits inside sector 41 and **Z.1 does not
separate it**. The Ginnie share of the guarantee complex cannot be recovered from this source
and is not claimed. Separating it would need Ginnie Mae or FHFA programme data, which is a
different source and outside this build.

The programme split reconstructs the federal holder share to **1.11 × 10⁻¹⁶**.

## 2. The holder leg by programme, 1947–2025

**Central rule:**

| Year | Holder total | GSE/agency guarantee | Federal direct | Federal Reserve | Fed retirement |
|---|---|---|---|---|---|
| 1947 | 0.0948 | 0.0013 | 0.0041 | **0.0894** | 0.0000 |
| 1965 | 0.0746 | 0.0077 | 0.0096 | 0.0574 | 0.0000 |
| 1980 | 0.1546 | 0.0856 | 0.0133 | 0.0556 | 0.0000 |
| 1990 | 0.2482 | 0.1954 | 0.0097 | 0.0406 | 0.0026 |
| 2000 | 0.3154 | **0.2561** | 0.0027 | 0.0548 | 0.0017 |
| 2007 | 0.3043 | 0.2548 | 0.0078 | 0.0406 | 0.0010 |
| 2013 | 0.3751 | 0.2566 | 0.0343 | 0.0832 | 0.0009 |
| 2021 | **0.4072** | 0.2311 | 0.0410 | **0.1346** | 0.0005 |
| 2025 | 0.3215 | 0.2102 | 0.0361 | 0.0747 | 0.0005 |

**Second-round rule:** the same shape at roughly half the level — guarantee complex 0.0043
(1965) → 0.1418 (2000) → 0.1197 (2025); holder total 0.0417 → 0.1759 → 0.1872.

## 3. Every programme's contribution to each phase, reported twice

| Phase | Rule | Holder total | GSE/agency | Federal direct | Federal Reserve | Fed retirement |
|---|---|---|---|---|---|---|
| **Guarantee 1965–2000** | central | **+0.2408** | **+0.2484** | −0.0068 | −0.0025 | +0.0017 |
| | second | **+0.1342** | **+0.1375** | −0.0029 | −0.0023 | +0.0019 |
| **Borrowing 2007–2025** | central | +0.0172 | **−0.0446** | **+0.0282** | **+0.0341** | −0.0006 |
| | second | −0.0106 | **−0.0447** | +0.0166 | +0.0170 | +0.0005 |
| **Post-2013** | central | −0.0536 | −0.0464 | +0.0018 | −0.0085 | −0.0005 |
| | second | −0.0579 | −0.0458 | −0.0016 | −0.0109 | +0.0003 |

**Three things, all robust to the backing rule:**

**(a) The guarantee phase is the GSE and agency complex, and nothing else.** It contributes
+0.2484 of a +0.2408 holder-leg move centrally, and +0.1375 of +0.1342 under the second-round
rule. Every other programme moves by less than 0.007 in either direction. This is as close to
a single-cause decomposition as a historical series produces.

**(b) After 2007 the state's guarantee position did not grow. It rotated.** The holder leg
moves +0.0172 centrally over eighteen years — essentially flat — but underneath it the GSE and
agency complex **falls 0.0446** while direct federal lending rises 0.0282 and the Federal
Reserve rises 0.0341. Under the second-round rule the holder leg is outright negative (−0.0106)
with the same rotation. **The composition changed; the total did not.**

**(c) Post-2013 the holder leg falls under both rules**, −0.0536 and −0.0579, almost entirely
the guarantee complex. The post-2013 rise in the *union* reported in session 2 (+0.0900
central, +0.0002 second-round) is therefore **entirely an obligor-leg phenomenon**. Under the
second-round rule, where the obligor contribution is halved, the union goes flat — which is
the session 2 result, now explained.

### A session 1 attribution corrected

Session 1 attributed the post-2008 divergence between the holder leg and the public GSE share
of mortgages to "Ginnie, direct student lending and Federal Reserve holdings". **The first of
those is wrong on this evidence.** The combined GSE and agency guarantee complex — which
contains Ginnie — is *falling* after 2007, not rising. The divergence is direct federal lending
and the Federal Reserve, and the public GSE-share series falls faster than the holder leg
because the holder leg's denominator is the wage-backed claim stock rather than mortgages.
Whether Ginnie specifically grew inside a shrinking complex cannot be answered from Z.1.

---

## 4. The decision: Section 4.5, not a standalone paper

The test set was: does the programme decomposition add a story the historians do not have on a
common denominator, or does it relabel known facts?

**It adds a story. The story is thinner than a paper needs.**

**What is genuinely new.** The rotation in (b) is not, as far as searching has found, stated
anywhere. It requires the common denominator to see at all: on a mortgage denominator the GSE
complex and the Fed are not commensurable, and direct student lending is not in the frame. And
it corrects a widely held view — that the state took on more credit risk after 2008. On this
measure **it did not; it borrowed more, and its guarantee position rotated and shrank.**

**Why that is not enough for a standalone paper.**

1. **Every component is individually documented.** GSE growth, the post-crisis Federal Reserve
   balance sheet, the 2010 shift to direct student lending. What is new is that they **net to
   approximately zero**, which is one paragraph of insight once the denominator exists.
2. **Session 1 already narrowed the contribution twice** — FHFA publishes a GSE share series on
   a mortgage denominator, CBO publishes a combined credit and insurance measure on a household
   asset denominator. The residual was the denominator, the synthesis and the long run. The
   programme decomposition adds the rotation and nothing structural.
3. **One headline claim is conditional.** Post-2013 continuation holds centrally and vanishes
   under the second-round rule (session 2). A paper must carry that caveat in its abstract; a
   section can carry it in a sentence.
4. **The findings all strengthen paper one rather than standing apart.** The U-shape reframes
   the 79.4 percent level paper one already reports — today is a *return*, not a record. The
   rotation explains the holder leg paper one already measures. As a section they make paper
   one's central measurement more interesting. As a paper they inherit every one of paper one's
   caveats without carrying paper one's main result.

**Recommendation: Section 4.5 of paper one, "How the state came to hold it".** Roughly three
exhibits — the U-shaped series with both legs; the two-phase orthogonality table; the
programme decomposition showing the rotation — and about 1,200 words. Both classification
series and both backing rules appear as columns, not as a robustness appendix.

**What would change this call.** If the euro-area holder leg could be built to the same
standard, the rotation becomes a comparative question — did other states rotate too, or is
this American? — and that is a paper. ECB QSA cannot support it (no issuer-counterpart detail),
so it would need national sources country by country. That is a real project and should be
scoped separately rather than bolted on.

**The stop rule was not triggered and is not being invoked.** This is not a kill; the thesis
survived session 2 and the decomposition confirmed it. It is a judgement that the result is
worth a section rather than a paper, and the owner can overrule it — the material is built
either way and the drafting cost differs by perhaps one session.

---

## 5. Files

| File | Contents |
|---|---|
| `s3_programme_decomposition.py` | the builder, with the 40/41 combination documented |
| `s3_programme_panel.csv` | per-class, per-year, per-programme, 1947–2025 |
| `s3_programme_series.csv` | holder leg by programme, both rules |
| `s3_meta.json` | reconstruction check |
