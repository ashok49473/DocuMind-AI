import os
import glob
from typing import List
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.config import Config
import streamlit as st

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_pdfs_from_folder(self, folder_path: str) -> List[Document]:
        """Load all PDF files from a folder and convert to documents"""
        documents = []
        
        if not os.path.exists(folder_path):
            st.error(f"Folder {folder_path} does not exist!")
            return documents
        
        pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
        
        if not pdf_files:
            st.warning(f"No PDF files found in {folder_path}")
            return documents
        
        for pdf_file in pdf_files:
            try:
                # Extract text from PDF
                text = self.extract_text_from_pdf(pdf_file)
                if text.strip():
                    # Create document with metadata
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": os.path.basename(pdf_file),
                            "file_path": pdf_file
                        }
                    )
                    documents.append(doc)
                    st.success(f"✅ Loaded: {os.path.basename(pdf_file)}")
                else:
                    st.warning(f"⚠️ No text extracted from: {os.path.basename(pdf_file)}")
                    
            except Exception as e:
                st.error(f"❌ Error loading {os.path.basename(pdf_file)}: {str(e)}")
        
        return documents
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
        
        return text
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        if not documents:
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        
        # Add chunk information to metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
            chunk.metadata["chunk_size"] = len(chunk.page_content)
        
        return chunks
    
    def process_documents(self, folder_path: str) -> List[Document]:
        """Complete document processing pipeline"""
        st.info("📄 Loading PDF documents...")
        documents = self.load_pdfs_from_folder(folder_path)
        
        if not documents:
            return []
        
        st.info("✂️ Splitting documents into chunks...")
        chunks = self.split_documents(documents)
        
        st.success(f"✅ Processed {len(documents)} documents into {len(chunks)} chunks")
        return chunks