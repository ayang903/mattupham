import praw
import pandas as pd

# import necessary libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re

ammountOfPosts = 1
 
reddit_read_only = praw.Reddit(client_id="RqbArZ6NcN2TVKR6MaPY1w",         # your client id
                               client_secret="a5qe8fn_CEOew2ryjaqfdWmYmR3Kvg",      # your client secret
                               user_agent="Scaper")        # your user agent
 
#news, technews, 
subreddit = reddit_read_only.subreddit("technews")
 
# Display the name of the Subreddit
print("Display Name:", subreddit.display_name)
 
# Display the title of the Subreddit
#print("Title:", subreddit.title)
 
# Display the description of the Subreddit
#print("Description:", subreddit.description)



# function to extract html document from given url
def getHTMLdocument(url):
      
    # request for HTML document of given url
    response = requests.get(url)
      
    # response will be provided in JSON format
    return response.text
 

for post in subreddit.hot(limit=ammountOfPosts):

    url_to_scrape = post.url
  
    # create document
    html_document = getHTMLdocument(url_to_scrape)
  
    # create soap object
    soup = BeautifulSoup(html_document, 'html.parser')
    
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)
  #  print(soup.body)
   
    # print(post.title)
    print(post.url)
    print()

   