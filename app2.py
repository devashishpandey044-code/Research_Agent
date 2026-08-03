import streamlit as st
from pathlib import Path

from agent import agent
from rag import build_vector_database, clear_database
from utils import save_uploaded_files


# ================= PAGE CONFIG ================= #

st.set_page_config(
    page_title="ResearchGPT",
    page_icon="🔬",
    layout="wide"
)


# ================= CSS ================= #

st.markdown("""
<style>

.stApp{
    background:linear-gradient(135deg,#0f172a,#1e293b);
}

.main-title{
    text-align:center;
    font-size:52px;
    color:white;
    font-weight:bold;
}

.sub-title{
    text-align:center;
    color:#CBD5E1;
    margin-bottom:25px;
}

[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)


UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"


# ================= SIDEBAR ================= #

with st.sidebar:

    st.title("🔬 ResearchGPT")

    st.markdown("---")

    st.subheader("📂 Upload Research Papers")

    uploaded_files = st.file_uploader(
        "Choose PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("📥 Process PDFs"):

        if uploaded_files:

            with st.spinner("Building Vector Database..."):

                save_uploaded_files(uploaded_files)

                try:

                    build_vector_database()

                    st.success("✅ PDFs processed successfully!")

                except Exception as e:

                    st.error(f"❌ {e}")

        else:

            st.warning("Please upload at least one PDF.")

    st.markdown("---")

    st.subheader("📄 Uploaded Papers")

    pdfs = list(UPLOAD_FOLDER.glob("*.pdf"))

    if pdfs:

        for pdf in pdfs:

            st.write(f"✅ {pdf.name}")

    else:

        st.info("No PDFs uploaded.")

    st.markdown("---")

    if st.button("🗑 Clear Database"):

        clear_database()

        st.success("Database Cleared!")

        st.rerun()

    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ================= HEADER ================= #

st.markdown(
    "<h1 class='main-title'>🔬 ResearchGPT</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>AI Research Assistant powered by LangChain + Groq</p>",
    unsafe_allow_html=True
)


# ================= CHAT HISTORY ================= #

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ================= CHAT INPUT ================= #

question = st.chat_input(
    "Ask about AI, ML, Research Papers..."
)


# ================= AGENT ================= #

if question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        with st.spinner("Researching..."):

            try:

                response = agent.invoke(
                    {
                        "messages": st.session_state.messages
                    }
                )

                messages = response["messages"]

                last_message = messages[-1]

                # -----------------------------
                # Extract final text safely
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

                answer = f"❌ Error:\n\n{e}"

            placeholder.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )