Sandstone Summit Mailing Automation
===================================

A robust, AI-driven automation suite designed to streamline outreach for **Sandstone Summit 5.0** at IIT Jodhpur. This system automates the workflow of scraping professional profiles, generating highly personalized invitation content using Google Gemini AI, and dispatching bulk emails via Google Apps Script.

🚀 Features
-----------

*   **Automated Data Extraction**: Utilizes **Selenium** to scrape LinkedIn profiles (scaffold layout) based on provided URLs.
    
*   **AI-Powered Personalization**: Integrates **Google Gemini 2.0 Flash Lite** to analyze professional profiles and generate context-aware, "cheesy" (personalized) paragraphs connecting the speaker's expertise to the summit's themes.
    
*   **Smart Caching**: Implements a caching mechanism to prevent redundant scraping and API calls, allowing for interrupted runs to resume seamlessly.
    
*   **Bulk Emailing**: A custom **Google Apps Script** handles the final dispatch, sending HTML-formatted emails with PDF attachments (brochures) directly from Google Sheets.
    

🛠️ Tech Stack
--------------

*   **Python 3.x**: Core logic for scraping and AI processing.
    
*   **Selenium**: For web automation and scraping LinkedIn.
    
*   **Google Gemini API**: For generating personalized text analysis.
    
*   **Pandas**: For CSV data manipulation.
    
*   **Google Apps Script**: For Gmail integration and bulk sending.
    

📂 File Structure
-----------------

File

Description

get\_about.py

**Main Orchestrator**. Handles LinkedIn login, iterates through the CSV, scrapes profiles, calls the AI module, and saves results. Includes caching.

generate.py

**AI Module**. Contains the logic to interact with the Gemini API using specific prompt engineering for the summit invitations.

AppScript.gs

**Emailer**. Google Apps Script code to be deployed in the Google Sheet for sending the final emails.

gen\_csv.py

Legacy/Utility script for scraping raw HTML data without immediate AI processing.

linkedin.csv

Sample input/output CSV format.

⚙️ Prerequisites
----------------

1.  **Python 3.8+** installed.
    
2.  **Google Chrome** installed.
    
3.  **ChromeDriver** compatible with your Chrome version.
    
4.  **Gemini API Key** from Google AI Studio.
    
5.  **LinkedIn Account** (standard credentials).
    

📥 Installation
---------------

1.  git clone \[https://github.com/diwanshuydv/sandstone\_mailing.git\](https://github.com/diwanshuydv/sandstone\_mailing.git)cd sandstone\_mailing
    
2.  pip install -r requirements.txt
    
3.  LINKEDIN\_EMAIL=your\_email@example.comLINKEDIN\_PASSWORD=your\_passwordGEMINI\_API\_KEY=your\_gemini\_api\_key_Note: Ensure generate.py is updated to read GEMINI\_API\_KEY from os.environ if it currently uses a hardcoded key._
    

🚀 Usage Guide
--------------

### Phase 1: Data Enrichment (Python)

1.  Prepare your input CSV (e.g., 9\_sept4.csv) with the following columns:
    
    *   NAME: Name of the recipient.
        
    *   linkedin: LinkedIn profile URL.
        
    *   company\_name: Current company of the recipient.
        
2.  python get\_about.py
    
    *   This script will open a browser, log in to LinkedIn, and process the rows.
        
    *   **Output**: The CSV will be updated with a new column (e.g., mail) containing the AI-generated paragraphs.
        

### Phase 2: Email Dispatch (Google Sheets)

1.  Open a new **Google Sheet**.
    
2.  Import the processed CSV from Phase 1 into a sheet named "Diwanshu" (or update the script to match your sheet name).
    
3.  Ensure your Sheet has the following column order (based on AppScript.gs):
    
    *   Col A: Email
        
    *   Col B: Name
        
    *   Col C: Company
        
    *   Col D: File ID (Drive ID for the attachment)
        
    *   Col E: Cheesy Paragraph (The AI output)
        
4.  Go to **Extensions > Apps Script**.
    
5.  Copy the content of AppScript.gs into the editor.
    
6.  Run the sendPersonalizedEmails function.
    
    *   _Note: You will need to authorize the script to access your Gmail and Drive._
        

⚠️ Important Notes
------------------

*   **LinkedIn Rate Limits**: This tool uses Selenium to automate user behavior. Use cautiously and implement reasonable delays (already included in scripts) to avoid account restrictions.
    
*   **API Usage**: Ensure your Google Gemini API quota is sufficient for the number of rows you are processing.
    

🤝 Contributing
---------------

Contributions to improve the prompt engineering or scraping resilience are welcome. Please open a pull request.

📄 License
----------

This project is licensed for use by the Sandstone Summit Team, IIT Jodhpur.