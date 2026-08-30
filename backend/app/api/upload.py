from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.upload_service import UploadService

router = APIRouter(tags=["Upload"])

service = UploadService()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        filename = await service.upload(file)

        return {
            "message": "Document uploaded successfully",
            "filename": filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))