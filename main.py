import sys

sys.path.append('src')

from summarizer import summarize
from data_retrieval import scrape
from data_preprocessing import lda
from gsheets import upload_csv_to_new_worksheet

import joblib
import gradio as gr


def main_orchestrator(num_reddit_posts, num_news_articles, num_youtube_videos, gpt_key, model):
  #scraping
  filename = scrape(num_reddit_posts=num_reddit_posts,
                  num_news_articles=num_news_articles,
                  num_youtube_videos=num_youtube_videos)

  # summarizing
  csv_filename = summarize(filename, gpt_key, model)
  print(csv_filename)

  # topic modeling
  topics, graph1, graph2 = lda(filename)
  print(topics)

  #upload to sheets
  gsheet_status = upload_csv_to_new_worksheet(topics)
  return gsheet_status, topics, graph1, graph2

demo = gr.Interface(
    fn=main_orchestrator,
    inputs=[gr.Number(precision=0, minimum=1, maximum=10), gr.Number(precision=0, minimum=1, maximum=10), gr.Number(precision=0, minimum=1, maximum=10), "text", "text"], # list of inputs that correspond to the parameters of the function.
    outputs=[gr.Textbox(label="Google Sheet Location"), gr.Textbox(label="Topics"), gr.Plot(label="Frequency of Topics"), gr.Plot(label="Top Words in Topics")], # list of outputs that correspond to the returned values in the function.
)
demo.launch()

