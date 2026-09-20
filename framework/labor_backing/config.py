"""Labour backing ratio: claim classes, tracing rules, holder map. PROVISIONAL throughout.

DEFINITION (B1). FIRST-ROUND servicing only. For each claim class, the labour backing
share is the fraction of the cash flow that DIRECTLY services that claim which is labour
income. One step, no further tracing. A class serviced out of business revenue has a
direct labour backing of ZERO BY RULE, because the cash flow that services it is business
revenue and not wages. That is not a claim that no labour income ever reaches it. It is
the first-round versus second-round distinction of the paper applied to the liability
side, and the second-round version is B2, reported separately and never blended.

PLAUSIBILITY BOUNDS, stated before any number:
  every backing share and every holder share lies in [0, 1]
  holder shares sum to 1 within each claim class
  labour-backed claims <= total claims in every class
  the aggregate ratio lies between the smallest and the largest class ratio
"""

# ---------------------------------------------------------------------------
# WAGE-BACKED SHARES from the non-working household result, BY CLAIM TYPE.
#
# ACS: the share of annual mortgage SERVICE and of RENT paid by working-core
# households, engine core definition (at least one employed member aged 25 to 64).
# Claim 42, standing: non-working households hold 16.0 percent of mortgage service
# and 27.3 percent of rent. Source data/processed/stress/a38_correction_decomposition.csv,
# stage 3_plus_engine_core_definition.
#
# SIPP: the working-core share of BALANCES by loan, from
# data/processed/under_reporting_factors.csv column working_core_share_of_full.
# These are the CORRECTED factors (claim 127: A80's factors conflated survey
# under-reporting with sample coverage).
# ---------------------------------------------------------------------------
ACS_MORTGAGE_SERVICE_WORKING_CORE = 1.0 - 0.159777      # 0.840223
ACS_RENT_WORKING_CORE = 1.0 - 0.272460                  # 0.727540

# read from under_reporting_factors.csv at build time; listed here for the record
SIPP_WORKING_CORE_SHARE = {"mortgage": 0.8205, "card": 0.7400,
                           "auto": 0.7737, "student": 0.8832}

# ---------------------------------------------------------------------------
# LABOUR-LINKED SHARE OF RECEIPTS
# Federal: data/processed/labor_tax_share.json. Central splits the individual income
# tax by the SOI wage share of AGI and adds social insurance contributions in full.
# The 77.7 percent upper bound treats all individual income tax as labour-linked; it is
# claim 34, WITHDRAWN as a central figure and retained here only as a bound.
# State and local: personal current taxes (FRED W071) split by the same SOI wage share,
# over total state and local current TAX receipts (FRED W070). Property tax is a capital
# levy and sales tax is consumption out of labour income at one remove, which is a
# SECOND-round channel and therefore excluded from the first-round central case.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# SOCIAL INSURANCE, a MEMO ITEM and never inside the headline ratio.
# Payroll share of each fund's own total income, 2026 Trustees summary Table 5.
# Carried separately because an unfunded social insurance obligation is not a financial
# claim in the Financial Accounts sense, and folding it in would double count against
# Treasury debt (feasibility.md judgement call 3, and the A43 double-counting warning).
# ---------------------------------------------------------------------------
SOCIAL_INSURANCE_PAYROLL_SHARE = {"OASI": 0.9054, "DI": 0.9571, "HI": 0.8720}

# ---------------------------------------------------------------------------
# CLAIM CLASSES. Z.1 LIABILITY codes, summed. Millions of dollars.
# "rule" is the one or two sentence tracing rule required by B1.
# ---------------------------------------------------------------------------
CLASSES = [
    dict(key="home_mortgage", label="Home mortgages, one to four family",
         liab=["FL153165105"], instrument="3065105", holder="mortgage",
         backing="acs_mortgage_service",
         rule="Serviced from household income. The labour backing share is the share of "
              "mortgage service paid by households with an employed member aged 25 to 64."),
    dict(key="credit_card", label="Revolving consumer credit",
         liab=["FL153166100"], instrument="3066000", holder="consumer",
         backing="sipp_card",
         rule="Serviced from household income. The labour backing share is the working-core "
              "share of card balances in SIPP."),
    dict(key="auto_loan", label="Consumer credit, automobile loans",
         liab=["FL153166400"], instrument="3066000", holder="consumer",
         backing="sipp_auto",
         rule="Serviced from household income. The labour backing share is the working-core "
              "share of vehicle loan balances in SIPP."),
    dict(key="student_loan", label="Consumer credit, student loans",
         liab=["FL153166220"], instrument="3066000", holder="student",
         backing="sipp_student",
         rule="Serviced from household income. The labour backing share is the working-core "
              "share of student loan balances in SIPP."),
    dict(key="other_consumer", label="Other non-revolving consumer credit",
         liab=["FL153166205"], instrument="3066000", holder="consumer",
         backing="sipp_consumer_blend",
         rule="Serviced from household income. No separate survey measure exists for this "
              "residual, so it carries the balance-weighted mean of the card, auto and "
              "student working-core shares. FLAGGED as a proxy."),
    dict(key="multifamily_mortgage", label="Multifamily residential mortgages",
         liab=["FL103165405", "FL113165405", "FL313165403"], instrument="3065405",
         holder="mortgage", backing="acs_rent",
         rule="Serviced from rent. The labour backing share is the share of rent paid by "
              "working-core households. One intermediary, tenant to landlord to lender."),
    dict(key="treasury", label="Treasury securities",
         liab=["FL313161105", "FL313169205"], instrument="3061105", holder="treasury",
         backing="federal_receipts",
         rule="Serviced from federal receipts. The labour backing share is the labour-linked "
              "share of those receipts: social insurance contributions in full plus the wage "
              "share of the individual income tax."),
    dict(key="state_local_debt", label="State and local government debt",
         liab=["FL213162005", "FL213168003", "FL214141005"], instrument="3062005",
         holder="municipal", backing="state_local_receipts",
         rule="Serviced from state and local receipts. The labour backing share is the wage "
              "share of personal current taxes over total state and local tax receipts. "
              "Property tax is a capital levy and sales tax is a second-round channel."),
    dict(key="corporate_bonds", label="Corporate bonds, nonfinancial corporate",
         liab=["FL103163005"], instrument="3063005", holder="corporate", backing="zero",
         rule="Serviced from business revenue. Direct labour backing is ZERO BY RULE: the "
              "cash flow that services the claim is corporate operating cash flow and not "
              "wages. Labour reaches it only through demand, which is B2."),
    dict(key="corporate_loans", label="Corporate loans, nonfinancial corporate",
         liab=["FL103168005", "FL103169005", "FL103169100"], instrument="3063005",
         holder="corporate", backing="zero",
         rule="Serviced from business revenue. ZERO BY RULE, as for corporate bonds."),
    dict(key="noncorporate_business_debt", label="Nonfinancial noncorporate business loans",
         liab=["FL113168005", "FL113169005", "FL113169535", "FL113167205"],
         instrument="3063005", holder="corporate", backing="zero",
         rule="Serviced from business revenue. ZERO BY RULE. FLAGGED: proprietors' income is "
              "mixed labour and capital by construction, so this is the class where the zero "
              "rule is least comfortable."),
    dict(key="commercial_mortgage", label="Commercial mortgages, excluding multifamily",
         liab=["FL103165505", "FL113165505", "FL163165505"], instrument="3065505",
         holder="mortgage", backing="zero",
         rule="Serviced from business revenue, that is from commercial rent paid out of "
              "tenant business revenue. ZERO BY RULE. Multifamily is the exception and is a "
              "separate class because its rent is paid out of wages directly."),
    dict(key="corporate_equity", label="Corporate equities, nonfinancial corporate",
         liab=["LM103164105"], instrument="3064105", holder="corporate", backing="zero",
         rule="A residual claim on business revenue. ZERO BY RULE, and more so than debt: "
              "the residual claimant is paid after every contractual claim including wages."),
]

# ---------------------------------------------------------------------------
# HOLDER MAP. Z.1 sector code to ultimate holder class.
# "Ultimately holds OR GUARANTEES": agency and GSE backed mortgage pools (41) and the
# GSEs themselves (40) go to the federal government, because the credit guarantee and
# not the pool investor bears the loss, and the GSEs are in conservatorship. The
# monetary authority (71) goes to the federal government because the Federal Reserve
# remits its net income to the Treasury. Both are judgement calls and both are varied.
# Aggregate sectors are NEVER used as holders; 89 is the all-sectors control total only.
# ---------------------------------------------------------------------------
HOLDER_OF_SECTOR = {
    "31": "federal_government", "40": "federal_government", "41": "federal_government",
    "34": "federal_government", "71": "federal_government", "36": "federal_government",
    "21": "state_local_government", "22": "state_local_government",
    "76": "banks", "74": "banks", "75": "banks", "47": "banks", "73": "banks",
    "51": "insurers", "54": "insurers",
    "57": "pensions",
    "15": "households", "16": "households",
    "26": "rest_of_world",
    "61": "other_financial", "63": "other_financial", "64": "other_financial",
    "65": "other_financial", "66": "other_financial", "67": "other_financial",
    "50": "other_financial", "46": "other_financial", "62": "other_financial",
    "45": "other_financial",
    "10": "nonfinancial_business", "11": "nonfinancial_business",
}
AGGREGATE_SECTORS = {"14", "17", "38", "79", "88", "89"}

# Sectors that are aggregates of other sectors. Used only when no component of the
# group is carried for that instrument, so nothing is ever double counted.
# 70 = private depository institutions = 76 + 74 + 75.  52 = 51 + 54.
# 59 = 57 + 34 + 22.  19 = households, 15 = households and nonprofits (16).
SECTOR_FALLBACK = {
    "70": ["76", "74", "75"],
    "52": ["51", "54"],
    "59": ["57", "34", "22"],
    "19": ["15"],
    "85": ["61", "63", "64", "65", "66", "67", "50", "46", "62", "45"],
    "81": ["61", "63", "64", "65", "66", "67", "50", "46", "62", "45"],
    "36": ["31", "21"],
}
FALLBACK_HOLDER = {"70": "banks", "52": "insurers", "59": "pensions",
                   "19": "households", "85": "other_financial",
                   "81": "other_financial", "36": "state_local_government"}

# OBLIGOR of each claim class: who pays, as distinct from who holds. The paper's
# federal share of LOSSES combines both, because a revenue shortfall lands on the
# obligor and a credit loss lands on the holder or guarantor.
OBLIGOR_OF_CLASS = {
    "home_mortgage": "households", "credit_card": "households",
    "auto_loan": "households", "student_loan": "households",
    "other_consumer": "households", "multifamily_mortgage": "nonfinancial_business",
    "treasury": "federal_government", "state_local_debt": "state_local_government",
    "corporate_bonds": "nonfinancial_business", "corporate_loans": "nonfinancial_business",
    "noncorporate_business_debt": "nonfinancial_business",
    "commercial_mortgage": "nonfinancial_business",
    "corporate_equity": "nonfinancial_business",
}
HOLDER_CLASSES = ["federal_government", "state_local_government", "banks", "insurers",
                  "pensions", "households", "rest_of_world", "other_financial",
                  "nonfinancial_business", "residual_unallocated"]

# instrument code used to enumerate holders for each holder scheme
HOLDER_INSTRUMENT = {"mortgage_1to4": "3065105", "mortgage_multi": "3065405",
                     "mortgage_comml": "3065505", "consumer": "3066000",
                     "treasury": "3061105", "municipal": "3062005",
                     "corporate": "3063005", "equity": "3064105"}
CLASS_HOLDER_INSTRUMENT = {
    "home_mortgage": "3065105", "multifamily_mortgage": "3065405",
    "commercial_mortgage": "3065505", "credit_card": "3066000",
    "auto_loan": "3066000", "other_consumer": "3066000", "student_loan": "3066000",
    "treasury": "3061105", "state_local_debt": "3062005",
    "corporate_bonds": "3063005", "corporate_loans": "3063005",
    "noncorporate_business_debt": "3063005", "corporate_equity": "3064105",
}
