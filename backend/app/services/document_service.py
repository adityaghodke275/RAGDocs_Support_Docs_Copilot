import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.rag.rag_service import RAGService
from app.core.config import settings
from app.models.document import Document
from app.services.parser_service import ParserService
from app.rag.vectorstore.vector_store import VectorStore

class DocumentService:

    @staticmethod
    def upload_document(file: UploadFile, db: Session):

        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {extension} is not supported."
            )

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        document_uuid = str(uuid.uuid4())
        stored_filename = f"{document_uuid}{extension}"

        file_path = os.path.join(
            settings.UPLOAD_DIR,
            stored_filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)

        if file_size > settings.MAX_FILE_SIZE:
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="File exceeds maximum size."
            )

        try:
            content = ParserService.extract_text(file_path)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail=f"Unable to parse document: {str(e)}"
            )

        document = Document(
            document_uuid=document_uuid,
            filename=stored_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_type=extension[1:],
            file_size=file_size,
            status="uploaded",
            content=content,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        print("\nStarting Automatic RAG Indexing...")

        try:
            result = RAGService.process_document(
                file_path=file_path,
                 document_uuid=document.document_uuid,
                 original_filename=document.original_filename,
            )
            document.status = result["status"]

            db.commit()
            db.refresh(document)

            print("Document Indexed Successfully!")

        except Exception as e:
            print(f"RAG Indexing Failed : {e}")
            document.status = "failed"
            db.commit()
            
        return document
    
    @staticmethod
    def get_all_documents(db: Session):
        return (
            db.query(Document)
            .order_by(Document.uploaded_at.desc())
            .all()
            )

    @staticmethod
    def delete_document(document_id: int, db: Session):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

    # Delete vectors from ChromaDB
        try:
            vector_store = VectorStore()

            vector_store.delete_document(
            document.original_filename
            )

            print("Vectors deleted successfully.")

        except Exception as e:
            print(f"Vector deletion failed: {e}")

     # Delete uploaded file 
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

    # Delete database record
        db.delete(document)
        db.commit()

        return {
            "message": "Document deleted successfully."
        }