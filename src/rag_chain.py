from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from src.config import Config
import streamlit as st

class RAGChain:
    def __init__(self, retriever):
        self.llm = ChatOpenAI(
            model_name=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.retriever = retriever
        self.chain = self._create_chain()
    
    def _create_chain(self):
        """Create the RAG chain with custom prompt"""
        
        template = """
        You are a helpful AI assistant that answers questions based on the provided context from PDF documents.
        
        Context from PDFs:
        {context}
        
        Question: {question}
        
        Instructions:
        1. Answer the question based primarily on the provided context
        2. If the context doesn't contain enough information, say so clearly
        3. Be specific and cite relevant information from the context
        4. If you're unsure, acknowledge the uncertainty
        5. Provide a clear, well-structured answer
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return chain
    
    def ask_question(self, question: str):
        """Ask a question and get an answer with sources"""
        try:
            result = self.chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            st.error(f"❌ Error generating answer: {str(e)}")
            return {
                "answer": "Sorry, I encountered an error while processing your question.",
                "source_documents": []
            }