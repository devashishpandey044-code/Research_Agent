import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


llm = ChatGroq(
    model="minimaxai/minimax-m2.7",
    temperature=0,
    max_tokens=500   
)
guardrail_llm = llm

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
