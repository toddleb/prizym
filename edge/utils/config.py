"""
Configuration module for the KPMG Edge application.
Handles environment variables and application settings.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import logging

logger = logging.getLogger("config")

# Load environment variables from .env file
load_dotenv()

class EdgeConfig(BaseSettings):
    """Configuration settings for the KPMG Edge application."""
    
    # Application settings
    APP_NAME: str = "KPMG Edge"
    APP_VERSION: str = "1.0.0"
    
    # Virtual Environment Directory
    VENV_DIR: str = Field(default="/Users/toddlebaron/prizym/edge/venv", env="VENV_DIR")
    
    # OpenAI API Settings
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    
    # Anthropic API Settings
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(default="claude-3-opus-20240229", env="ANTHROPIC_MODEL")
    
    # Hugging Face API Settings
    HUGGINGFACE_API_KEY: str = Field(default="", env="HUGGINGFACE_API_KEY")
    
    # Processing Configuration
    WORKERS: int = Field(default=4, env="WORKERS")
    
    # Database Settings
    DB_NAME: str = Field(default="edge_db", env="DB_NAME")
    DB_USER: str = Field(default="todd", env="DB_USER")
    DB_PASSWORD: str = Field(default="Fubijar", env="DB_PASSWORD")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    
    # Data Directories - Make all fields optional with defaults
    PLAN_INPUT_DIR: str = Field(default="", env="PLAN_INPUT_DIR")
    PLAN_OUTPUT_DIR: str = Field(default="", env="PLAN_OUTPUT_DIR")
    PLAN_DIR: str = Field(default="", env="PLAN_DIR")
    
    # UI Settings
    UI_THEME: str = Field(default="light", env="UI_THEME")
    UI_FONT_SIZE: int = Field(default=10, env="UI_FONT_SIZE")
    
    # KPMG Branding Colors
    PRIMARY_COLOR: str = Field(default="#00338D", env="PRIMARY_COLOR")  # KPMG blue
    SECONDARY_COLOR: str = Field(default="#005EB8", env="SECONDARY_COLOR")
    ACCENT_COLOR: str = Field(default="#0091DA", env="ACCENT_COLOR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields

    def get_db_connection_string(self) -> str:
        """Get the database connection string."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def validate_config(self) -> bool:
        """Validate the configuration settings."""
        missing_fields = []
        
        # Check if any API key is set for AI features
        if not self.OPENAI_API_KEY and not self.ANTHROPIC_API_KEY and not self.HUGGINGFACE_API_KEY:
            missing_fields.append("API Keys (OpenAI, Anthropic, or Hugging Face)")
        
        # Check data directories if AI processing is enabled
        if not self.PLAN_INPUT_DIR:
            missing_fields.append("PLAN_INPUT_DIR")
        if not self.PLAN_OUTPUT_DIR:
            missing_fields.append("PLAN_OUTPUT_DIR")
            
        if missing_fields:
            logger.warning(f"⚠️ Missing recommended configuration fields: {', '.join(missing_fields)}")
            logger.warning("Some features may be unavailable. Configure these in Settings > System Configuration.")
            return False
            
        return True
        
    def get_color_scheme(self) -> dict:
        """Get the application color scheme."""
        return {
            "primary": self.PRIMARY_COLOR,
            "secondary": self.SECONDARY_COLOR,
            "accent": self.ACCENT_COLOR,
            "light": "#E0E6ED",
            "white": "#FFFFFF",
            "dark": "#333333",
            "success": "#28a745",
            "warning": "#ffc107",
            "danger": "#dc3545"
        }
    
    def get_available_ai_providers(self) -> list:
        """Get a list of available AI providers based on configured API keys."""
        providers = []
        if self.OPENAI_API_KEY:
            providers.append("OpenAI")
        if self.ANTHROPIC_API_KEY:
            providers.append("Anthropic")
        if self.HUGGINGFACE_API_KEY:
            providers.append("Hugging Face")
        return providers

# Create a global config instance
try:
    config = EdgeConfig()
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    # Create a fallback config with defaults
    config = EdgeConfig.construct()
    logger.warning("Using fallback configuration with defaults")
