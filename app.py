import streamlit as st
import os
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="PDF RAG System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📚 PDF RAG System")
    st.markdown("Ask questions about your PDF documents using AI!")
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📄 Document Management")
        
        # Data folder path
        data_folder = st.text_input("Data Folder Path", value="data/")
        
        # Document processing button
        if st.button("🔄 Process Documents", type="primary"):
            process_documents(data_folder)
        
        # Display current status
        if "vector_store_ready" in st.session_state:
            st.success("✅ Vector store ready!")
            st.info(f"📊 Documents processed: {st.session_state.get('doc_count', 0)}")
        else:
            st.warning("⚠️ Please process documents first")
    
    # Main content area
    if "vector_store_ready" in st.session_state and st.session_state.vector_store_ready:
        
        # Question input
        st.header("🤔 Ask Questions")
        question = st.text_input("Enter your question about the PDFs:")
        
        # Question processing
        if st.button("🔍 Get Answer") and question:
            with st.spinner("Thinking..."):
                answer_data = ask_question(question)
                display_answer(answer_data)
        
        # Chat history
        if "chat_history" in st.session_state:
            st.header("💬 Chat History")
            for i, (q, a) in enumerate(st.session_state.chat_history):
                with st.expander(f"Q{i+1}: {q[:50]}..."):
                    st.write(f"**Question:** {q}")
                    st.write(f"**Answer:** {a}")
    
    else:
        st.info("👆 Please process your PDF documents first using the sidebar")

def process_documents(data_folder):
    """Process documents and create vector store"""
    try:
        # Initialize components
        processor = DocumentProcessor()
        vector_manager = VectorStoreManager()
        
        # Process documents
        documents = processor.process_documents(data_folder)
        
        if documents:
            # Add to vector store
            vector_manager.add_documents(documents)
            
            # Store in session state
            st.session_state.vector_store_ready = True
            st.session_state.doc_count = len(documents)
            st.session_state.vector_manager = vector_manager
            
            st.success("🎉 Documents processed successfully!")
        else:
            st.error("❌ No documents were processed")
            
    except Exception as e:
        st.error(f"❌ Error processing documents: {str(e)}")

def ask_question(question):
    """Process question and return answer"""
    try:
        # Get vector manager from session state
        vector_manager = st.session_state.vector_manager
        
        # Create RAG chain
        retriever = vector_manager.get_retriever()
        rag_chain = RAGChain(retriever)
        
        # Get answer
        result = rag_chain.ask_question(question)
        
        # Store in chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.append((question, result["answer"]))
        
        return result
        
    except Exception as e:
        st.error(f"❌ Error asking question: {str(e)}")
        return {"answer": "Error processing question", "source_documents": []}

def display_answer(answer_data):
    """Display the answer and sources"""
    st.header("💡 Answer")
    st.write(answer_data["answer"])
    
    # Display sources
    if answer_data["source_documents"]:
        st.header("📖 Sources")
        for i, doc in enumerate(answer_data["source_documents"]):
            with st.expander(f"Source {i+1}: {doc.metadata.get('source', 'Unknown')}"):
                st.write(doc.page_content)
                st.json(doc.metadata)

# Sidebar additional features
def sidebar_features():
    """Additional sidebar features"""
    st.sidebar.markdown("---")
    st.sidebar.header("🛠️ Advanced Options")
    
    # Clear vector store
    if st.sidebar.button("🗑️ Clear Vector Store"):
        if "vector_manager" in st.session_state:
            st.session_state.vector_manager.delete_index()
            del st.session_state.vector_store_ready
            del st.session_state.vector_manager
            st.sidebar.success("Vector store cleared!")
    
    # Clear chat history
    if st.sidebar.button("🧹 Clear Chat History"):
        if "chat_history" in st.session_state:
            del st.session_state.chat_history
            st.sidebar.success("Chat history cleared!")

if __name__ == "__main__":
    main()
    sidebar_features()