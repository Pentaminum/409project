from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .config import OPENAI_API_KEY, VECTOR_DB_PATH

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_store = None

    def create_vector_store(self, documents):
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=VECTOR_DB_PATH
        )
        self.vector_store.persist()

    def load_vector_store(self):
        self.vector_store = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=self.embeddings
        )

    def similarity_search(self, query, k=4):
        return self.vector_store.similarity_search(query, k=k)