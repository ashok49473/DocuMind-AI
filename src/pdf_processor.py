import PyPDF2
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import streamlit as st

class PDFProcessor:
    """Handles PDF text extraction and processing"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def create_documents(self, text: str, source: str = "uploaded_pdf") -> List[Document]:
        """Split text into chunks and create Document objects"""
        if not text.strip():
            return []
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create Document objects
        documents = [
            Document(
                page_content=chunk,
                metadata={"source": source, "chunk_id": i}
            )
            for i, chunk in enumerate(chunks)
        ]
        
        return documents