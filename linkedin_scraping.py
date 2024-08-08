import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_service = Service('C:\\Drivers\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')  # Path to your chromedriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Define the URLs for job postings
urls = [
    'https://www.linkedin.com/jobs/search?location=India&geoId=102713980&f_C=1035&position=1&pageNum=0',
    'https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_C=1441',
    'https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_TPR=r86400&f_C=1586&position=1&pageNum=0'
]

job_data = []

print("Starting the job scraping process...")

for url_index, url in enumerate(urls, start=1):
    print(f"Scraping URL {url_index}/{len(urls)}: {url}")
    driver.get(url)
    time.sleep(3)  # Allow the page to load

    # Scroll to the bottom to load all job postings
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_cards = soup.find_all('div', class_='base-card')
    print(f"Found {len(job_cards)} job cards on URL {url_index}/{len(urls)}")

    for job_index, job_card in tqdm(enumerate(job_cards, start=1), total=len(job_cards), desc=f"URL {url_index}/{len(urls)} Jobs"):
        try:
            company_name = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
            job_title = job_card.find('h3', class_='base-search-card__title').text.strip()
            job_id = job_card.find('a', class_='base-card__full-link')['href'].split('/')[-2].split('?')[0]
            location = job_card.find('span', class_='job-search-card__location').text.strip()
            posted_on = job_card.find('time')['datetime']

            # Convert posted_on to 'DD-MM-YYYY' format
            posted_date = datetime.strptime(posted_on, '%Y-%m-%d').strftime('%d-%m-%Y')

            # Find additional job details
            job_url = job_card.find('a', class_='base-card__full-link')['href']
            driver.get(job_url)
            time.sleep(3)
            job_soup = BeautifulSoup(driver.page_source, 'html.parser')
            seniority_level = job_soup.find('span', string='Seniority level').find_next_sibling('span').text.strip() if job_soup.find('span', string='Seniority level') else 'null'
            employment_type = job_soup.find('span', string='Employment type').find_next_sibling('span').text.strip() if job_soup.find('span', string='Employment type') else 'null'

            job_data.append({
                "company": company_name,
                "job_title": job_title,
                "linkedin_job_id": job_id,
                "location": location,
                "posted_on": posted_on,
                "posted_date": posted_date,
                "employment_type": employment_type,
                "seniority_level": seniority_level
            })

        except Exception as e:
            print(f"Error occurred while scraping job {job_index}/{len(job_cards)}: {e}")
            continue

driver.quit()

# Save data to JSON and CSV
with open('linkedin_jobs.json', 'w') as json_file:
    json.dump(job_data, json_file, indent=4)

df = pd.DataFrame(job_data)
df.to_csv('linkedin_jobs.csv', index=False)

# Check if we have at least 50 job postings
if len(job_data) >= 50:
    print(f"Successfully scraped {len(job_data)} job postings.")
else:
    print(f"Only scraped {len(job_data)} job postings. Please check the script or the source.")

# Print job data for reference
for job in job_data:
    print(json.dumps(job, indent=4))
