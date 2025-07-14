from fastapi import Depends
from redis.asyncio import Redis

from app.application.hh.auth.oauth import HHOAuthService
from app.infrastructure.database import RedisStateRepository
from app.infrastructure.database.users.repositories import HeadHunterTokenRepository
from app.presentation.deps import SessionDep, get_redis_client
from config.hh import hh_config


def get_redis_state_repository(
        redis_client: Redis = Depends(get_redis_client)
    ) -> RedisStateRepository:
    return RedisStateRepository(redis_client=redis_client)


def get_hh_token_repository(session: SessionDep) -> HeadHunterTokenRepository:
    return HeadHunterTokenRepository(session)


def get_hh_auth_service(
    session: SessionDep,
    state_repo: RedisStateRepository = Depends(get_redis_state_repository),
    hh_token_repo: HeadHunterTokenRepository = Depends(get_hh_token_repository),
) -> HHOAuthService:
    return HHOAuthService(
        session=session,
        state_repo=state_repo,
        token_repo=hh_token_repo,
        client_id=hh_config.client_id,
        secret_key=hh_config.client_secret,
        redirect_uri=hh_config.redirect_uri
    )