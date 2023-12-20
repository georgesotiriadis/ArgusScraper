import argparse
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Argument Parser
parser = argparse.ArgumentParser(description='LinkedIn Scraper')
parser.add_argument('--base_url', type=str, help='Base URL for LinkedIn search')
parser.add_argument('--log', action='store_true', help='Enable logging of results')
parser.add_argument('--location', type=str, help='Filter results by location')
parser.add_argument('--lt', action='store_true', help='Filter for less technical positions')
parser.add_argument('--csv', action='store_true', help='Export results to CSV')
parser.add_argument('--max_page', type=int, help='Maximum page number to scrape')
args = parser.parse_args()

# Less technical keywords
lt_keywords = ["sustainability", "marketing", "hr", "recruiter", "sales"]

# Your LinkedIn credentials

username = 'notatestlol@proton.me'
password = 'X$C6#moD8ka!TV!U'

# Initialize the WebDriver with options
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# Function to log in to LinkedIn
def login_to_linkedin(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    driver.find_element(By.XPATH, '//*[@type="submit"]').click()

# Function to extract details from search results
def extract_search_results(driver, url):
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

# Function to export data to CSV
def export_to_csv(data, filename='results.csv'):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Log in
login_to_linkedin(driver, username, password)
time.sleep(5)  # Wait for login to complete

# Pagination and Data Extraction
all_extracted_data = []
page = 1
while True:
    if args.max_page and page > args.max_page:
        if args.log:
            print(f"Stopping at user-defined max page: {args.max_page}")
        break

    current_url = f"{args.base_url}&page={page}"
    extracted_data = extract_search_results(driver, current_url)
    all_extracted_data.extend(extracted_data)

    # Check for the 'Next' button
    next_button = driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')
    if not next_button or not next_button[0].is_enabled():
        if args.log:
            print("No more pages left.")
        break

    page += 1
    time.sleep(5)  # Delay to avoid overloading the server

# Export to CSV if required
if args.csv and all_extracted_data:
    export_to_csv(all_extracted_data)
    if args.log:
        print("Results exported to CSV.")

# Close the browser
driver.quit()
