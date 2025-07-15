import secrets
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ENV_DIR / ".env"


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PROJECT_NAME: str
    
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str


app_config = AppConfig()  # type: ignore


INTERFACE_ALLOWLIST = {
    "https://bot.interface.com",
    "https://web.interface.com",
    "http://localhost:3000",
}
