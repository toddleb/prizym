import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

# Load .env
dotenv_path = "/Users/toddlebaron/prizym/spmedge/.env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Ensure API Key is set
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("❌ OPENAI_API_KEY not loaded! Check your .env file.")

class Config(BaseSettings):
    """Application Configuration"""

    ###########################
    # 🔐 API Configuration
    ###########################
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field("gpt-4o", env="OPENAI_MODEL")

    ###########################
    # 🛢️ Database Configuration
    ###########################
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")  # Use a secrets manager if possible
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")

    ###########################
    # 📂 File System Paths
    ###########################
    DATA_DIR: str = Field(..., env="DATA_DIR")
    UNPROCESSED_DOCS_DIR: str = Field(..., env="UNPROCESSED_DOCS_DIR")  
    NEW_DOCS_DIR: str = Field(..., env="NEW_DOCS_DIR")  
    PROCESSED_DOCS_DIR: str = Field(..., env="PROCESSED_DOCS_DIR")
    STORAGE_DIR: str = Field(..., env="STORAGE_DIR")
    ARCHIVE_DIR: str = Field(..., env="ARCHIVE_DIR")
    LOG_DIR: str = Field(..., env="LOG_DIR")
    KNOWLEDGE_FILES_DIR: str = Field(..., env="KNOWLEDGE_FILES_DIR")

    ###########################
    # 📊 Reports & Models
    ###########################
    REPORTS_DIR: str = Field(..., env="REPORTS_DIR")
    REPORTS_MD_DIR: str = Field(..., env="REPORTS_MD_DIR")
    REPORTS_JSON_DIR: str = Field(..., env="REPORTS_JSON_DIR")
    MODEL_PATH: str = Field(..., env="MODEL_PATH")
    PYTHON_PATH: str = Field("/opt/homebrew/bin/python3", env="PYTHON_PATH")

    ###########################
    # ⚡ Processing Configuration
    ###########################
    WORKERS: int = Field(4, env="WORKERS")  # Number of worker threads/processes

    ###########################
    # 🎨 UI Configuration
    ###########################
    UI_THEME: str = Field("light", env="UI_THEME")
    UI_FONT_SIZE: int = Field(10, env="UI_FONT_SIZE")

    class Config:
        env_file = dotenv_path
        env_file_encoding = "utf-8"
        extra = "ignore"

    def ensure_directories(self):
        """Ensure all required directories exist."""
        paths_to_create = [
            Path(self.REPORTS_MD_DIR), Path(self.REPORTS_JSON_DIR),
            Path(self.NEW_DOCS_DIR), Path(self.PROCESSED_DOCS_DIR),
            Path(self.STORAGE_DIR), Path(self.ARCHIVE_DIR),
            Path(self.LOG_DIR), Path(self.REPORTS_DIR),
            Path(self.KNOWLEDGE_FILES_DIR), Path(self.UNPROCESSED_DOCS_DIR),
            Path(self.DATA_DIR) / "stage_input",
            Path(self.DATA_DIR) / "stage_load",
            Path(self.DATA_DIR) / "stage_clean",
            Path(self.DATA_DIR) / "stage_process",
            Path(self.DATA_DIR) / "stage_knowledge",
            Path(self.DATA_DIR) / "stage_report",
            Path(self.REPORTS_DIR) / "json" / "raw_json"
        ]

        for path in paths_to_create:
            path.mkdir(parents=True, exist_ok=True)

# Create a global instance of settings
config = Config()
config.ensure_directories()
