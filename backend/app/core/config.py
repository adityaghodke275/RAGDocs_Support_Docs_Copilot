from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):

    APP_NAME: str = "Support Docs Copilot"
    APP_VERSION: str = "1.0.0"

    APP_DESCRIPTION: str = (
        "Enterprise AI-powered Retrieval-Augmented Generation platform."
    )

    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./support_docs.db"

    GEMINI_API_KEY: str

    CHROMA_DB_PATH: str = "./data/chroma_dbx"

    # ---------------------------
    # Upload Settings
    # ---------------------------

    UPLOAD_DIR: str = "../data/uploads"

    MAX_FILE_SIZE: int = 20 * 1024 * 1024

    ALLOWED_EXTENSIONS: list[str] = [
        ".pdf",
        ".docx",
        ".txt",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()