from langchain.document_loaders import UnstructuredFileLoader, TextLoader, BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import DOCUMENT_TYPES
import os

class DocumentLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def get_appropriate_loader(self, file_path):
        """Return appropriate loader based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.html':
            return BSHTMLLoader(file_path)
        elif ext in ['.txt', '.py']:
            return TextLoader(file_path)
        else:
            return UnstructuredFileLoader(file_path)

    def load_directory(self, directory=None):
        """Load documents from a specific directory"""
        documents = []
        base_path = self.data_dir if directory is None else os.path.join(self.data_dir, directory)
        
        for root, _, files in os.walk(base_path):
            rel_path = os.path.relpath(root, self.data_dir)
            doc_type = rel_path.split(os.path.sep)[0] if rel_path != "." else "other"
            
            for file in files:
                if file.startswith('.') or file.endswith(('.pyc', '.git')):
                    continue
                    
                file_path = os.path.join(root, file)
                
                # Check if file is in DOCUMENT_TYPES
                if doc_type in DOCUMENT_TYPES and file not in DOCUMENT_TYPES[doc_type].get("files", []):
                    continue
                
                try:
                    loader = self.get_appropriate_loader(file_path)
                    docs = loader.load()
                    
                    # Add rich metadata
                    for doc in docs:
                        doc.metadata.update({
                            "source": file_path,
                            "directory": rel_path,
                            "file_type": os.path.splitext(file)[1],
                            "doc_type": doc_type
                        })
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        return self.text_splitter.split_documents(documents)

    def load_documents(self):
        """Load all documents from the data directory"""
        return self.load_directory()