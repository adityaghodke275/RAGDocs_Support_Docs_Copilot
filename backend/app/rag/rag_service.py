from app.rag.chunking.chunker import TextChunker
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.retrieval.retrieval_service import RetrievalService
from app.rag.prompting.prompt_builder import PromptBuilder
from app.rag.generator.generator_service import GeneratorService
from app.rag.vectorstore.vector_store import VectorStore
from app.rag.loaders.loader_factory import LoaderFactory
from app.rag.utils.text_cleaner import TextCleaner


class RAGService:

    def __init__(self):
        self.chunker = TextChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

        self.retriever = RetrievalService()
        self.generator = GeneratorService()

        self.loader = LoaderFactory()

    # ---------------------------------------------------------
    # DOCUMENT INDEXING
    # ---------------------------------------------------------

    @staticmethod
    def process_document(
        file_path: str,
        document_uuid: str,
        original_filename: str,
    ):

        loader = LoaderFactory()
        chunker = TextChunker()
        embedding_service = EmbeddingService()
        vector_store = VectorStore()

        print("\n" + "=" * 70)
        print("STARTING DOCUMENT INDEXING")
        print("Document:", original_filename)
        print("UUID:", document_uuid)
        print("=" * 70)

        # Load
        text = loader.load(file_path)

        if not text or not text.strip():
            raise ValueError("Document contains no readable text.")

        # Clean
        text = TextCleaner.clean(text)

        if not text:
            raise ValueError("Document contains no usable text after cleaning.")

        print("TEXT LENGTH:", len(text))

        # Chunk
        chunks = chunker.split_text(text)

        if not chunks:
            raise ValueError("No chunks could be created from the document.")

        print("TOTAL CHUNKS:", len(chunks))

        # Embed
        embeddings = embedding_service.embed_texts(chunks)

        print("TOTAL EMBEDDINGS:", len(embeddings))

        # Store
        vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            document_name=original_filename,
        )

        print("=" * 70)
        print("DOCUMENT INDEXING COMPLETE")
        print("=" * 70)

        return {
            "status": "indexed",
            "chunks": len(chunks),
        }

    # ---------------------------------------------------------
    # QUESTION ANSWERING
    # ---------------------------------------------------------

    def ask(self, question: str):

        chunks = self.retriever.retrieve(
            question=question,
            top_k=10,
        )

        prompt = PromptBuilder.build(
            question=question,
            contexts=chunks,
        )

        print("\n" + "=" * 80)
        print(prompt)
        print("=" * 80 + "\n")

        answer = self.generator.generate(prompt)

        unique_sources = {}

        for chunk in chunks:

            document = chunk.get(
                "document",
                "Unknown"
            )

            chunk_no = chunk.get(
                "chunk",
                -1
            )

            if document not in unique_sources:

                unique_sources[document] = {
                    "document": document,
                    "chunks": [],
                }

            if chunk_no not in unique_sources[document]["chunks"]:

                unique_sources[document]["chunks"].append(
                    chunk_no
                )

        sources = list(unique_sources.values())

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }