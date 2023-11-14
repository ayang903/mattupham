import os
import json
import praw
import requests
import datetime
import http.client
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

def get_reddit_data(num_posts):
    clientSecretKey = 'u8gnI-3_I70MZ0H52Wg-RYAytkWWeQ'
    reddit = praw.Reddit(client_id="kMolVsEMMe0041y37FnL_Q",
                         client_secret=clientSecretKey,
                         user_agent="Scraper")
    subreddit = reddit.subreddit("technews")
    posts = []

    for post in subreddit.hot(limit=num_posts):
        url = post.url
        try:
          html_doc = requests.get(url).text
          soup = BeautifulSoup(html_doc, 'html.parser')
          for script_or_style in soup(["script", "style"]):
              script_or_style.decompose()
          text = ' '.join(soup.stripped_strings)
          posts.append({'title': post.title, 'url': post.url, 'text': text})
        except:
          continue
    return posts



# old newsapi section
# def get_news_data(query, num_articles):
#   conn = http.client.HTTPSConnection("newsapi.org")
#   fromDate = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
#   headers = {'Authorization': '0db7ab8d26b34533b00be11af29b8c73','User-Agent': 'Andys News Agent'}
#   encoded_query = quote(query)
#   conn.request("GET", f"/v2/everything?q={encoded_query}&from={fromDate}&pageSize={num_articles}", headers=headers)
#   res = conn.getresponse().read()
#   response_json = json.loads(res)
#   articles = response_json.get('articles', [])
#   cleaned_articles = [{'title': a['title'], 'url': a['url'], 'text': a['content']} for a in articles]

#   return cleaned_articles

def get_full_text(url):
  response = requests.get(url)
  response.raise_for_status()  # Check if the request was successful
  soup = BeautifulSoup(response.text, 'html.parser')
  paragraphs = soup.find_all('p')  # Assume the text is in <p> tags
  text = ' '.join([p.get_text() for p in paragraphs])
  return text

def get_news_data(query, num_articles):
  conn = http.client.HTTPSConnection("newsapi.org")
  fromDate = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
  headers = {'Authorization': '0db7ab8d26b34533b00be11af29b8c73','User-Agent': 'Andys News Agent'}
  encoded_query = quote(query)
  conn.request("GET", f"/v2/everything?q={encoded_query}&from={fromDate}&pageSize={num_articles}", headers=headers)
  res = conn.getresponse().read()
  response_json = json.loads(res)
  # print(json.dumps(response_json, indent=4))
  articles = response_json.get('articles', [])
  cleaned_articles = []
  for a in articles:
      try:
          full_text = get_full_text(a['url'])
      except Exception as e:
          print(f"Failed to retrieve full text for {a['url']}: {e}")
          full_text = a['content']  # Fall back to the snippet if the scrape fails
      cleaned_articles.append({'title': a['title'], 'url': a['url'], 'text': full_text})

  return cleaned_articles

def get_youtube_data(query, max_results):
    search = YoutubeSearch(query, max_results=max_results)
    results = search.to_dict()
    videos = []

    for result in results:
        video_id = result['id']
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([entry['text'] for entry in transcript_data])
        except Exception:
            transcript = "Transcript not available"
        videos.append({'title': yt.title, 'url': yt.watch_url, 'text': transcript})

    return videos

def scrape(num_reddit_posts, num_news_articles, num_youtube_videos):
    reddit_data = get_reddit_data(num_reddit_posts)
    news_data = get_news_data('artificial intelligence', num_news_articles)
    youtube_data = get_youtube_data('tech news', num_youtube_videos)
    all_data = {
        'reddit': reddit_data,
        'news': news_data,
        'youtube': youtube_data
    }

    filename = f'data/raw.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json_string = json.dumps(all_data, ensure_ascii=False, indent=4)
        f.write(json_string)
    return filename
