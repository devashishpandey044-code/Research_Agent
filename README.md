# 🔬 ResearchGPT

An AI-powered Research Assistant built with **LangChain**, **LangGraph**, **Groq LLM**, **ChromaDB**, and **Streamlit**.

ResearchGPT allows users to upload research papers in PDF format and ask questions in natural language. The assistant retrieves relevant information using Retrieval-Augmented Generation (RAG) and provides accurate, context-aware answers.

---

## 🚀 Features

- 📄 Upload one or multiple research papers (PDF)
- 🔍 Semantic search using Chroma Vector Database
- 🤖 AI-powered question answering using Groq LLM
- 📝 Summarize research papers
- 📚 Explain concepts from uploaded papers
- 🔎 Search latest papers from arXiv
- 🌐 Web search using DuckDuckGo
- 📖 Wikipedia integration
- 💬 Beautiful Streamlit chat interface
- ⚡ Fast retrieval using HuggingFace Embeddings

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- ChromaDB
- HuggingFace Embeddings
- Groq LLM
- PyPDF Loader
- DuckDuckGo Search
- Wikipedia API
- arXiv API

---

## ⚙️ Project Workflow

1. Upload one or more PDF research papers.
2. PDFs are split into chunks.
3. Chunks are converted into vector embeddings.
4. Embeddings are stored in ChromaDB.
5. User asks a question.
6. Relevant chunks are retrieved.
7. Groq LLM generates the final answer using retrieved context.

---

## 📂 Project Structure

```
ResearchGPT/
│
├── app.py
├── agent.py
├── config.py
├── rag.py
├── prompts.py
├── tools.py
├── utils.py
├── uploads/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ResearchGPT.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
```

Run the application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

Add screenshots of:

- Home Page
- Upload PDF
- Asking Questions
- Paper Summary
- RAG Workflow (optional)

---

## 📈 Future Improvements

- Multi-user authentication
- Chat history persistence
- Citation generation
- PDF highlighting
- Research paper comparison
- Export chat as PDF
- Voice interaction
- Dark/Light mode

---

## 👨‍💻 Author

**Devashish Pandey**

B.Tech (ECE) Student

Interested in:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Generative AI
- Retrieval-Augmented Generation (RAG)

LinkedIn: *(Add your LinkedIn URL here)*

GitHub: *(Add your GitHub URL here)*

---

## ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub.