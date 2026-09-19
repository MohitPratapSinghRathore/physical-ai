"""Registry of every raw series. Units are taken from FRED metadata at fetch time
(data/raw/fred/_titles.json), never asserted here. SOURCES.md is generated from this."""

# leg: legW household | legW_sov sovereign | taxbase | wagebill | denom | legA_ctx | stress
FRED_SERIES = {
    # --- Leg W: US household liabilities (Fed Z.1) ---
    "CMDEBT":       "legW",       # HH & nonprofit: debt securities and loans, liability
    "HHMSDODNS":    "legW",       # HH & nonprofit: 1-4 family residential mortgages
    "CCLBSHNO":     "legW",       # HH & nonprofit: consumer credit
    "FGCCSAQ027S":  "legW",       # Federal govt: student loans, asset (= HH liability)
    "TDSP":         "legW",       # debt service as % of DPI
    "HDTGPDUSQ163N":"legW",       # household debt to GDP (BIS-consistent)
    # --- Leg W: sovereign leg and the labor tax base ---
    "GFDEBTN":      "legW_sov",   # federal total public debt
    "FGRECPT":      "taxbase",    # federal current receipts
    "W006RC1Q027SBEA": "taxbase", # federal current TAX receipts
    "A074RC1Q027SBEA": "taxbase", # federal personal current taxes
    "W780RC1Q027SBEA": "taxbase", # FEDERAL contributions for govt social insurance
    "W782RC1Q027SBEA": "taxbase", # ALL-GOVERNMENT contributions for social insurance
    "W055RC1Q027SBEA": "taxbase", # personal current taxes, all levels of government
    "GDI":             "denom",   # gross domestic income (wage-share denominator)
    "A053RC1Q027SBEA": "taxbase", # corporate profits before tax (non-labor base proxy)
    # --- wage bill and denominators ---
    "WASCUR":       "wagebill",   # wages and salary accruals
    "COE":          "wagebill",   # total compensation of employees
    "W270RE1A156NBEA": "wagebill",# wage share of GDI
    "GDP":          "denom",
    "DPI":          "denom",
    # --- Leg A context: aggregate investment and corporate debt ---
    "Y033RC1Q027SBEA": "legA_ctx",# nonresidential equipment investment
    "B985RC1Q027SBEA": "legA_ctx",# software investment
    "PNFI":         "legA_ctx",   # private nonresidential fixed investment
    "TCMILBSNNCB":  "legA_ctx",   # nonfin corporate: debt securities AND loans
    # --- stress / early-warning indicators (WS8 falsifiable predictions) ---
    "CORCACBS":     "stress",     # consumer loan charge-off rate
    "DRSFRMACBS":   "stress",     # single-family mortgage delinquency rate
}

SEC_COMPANIES = {
    "MSFT":  ("0000789019", "Microsoft Corp", "hyperscaler"),
    "GOOGL": ("0001652044", "Alphabet Inc", "hyperscaler"),
    "AMZN":  ("0001018724", "Amazon.com Inc", "hyperscaler"),
    "META":  ("0001326801", "Meta Platforms Inc", "hyperscaler"),
    "ORCL":  ("0001341439", "Oracle Corp", "hyperscaler"),
    "CRWV":  ("0001769628", "CoreWeave Inc", "neocloud"),
    "NBIS":  ("0001861449", "Nebius Group NV", "neocloud"),
    "EQIX":  ("0001101239", "Equinix Inc", "datacenter_reit"),
    "DLR":   ("0001297996", "Digital Realty Trust Inc", "datacenter_reit"),
    "TSLA":  ("0001318605", "Tesla Inc", "robotics"),
}

SEC_TAGS = {
    "capex":       "PaymentsToAcquirePropertyPlantAndEquipment",
    "ocf":         "NetCashProvidedByUsedInOperatingActivities",
    "lt_debt":     "LongTermDebtNoncurrent",
    "debt_issued": "ProceedsFromIssuanceOfLongTermDebt",
    "fin_lease":   "FinanceLeaseLiabilityNoncurrent",
    "ppe_net":     "PropertyPlantAndEquipmentNet",
}
