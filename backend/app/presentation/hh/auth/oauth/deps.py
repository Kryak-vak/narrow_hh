from fastapi import Depends
from redis.asyncio import Redis

from app.application.hh.auth.oauth import HHOAuthService
from app.infrastructure.database import RedisStateRepository
from app.infrastructure.database.users.repositories import UserTokenRepository
from app.presentation.deps import SessionDep, get_redis_client
from core.config import settings


def get_redis_state_repository(
        redis_client: Redis = Depends(get_redis_client)
    ) -> RedisStateRepository:
    return RedisStateRepository(redis_client=redis_client)


def get_user_token_repository(session: SessionDep) -> UserTokenRepository:
    return UserTokenRepository(session)


def get_hh_auth_service(
    state_repo: RedisStateRepository = Depends(get_redis_state_repository),
    user_token_repo: RedisStateRepository = Depends(get_redis_state_repository),
) -> HHOAuthService:
    return HHOAuthService(
        state_repo=state_repo,
        token_repo=user_token_repo,
        client_id=settings.HH_CLIENT_ID,
        secret_key=settings.HH_CLIENT_SECRET,
        redirect_uri=settings.HH_REDIRECT_URI
    )