from rag import get_vector_database

db = get_vector_database()

print("Documents:", db._collection.count())

retriever = db.as_retriever(search_kwargs={"k": 4})

docs = retriever.invoke("deep residual learning")

print("Retrieved:", len(docs))

for doc in docs:
    print("=" * 80)
    print(doc.page_content[:500])