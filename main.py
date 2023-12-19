
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from Arguments.argparse_config import get_parser
from Scraper.linkedin_scraper import login_to_linkedin, extract_search_results
from Exporter.csv_exporter import export_to_csv

username = 'a@p.co'
password = 'password'

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

parser = get_parser()
args = parser.parse_args()

login_to_linkedin(driver, username, password)
time.sleep(5)

all_extracted_data = []
page = 1
while True:
    if args.max_page and page > args.max_page:
        if args.log:
            print(f"Stopping at user-defined max page: {args.max_page}")
        break

    current_url = f"{args.base_url}&page={page}"
    extracted_data = extract_search_results(driver, current_url, args)
    all_extracted_data.extend(extracted_data)

    next_button = driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')
    if not next_button or not next_button[0].is_enabled():
        if args.log:
            print("No more pages left.")
        break

    page += 1
    time.sleep(5)

    if args.csv and all_extracted_data:
        export_to_csv(all_extracted_data)
        if args.log:
            print("Results exported to CSV.")

    driver.quit()
