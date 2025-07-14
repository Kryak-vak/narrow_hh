from sqlalchemy import select

from app.application.users.dto import (
    HeadHunterTokenCreateDTO,
    HeadHunterTokenDTO,
    HeadHunterTokenUpdateDTO,
    UserCreateDTO,
    UserDTO,
    UserUpdateDTO,
)
from app.infrastructure.database import AbstractSQLAlchemyRepository
from app.infrastructure.database.users.models import HeadHunterToken, User


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