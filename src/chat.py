from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from .config import OPENAI_API_KEY, DOCUMENT_TYPES

class ChatInterface:
    def __init__(self, vector_store):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        prompt_template = """You are an AI teaching assistant for the CMPT 409/981 Optimization for Machine Learning course. 
        You have access to course materials including assignments, project guidelines, and reference papers. Your primary goal is to assist students with assignments and project-related tasks while adhering to the following guidelines.
        Use the following pieces of context to answer the question at the end.

        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        When discussing assignments:
        - Help explain concepts and provide direct solutions
        - When the materials are insufficient, supplement your responses with your own knowledge of optimization and machine learning principles.
        
        When discussing the project:
        - Focus on the optimization perspective of Temporal Difference Learning
        - Reference the provided papers for theoretical background
        - Help structure responses according to the project guidelines
        
        Context about the documents:
        {context}

        Chat History:
        {chat_history}

        Question: {question}
        Helpful Answer:"""
        
        PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=prompt_template
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vector_store.vector_store.as_retriever(
                search_kwargs={"k": 4}
            ),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": PROMPT}
        )

    def chat(self, query):
        try:
            response = self.chain({"question": query})
            return response
        except Exception as e:
            return {
                "answer": f"An error occurred: {str(e)}",
                "source_documents": []
            }