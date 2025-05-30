import sys, csv, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scrape_vanguard(name):
    options = Options()
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f'https://www.vanguard.ca/en/product/etf/equity/9561/vanguard-ftse-canada-all-cap-index-etf')
        wait = WebDriverWait(driver, 20)
        expense_ratio = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'detail-fund-card-label')]//button[contains(text(), 'MER')]/../../div[contains(@class, 'h-xxl')]"))
        ).text.strip()

        if expense_ratio == '-':
            time.sleep(3)
            expense_ratio = driver.find_element(By.XPATH, "//div[contains(@class, 'detail-fund-card-label')]//button[contains(text(), 'MER')]/../../div[contains(@class, 'h-xxl')]").text.strip()


        return {"symbol": name, "MER": expense_ratio}
    finally:
        driver.quit()
