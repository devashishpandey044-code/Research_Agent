import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
guardrail_llm = llm

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
