from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.database.dependencies import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    document = DocumentService.upload_document(
        file=file,
        db=db,
    )

    return document
@router.get(
    "",
    response_model=List[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db)
):
    return DocumentService.get_all_documents(db)

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    return DocumentService.delete_document(
        document_id=document_id,
        db=db,
    )