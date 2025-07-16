from app.application.users.dto import (
    TokenCreateDTO,
    TokenDTO,
    TokenUpdateDTO,
    UserCreateDTO,
    UserDTO,
    UserUpdateDTO,
)
from app.infrastructure.database import AbstractSQLAlchemyRepository
from app.infrastructure.database.users.models import HeadHunterToken, User, UserToken


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


class HeadHunterTokenRepository(
        AbstractSQLAlchemyRepository[
            HeadHunterToken,
            TokenDTO,
            TokenCreateDTO,
            TokenUpdateDTO
        ]
    ):
    model = HeadHunterToken
    read_dto = TokenDTO


class UserTokenRepository(
        AbstractSQLAlchemyRepository[
            UserToken,
            TokenDTO,
            TokenCreateDTO,
            TokenUpdateDTO
        ]
    ):
    model = UserToken
    read_dto = TokenDTO