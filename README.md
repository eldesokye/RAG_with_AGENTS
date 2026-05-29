# 🤖 Multi-Agent RAG System

An advanced AI-powered **Retrieval-Augmented Generation (RAG)** platform built with **FastAPI**, **Streamlit**, **LangChain**, and autonomous **AI Agents**.

This system allows users to:

* Upload PDF documents
* Ask context-aware questions
* Run autonomous research workflows
* Use specialized AI agents
* Retrieve information from vector databases
* Interact through a modern chat interface

---

# 🚀 Features

## 📄 PDF Processing

* Upload multiple PDFs
* Automatic text extraction
* Smart chunking pipeline
* Persistent vector storage

---

## 🧠 RAG Pipeline

* Semantic document retrieval
* Context-aware question answering
* Vector similarity search
* ChromaDB integration

---

## 🤖 Multi-Agent System

### 📚 RAG Assistant

Answers questions using uploaded documents.

### 🔍 Research Agent

Autonomous ReAct-style AI agent capable of:

* reasoning
* planning
* research
* tool usage
* report generation

### 🛠 Support Agent

Customer support assistant with memory capabilities.

---

## ⚡ FastAPI Backend

* RESTful API
* Async-ready architecture
* Error handling middleware
* Modular services

---

## 🎨 Streamlit Frontend

* Interactive chat UI
* Multi-agent mode selection
* Chat history
* Source visualization

---

# 🏗️ System Architecture

```text
                ┌────────────────────┐
                │   Streamlit UI     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │    FastAPI API     │
                └─────────┬──────────┘
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
┌──────────────┐  ┌────────────────┐  ┌────────────────┐
│ RAG Pipeline │  │ Research Agent │  │ Support Agent  │
└──────┬───────┘  └────────┬───────┘  └────────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────┐
│               Vector Database (Chroma)             │
└─────────────────────────────────────────────────────┘
```

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn

## Frontend

* Streamlit

## AI / LLM

* LangChain
* Groq API
* OpenAI-compatible APIs

## Vector Database

* ChromaDB

## Embeddings

* HuggingFace Embeddings
* all-MiniLM-L12-v2

## Utilities

* PyPDF
* Logging
* dotenv

---

# 📂 Project Structure

```text
multi-agent-rag/
│
├── client/
│   ├── components/
│   │   └── chatUI.py
│   │
│   ├── utils/
│   │   └── api.py
│   │
│   ├── config.py
│   └── app.py
│
├── server/
│   ├── Action/
│   │   └── ReAct_engine.py
│   │
│   ├── modules/
│   │   ├── load_vectorstore.py
│   │   ├── llm.py
│   │   └── query_handlers.py
│   │
│   ├── output/
│   │   ├── Active_research_agent.py
│   │   └── costs_failures.py
│   │
│   ├── logger.py
│   └── main.py
│
├── chroma_db/
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/multi-agent-rag.git

cd multi-agent-rag
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_google_api_key

LANGCHAIN_API_KEY=your_langchain_api_key

LANGCHAIN_TRACING_V2=true

LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

---

# ▶️ Running the Project

## Start Backend

```bash
cd server

uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## Start Frontend

```bash
cd client

streamlit run app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📡 API Endpoints

| Endpoint        | Method | Description          |
| --------------- | ------ | -------------------- |
| `/upload_pdfs/` | POST   | Upload PDF documents |
| `/ask/`         | POST   | Ask RAG questions    |
| `/search/`      | GET    | Research agent       |
| `/support/`     | GET    | Support agent        |

---

# 🧠 AI Workflow

```text
User Query
    │
    ▼
AI Router
    │
 ┌──┴──────────────┐
 │                 │
RAG Mode      Agent Mode
 │                 │
 ▼                 ▼
Vector DB      ReAct Agent
 │                 │
 ▼                 ▼
LLM Response   Tool Usage
```

---

# 📸 UI Preview

Add screenshots later:

```text
/docs/chat-ui.png
/docs/research-agent.png
/docs/upload-page.png
```

---

# 🧪 Future Improvements

* Multi-agent orchestration
* Memory persistence
* Redis caching
* Docker deployment
* Kubernetes support
* Authentication system
* Streaming responses
* Observability dashboard
* Hybrid search
* Agent routing system

---

# 📈 Use Cases

* Enterprise document assistant
* AI research assistant
* Customer support automation
* Knowledge base chatbot
* Internal search engine
* Educational AI assistant

---

# 🤝 Contributing

Contributions are welcome.

## Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Commit Changes

```bash
git commit -m "Add new feature"
```

## Push Branch

```bash
git push origin feature/your-feature-name
```

## Open Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Hisham Yahya Eldesoky

AI Engineer | AI Agents | Computer Vision | RAG Systems

* AI Agents
* NLP
* RAG Architectures
* AI SaaS Systems
* Computer Vision

---

# ⭐ Support

If you found this project useful:

* Star the repository
* Fork the project
* Share it with others

---

# 📬 Contact

GitHub: [https://github.com/yourusername](https://github.com/eldesokye)

LinkedIn: [https://linkedin.com/in/yourprofile]((https://www.linkedin.com/in/hisham-el-desoky-440586263/))

Email: [your-email@example.com](mailto:hishameldesoky111@gmail.com)
