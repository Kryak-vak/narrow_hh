from sqlalchemy.ext.asyncio import AsyncSession

from app.application.hh.auth.dto import HHUserDTO, OauthTokensDTO
from app.application.hh.auth.oauth import HHOAuthService
from app.application.users.dto import (
    UserCreateDTO,
    UserDTO,
)
from app.infrastructure.database.users.repositories import UserRepository


class UserService:
    def __init__(
            self, session: AsyncSession, 
            user_repo: UserRepository,
            hh_auth_service: HHOAuthService
        ):
        self.session = session
        self.user_repo = user_repo
        self.hh_auth_service = hh_auth_service
    
    async def start_auth(
            self, notify_link: str = None,
            interface_redirect_url: str = None
        ):
        return await self.hh_auth_service.get_user_authorize_url()
    
    async def authorize_hh_user(
            self, authorization_code: str,
            state: str
        ) -> tuple[HHUserDTO, OauthTokensDTO]:
        hh_user_dto, hh_tokens_dto = await self.hh_auth_service.authorize_user(
            authorization_code,
            state
        )

        return hh_user_dto, hh_tokens_dto
    
    async def get_or_create_user(self) -> UserDTO:
        self.hh_auth_service.authorize_user()




