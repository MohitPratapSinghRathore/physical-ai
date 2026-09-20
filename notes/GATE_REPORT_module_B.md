# GATE REPORT, MODULE B. The AI bust, run through the engine.

Code and outputs: `framework/ai_bust/`. SCENARIO throughout, except where marked. The wealth
distribution, the nine filers and the two historical episodes are MEASURED.

---

## PART 1. PLAUSIBILITY VIOLATIONS

**None found in Module B.** Every bound held: the equity shares by wealth percentile sum to
1.000; no holder's AI-leg or wage-leg share exceeds 1; the implied consumption fall never
exceeds the wealth fall; the bust's wage-bill equivalent stays inside [0, 1].

One check is worth printing because it constrains an input the module depends on. **The
marginal propensity to consume out of wealth is a STATED ASSUMPTION here, not a sourced
parameter**, and it is the weakest input in the module. At the central 0.03, the two verified
episodes imply consumption falls of 0.75 and 0.57 percent of GDP, which is the right order of
magnitude for the 2001 recession and too small for 2008 to 2009. **That asymmetry is itself
informative: the 2008 fall was not a wealth effect, it was a credit event.**

---

## PART 2. THESIS-WEAKENING RESULTS

### 2.1 The "resembles 2000, not 2008" verdict is fragile, and it flips on a quantity we have not measured

The verdict rests on a debt-financed share of AI capex of **0.0654**, computed from the nine
filers' own filings. Solving for what would move it:

| additional debt-financed capex | share | verdict |
|---|---|---|
| 0 | 0.065 | resembles 2000 |
| **66.1bn** | **0.200** | **leaves the 2000 pattern** |
| **213.4bn** | **0.500** | **resembles 2008** |

**66.1bn is 14.7 percent of the 450bn of AI-adjacent bank commitments the Chicago Fed has
already identified.** Worse: the same source implies roughly **162bn already drawn** (9
percent of tier 1 outstanding against 25 percent committed), which is **2.5 times the flip
threshold**. If even 41 percent of that drawn amount funded capex in the measured year, the
verdict flips out of the 2000 pattern.

And Tier 4, the off-balance-sheet vehicles, GPU-backed loans, private credit to data centres,
data centre ABS and CMBS and vendor financing, **is not sourced at all**, while BIS Quarterly
Review March 2026 calls off-balance-sheet SPV structures **dominant** in data centre
financing.

> **The verdict must be restated as conditional on Tier 1 rather than as a finding about the
> AI financing structure. "On the nine filers' own balance sheets the structure resembles
> 2000" is defensible. "The structure resembles 2000" is not.**

### 2.2 The federal government loses in ALL THREE outcomes, and the payoff table now shows it

| holder | wage leg | AI leg | AI fails | partial | success |
|---|---|---|---|---|---|
| **federal government** | **0.3215** | **0.0100** | **-0.013** | **-0.166** | **-0.312** |
| banks | 0.1844 | 0.0318 | -0.034 | -0.108 | -0.153 |
| rest of world | 0.1801 | 0.1808 | -0.183 | -0.180 | **+0.001** |
| other financial | 0.1532 | 0.1633 | -0.165 | -0.158 | +0.010 |
| **households** | 0.0607 | **0.3842** | -0.385 | -0.222 | **+0.324** |
| pensions | 0.0110 | 0.0437 | -0.044 | -0.027 | +0.033 |

**Only the federal government and banks lose in every column.** Households, pensions, the
rest of the world and other financial institutions are roughly hedged or gain under success,
because they hold enough of the AI leg to offset. **The state holds 0.010 and cannot offset
anything.**

This is the empirical form of the hedge failure proposition and it is now a table rather than
an assertion. **It also confirms what the outline already conceded: partial success is not
the only regime in which the state loses.**

### 2.3 But the payoff table UNDERSTATES the federal position, and the correction matters

The table scores each holder by what it **holds**. The federal government holds 1.0 percent
of the AI leg, so it scores as barely exposed when AI fails. **B3 shows federal receipts
falling 569 to 955bn in a bust**, through capital gains and corporate tax.

> **The state's claim on the AI upside is FISCAL, not proprietary. It is the capital tax,
> which is exactly the contested rate of section 5.1.** The state is exposed to an AI bust
> roughly in proportion to how much of the AI surplus it taxes, and at the operative 0.0708
> that exposure is small. **Being barely exposed to the bust and being unhedged on the upside
> are the same fact.**

A holder-share table cannot show this. The words must sit beside it.

---

## PART 3. RESULTS THAT STAND

### 3.1 An AI bust is a LARGE FISCAL event and a SMALL CREDIT event, which inverts the displacement case

| | AI bust | 10 pct displacement |
|---|---|---|
| wage-bill equivalent | **0.12 to 0.84 pct** | 10 pct |
| household credit losses | **0.8 to 5.4bn** | 30.7bn |
| federal receipts fall | **569 to 955bn** (verified episodes) | 85.2bn terminal-year fiscal loss |

**The bust reaches the wage side 12 to 80 times more weakly than displacement, and the
federal budget through a completely different door.** Displacement is a wage tax base event;
a bust is a capital gains and corporate tax event. Corporate tax receipts fell **35.1 percent
in 2000 to 2002 and 53.4 percent in 2007 to 2009**.

### 3.2 Why the bust transmits weakly, and it is a distributional fact

**Corporate equity is extraordinarily concentrated.** At 2026Q2, measured from the
Distributional Financial Accounts:

| | share of corporate equity |
|---|---|
| top 0.1 pct | 25.0 pct |
| rest of top 1 pct | 25.9 pct |
| **top 1 pct total** | **50.9 pct** |
| next 9 pct | 37.2 pct |
| next 40 pct | 11.4 pct |
| **bottom 50 pct** | **0.58 pct** |

**An equity shock lands almost entirely on the households with the lowest marginal propensity
to consume.** That is why the wealth channel is weak, and it is measured rather than assumed.
GDP falls 0.34 to 1.69 percent and unemployment rises 0.13 to 0.84 points across every
combination of assumptions, against the Federal Reserve severely adverse scenario's 4.6
percent GDP fall.

### 3.3 The disjointness claim survives, narrowed, and the reason changes

The paper claims the instrument sets are nearly disjoint across the two failure directions.
**It survives, but not for the reason previously given.**

It is **not** that a bust leaves the wage side untouched. It does touch it, and B3 sizes that
at 0.12 to 0.84 percent of the wage bill. It is that:

> **The two failure directions hit the same institution, the federal government, through
> DIFFERENT TAX BASES. Displacement erodes the wage tax base; a bust erodes the capital gains
> and corporate tax base. An instrument that protects one does not protect the other.**

That is sharper and more defensible than disjointness of instrument sets, and it connects
directly to section 5.1: the capital tax rate is both the state's only claim on the AI upside
and the thing that would have to rise to close the fiscal condition after displacement.
**The same instrument is being asked to do two opposite jobs.**

---

## PART 4. LIMITATIONS OF THIS MODULE

1. **The MPC out of wealth is a stated assumption**, 1 to 5 cents, not a sourced parameter.
   It is checked against the two verified episodes and the check is printed, but it is the
   weakest input here.
2. **The AI investment share of recent GDP growth is a stated assumption**, swept from 0.10
   to 0.40, because this project has not verified a source for it. It is reported separately
   so a reader can substitute.
3. **Tier 3 has no defensible selection rule.** "Listed AI-exposed equity" is carried as this
   project's existing convention, a swept share of nonfinancial corporate equity, and
   labelled scenario. A real selection rule needs a security-level dataset we do not have.
4. **Tier 4 is not sourced at all**, and section 2.1 shows the headline verdict turns on it.
5. **The credit-led scenario's extra damage is not in its GDP path.** B2 captures the wealth
   and investment channels only; the additional bank-channel damage in a credit-led bust runs
   through Module A and is not added back into GDP, so the credit-led GDP fall is understated
   relative to the equity-led one.
6. **The unemployment-to-wage-bill conversion is one for one at average wages.** A bust falls
   on above-average earners, so the wage-bill effect is a lower bound.
7. **Chip supply chain is named and not sized**, deliberately: it is an input market, not a
   claim on AI capital, and folding it into a debt-financed share would double count.
