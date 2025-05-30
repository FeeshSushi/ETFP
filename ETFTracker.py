import csv
from yf_scraper import scrape_yf
from vanguard_scraper import scrape_vanguard

US = [
  "SPY",
  "VOO",
  "QQQ",
  "VTI",
  "DIA",
  "IWM",
  "ARKK",
  "XLF",
  "XLV",
  "VNQ"]
CAD = [
  "VCN.TO",
  "XIC.TO",
  "ZCN.TO",
  "VCE.TO",
  "HXT.TO",
  "ZDV.TO",
  "XEI.TO",
  "ZRE.TO",
  "VE.TO",
  "XGRO.TO"
]
results = []

for us in US:
    target = scrape_yf(us)
    results.append(target)

for cad in CAD:
    target = scrape_vanguard(cad)
    results.append(target)


with open('expense_ratio_records.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    for result in results:
        writer.writerow([result["symbol"], result["MER"]])