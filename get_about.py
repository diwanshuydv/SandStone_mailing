import warnings
warnings.filterwarnings("ignore")

import os
import time
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from generate import get_gemini_analysis

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()
LINKEDIN_EMAIL = "yigagek403@knilok.com"
LINKEDIN_PASSWORD = "boiidontlikedis"

# CSV file configuration
CSV_FILE_PATH = '9_sept4.csv'
URL_COLUMN_NAME = 'linkedin'
OUTPUT_COLUMN_NAME = 'mail'
SAVE_PROGRESS_INTERVAL = 10

# --- Main Script ---

# 1. Initialize Selenium WebDriver
print("Starting the script...")
driver = webdriver.Chrome()

try:
    # 2. Log in to LinkedIn
    print("Logging into LinkedIn...")
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    driver.find_element(By.ID, 'username').send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, 'password').send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.ID, 'password').submit()

    print("Successfully logged in.")
    time.sleep(5)

    # 3. Read the CSV file
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
        exit()

    # 4. Ensure the output column exists
    if OUTPUT_COLUMN_NAME not in df.columns:
        df[OUTPUT_COLUMN_NAME] = pd.NA
        print(f"Created new column: '{OUTPUT_COLUMN_NAME}'")

    # **NEW**: Create and pre-populate an in-memory cache from existing data
    url_cache = {}
    print("Pre-populating cache from existing CSV data...")
    for index, row in df.iterrows():
        url = row[URL_COLUMN_NAME]
        result = row[OUTPUT_COLUMN_NAME]
        # If a URL and a corresponding result already exist, add them to the cache
        if pd.notna(url) and pd.notna(result):
            url_cache[url] = result
    print(f"Cache pre-populated with {len(url_cache)} entries.")


    # 5. Loop through each row in the DataFrame
    print(f"Starting to process URLs from the '{URL_COLUMN_NAME}' column...")
    for index, row in df.iterrows():
        # print("dtype of index is ",type(index))
        url = row[URL_COLUMN_NAME]
        company_name = row["company_name"]

        # Basic validation
        if pd.isna(url) or 'linkedin.com/in/' not in str(url):
            print("Skipping invalid or empty URL at row " + str(index + 2) + ": " + str(url))
            df.loc[index, OUTPUT_COLUMN_NAME] = "Invalid URL"
            continue

        # **MODIFIED**: Primary Caching Logic
        # Check if this URL's result is already in our cache
        if url in url_cache:
            print(f"CACHE HIT for URL ({index + 1}/{len(df)}): {url}. Reusing previous result.")
            # If the current cell is empty, fill it with the cached value
            if pd.isna(df.loc[index, OUTPUT_COLUMN_NAME]):
                 df.loc[index, OUTPUT_COLUMN_NAME] = url_cache[url]
            continue # Move to the next row

        # If not in cache, proceed with scraping
        print(f"CACHE MISS. Processing URL ({index + 1}/{len(df)}): {url}")
        
        try:
            driver.get(url)
            time.sleep(4)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            scaffold_div = soup.find('div', class_='scaffold-layout')
            
            result_to_cache = ""
            if scaffold_div:
                analysis_result = get_gemini_analysis(str(scaffold_div.prettify()), company_name)
                result_to_cache = analysis_result
            else:
                result_to_cache = "Scaffold layout not found on page."
            
            # Update DataFrame and the cache
            df.loc[index, OUTPUT_COLUMN_NAME] = result_to_cache
            url_cache[url] = result_to_cache # **NEW**: Add the new result to the cache

        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")
            error_message = f"Error processing URL: {e}"
            df.loc[index, OUTPUT_COLUMN_NAME] = error_message
            url_cache[url] = error_message # **NEW**: Also cache errors to avoid retrying

        # Add a delay
        time.sleep(2)

        # Save progress periodically
        if (index + 1) % SAVE_PROGRESS_INTERVAL == 0:
            df.to_csv(CSV_FILE_PATH, index=False)
            print(f"--- Progress saved to '{CSV_FILE_PATH}' at row {index + 2} ---")

    # 6. Final save
    print("\nFinished processing. Saving final data to CSV.")
    df.to_csv(CSV_FILE_PATH, index=False)
    print(f"Successfully saved all updated data to '{CSV_FILE_PATH}'.")

finally:
    # 7. Always close the browser
    print("Closing the browser.")
    driver.quit()