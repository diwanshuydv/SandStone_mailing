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

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# CSV file configuration
CSV_FILE_PATH = 'profiles.csv'          # The name of your CSV file
URL_COLUMN_NAME = 'linkedin_url'        # The name of the column with LinkedIn URLs
OUTPUT_COLUMN_NAME = 'scaffold_html'    # The name for the new column with scraped data

# --- Main Script ---

# 1. Initialize Selenium WebDriver
print("Starting the script...")
driver = webdriver.Chrome()

try:
    # 2. Log in to LinkedIn
    print("Logging into LinkedIn...")
    driver.get('https://www.linkedin.com/login')
    time.sleep(2) # Wait for the page to load

    email_field = driver.find_element(By.ID, 'username')
    email_field.send_keys(LINKEDIN_EMAIL)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(LINKEDIN_PASSWORD)
    password_field.submit()

    print("Successfully logged in.")
    time.sleep(5) # Wait for the homepage to load completely

    # 3. Read the CSV file
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
        exit() # Exit the script if the file doesn't exist

    # 4. Prepare to store scraped data
    scraped_data = []

    # 5. Loop through each URL in the specified column
    print(f"Starting to process URLs from '{URL_COLUMN_NAME}' column...")
    for index, row in df.iterrows():
        url = row[URL_COLUMN_NAME]
        
        # Simple check for a valid URL
        if pd.isna(url) or 'linkedin.com/in/' not in str(url):
            print(f"Skipping invalid or empty URL at row {index + 2}: {url}")
            scraped_data.append("Invalid URL")
            continue

        print(f"Processing URL ({index + 1}/{len(df)}): {url}")
        
        try:
            driver.get(url)
            # Wait for the page to load. You might need to adjust this value.
            time.sleep(4) 

            # Get page source and parse with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            
            # Find the scaffold layout div
            scaffold_div = soup.find('div', class_='scaffold-layout')
            
            if scaffold_div:
                # If found, append its HTML content as a string
                scraped_data.append(str(scaffold_div.prettify()))
            else:
                # If not found, append an error message
                scraped_data.append("Scaffold layout not found on page.")

        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")
            scraped_data.append(f"Error processing URL: {e}")

        # Add a random delay to mimic human behavior and avoid getting blocked
        time.sleep(2) # Wait 2 seconds between requests

    # 6. Add the scraped data as a new column to the DataFrame
    print("\nFinished scraping. Adding data to CSV.")
    df[OUTPUT_COLUMN_NAME] = scraped_data

    # 7. Save the updated DataFrame back to the same CSV file
    df.to_csv(CSV_FILE_PATH, index=False)
    print(f"Successfully saved updated data to '{CSV_FILE_PATH}'.")

finally:
    # 8. Always close the browser
    print("Closing the browser.")
    driver.quit()