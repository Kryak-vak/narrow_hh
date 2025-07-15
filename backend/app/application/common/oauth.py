import secrets
from abc import ABC
from typing import Generic, TypeVar

from app.infrastructure.database import AbstractRedisRepository, AbstractSQLAlchemyRepository

StateRepoType = TypeVar('StateRepoType', bound=AbstractRedisRepository)
TokeRepoType = TypeVar('TokeRepoType', bound=AbstractSQLAlchemyRepository)


class BaseOAuthService(  # TODO finish
        ABC, Generic[StateRepoType, TokeRepoType]
    ):
    def __init__(
            self,
            state_repo: StateRepoType,
            token_repo: TokeRepoType
        ) -> None:
        self.state_repo = state_repo
        self.hh_token_repo = state_repo
        self.hh_client = token_repo

    async def generate_state(self) -> str:
        state = secrets.token_urlsafe(16)
        await self.state_repo.create_ex(state)

        return state
    
    async def validate_state(self, state: str) -> int:
        result = await self.state_repo.get(state)

        if not result:
            raise RuntimeError('CSRF protection failed')  # TODO change to custom app exception
        
        await self.state_repo.delete(state)