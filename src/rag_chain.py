from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import Config
import streamlit as st

class QAChain:
    """Handles question-answering using retrieval-augmented generation"""
    
    def __init__(self, vector_store_manager):
        self.vector_store_manager = vector_store_manager
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            model_name=Config.LLM_MODEL,
            temperature=0.1
        )
        self.qa_chain = None
        self._setup_qa_chain()
    
    def _setup_qa_chain(self):
        """Setup the QA chain with custom prompt"""
        if not self.vector_store_manager.vector_store:
            return
        
        # Custom prompt template
        prompt_template = """
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context provided, just say that you don't know, 
        don't try to make up an answer.

        Context:
        {context}

        Question: {question}
        
        Answer: Provide a comprehensive answer based on the context above. If relevant, 
        include specific details and examples from the document.
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        try:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store_manager.vector_store.as_retriever(
                    search_kwargs={"k": 4}
                ),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
        except Exception as e:
            st.error(f"Error setting up QA chain: {str(e)}")
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question and get an answer with sources"""
        if not self.qa_chain:
            return {
                "answer": "QA system is not properly initialized. Please upload a PDF first.",
                "sources": []
            }
        
        try:
            result = self.qa_chain({"query": question})
            
            return {
                "answer": result["result"],
                "sources": result.get("source_documents", [])
            }
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
            return {
                "answer": "Sorry, I encountered an error while processing your question.",
                "sources": []
            }
