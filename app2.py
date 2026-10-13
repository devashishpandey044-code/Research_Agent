import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env variables
load_dotenv()

# Load secrets configured in Streamlit Cloud
try:
    for key in (
        "GROQ_API_KEY",
        "LANGSMITH_TRACING",
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
    ):
        if key in st.secrets:
            os.environ[key] = str(st.secrets[key])
except Exception:
    # Local development may not have Streamlit secrets configured
    pass

# Import your existing modules only after configuration
from config import llm
from agent import agent  # Adapt to your existing agent variable/import

import streamlit as st
from pathlib import Path

from config import llm
from guardrails import check_user_input, check_final_answer


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



# =====================================================
# AGENT WITH LLM-BASED GUARDRAILS
# =====================================================

if question:

    # Store and display the user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        with st.spinner("🛡️ Checking query and researching..."):

            try:
                # -------------------------------------
                # 1. INPUT GUARDRAIL
                # -------------------------------------

                input_decision = check_user_input(
                    guardrail_llm=llm,
                    question=question,
                )

                if not input_decision.allowed:

                    answer = (
                        "🛡️ **Request blocked by ResearchMate**\n\n"
                        f"{input_decision.reason}"
                    )

                else:
                    # ---------------------------------
                    # 2. RUN YOUR EXISTING AGENT
                    # ---------------------------------

                    response = agent.invoke({
                        "messages": st.session_state.messages
                    })

                    messages = response["messages"]
                    last_message = messages[-1]

                    # Extract the final answer using your
                    # existing response-handling approach.
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

                    # ---------------------------------
                    # 3. COLLECT ACTUAL TOOL EVIDENCE
                    # ---------------------------------

                    evidence_parts = []

                    for message in messages:
                        if getattr(message, "type", None) == "tool":
                            content = message.content

                            if isinstance(content, str):
                                evidence_parts.append(content)

                            elif isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict):
                                        evidence_parts.append(
                                            item.get("text", str(item))
                                        )
                                    else:
                                        evidence_parts.append(str(item))

                            else:
                                evidence_parts.append(str(content))

                    evidence = "\n\n".join(evidence_parts)

                    # ---------------------------------
                    # 4. OUTPUT GUARDRAIL
                    # ---------------------------------

                    output_decision = check_final_answer(
                        guardrail_llm=llm,
                        question=question,
                        evidence=evidence,
                        answer=answer,
                    )

                    if not output_decision.safe:
                        answer = (
                            "🛡️ **Answer blocked by ResearchMate**\n\n"
                            "The answer did not pass the security check."
                        )

                    elif not output_decision.grounded:
                        answer = (
                            "⚠️ **Answer could not be verified**\n\n"
                            "The generated answer could not be adequately "
                            "supported by the retrieved research evidence. "
                            "Please try a more specific question or review "
                            "the original sources."
                        )

            except Exception:
                # Avoid displaying internal errors or credentials.
                answer = (
                    "The request could not be completed safely. "
                    "Please try again."
                )

        response_placeholder.markdown(answer)

    # Store the final displayed response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

