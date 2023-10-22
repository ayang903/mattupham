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
import time

#Summarization
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")



# Reddit Section
def get_reddit_data(num_posts):
    clientSecretKey = os.getenv("CLIENT_SECRET_KEY")
    reddit = praw.Reddit(client_id="kMolVsEMMe0041y37FnL_Q",
                         client_secret=clientSecretKey,
                         user_agent="Scraper")
    subreddit = reddit.subreddit("technews")
    posts = []

    for post in subreddit.hot(limit=num_posts):
        url = post.url
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        text = ' '.join(soup.stripped_strings)
        
        posts.append({'title': post.title, 'url': post.url, 'text': text})
    
    return posts
    
    
        
        
    

# NewsAPI Section
def get_news_data(query, num_articles):
    conn = http.client.HTTPSConnection("newsapi.org")
    fromDate = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    headers = {'Authorization': '0db7ab8d26b34533b00be11af29b8c73','User-Agent': 'Andys News Agent'}
    encoded_query = quote(query)
    conn.request("GET", f"/v2/everything?q={encoded_query}&from={fromDate}&pageSize={num_articles}", headers=headers)
    res = conn.getresponse().read()
    response_json = json.loads(res)
    print(json.dumps(response_json, indent=4))
    articles = response_json.get('articles', [])
    cleaned_articles = [{'title': a['title'], 'url': a['url'], 'text': a['content']} for a in articles]

    return cleaned_articles

# YouTube Section
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

# JSON -> CSV  Section
def read_json(filename: str) -> dict: 

    try: 
        with open(filename, "r") as f: 
            data = json.loads(f.read()) 
    except: 
        raise Exception(f"Reading {filename} file encountered an error") 

    return data 


def normalize_json(data: dict) -> dict: 

    new_data = dict() 
    for key, value in data.items(): 
        if not isinstance(value, dict): 
            new_data[key] = value 
        else: 
            for k, v in value.items(): 
                new_data[key + "_" + k] = v 

    return new_data 


def generate_csv_data(data: dict) -> str: 

    # Defining CSV columns in a list to maintain 
    # the order 
    csv_columns = data.keys() 

    # Generate the first row of CSV 
    csv_data = ",".join(csv_columns) + "\n"

    # Generate the single record present 
    new_row = list() 
    for col in csv_columns: 
        new_row.append(str(data[col])) 

    # Concatenate the record with the column information 
    # in CSV format 
    csv_data += ",".join(new_row) + "\n"

    return csv_data 


def write_to_file(data: str, filepath: str) -> bool: 

    try: 
        with open(filepath, "w+") as f: 
            f.write(data) 
    except: 
        raise Exception(f"Saving data to {filepath} encountered an error") 






# Main function to get data from all sources and save to a JSON file
def main():
    numRedditPosts = 3
    numNewsPosts = 5
    numYoutubePosts = 5

    reddit_data = get_reddit_data(numRedditPosts)
    news_data = get_news_data('artificial intelligence', numNewsPosts)
    youtube_data = get_youtube_data('tech news', numYoutubePosts)
#edit the number to modify the number of articles in the json file
    all_data = {
        'reddit': reddit_data,
        'news': news_data,
        'youtube': youtube_data
    }

    # Get the current date and time and format it as a string
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Include the timestamp in the output filename
    filename = f'all_data_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json_string = json.dumps(all_data, ensure_ascii=False, indent=4)
        f.write(json_string)
        print(json_string.encode('utf-8'))  # This line will print the JSON to the console
    


    #Opening created all data json file
    f = open(filename)
    allDataFile = json.load(f)

    #Query for GPT-4
    query = "Summarize the text based of the title into 10 concise key points."

   
    
    
    #Reddit Summarization
    for x in range(3):
        
        #Putting data into txt file to be summarized
        with open("summarizedData.txt", "w") as f:
            f.write('title : ' + repr(allDataFile["reddit"][x]["title"]) + '\n' )
            f.write(repr(allDataFile["reddit"][x]["text"]) + '\n' )
        
        

        #loading data into usable data for summarization
        loader = TextLoader('summarizedData.txt')
        index = VectorstoreIndexCreator().from_loaders([loader])


        #allDataFile['reddit'][x]['text'] = index.query(query)
        summarizedData = index.query(query) 

        # edit data
        allDataFile["reddit"][x]["summarizedText"] = summarizedData

        # overwrite file
        with open(filename, 'w') as f:
            json.dump(allDataFile, f, indent=4)


        #deleting everything within the summarized file
        with open("summarizedData.txt", "w") as f:
            f.truncate(0)
     

    #------ UNABLE TO SUMMARIZE FOR NOW -----
    #News Summarization
    """ for x in range(5):
               
        with open("summarizedData.txt", "w") as f:
            f.write('title : ' + repr(allDataFile["news"][x]["title"]) + '\n' )
            f.write(repr(allDataFile["news"][x]["text"]) + '\n' )
        
        


        loader = TextLoader('summarizedData.txt')
        index = VectorstoreIndexCreator().from_loaders([loader])


        #allDataFile['reddit'][x]['text'] = index.query(query)
        summarizedData = index.query(query) 

        # edit data
        allDataFile["news"][x]["summarizedText"] = summarizedData

        # overwrite file
        with open(filename, 'w') as f:
            json.dump(allDataFile, f, indent=4)

        with open("summarizedData.txt", "w") as f:
            f.truncate(0) """
        

   #Youtube Summarization

    query1 = "Summarize the data into 10 sentences. DO not include information about the narrator. make the summarization only based on the text."
    for x in range(5):
               
        with open("summarizedData.txt", "w") as f:
            f.write(repr(allDataFile["youtube"][x]["text"]) + '\n' )
        
        time.sleep(2)

        loader1 = TextLoader('summarizedData.txt')
        index1 = VectorstoreIndexCreator().from_loaders([loader1])


        #allDataFile['reddit'][x]['text'] = index.query(query)
        summarizedData = index1.query(query1) 

        # edit data
        allDataFile["youtube"][x]["summarizedText"] = summarizedData

        # overwrite file
        with open(filename, 'w') as f:
            json.dump(allDataFile, f, indent=4)

        with open("summarizedData.txt", "w") as f:
            f.truncate(0)   



    # JSON -> CSV SECTION


   # Read the JSON file as python dictionary 
    data = read_json(filename="all_data_" + timestamp + ".json") 

    # Normalize the nested python dict 
    new_data = normalize_json(data=data) 

    # Pretty print the new dict object 
    print("New dict:", new_data) 

    # Generate the desired CSV data 
    csv_data = generate_csv_data(data=new_data) 

    # Save the generated CSV data to a CSV file 
    write_to_file(data=csv_data, filepath="data.csv") 

        


if __name__ == "__main__":
    main()








