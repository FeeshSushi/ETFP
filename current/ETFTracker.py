import csv, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from etfm_scraper import scrape_page

def scrape_single_page(num):
    link = "https://etfmarket.cboe.com/canada/en/etf-screener?p="
    temp = link + str(num)
    try:
        result = scrape_page(temp)
        return result
    except Exception as e:
        print(f"Error scraping page {num}")
        return []

PAGE_COUNT = 84

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

results = []

with ThreadPoolExecutor(max_workers=5) as executor:
    page_numbers = range(1, PAGE_COUNT-1)
    results = list(executor.map(scrape_single_page, page_numbers))



output = os.path.join(output_dir, 'expense_ratio_records.csv')

with open(output, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Symbol', 'MER'])
    
    for page_data in results: 
        for etf in page_data:
            writer.writerow([etf["symbol"], etf["MER"]])
    