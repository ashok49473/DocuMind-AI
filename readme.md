# DocuMind AI 🧠📚

### *Transform Your PDFs into Conversational Knowledge*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green.svg)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple.svg)](https://pinecone.io)

---

## 🚀 Overview

**DocuMind AI** is an intelligent document question-answering system that leverages **Retrieval-Augmented Generation (RAG)** to help users extract insights from PDF documents through natural language conversations. Built with cutting-edge AI technologies, it transforms static documents into an interactive knowledge base.

### ✨ Key Features

- 📄 **PDF Processing**: Automatic text extraction and intelligent chunking
- 🧠 **Semantic Search**: Vector-based similarity search using OpenAI embeddings
- 🤖 **AI-Powered Q&A**: Natural language responses powered by GPT-4
- 📊 **Source Attribution**: Transparent citations showing which documents informed each answer
- 💬 **Chat Interface**: Intuitive Streamlit web interface with conversation history
- 🔄 **Real-time Processing**: Dynamic document ingestion and querying

---


## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | LangChain | AI application orchestration |
| **LLM** | OpenAI GPT-4 | Natural language generation |
| **Vector DB** | Pinecone | Scalable similarity search |
| **Embeddings** | OpenAI Ada-002 | Text vectorization |
| **Frontend** | Streamlit | Interactive web interface |
| **Document Processing** | PyPDF2 | PDF text extraction |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Pinecone account and API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/documind-ai.git
   cd documind-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your API keys to .env
   OPENAI_API_KEY=sk-your-openai-key-here
   PINECONE_API_KEY=your-pinecone-api-key
   PINECONE_ENVIRONMENT=your-pinecone-environment
   ```

4. **Add your PDF documents**
   ```bash
   mkdir data
   # Copy your PDF files to the data/ folder
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   ```
   Navigate to: http://localhost:8501
   ```

---

## 📋 Usage Guide

### Step 1: Document Processing
1. Place your PDF files in the `data/` folder
2. Open the Streamlit interface
3. Click **"🔄 Process Documents"** in the sidebar
4. Wait for processing to complete

### Step 2: Ask Questions
1. Enter your question in the main interface
2. Click **"🔍 Get Answer"**
3. Review the AI-generated response
4. Check the **Sources** section for document references

### Step 3: Explore Features
- View **Chat History** for previous conversations
- Use **Advanced Options** to manage the vector store
- Clear data or reset the system as needed

---

## 📁 Project Structure

```
documind-ai/
├── 📁 data/                    # PDF documents folder
├── 📁 src/                     # Core application modules
│   ├── 📄 __init__.py
│   ├── 📄 config.py           # Configuration management
│   ├── 📄 document_processor.py # PDF processing and chunking
│   ├── 📄 vector_store.py     # Pinecone integration
│   └── 📄 rag_chain.py        # RAG implementation
├── 📄 app.py                  # Main Streamlit application
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env.example           # Environment variables template
└── 📄 README.md              # This file
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 and embeddings | ✅ |
| `PINECONE_API_KEY` | Pinecone API key for vector storage | ✅ |
| `PINECONE_ENVIRONMENT` | Pinecone environment (e.g., us-west1-gcp) | ✅ |
| `PINECONE_INDEX_NAME` | Name for your Pinecone index | ❌ (default: pdf-rag-index) |

### Customizable Parameters

```python
# In src/config.py
CHUNK_SIZE = 1000          # Document chunk size
CHUNK_OVERLAP = 200        # Overlap between chunks
MODEL_NAME = "gpt-3.5-turbo" # OpenAI model
TEMPERATURE = 0.7          # Response creativity
TOP_K = 4                  # Number of retrieved documents
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain** team for the incredible framework
- **OpenAI** for powerful language models
- **Pinecone** for scalable vector search
- **Streamlit** for the intuitive web framework

---

## 📞 Contact

**Ashok Kumar** - [ashokpalivela123.@gmail.com](mailto:ashokpalivela123.@gmail.com)

**Project Link**: [https://github.com/ashok49473/DocuMind-AI](https://github.com/ashok49473/DocuMind-AI)

**Live Demo**: [https://documind-ai.streamlit.app](https://documind-ai.streamlit.app)

---

<div align="center">

### ⭐ Star this project if you found it helpful!

**Built with ❤️ using LangChain, OpenAI, and Streamlit**

</div>