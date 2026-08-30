import uuid
import chromadb

from app.core.config import settings


class VectorStore:

    def __init__(self):

        print("=" * 60)
        print("CHROMA PATH:", settings.CHROMA_DB_PATH)
        print("=" * 60)

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="support_docs"
        )

    def add_documents(
        self,
        chunks,
        embeddings,
        document_name,
    ):

        if not chunks:
            return

        ids = []
        metadatas = []

        for i in range(len(chunks)):
            ids.append(str(uuid.uuid4()))

            metadatas.append(
                {
                    "document": document_name,
                    "chunk": i,
                }
            )

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print("=" * 60)
        print("Stored", len(chunks), "chunks")
        print("Collection size:", self.collection.count())
        print("=" * 60)

    def search(
        self,
        query_embedding,
        top_k=5,
    ):

        if self.collection.count() == 0:
            print("WARNING: Vector store is empty")
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(
                top_k,
                self.collection.count(),
            ),
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        retrieved = []

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]

        for doc, meta, dist in zip(
            docs,
            metas,
            dists,
        ):
            retrieved.append(
                {
                    "text": doc,
                    "metadata": meta,
                    "distance": dist,
                }
            )

        return retrieved

    def delete_document(self, document_name: str):

        print("\n" + "=" * 60)
        print("DELETE REQUEST")
        print("Document:", document_name)

        before = self.collection.count()
        print("Collection before:", before)

        matches = self.collection.get(
            where={"document": document_name}
        )

        print("Matches found:", len(matches["ids"]))

        if matches["ids"]:
            print("First metadata:", matches["metadatas"][0])


        self.collection.delete(
            where={
                "document": document_name
            }
        )

        after = self.collection.count()
        print("Collection after:", after)
        print("=" * 60 + "\n")
        
    def count(self):
        return self.collection.count()