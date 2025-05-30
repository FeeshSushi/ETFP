import sys, csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def scrape_yf(name):
    options = Options()
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f'https://ca.finance.yahoo.com/quote/{name}/')
        
        label_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Expense Ratio')]")
        parent = label_element.find_element(By.XPATH, "..")
        expense_ratio = parent.find_element(By.XPATH, ".//span[contains(text(), '%')]").text

        return {"symbol": name, "MER": expense_ratio}
    finally:
        driver.quit()

