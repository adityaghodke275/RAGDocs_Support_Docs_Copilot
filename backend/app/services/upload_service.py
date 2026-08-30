from pathlib import Path
import shutil

from fastapi import UploadFile

from app.rag.loaders.loader_factory import LoaderFactory
from app.rag.chunking.chunker import TextChunker
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstore.vector_store import VectorStore
from app.rag.utils.text_cleaner import TextCleaner


class UploadService:

    def __init__(self):

        self.upload_dir = Path("data/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        self.loader = LoaderFactory()
        self.chunker = TextChunker()
        self.embedding = EmbeddingService()
        self.vectorstore = VectorStore()

    async def upload(self, file: UploadFile):

        # ----------------------------------------------------
        # Save uploaded file
        # ----------------------------------------------------
        filepath = self.upload_dir / file.filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("=" * 70)
        print("FILE SAVED")
        print(filepath)
        print("=" * 70)

        # ----------------------------------------------------
        # Load document
        # ----------------------------------------------------
        text = self.loader.load(str(filepath))

        print("TEXT LENGTH:", len(text))
        print(text[:500])

        # ----------------------------------------------------
        # Clean text
        # ----------------------------------------------------
        text = TextCleaner.clean(text)

        print("AFTER CLEAN:", len(text))

        # ----------------------------------------------------
        # Chunk text
        # ----------------------------------------------------
        chunks = self.chunker.split_text(text)

        print("TOTAL CHUNKS:", len(chunks))

        if chunks:
            print("\nFIRST CHUNK\n")
            print(chunks[0][:500])

        # ----------------------------------------------------
        # Generate embeddings
        # ----------------------------------------------------
        embeddings = self.embedding.embed_texts(chunks)

        print("TOTAL EMBEDDINGS:", len(embeddings))

        # ----------------------------------------------------
        # Store in Chroma
        # ----------------------------------------------------
        self.vectorstore.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            document_name=file.filename,
        )

        print("=" * 70)
        print("UPLOAD FINISHED")
        print("=" * 70)

        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "chunks": len(chunks),
        }