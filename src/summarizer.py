import os
import json
import openai
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def summarize(filename):

  # Opening created all data json file
  f = open(filename)
  allDataFile = json.load(f)

  finaldf = pd.DataFrame()

  for source, articles in allDataFile.items():
    for article in articles:

      title = article['title']
      text = article['text']
      combined_text = 'title: ' + title + '\n' + text

      try:
        # GPT-3.5 API for summarization
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant."
            }, {
                "role":
                "user",
                "content":
                f"Please summarize this news article text or youtube video transcript in four sentences or less. If no article/transcript is present, or it is unclear what the transcript is talking about, output 'Unable to summarize.'. {combined_text} "
            }])

        summarizedData = response['choices'][0]['message']['content']
        print(f"SUMMARY: {summarizedData} \n\n")

        # GPT-3.5 API for talking points from summarization generated
        follow_up = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[{
            "role": "system",
                "content": "You are a helpful assistant."
            }, {
                "role":
                "user",
                "content":
                f"Using this article, give me five sequential talking points that I can use to make a shortform video. Do not use more than 100 words. If the summarized article says 'Unable to summarize,' output 'No talking points available'. {summarizedData}"
          }])
        
        talking_pointsData = follow_up['choices'][0]['message']['content']
        print(f"TALKING POINTS: {talking_pointsData} \n\n")

        articleinfo = pd.DataFrame.from_records([{
            "title":
            article["title"],
            "source":
            source,
            "url":
            article["url"],
            "summarized_text":
            summarizedData,
            "talking_points":
            talking_pointsData
        }])
        finaldf = pd.concat([finaldf, articleinfo], ignore_index=True)

      except openai.error.InvalidRequestError as e:
        print(f"An error occurred: {e}")
        continue

  csvname = 'data.csv'
  finaldf.to_csv(csvname, index=False)
  return csvname
