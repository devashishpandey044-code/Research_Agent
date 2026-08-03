from rag import get_rag_chain

rag = get_rag_chain()

print(rag.invoke("What is this paper about?"))