
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

lt_keywords = ["sustainability", "marketing", "hr", "recruiter", "sales"]

def login_to_linkedin(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    driver.find_element(By.XPATH, '//*[@type="submit"]').click()

def extract_search_results(driver, url, args):
    driver.get(url)
    time.sleep(10)  # Wait for the page to load

    results = driver.find_elements(By.XPATH, '//li[@class="reusable-search__result-container"]')
    extracted_data = []

    for index, result in enumerate(results):
        try:
            name = result.find_element(By.XPATH, './/span[contains(@class, "entity-result__title-text")]/a').text
            position = result.find_element(By.XPATH, './/div[contains(@class, "entity-result__primary-subtitle")]').text
            location = result.find_element(By.XPATH, './/div[contains(@class, "entity-result__secondary-subtitle")]').text

            if args.location and args.location.lower() not in location.lower():
                continue
            if args.lt and not any(keyword.lower() in position.lower() for keyword in lt_keywords):
                continue

            record = {'Name': name, 'Position': position, 'Location': location}
            extracted_data.append(record)

            if args.log:
                print(f'Result {index + 1}: {record}')
        except Exception as e:
            if args.log:
                print(f"Error extracting details for result {index + 1}: {e}")

    return extracted_data
