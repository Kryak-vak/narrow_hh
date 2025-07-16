from abc import ABC
from typing import Generic, TypeVar

from app.infrastructure.database import AbstractRedisRepository, AbstractSQLAlchemyRepository

StateRepoType = TypeVar('StateRepoType', bound=AbstractRedisRepository)
TokeRepoType = TypeVar('TokeRepoType', bound=AbstractSQLAlchemyRepository)


class AbstractOAuthService(  # TODO finish
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