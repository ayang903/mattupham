# AI News Analyzer

AI News Analyzer is a Python-based application that scrapes, processes, and summarizes news articles, YouTube video transcripts, and Reddit posts related to technology. It performs topic modeling on the collected data and visualizes the results. The project is contributed by AI Camp GI Team, leaded by Andy Yang, and contributed by Bob Fan, Blake Almon, Janice, Rayan Javaid, Lucy Grindler, Ava Tuntikanokporn, and coached by AI Camp's leaders.

# Description

This project consists of several Python scripts that work together to extract data from various online sources, preprocess the text data for natural language processing, apply topic modeling algorithms, and summarize the content. The results are then uploaded to a Google Sheets document for easy viewing and analysis.

---

This project leverages the `gspread` library to interact with the Google Sheets API, allowing for programmatic access to update and manipulate Google Sheets. It takes structured data from CSV files and updates or appends the information to a designated Google Sheet, streamlining workflows for data analysis, reporting, or any other collaborative data-driven task.

# Installation

To set up your development environment, clone the repo and install the necessary dependencies.

Ensure you have the following environment variables set for API access (ideally, in a .env file):
CLIENT_SECRET_KEY for Reddit API access
OPENAI_API_KEY for OpenAI API access


Here are some necessary libs for the project:
nltk
sklearn
pandas
numpy
matplotlib
praw
requests
beautifulsoup4
youtube-search-python
youtube-transcript-api
pytube
python-dotenv
gspread
oauth2client
openai

you can also find these info in requirement.txt.

---

Before you begin, ensure Python is installed on your system. You will need a Google account with the Google Sheets API enabled and a service account for API authentication.

# usage

Run the main.py script with arguments to scrape data, summarize and process it. Here's an example of how to use it:
python main.py --reddit 5 --news 10 --youtube 5
This command will scrape 5 Reddit posts, 10 news articles, and 5 YouTube videos, summarize them and record the results in the google sheet.


```bash
git clone [repository_url]
cd [repository_directory]
pip install -r requirements.txt

# CSV to Google Sheets Uploader

The CSV to Google Sheets Uploader is a Python-based automation tool that simplifies data transfer from CSV files directly into Google Sheets. Designed for efficiency and ease of use, this tool is ideal for individuals and teams who frequently work with data sets and require a seamless way to populate Google Sheets without manual data entry.

# Setting Up API Credentials

1. Visit the Google Cloud Console.

2. Create a new project.

3. Enable Google Sheets API and Google Drive API.

4. Create credentials for a service account.

5. Download the JSON key file for your service account.

# Environment Setup

Clone the repository, install the required dependencies, and set up your environment 
variable pointing to its location.

# Usage

Prepare your CSV file with the data to be uploaded. Share the target Google Sheet with your service account email and note the Google Sheet ID.

Update the config.py file (or any relevant script file) with the following details:

-   Path to your service account JSON file
    
-   Google Sheet ID of the target sheet
    

Run the upload_to_sheets.py script with the path to your CSV file as an argument:

bash

Copy code

python upload_to_sheets.py path_to_your_csv_file.csv

  

The script will read the CSV file and update the specified Google Sheet with its contents.
