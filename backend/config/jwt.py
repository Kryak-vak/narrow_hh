from pydantic_settings import BaseSettings, SettingsConfigDict

from config.app import ENV_FILE


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=ENV_FILE,
        extra="ignore"
    )
    
    algorithm: str
    access_expire: int
    refresh_expire: int


jwt_config = JWTConfig()  # type: ignore[call-arg]
