import os
import pytest
from app.config import get_settings, Settings


def test_settings_default_values(monkeypatch):
    # Set a dummy key in env
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key_123456789")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    settings = Settings()
    assert settings.gemini_api_key == "test_gemini_key_123456789"
    assert settings.gemini_model in ["gemini-2.5-flash", "gemini-3.7-flash"]
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_settings_custom_model(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key_123456789")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.7-flash")

    settings = Settings()
    assert settings.gemini_model == "gemini-3.7-flash"


def test_masked_api_key_security(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSySecretLongKey987654321")
    settings = Settings()

    # The masked key should not expose the full secret
    masked = settings.masked_api_key
    assert "987654321" not in masked
    assert masked.endswith("****")
    assert masked.startswith("AIza")

    # Repr of Settings should not expose raw API key
    assert "AIzaSySecretLongKey987654321" not in repr(settings)
