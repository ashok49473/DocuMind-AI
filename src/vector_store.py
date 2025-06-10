from typing import List, Optional
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from src.config import Config
import streamlit as st
import time

class VectorStoreManager:
    """Manages vector store operations with Pinecone v6.0.0"""
    
    def __init__(self):
        print(Config.OPENAI_API_KEY)
        self.embeddings = OpenAIEmbeddings(
            api_key=Config.OPENAI_API_KEY,
            model=Config.EMBEDDING_MODEL
        )
        self.pc = None
        self.index = None
        self.vector_store = None
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and index using v6.0.0 API"""
        try:
            # Initialize Pinecone client
            self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
            
            # Check if index exists, create if it doesn't
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if Config.PINECONE_INDEX_NAME not in existing_indexes:
                st.info(f"Creating new Pinecone index: {Config.PINECONE_INDEX_NAME}")
                
                # Create index with serverless specification
                self.pc.create_index(
                    name=Config.PINECONE_INDEX_NAME,
                    dimension=Config.PINECONE_DIMENSION,
                    metric=Config.PINECONE_METRIC,
                    spec=ServerlessSpec(
                        cloud=Config.PINECONE_CLOUD,
                        region=Config.PINECONE_REGION
                    )
                )
                
                # Wait for index to be ready
                st.info("Waiting for index to be ready...")
                time.sleep(10)  # Give time for index initialization
            
            # Get index instance
            self.index = self.pc.Index(Config.PINECONE_INDEX_NAME)
            
            # Initialize LangChain PineconeVectorStore
            self.vector_store = PineconeVectorStore(
                index=self.index,
                embedding=self.embeddings,
                text_key="text"
            )
            
            
        except Exception as e:
            st.error(f"Error initializing Pinecone: {str(e)}")
            self.vector_store = None
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to vector store"""
        if not self.vector_store or not documents:
            return False
        
        try:
            # Add documents to the vector store
            self.vector_store.add_documents(documents)
            
            # Wait a moment for indexing to complete
            time.sleep(2)
            
            return True
        except Exception as e:
            st.error(f"Error adding documents to vector store: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search"""
        if not self.vector_store:
            return []
        
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            st.error(f"Error performing similarity search: {str(e)}")
            return []
    
    def clear_index(self) -> bool:
        """Clear all vectors from the index"""
        try:
            if self.index:
                # Get index stats to check if there are vectors
                stats = self.index.describe_index_stats()
                total_vectors = stats.get('total_vector_count', 0)
                
                if total_vectors > 0:
                    # Delete all vectors from all namespaces
                    self.index.delete(delete_all=True)
                    st.success(f"Cleared {total_vectors} vectors from index")
                else:
                    st.info("Index is already empty")
                
                return True
        except Exception as e:
            st.error(f"Error clearing index: {str(e)}")
            return False
    
    def get_index_stats(self) -> dict:
        """Get index statistics"""
        try:
            if self.index:
                return self.index.describe_index_stats()
            return {}
        except Exception as e:
            st.error(f"Error getting index stats: {str(e)}")
            return {}