from app.rag.embeddings.embedding_service import EmbeddingService

embedding_service = EmbeddingService()

text = """
The Smart Pharmacy Predictive Analytics System predicts medicine demand.
"""

vector = embedding_service.embed_text(text)

print("Embedding Dimension :", len(vector))
print()
print(vector[:20])