from sqlalchemy.ext.asyncio import AsyncSession

from app.application.users.dto import (
    UserCreateDTO,
    UserDTO,
)
from app.infrastructure.database.users.repositories import UserRepository


class UserService:
    def __init__(
            self, session: AsyncSession, 
            user_repo: UserRepository
        ):
        self.session = session
        self.user_repo = user_repo
    
    async def get_or_create_user(self) -> UserDTO:
        # user_dto = self.user_repo.get_by_telegram_id(telegram_id)
        # if not user_dto:
        #     user_dto = await self.user_repo.create(
        #         UserCreateDTO()
        #     )

        # telegram_account_dto = await self.telegram_account_repo.create(telegram_account_create_dto)
        pass




