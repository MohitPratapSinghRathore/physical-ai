"""Layer 2 (2020 episode): pre-shock 2019Q2 balance sheets, SOD 2019, and
outcomes 2020Q1-2022Q4. Construct rebuilt on 2019 pre-shock data per section 6."""
import json, time, urllib.parse, urllib.request
from pathlib import Path
import pandas as pd
RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "validation"
API = "https://banks.data.fdic.gov/api"
FIN = ["CERT","REPDTE","NAMEFULL","STNAME","ASSET","DEP","EQ","SC","SCMUNI",
       "LNLSGR","LNRECONS","LNRENRES","LNREMULT","LNRERES","LNRELOC","LNREAG",
       "LNCI","LNAG","LNCRCD","LNAUTO","LNCONOTH","BRO","RBC1AAJ","RBCT1J"]
OUTF = ["CERT","REPDTE","NTRERES","NTRERESQ","NTCRCD","NTCRCDQ","NTAUTO",
        "NTAUTOQ","NTCONOTH","NTCI","NTCIQ","NTRENRES","NTRECONS","NTLNLSQ",
        "LNLSGR","RBC1AAJ"]
def fetch(ep, filt, fields):
    out, off = [], 0
    while True:
        q = urllib.parse.urlencode({"filters": filt, "fields": ",".join(fields),
                                    "limit": 10000, "offset": off, "format": "json"})
        for a in range(5):
            try:
                with urllib.request.urlopen(f"{API}/{ep}?{q}", timeout=180) as r:
                    p = json.load(r)
                break
            except Exception:
                if a == 4: raise
                time.sleep(3*(a+1))
        rows = [d["data"] for d in p.get("data", [])]
        out.extend(rows); off += 10000
        if off >= p["meta"]["total"] or not rows: break
    return pd.DataFrame(out)
fetch("financials","REPDTE:20190630",FIN).to_csv(RAW/"fdic_financials_20190630.csv",index=False)
print("fin 2019Q2 done")
fetch("sod","YEAR:2019",["CERT","YEAR","STCNTYBR","DEPSUMBR"]).to_csv(RAW/"fdic_sod_2019.csv",index=False)
print("sod 2019 done")
fr=[]
for y in range(2020,2023):
    for m in ("0331","0630","0930","1231"):
        d=fetch("financials",f"REPDTE:{y}{m}",OUTF); d["REPDTE"]=f"{y}{m}"; fr.append(d)
        print(f"  {y}{m}: {len(d)}")
pd.concat(fr,ignore_index=True).to_csv(RAW/"fdic_outcomes_2020_raw.csv",index=False)
print("outcomes done")
