from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine, redis
from app.repositories.hh import RedisStateRepository
from app.services.hh import HHAuthService


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_redis() -> Redis:
    return redis


def get_redis_state_repository(redis: Redis = Depends(get_redis)) -> RedisStateRepository:
    return RedisStateRepository(redis=redis)


def get_hh_auth_service(
    state_repo: RedisStateRepository = Depends(get_redis_state_repository),
) -> HHAuthService:
    return HHAuthService(
        state_repository=state_repo,
        client_id=settings.HH_CLIENT_ID,
        secret_key=settings.HH_CLIENT_SECRET,
        redirect_uri=settings.HH_REDIRECT_URI,
        state_exp=settings.STATE_EXP
    )