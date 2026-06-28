from app.database.base import Base
from app.database.connection import engine

# Import all models here
from app.models.document import Document


def init_db():
    Base.metadata.create_all(bind=engine)