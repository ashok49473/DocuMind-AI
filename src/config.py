import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "pdf-rag-index")
    
    # Document processing settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # LLM settings
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    # Retrieval settings
    TOP_K = 4
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            cls.OPENAI_API_KEY,
            cls.PINECONE_API_KEY,
            cls.PINECONE_ENVIRONMENT
        ]
        
        missing_vars = []
        for i, var in enumerate(required_vars):
            if not var:
                var_names = ["OPENAI_API_KEY", "PINECONE_API_KEY", "PINECONE_ENVIRONMENT"]
                missing_vars.append(var_names[i])
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True