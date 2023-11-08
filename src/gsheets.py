import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def upload_csv_to_new_worksheet(topic_string):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
  
  # link service account with roles set and api enabled
    creds = ServiceAccountCredentials.from_json_keyfile_name('serviceaccount/gsheets-upload-403705-efeef293c71f.json', scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/12N10KBYoPwFnvu3iTRgfGhVVlNFeo06BxVDlcFnwSC4/edit#gid=1761713442')

    # create a new "sheet" in the spreadsheet, name it the current date
    current = datetime.now().strftime("%m/%d/%Y_%H:%M:%S")
    worksheet = spreadsheet.add_worksheet(title=current, rows="100", cols="50")

    data = pd.read_csv('data.csv')
    set_with_dataframe(worksheet, data)

  # do the same for topic model words
    topic_sheet_name = f"{current}_topics"
    topic_worksheet = spreadsheet.add_worksheet(title=topic_sheet_name, rows="100", cols="1")

    # split by "\n\n" and write each topic to the new worksheet
    topics = topic_string.split("\n\n")
    for i, topic in enumerate(topics, start=1):
        topic_worksheet.update_cell(i, 1, topic)

    return f"Successfully uploaded worksheets: {current} and {topic_sheet_name} to 'https://docs.google.com/spreadsheets/d/12N10KBYoPwFnvu3iTRgfGhVVlNFeo06BxVDlcFnwSC4/edit#gid=1761713442"

