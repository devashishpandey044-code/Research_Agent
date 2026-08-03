from pathlib import Path
import shutil

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import llm, embeddings


# ================= PATHS ================= #

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
CHROMA_PATH = BASE_DIR / "chroma_db"

UPLOAD_FOLDER.mkdir(exist_ok=True)

print("=" * 60)
print("BASE_DIR :", BASE_DIR)
print("UPLOAD_FOLDER :", UPLOAD_FOLDER)
print("CHROMA_PATH :", CHROMA_PATH)
print("=" * 60)


# ================= BUILD VECTOR DATABASE ================= #

def build_vector_database():

    pdf_files = list(UPLOAD_FOLDER.glob("*.pdf"))

    if len(pdf_files) == 0:
        print("No PDF files found.")
        return None

    print(f"\nFound {len(pdf_files)} PDF(s).\n")

    # Create directory if it doesn't exist
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    # Delete old database
    if CHROMA_PATH.exists():
        try:
            shutil.rmtree(CHROMA_PATH)
            print("Old Chroma database deleted.")
        except Exception as e:
            print("Could not delete old database:", e)

    documents = []

    for pdf in pdf_files:

        print(f"Loading: {pdf.name}")

        loader = PyPDFLoader(str(pdf))

        docs = loader.load()

        print(f"Pages Loaded: {len(docs)}")

        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Total Chunks: {len(chunks)}")

    print("\nCreating Chroma database...")
    print("Database Location:", CHROMA_PATH)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    print("\nVector Database Created Successfully!")

    print("Folder Exists:", CHROMA_PATH.exists())

    if CHROMA_PATH.exists():
        print("\nFiles Created:")

        for file in CHROMA_PATH.rglob("*"):
            print(file)

    print("\nTotal Documents Stored:",
          vectorstore._collection.count())

    return vectorstore


# ================= LOAD DATABASE ================= #

def get_vector_database():

    print("Opening Database From:")
    print(CHROMA_PATH)

    return Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )


# ================= RETRIEVER ================= #

def get_retriever():

    db = get_vector_database()

    print("Documents in DB:", db._collection.count())

    return db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )


# ================= FORMAT DOCUMENTS ================= #

def format_docs(docs):

    return "\n\n".join(doc.page_content for doc in docs)


# ================= PROMPT ================= #

def get_prompt():

    return ChatPromptTemplate.from_template(
        """
You are ResearchGPT.

Answer ONLY using the provided research paper context.

If the answer cannot be found in the context, reply exactly:

I couldn't find this information in the uploaded research papers.

Context:
{context}

Question:
{question}

Answer:
"""
    )


# ================= RAG CHAIN ================= #

def get_rag_chain():

    retriever = get_retriever()

    prompt = get_prompt()

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ================= CLEAR DATABASE ================= #

def clear_database():

    if CHROMA_PATH.exists():

        try:
            shutil.rmtree(CHROMA_PATH)
            print("Database Deleted.")
        except Exception as e:
            print(e)

    for pdf in UPLOAD_FOLDER.glob("*.pdf"):
        pdf.unlink()

    print("Uploads Deleted.")