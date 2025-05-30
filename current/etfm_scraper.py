import sys, csv, time, re, tempfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def clean_mer(mer):
    match = re.search(r'(\d+\.?\d*%)', mer)
    if match:
        return match.group(1)
    else:
        return mer.strip()


def scrape_page(link):
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'lCLWh8')]"))
        )
        time.sleep(3)

        table = driver.find_element(By.XPATH, "//table[contains(@class, 'p1dBYW')]")
        table_rows = table.find_elements(By.XPATH, "//tr[contains(@class, 'lCLWh8')]")

        data = []
        for row in table_rows:
            try:
                name = row.find_element(By.CLASS_NAME, "vK1M9b").text
                mer_raw = row.find_element(By.XPATH, ".//td[@data-id='expense_ratio']").text
                mer = clean_mer(mer_raw)
                data.append({"symbol": name, "MER": mer})
            except Exception as e:
                print("Error extracting row {e}")
                continue

        return data
    finally:
        driver.quit()
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

