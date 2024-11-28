from langchain.embeddings import OpenAIEmbeddings
from typing import List
import numpy as np

class DocumentEmbeddings:
    def __init__(self, api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts"""
        try:
            embeddings = self.embeddings.embed_documents(texts)
            return embeddings
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return []
    
    def create_query_embedding(self, query: str) -> List[float]:
        """Create embedding for a single query"""
        try:
            embedding = self.embeddings.embed_query(query)
            return embedding
        except Exception as e:
            print(f"Error creating query embedding: {e}")
            return []