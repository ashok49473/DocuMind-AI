import streamlit as st
from src.config import Config
from src.pdf_processor import PDFProcessor
from src.vector_store import VectorStoreManager
from src.qa_chain import QAChain
import time


st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DocuMindAI:
    """Main application class for DocuMind AI"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.vector_store_manager = None
        self.qa_chain = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize vector store and QA chain"""
        try:
            Config.validate_config()
            self.vector_store_manager = VectorStoreManager()
            self.qa_chain = QAChain(self.vector_store_manager)
        except ValueError as e:
            st.error(f"Configuration error: {str(e)}")
            st.info("Please set up your environment variables in a .env file")
    
    def process_pdf(self, pdf_file):
        """Process uploaded PDF file"""
        if not pdf_file:
            return False
        
        with st.spinner("Processing PDF..."):
            # Extract text
            text = self.pdf_processor.extract_text_from_pdf(pdf_file)
            
            if not text:
                st.error("Failed to extract text from PDF")
                return False
            
            # Create documents
            documents = self.pdf_processor.create_documents(text, pdf_file.name)
            
            if not documents:
                st.error("Failed to create document chunks")
                return False
            
            # Clear existing index and add new documents
            self.vector_store_manager.clear_index()
            time.sleep(2)  # Wait for index to clear
            
            success = self.vector_store_manager.add_documents(documents)
            
            if success:
                # Reinitialize QA chain with new documents
                self.qa_chain = QAChain(self.vector_store_manager)
                st.success(f"Successfully processed PDF: {pdf_file.name}")
                st.info(f"Created {len(documents)} document chunks")
                return True
            else:
                st.error("Failed to add documents to vector store")
                return False
    
    def run(self):
        """Run the Streamlit application"""
        # Header
        st.title("DocuMind AI 🧠📚")
        st.markdown("### Transform Your PDFs into Conversational Knowledge")
        
        # Sidebar
        with st.sidebar:
            st.header("📁 Document Upload")
            
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type="pdf",
                help="Upload a PDF document to analyze"
            )
            
            if uploaded_file:
                if st.button("Process PDF", type="primary"):
                    self.process_pdf(uploaded_file)
            
            st.markdown("---")
            st.header("ℹ️ How to Use")
            st.markdown("""
            1. Upload a PDF document
            2. Click "Process PDF" to analyze
            3. Ask questions about the content
            4. Get AI-powered answers with sources
            """)
            
            st.markdown("---")
            st.header("🔧 Configuration")
            if st.button("Clear Vector Store"):
                if self.vector_store_manager:
                    self.vector_store_manager.clear_index()
                    st.success("Vector store cleared!")
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("💬 Ask Questions")
            
            # Question input
            question = st.text_input(
                "Enter your question:",
                placeholder="What is this document about?",
                help="Ask any question about the uploaded PDF content"
            )
            
            if st.button("Ask Question", type="primary", disabled=not question):
                if not self.qa_chain:
                    st.warning("Please upload and process a PDF first!")
                else:
                    with st.spinner("Thinking..."):
                        result = self.qa_chain.ask_question(question)
                        
                        # Store the question in session state
                        st.session_state.recent_questions.append(question)
                        
                        # Display answer
                        st.subheader("🎯 Answer")
                        st.write(result["answer"])
                        
                        # Display sources
                        if result["sources"]:
                            with st.expander("📚 Source Documents", expanded=False):
                                for i, doc in enumerate(result["sources"], 1):
                                    st.markdown(f"**Source {i}:**")
                                    st.text(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                                    st.markdown("---")
        
        with col2:
            st.header("📊 Status")
            
            # System status
            status_container = st.container()
            with status_container:
                if self.vector_store_manager and self.vector_store_manager.vector_store:
                    st.success("✅ Vector Store: Ready")
                    
                    # Display index statistics
                    stats = self.vector_store_manager.get_index_stats()
                    if stats:
                        total_vectors = stats.get('total_vector_count', 0)
                        st.info(f"📊 Vectors in index: {total_vectors}")
                else:
                    st.error("❌ Vector Store: Not Ready")
                
                if self.qa_chain and self.qa_chain.qa_chain:
                    st.success("✅ QA System: Ready")
                else:
                    st.error("❌ QA System: Not Ready")
            
            # Recent questions (if implementing session state)
            if 'recent_questions' not in st.session_state:
                st.session_state.recent_questions = []
            
            if st.session_state.recent_questions:
                st.subheader("🕒 Recent Questions")
                for q in st.session_state.recent_questions[-5:]:
                    st.text(f"• {q}")

def main():
    """Main function to run the application"""
    app = DocuMindAI()
    app.run()

if __name__ == "__main__":
    main()
    