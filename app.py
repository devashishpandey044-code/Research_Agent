import streamlit as st
from pathlib import Path

from config import llm
from guardrails import check_user_input, check_final_answer


from agent import agent
from rag import build_vector_database, clear_database
from utils import save_uploaded_files


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ResearchMate",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{
    background:linear-gradient(
        135deg,
        #020617 0%,
        #0f172a 40%,
        #1e293b 100%
    );
}

/* Hide Streamlit Header */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:#0f172a;
    border-right:1px solid #334155;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* Title */

.main-title{

    font-size:64px;

    font-weight:700;

    color:white;

    text-align:center;

    margin-top:10px;

    margin-bottom:5px;
}

.subtitle{

    font-size:22px;

    color:#CBD5E1;

    text-align:center;

    margin-bottom:30px;
}

/* Cards */

.metric-card{

    background:rgba(255,255,255,.05);

    border:1px solid rgba(255,255,255,.08);

    padding:20px;

    border-radius:18px;

    text-align:center;

    backdrop-filter:blur(15px);

    box-shadow:0 10px 25px rgba(0,0,0,.25);

    margin-bottom:15px;
}

/* Chat */

[data-testid="stChatMessage"]{

    border-radius:18px;

    padding:18px;

    margin-bottom:18px;

    border:1px solid rgba(255,255,255,.08);

    background:rgba(255,255,255,.05);

    backdrop-filter:blur(10px);

}

/* Assistant */

[data-testid="stChatMessage"]:nth-child(even){

    background:#111827;

    border-left:5px solid #22c55e;

}

/* User */

[data-testid="stChatMessage"]:nth-child(odd){

    background:#172554;

    border-left:5px solid #3b82f6;

}

/* Make assistant response bright */

[data-testid="stMarkdownContainer"]{

    color:white !important;

    font-size:17px;

    line-height:1.8;

}

/* Chat Input */

[data-testid="stChatInput"]{

    border-radius:18px;

}

/* Buttons */

.stButton>button{

    width:100%;

    border-radius:12px;

    height:48px;

    font-size:16px;

    font-weight:600;

    border:none;

    background:linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );

    color:white;

    transition:.3s;
}

.stButton>button:hover{

    transform:scale(1.02);

    background:linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb
    );

}

/* Uploaded file */

[data-testid="stFileUploader"]{

    background:#1e293b;

    border-radius:12px;

    padding:10px;

}

/* Success */

.stSuccess{

    border-radius:12px;

}

/* Warning */

.stWarning{

    border-radius:12px;

}

/* Error */

.stError{

    border-radius:12px;

}

/* Scrollbar */

::-webkit-scrollbar{

    width:10px;
}

::-webkit-scrollbar-thumb{

    background:#475569;

    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🔬 ResearchMate")

    st.caption("AI Powered Research Assistant")

    st.markdown("---")

    # ==========================================
    # Upload Section
    # ==========================================

    st.subheader("📂 Upload Research Papers")

    uploaded_files = st.file_uploader(
        "Choose one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload your research papers to build a searchable knowledge base."
    )

    if st.button("🚀 Build Knowledge Base"):

        if uploaded_files:

            with st.spinner("📚 Reading PDFs and creating vector database..."):

                try:

                    save_uploaded_files(uploaded_files)

                    build_vector_database()

                    st.success("✅ Knowledge Base Created Successfully!")

                except Exception as e:

                    st.error(str(e))

        else:

            st.warning("Please upload at least one PDF.")

    st.markdown("---")

    # ==========================================
    # Uploaded Files
    # ==========================================

    st.subheader("📄 Uploaded Papers")

    pdfs = sorted(list(UPLOAD_FOLDER.glob("*.pdf")))

    if pdfs:

        st.success(f"📚 {len(pdfs)} Research Paper(s) Loaded")

        for pdf in pdfs:

            size = pdf.stat().st_size / (1024 * 1024)

            st.markdown(
                f"""
✅ **{pdf.name}**

<small style="color:#94a3b8;">
{size:.2f} MB
</small>
""",
                unsafe_allow_html=True,
            )

    else:

        st.info("No papers uploaded.")

    st.markdown("---")

    # ==========================================
    # Database Controls
    # ==========================================

    st.subheader("⚙️ Controls")

    if st.button("🗑 Clear Knowledge Base"):

        clear_database()

        st.success("Database Cleared Successfully!")

        st.rerun()

    if st.button("💬 Clear Chat History"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    # ==========================================
    # Project Info
    # ==========================================

    st.subheader("📊 Project Status")

    st.markdown(
        f"""
🧠 **LLM:** Groq Llama 3.1 8B

📚 **Embedding:** BAAI bge-small

📄 **Uploaded PDFs:** {len(pdfs)}

💬 **Chat Messages:** {len(st.session_state.messages)}
"""
    )

    st.markdown("---")

    st.caption("🚀 Built with LangChain • ChromaDB • Streamlit • Groq")
    # =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-title">
🔬 ResearchMate
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Chat with Research Papers using LangChain, ChromaDB & Groq
</div>
""", unsafe_allow_html=True)


# =====================================================
# DASHBOARD CARDS
# =====================================================

pdfs = list(UPLOAD_FOLDER.glob("*.pdf"))

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(f"""
    <div class="metric-card">
        <h2>📄 {len(pdfs)}</h2>
        <p>Uploaded Papers</p>
    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">
        <h2>💬 {len(st.session_state.messages)}</h2>
        <p>Chat Messages</p>
    </div>
    """, unsafe_allow_html=True)

with c3:

    status = "Ready" if len(pdfs) else "Waiting"

    st.markdown(f"""
    <div class="metric-card">
        <h2>🟢 {status}</h2>
        <p>Knowledge Base</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# WELCOME MESSAGE
# =====================================================

if len(st.session_state.messages) == 0:

    st.info("""
# 👋 Welcome to ResearchMate

ResearchMate is an AI-powered assistant for understanding research papers.

### You can:

📄 Upload one or multiple PDFs

🧠 Ask questions about uploaded papers

📝 Generate summaries

📚 Explain difficult concepts

🔍 Search research papers

🌐 Search the web

📖 Search Wikipedia

---

### Try questions like:

• Summarize this paper.

• What is the methodology?

• Explain the Transformer architecture.

• What dataset was used?

• What are the conclusions?

""")



# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "assistant":

            st.markdown(
                f"""
<div style="
background:#111827;
padding:20px;
border-radius:18px;
border:1px solid #334155;
box-shadow:0 6px 18px rgba(0,0,0,.35);
">

### 🤖 ResearchMate

{message["content"]}

</div>
""",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
<div style="
background:#1D4ED8;
padding:18px;
border-radius:18px;
color:white;
margin-left:80px;
">

### 👤 You

{message["content"]}

</div>
""",
                unsafe_allow_html=True
            )


# =====================================================
# CHAT INPUT
# =====================================================

question = st.chat_input(
    "💬 Ask anything about your uploaded research papers..."
)
# =====================================================
# AGENT
# =====================================================

if question:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        with st.spinner("🧠 Reading research papers and thinking..."):

            try:

                response = agent.invoke(
                    {
                        "messages": st.session_state.messages
                    }
                )

                messages = response["messages"]

                last_message = messages[-1]

                # -----------------------------
                # Extract response safely
                # -----------------------------

                if isinstance(last_message.content, str):

                    answer = last_message.content

                elif isinstance(last_message.content, list):

                    answer = ""

                    for item in last_message.content:

                        if isinstance(item, dict):

                            answer += item.get("text", "")

                        elif hasattr(item, "text"):

                            answer += item.text

                        else:

                            answer += str(item)

                else:

                    answer = str(last_message.content)

            except Exception as e:

                answer = f"""
❌ **Error**

{str(e)}
"""

            response_placeholder.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =====================================================
# FOOTER
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🤖 LLM", "Groq")

with col2:
    st.metric("🧠 Framework", "LangChain")

with col3:
    st.metric("📚 Vector DB", "ChromaDB")

with col4:
    st.metric("📄 PDFs", len(list(UPLOAD_FOLDER.glob("*.pdf"))))

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
"""
<div style="
text-align:center;
color:#94A3B8;
font-size:15px;
padding-bottom:25px;
">

🔬 <b>ResearchMate</b><br>

Powered by LangChain • Groq • HuggingFace • ChromaDB

</div>
""",
unsafe_allow_html=True
)

