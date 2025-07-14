from fastapi import FastAPI

from app.presentation.router import router
from config.app import app_config

app = FastAPI(
    title=app_config.PROJECT_NAME,
    openapi_url=f"{app_config.API_V1_STR}/openapi.json",
)

app.include_router(router, prefix=app_config.API_V1_STR)
