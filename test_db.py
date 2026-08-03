from rag import build_vector_database

db = build_vector_database()

print(db._collection.count())