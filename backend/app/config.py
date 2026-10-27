from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration with strict security rules.
    Loads secrets safely from .env without exposing keys.
    """
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API Key for driving the multi-agent system"
    )
    gemini_model: str = Field(
        default="ag/gemini-3.8-flash-high",
        description="Gemini Model version (e.g., ag/gemini-3.8-flash-high)"
    )
    llm_base_url: Optional[str] = Field(
        default="http://localhost:20128/v1",
        description="Base URL for 9router or OpenAI-compatible gateway (e.g. http://localhost:20128/v1)"
    )
    host: str = Field(
        default="0.0.0.0",
        description="Server listening host"
    )
    port: int = Field(
        default=8000,
        description="Server listening port"
    )

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    @property
    def masked_api_key(self) -> str:
        """
        Returns a securely masked version of the Gemini API Key.
        Guarantees that sensitive credentials are never leaked.
        """
        if not self.gemini_api_key:
            return "NOT_SET"
        if len(self.gemini_api_key) <= 8:
            return "****"
        return f"{self.gemini_api_key[:4]}...****"

    def __repr__(self) -> str:
        return (
            f"Settings(gemini_model='{self.gemini_model}', "
            f"host='{self.host}', port={self.port}, "
            f"gemini_api_key='{self.masked_api_key}')"
        )

    def __str__(self) -> str:
        return self.__repr__()


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings instance.
    """
    return Settings()
