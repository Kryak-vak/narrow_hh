from fastapi import FastAPI

from src.app.presentation.router import router
from src.config.app import app_config

app = FastAPI(
    title=app_config.project_name,
    openapi_url=f"{app_config.api_v1_str}/openapi.json",
)

app.include_router(router, prefix=app_config.api_v1_str)
