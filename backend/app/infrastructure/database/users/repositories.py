from app.application.users.dto import (
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
from app.infrastructure.database import AbstractSQLAlchemyRepository
from app.infrastructure.database.users.models import HeadHunterToken, User, UserRefreshToken


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