# || OPENAI API KEY REQUIRED ||
# CREATE dot .env file as the same level as LangChainQA.py and put the key as OPENAI_API_KEY=key

# summarizedText.txt to be changed later to where input is directly but into vector database (not from file = file just for demo)

#imports
import os
import sys

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

#dot env for not leaking the openai API key
from dotenv import load_dotenv
load_dotenv()

#used for setting the openai api key to the model
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

#this is where you ask the model a question
# type this into the terminal to get a response : python3 LangChainQAgpt/LangChainQA.py "The question your asking"
#query = sys.argv[1]
query = "Summarize this text for me in 5 sentences then put everything in json format with it being called 'redditsummary' "

#loads a txt file where you can input data and the response will be based on the data
loader = TextLoader('mattupham/summarizedText.txt')

#this can be used to load a directory of txt (used for multiple txt files)
#loader = DirectoryLoader(".", glob="*.txt")

index = VectorstoreIndexCreator().from_loaders([loader])

#prints response to terminal
print(index.query(query))