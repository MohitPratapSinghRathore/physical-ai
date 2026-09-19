# Dose-response table

Version 0.7.0, generated 2026-09-20.

Rows are displacement as a share of the TOTAL US wage bill. Columns are balance sheets. Every cell reports the loss in dollars, as a share of GDP, and as a share of that sheet's own absorbing capacity, whose measure and source are in `absorbing_capacities.json`.

## Two columns, and what they mean

**First round** is an accounting exercise on measured balances: displaced households, their obligations, and a default uplift from Gerardi, Herkenhoff, Ohanian and Willen. It holds house prices, consumer demand, business revenue and the employment of non-displaced workers FIXED. Against an economy-wide supervisory scenario it is a LOWER BOUND, not an estimate.

**With second-round effects** is SCENARIO throughout. It maps each dose onto a macroeconomic severity and then borrows the Federal Reserve's own 2026 severely adverse loss rates at that severity. Beyond the Fed's own scenario the numbers are an extrapolation of its rates and are labelled as such.

## What must travel with every number

- **Cognitive exposure measures TASK OVERLAP, not displacement and not timing.** Top-quintile occupations on either cognitive index include a great deal of work more likely to be augmented than replaced.
- **Only the 5 and 10 percent doses are fully inside the observed data range for every exposure type.** At 25 percent the embodied rows are already outside it.
- **No single exposure type can deliver a 75 percent dose.** Embodied saturates at 33.7 percent of the total wage bill, cognitive AIOE at 47.4 and cognitive GPT at 53.6. Saturated rows report the loss at the largest attainable dose.
- **No result is quoted as a cumulative percentage without its horizon.**
- **No dollar figure is quoted without naming the incidence assumption.** On household counts incidence moves the answer by 5 to 9 percent; on dollars by 1.75 to 3.01 times.
- **Exposure type is mostly a pay proxy.** Neither the household nor the fiscal exposure-type contrast survives controlling for wage level. `by_wage_quintile.csv` is the version organised around the primitive that actually does the work.
