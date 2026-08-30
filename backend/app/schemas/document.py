from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):

    id: int
    document_uuid: str
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )