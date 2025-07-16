from fastapi import Depends
from redis.asyncio import Redis

from app.application.common.csrf import StateManager
from app.application.hh.auth.oauth import HHOAuthService
from app.application.users.auth.user import UserAuthService
from app.infrastructure.database import RedisStateRepository
from app.infrastructure.database.users.repositories import (
    HeadHunterTokenRepository,
    UserRepository,
    UserTokenRepository,
)
from app.presentation.deps import SessionDep, get_redis_client


def get_redis_state_repository(
        redis_client: Redis = Depends(get_redis_client)
    ) -> RedisStateRepository:
    return RedisStateRepository(redis_client=redis_client)

def get_state_manager(
        state_repo: RedisStateRepository = Depends(get_redis_state_repository)
    ) -> StateManager:
    return StateManager(state_repo=state_repo)

def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session=session)

def get_hh_token_repository(session: SessionDep) -> HeadHunterTokenRepository:
    return HeadHunterTokenRepository(session)

def get_user_token_repository(session: SessionDep) -> UserTokenRepository:
    return UserTokenRepository(session)

def get_hh_auth_service(
        session: SessionDep,
        state_manager: StateManager = Depends(get_state_manager),
    ) -> HHOAuthService:
    return HHOAuthService(
        session=session,
        state_manager=state_manager,
    )

def get_user_auth_service(
        session: SessionDep,
        user_repository: UserRepository = Depends(get_user_repository),
        user_token_repo: UserTokenRepository = Depends(get_user_token_repository),
        hh_token_repo: HeadHunterTokenRepository = Depends(get_hh_token_repository),
        state_manager: StateManager = Depends(get_state_manager),
        hh_auth_service: HHOAuthService = Depends(get_hh_auth_service),
    ) -> UserAuthService:
    return UserAuthService(
        session=session,
        user_repo=user_repository,
        user_token_repo=user_token_repo,
        hh_token_repo=hh_token_repo,
        state_manager=state_manager,
        hh_auth_service=hh_auth_service
    )
    