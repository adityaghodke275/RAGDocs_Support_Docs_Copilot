from sqlalchemy import Text
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    document_uuid = Column(String, unique=True, nullable=False)

    filename = Column(String, nullable=False)

    original_filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    file_type = Column(String, nullable=False)

    file_size = Column(Integer, nullable=False)

    status = Column(String, default="uploaded")

    content = Column(Text)

    uploaded_at = Column(DateTime, default=datetime.utcnow)