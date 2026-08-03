from rag import get_rag_chain

chain = get_rag_chain()

response = chain.invoke(
    "What is GRadient boosting?"
)

print(response)