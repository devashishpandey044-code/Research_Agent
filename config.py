import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
)
guardrail_llm = llm

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
