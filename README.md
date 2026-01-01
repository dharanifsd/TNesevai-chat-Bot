# 🏛️ TN eSevai RAG Chatbot
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

A conversational AI chatbot that answers questions about **Tamil Nadu Government Services** using Retrieval-Augmented Generation (RAG).  
The bot understands your questions, retrieves relevant answers from an official PDF, and responds intelligently using a locally running LLM.

---

## ✨ Features
- 🔍 Ask natural language questions about TN Govt services  
- 📄 Reads & understands PDF content  
- 🧠 RAG-based intelligent answering  
- 🚀 Fast semantic search using Qdrant  
- 🤖 Local inference using Ollama (no external API required)  
- ⚡ Real-time streaming responses  
- ☁️ Persistent storage via Qdrant Cloud  

---

## 🛠️ Tech Stack
| Component | Purpose |
|--------|--------|
| **Streamlit** | Web Chat UI |
| **LangChain** | RAG pipeline + document handling |
| **Qdrant Cloud** | Vector Database |
| **Ollama** | Local LLM engine |
| **Qwen Model** | Answer generation |
| **Nomic Embed Text** | Text embeddings |

---

## 🧠 Flow

A[PDF Document] --> B[Text Splitter]
B --> C[Embedding Model]
C --> D[Qdrant Vector DB]

E[User Question] --> F[Embedding Model]
F --> G[Vector Similarity Search]
G --> H[Relevant Chunks]

H --> I[Qwen LLM via Ollama]
E --> I
I --> J[Final Answer]

---
📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/YOUR-USERNAME/tn-esavai-chatbot.git

2️⃣ Install Python Dependencies
pip install streamlit langchain langchain-community langchain-text-splitters langchain-qdrant qdrant-client litellm pypdf

3️⃣ Setup Ollama + Models
Install Ollama:
👉 https://ollama.ai

Pull Chat Model:---> ollama pull qwen:0.6b

Pull Embedding Model:---> ollama pull nomic-embed-text
Ensure Ollama is running:---> ollama serve

4️⃣ Setup Qdrant Cloud
Create a cluster:
👉 https://cloud.qdrant.io

Add:

QDRANT_URL

QDRANT_API_KEY

Example URL format:

https://xxxx-xxxx-xxxx.gcp.cloud.qdrant.io


5️⃣ Set Your PDF
Set your PDF path in code:
pdf_file = "data/tnesevai.pdf"

▶️ Run the App
streamlit run stream.py
Open:
👉 http://localhost:8501

---
✅ Expected Startup Log
Initializing RAG system...
Loaded 66 documents
Split into 134 chunks
Connected to Qdrant
Chatbot Ready

---
🚀 Future Enhancements
📎 Show source text + page number

📚 Multi-PDF support

🌐 Multi-language support

🤖 Upgrade to Qwen 7B for better reasoning

🧪 Confidence scoring

---

❤️ Credits
Built with:

LangChain

Qdrant

Ollama

Streamlit

---
⭐ Support
If you like this project, please ⭐ star the repo!