from app.rag.retrieval.retrieval_service import RetrievalService

retriever = RetrievalService()

results = retriever.retrieve(
    "What is Artificial Intelligence?"
)

print(results)