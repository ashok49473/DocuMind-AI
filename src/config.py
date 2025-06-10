# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for DocuMind AI"""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "documind-ai")
    
    # Model configurations
    EMBEDDING_MODEL = "text-embedding-ada-002"
    LLM_MODEL = "gpt-3.5-turbo"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Pinecone index specifications
    PINECONE_DIMENSION = 1536  # OpenAI ada-002 embedding dimension
    PINECONE_METRIC = "cosine"
    PINECONE_CLOUD = "aws"
    PINECONE_REGION = "us-east-1"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set"""
        required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY"]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
