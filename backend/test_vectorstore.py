from app.rag.vectorstore.vector_store import VectorStore

vs = VectorStore()

print("Total:", vs.collection.count())

result = vs.collection.get(
    limit=5,
    include=["metadatas"]
)

print(result["metadatas"])