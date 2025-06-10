# DocuMind AI 🧠📚

### *Transform Your PDFs into Conversational Knowledge*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green.svg)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.84.0-orange.svg)](https://openai.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-v6.0.0-purple.svg)](https://pinecone.io)

---

## 🚀 Overview

**DocuMind AI** is an intelligent PDF question-answering system that leverages **Retrieval-Augmented Generation (RAG)** to help users extract insights from PDF documents through natural language conversations. It transforms static documents into an interactive knowledge base with real-time document processing and intelligent responses.

### ✨ Key Features

- 📄 **Dynamic PDF Upload**: Real-time PDF processing with drag-and-drop interface
- 🧠 **Semantic Search**: Vector-based similarity search using OpenAI embeddings and Pinecone
- 🤖 **AI-Powered Q&A**: Natural language responses powered by GPT-3.5-Turbo
- 📊 **Source Attribution**: Transparent citations showing which document sections informed each answer
- 💬 **Interactive Interface**: Modern Streamlit web interface with real-time status monitoring
- 🔄 **Modular Architecture**: Clean, maintainable code structure for easy customization
- 📈 **Index Management**: Real-time vector count display and index clearing capabilities

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | LangChain | AI application orchestration |
| **LLM** | OpenAI GPT-3.5-Turbo | Natural language generation |
| **Vector DB** | Pinecone v6.0.0 | Scalable serverless similarity search |
| **Embeddings** | OpenAI text-embedding-ada-002 | Text vectorization |
| **Frontend** | Streamlit | Interactive web interface |
| **Document Processing** | PyPDF2 | PDF text extraction |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- Pinecone account and API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashok49473/DocuMind-AI.git
   cd DocuMind-AI
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
   PINECONE_INDEX_NAME=documind-ai
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   ```
   Navigate to: http://localhost:8501
   ```

---

## 📋 Usage Guide

### Step 1: Upload PDF Document
1. Open the Streamlit interface
2. Use the sidebar file uploader to select a PDF
3. Click **"Process PDF"** to analyze the document
4. Wait for processing confirmation

### Step 2: Ask Questions
1. Enter your question in the main interface text input
2. Click **"Ask Question"**
3. Review the AI-generated response with source citations
4. Expand **"Source Documents"** to see referenced text sections

### Step 3: Manage Your Knowledge Base
- Monitor system status in the right panel
- View real-time vector count statistics
- Clear the vector store to reset the system
- Process new documents to update the knowledge base

---

## 📁 Project Structure

```
DocuMind-AI/
|──src/
   |
   ├── 📄 app.py                    # Main Streamlit application
   ├── 📄 config.py                 # Configuration management
   ├── 📄 pdf_processor.py          # PDF processing and chunking
   ├── 📄 vector_store.py           # Pinecone v6.0.0 integration
   ├── 📄 qa_chain.py               # RAG implementation
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example             # Environment variables template
└── 📄 README.md                # This documentation
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-3.5-Turbo and embeddings | ✅ |
| `PINECONE_API_KEY` | Pinecone API key for vector storage | ✅ |
| `PINECONE_INDEX_NAME` | Name for your Pinecone index | ❌ (default: documind-ai) |

### Customizable Parameters

```python
# In config.py
CHUNK_SIZE = 1000              # Document chunk size
CHUNK_OVERLAP = 200            # Overlap between chunks
LLM_MODEL = "gpt-3.5-turbo"    # OpenAI model
EMBEDDING_MODEL = "text-embedding-ada-002"  # Embedding model
PINECONE_DIMENSION = 1536      # Embedding dimension
PINECONE_METRIC = "cosine"     # Similarity metric
PINECONE_CLOUD = "aws"         # Cloud provider
PINECONE_REGION = "us-east-1"  # Region
```

---

## 🔧 Modular Architecture

### Core Components

#### **PDFProcessor**
- Extracts text from uploaded PDF files
- Splits text into manageable chunks with overlap
- Creates LangChain Document objects with metadata

#### **VectorStoreManager**
- Manages Pinecone serverless index operations
- Handles document embedding and storage
- Performs similarity searches with configurable parameters
- Provides index statistics and management

#### **QAChain**
- Implements retrieval-augmented generation
- Uses custom prompts for context-aware responses
- Returns answers with source document attribution
- Handles error cases gracefully

#### **Config**
- Centralized configuration management
- Environment variable validation

---
![documind](https://github.com/user-attachments/assets/ba061e38-d056-46fa-9001-26c402e5f401)

## 🔍 How It Works

1. **Document Ingestion**: PDF text is extracted and split into semantic chunks
2. **Embedding Generation**: OpenAI creates vector representations of text chunks
3. **Vector Storage**: Embeddings are stored in Pinecone serverless index
4. **Query Processing**: User questions are embedded and matched against stored vectors
5. **Context Retrieval**: Most relevant document chunks are retrieved
6. **Answer Generation**: GPT-3.5-Turbo generates responses using retrieved context
7. **Source Attribution**: Original document sections are provided for transparency

---


### Considerations
- Requires OpenAI and Pinecone API credits
- Processing time depends on document size
- Accuracy depends on document quality and structure
- Best results with well-structured, text-based PDFs


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain** team for the incredible RAG framework
- **OpenAI** for powerful language models and embeddings
- **Pinecone** for scalable serverless vector search
- **Streamlit** for the intuitive web framework
- **PyPDF2** for reliable PDF processing

---

## 📞 Contact

**Ashok Kumar** - [ashokpalivela123@gmail.com](mailto:ashokpalivela123@gmail.com)

**Project Link**: [https://github.com/ashok49473/DocuMind-AI](https://github.com/ashok49473/DocuMind-AI)

**Portfolio**: [https://ashok49473.github.io](https://ashok49473.github.io)

---

## 🚀 Future Enhancements

- [ ] Multi-document conversation support
- [ ] Advanced filtering and search options
- [ ] Integration with cloud storage services
- [ ] Batch document processing
- [ ] Custom embedding model support

---

<div align="center">

### ⭐ Star this project if you found it helpful!

**Built with ❤️ using LangChain, OpenAI, and Pinecone**

</div>
