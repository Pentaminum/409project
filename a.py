import os
import sys
from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

load_dotenv()

os.environ['OPENAI_API_KEY'] = constants.APIKEY

query = sys.argv[1]

loader = TextLoader("first.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query))