from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store import VectorStore


class RetrievalService:

    def __init__(self):

        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ):

        # Generate query embedding
        query_embedding = self.embedder.embed_text(question)

        # Search vector database
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        print("\nRetrieved Chunks\n")

        if not results:
            print("No chunks found.")
            return []

        output = []

        for item in results:

            output.append(
                {
                    "text": item["text"],
                    "document": item["metadata"].get("document", "Unknown"),
                    "chunk": item["metadata"].get("chunk", -1),
                    "distance": float(item["distance"]),
                }
            )

        for item in output:

            print("=" * 80)
            print(f'Document : {item["document"]}')
            print(f'Chunk    : {item["chunk"]}')
            print(f'Distance : {item["distance"]:.4f}')
            print("-" * 80)
            print(item["text"])

        return output