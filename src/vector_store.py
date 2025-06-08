import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List
from src.config import Config
import streamlit as st
import time

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.index_name = Config.PINECONE_INDEX_NAME
        self.vector_store = None
        self.pc = None
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client"""
        try:
            self.pc = pinecone.Pinecone(
                api_key=Config.PINECONE_API_KEY
            )
            st.success("🌲 Connected to Pinecone")
        except Exception as e:
            st.error(f"❌ Failed to connect to Pinecone: {str(e)}")
            raise e
    
    def create_index_if_not_exists(self):
        """Create Pinecone index if it doesn't exist"""
        try:
            existing_indexes = self.pc.list_indexes().names()
            
            if self.index_name not in existing_indexes:
                st.info(f"Creating new index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric='cosine'
                )
                # Wait for index to be ready
                time.sleep(10)
                st.success(f"✅ Created index: {self.index_name}")
            else:
                st.info(f"📋 Using existing index: {self.index_name}")
                
        except Exception as e:
            st.error(f"❌ Error with index creation: {str(e)}")
            raise e
    
    def add_documents(self, documents: List[Document]):
        """Add documents to Pinecone vector store"""
        if not documents:
            st.warning("No documents to add to vector store")
            return
        
        try:
            self.create_index_if_not_exists()
            
            st.info("🔄 Adding documents to vector store...")
            
            # Create vector store and add documents
            self.vector_store = Pinecone.from_documents(
                documents=documents,
                embedding=self.embeddings,
                index_name=self.index_name
            )
            
            st.success(f"✅ Added {len(documents)} documents to vector store")
            
        except Exception as e:
            st.error(f"❌ Error adding documents to vector store: {str(e)}")
            raise e
    
    def get_retriever(self, k: int = Config.TOP_K):
        """Get retriever for similarity search"""
        if not self.vector_store:
            # Connect to existing vector store
            self.vector_store = Pinecone.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings
            )
        
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def similarity_search(self, query: str, k: int = Config.TOP_K):
        """Perform similarity search"""
        if not self.vector_store:
            self.vector_store = Pinecone.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings
            )
        
        return self.vector_store.similarity_search(query, k=k)
    
    def delete_index(self):
        """Delete the Pinecone index"""
        try:
            self.pc.delete_index(self.index_name)
            st.success(f"🗑️ Deleted index: {self.index_name}")
        except Exception as e:
            st.error(f"❌ Error deleting index: {str(e)}")