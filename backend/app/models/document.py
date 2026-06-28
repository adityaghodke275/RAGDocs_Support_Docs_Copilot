from datetime import datetime
import uuid

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    document_uuid: Mapped[str] = mapped_column(
        String,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(String, nullable=False)

    original_filename: Mapped[str] = mapped_column(String, nullable=False)

    file_path: Mapped[str] = mapped_column(String, nullable=False)

    file_type: Mapped[str] = mapped_column(String, nullable=False)

    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        String,
        default="UPLOADED",
        nullable=False,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )