from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.database.init_db import init_db

from app.api.routes.documents import router as document_router
from app.api.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware




logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully.")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(document_router)
app.include_router(chat_router)




@app.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }