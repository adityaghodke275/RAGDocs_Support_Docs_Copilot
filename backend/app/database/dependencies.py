from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session for each request.
    Automatically closes the session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()