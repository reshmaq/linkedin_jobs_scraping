# LinkedIn Job Scraping

## Overview

This project is a Python script designed to scrape recent job postings from LinkedIn for Microsoft, Google, and Amazon in India. It uses Selenium and BeautifulSoup to extract job details, including the company name, job title, location, and more. The extracted data is then saved in both JSON and CSV formats.

## Features

- **Scrapes** job postings from the last week.
- **Extracts** details such as job title, company, location, LinkedIn job ID, posted date, seniority level, and employment type.
- **Saves** data in JSON and CSV formats.
- **Provides** real-time progress updates during scraping.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- pandas
- tqdm (for progress tracking)

## Setup

1. **Install Required Libraries**:
    Ensure you have the necessary Python libraries installed. You can install them using pip:
    ```bash
    pip install selenium beautifulsoup4 pandas tqdm
    ```

2. **Download ChromeDriver**:
    Download ChromeDriver from the [official site](https://sites.google.com/chromium.org/driver/). Choose the version that matches your installed version of Chrome.

3. **Update the ChromeDriver Path**:
    Place the downloaded ChromeDriver in a known directory. Update the `chrome_service` path in the script to point to your ChromeDriver executable:
    ```python
    chrome_service = Service('path_to_your_chromedriver')
    ```

## Usage

1. **Run the Script**:
    Execute the script to start scraping job postings:
    ```bash
    python linkedin_scraping.py
    ```

2. **Check Output Files**:
    After running the script, the extracted job data will be saved in the following files:
    - **JSON File**: `linkedin_jobs.json` - Contains job postings in JSON format.
    - **CSV File**: `linkedin_jobs.csv` - Contains job postings in CSV format.

## Notes

- The script filters job postings from the last week.
- Ensure compliance with LinkedIn’s terms of service to avoid potential issues.
- Adjust the path to the ChromeDriver executable as needed.

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.
