from sqlalchemy import Select
from sqlalchemy.orm import selectinload

from src.app.application.users.dto import (
    HeadHunterTokenCreateDTO,
    HeadHunterTokenDTO,
    HeadHunterTokenUpdateDTO,
    UserCreateDTO,
    UserDTO,
    UserRefreshTokenCreateDTO,
    UserRefreshTokenDTO,
    UserRefreshTokenUpdateDTO,
    UserUpdateDTO,
)
from src.app.infrastructure.database import AbstractSQLAlchemyRepository
from src.app.infrastructure.database.users.models import HeadHunterToken, User, UserRefreshToken


class UserRepository(
        AbstractSQLAlchemyRepository[
            User,
            UserDTO,
            UserCreateDTO,
            UserUpdateDTO
        ]
    ):
    model = User
    read_dto = UserDTO

    def _apply_loader_options(self, stmt: Select) -> Select:
        return stmt.options(selectinload(User.hh_token))


class HeadHunterTokenRepository(
        AbstractSQLAlchemyRepository[
            HeadHunterToken,
            HeadHunterTokenDTO,
            HeadHunterTokenCreateDTO,
            HeadHunterTokenUpdateDTO
        ]
    ):
    model = HeadHunterToken
    read_dto = HeadHunterTokenDTO


class UserTokenRepository(
        AbstractSQLAlchemyRepository[
            UserRefreshToken,
            UserRefreshTokenDTO,
            UserRefreshTokenCreateDTO,
            UserRefreshTokenUpdateDTO
        ]
    ):
    model = UserRefreshToken
    read_dto = UserRefreshTokenDTO