# What is already inside each rate, and what may therefore not be counted again

Item 1 of the tau_k rebuild. Read before anything else in this folder. Its only job is to
stop a layer being counted twice.

## 1. Acemoglu, Manera and Restrepo (2020), effective tax rates on equipment and software

Read in full from `data/raw/manual/AMR2020.txt`, extracted from the paper PDF in
`data/raw/manual/AMR2020_tax_automation.pdf`. The construction is in their equations 12 to
18.

**It is a MARGINAL rate, Hall and Jorgenson in form.** It prices the wedge on the marginal
investment dollar, not the tax collected on the existing capital stock.

**It already includes personal-level taxes.** This is the fact that governs everything that
follows. Their rate carries, explicitly:

- the entity-level corporate tax, `tau_c`
- the present value of depreciation allowances, `z_j`, asset class by asset class
- the financing margin, debt against equity, weighted by observed investment shares
- **the personal-level tax on the return**: `tau_e,c` on equity holders, `tau_b,c` on
  bondholders, `tau_o,p` on pass-through owners
- aggregation across the C-corporation and pass-through sectors by investment share

**The algebraic result that matters here.** Set `z_j = 1`, which is 100 percent expensing
under 26 USC 168(k). Their expressions collapse:

| financing and entity | effective marginal rate on the normal return |
|---|---|
| C-corporation, equity financed | **`tau_e,c`**, the shareholder rate alone. The entity-level tax washes out entirely |
| C-corporation, debt financed | **`tau_b,c` minus `tau_c`**, which AMR note is negative where bondholders face a lower rate than the corporation |
| pass-through, equity financed | **zero** |

So under full expensing the normal-return effective rate **is** the shareholder-level rate.
It is not zero.

## 2. IMF SDN/2024/002 (Brollo and others, June 2024), the average tax rate on capital

Read in full from `data/raw/manual/`. Built on the Bachas and others macro-historical
database.

**Numerator**: taxes attributed to capital, by OECD Revenue Statistics category. Category
1200, corporate income tax, is attributed to capital in full. Category 2000, social security
contributions, is attributed to labour in full. Category 1100, personal income tax, is split
between capital and labour. Property and wealth taxes are excluded deliberately, "to better
reflect taxes affecting firms' automation decisions". Consumption taxes are excluded.

**Denominator**: the capital income share from the national accounts.

**So it is an AVERAGE rate on the EXISTING stock, and it also includes personal-level
taxes.** It is broader than AMR in base and narrower in nothing that matters here.

## 3. The no-double-counting statement

Both published rates already contain the shareholder layer. Our own operative rate does not.

The project's published figure is

    tau_k = 0.351 x (0.52 x 0.21) + 0.649 x 0.05 = 0.0708

and inspection of that expression shows it stops at the **entity** level. There is no
shareholder-level term in it at all. Under AMR's own algebra the second term should be the
shareholder rate rather than an assumed 0.05, because expensing does not make the normal
return untaxed, it makes the *entity* tax on the normal return vanish and leaves the
shareholder tax standing.

**Therefore 0.0708 omits a layer. It does not avoid double-counting; it under-counts.** The
rebuild in `components.py` and `assemble.py` adds that layer once and only once:

- the entity layer enters through the federal rate, the state rate net of federal
  deductibility, and the current preferential foreign rate;
- the shareholder layer enters once, applied to what survives the entity layer;
- the AMR expensing result is used for the normal-return component, so the normal return
  carries the shareholder rate and no entity rate;
- **nothing is taken from the IMF average rate into the assembly.** The IMF figure is used
  only as a marked comparison point, because mixing an average rate on the stock into a
  marginal rate on the flow would be exactly the double count this note exists to prevent.
