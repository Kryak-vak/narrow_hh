from uuid import UUID

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.users.dto import (
    UserCreateDTO,
    UserDTO,
    UserUpdateDTO,
)
from src.app.infrastructure.database.users.repositories import UserRepository

faker_ = Faker()
test_amount = 3


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
            for _ in range(test_amount)
        ],
        ids=lambda val: f"hh_id={val.hh_user_id}"
    )
    def user_create_dto(self, request):
        return request.param
    
    @pytest.fixture(
        scope="class",
        params=[
            UserUpdateDTO(
                hh_user_id=str(faker_.uuid4()),
            )
            for _ in range(test_amount)
        ],
        ids=lambda val: f"hh_id={val.hh_user_id}"
    )
    def user_update_dto(self, request):
        return request.param

    @pytest.fixture(scope="class")
    def user_dto(self):
        return UserDTO(
            id=UUID(faker_.uuid4()),
            hh_user_id=str(faker_.random_int(min=10000, max=999999))
        )
    
    @pytest.mark.asyncio
    async def test_create(self, user_repository: UserRepository, user_create_dto: UserCreateDTO):
        user_db_dto = await user_repository.create(user_create_dto)

        assert all(
            getattr(user_db_dto, key) == value
            for key, value in user_create_dto.model_dump().items()
        )

        assert user_db_dto.id is not None
    
    @pytest.mark.asyncio
    async def test_update(
        self, user_repository: UserRepository,
        user_create_dto: UserCreateDTO,
        user_update_dto: UserUpdateDTO
    ):
        user_db_dto = await user_repository.create(user_create_dto)
        user_updated_db_dto = await user_repository.update(
            pk=user_db_dto.id,
            update_dto=user_update_dto
        )

        assert user_updated_db_dto.id == user_db_dto.id
        
        assert all(
            getattr(user_updated_db_dto, key) == value
            for key, value in user_update_dto.model_dump().items()
        )


