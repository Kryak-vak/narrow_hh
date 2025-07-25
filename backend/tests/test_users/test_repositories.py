from uuid import UUID

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

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
from src.app.infrastructure.database.users.repositories import (
    HeadHunterTokenRepository,
    UserRepository,
    UserTokenRepository,
)

faker_ = Faker()


class TestUserRepository:
    @pytest.fixture(scope="function")
    def user_repository(self, session: AsyncSession):
        return UserRepository(
            session=session
        )
    
    @pytest.fixture(
        scope="class",
        params=[
            UserCreateDTO(
                hh_user_id=str(faker_.uuid4()),
            )
            for _ in range(5)
        ],
        ids=lambda val: f"hh_id={val.hh_user_id}"
    )
    def user_create_dto(self, request):
        return request.param
    
    @pytest.fixture(scope="class")
    def user_update_dto(self):
        return UserUpdateDTO(
            hh_user_id=str(faker_.random_int(min=10000, max=999999))
        )

    @pytest.fixture(scope="class")
    def user_dto(self):
        return UserDTO(
            id=UUID(faker_.uuid4()),
            hh_user_id=str(faker_.random_int(min=10000, max=999999))
        )
    
    @pytest.mark.asyncio
    async def test_create(self, user_repository: UserRepository, user_create_dto: UserCreateDTO):
        user_db_dto = await user_repository.create(user_create_dto)
        
        assert all((
            user_db_dto.hh_user_id == user_create_dto.hh_user_id,
        ))
        
        assert all(
            key in user_db_dto.model_dump()
            for key in (
                "id",
                "hh_user_id",
            )
        )

        assert user_db_dto.id is not None


