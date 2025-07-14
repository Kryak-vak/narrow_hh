from pydantic_settings import BaseSettings, SettingsConfigDict

from config.app import ENV_FILE


class HHConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="HH_",
        env_file=ENV_FILE,
        extra="ignore"
    )
    
    app_name: str
    client_id: str
    client_secret: str
    redirect_uri: str
    contact_email: str


hh_config = HHConfig()  # type: ignore[call-arg]
