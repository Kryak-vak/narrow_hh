from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.csrf import StateManager
from app.application.hh.auth.dto import HeadHunterUserDTO, OauthTokenDTO
from app.application.hh.auth.oauth import HHOAuthService
from app.application.users.dto import (
    TokenCreateDTO,
    TokenDTO,
    TokenUpdateDTO,
    UserCreateDTO,
    UserDTO,
)
from app.infrastructure.clients import HHAsyncClient
from app.infrastructure.database.users.repositories import (
    HeadHunterTokenRepository,
    UserRepository,
    UserTokenRepository,
)


class UserAuthService:
    def __init__(
            self, session: AsyncSession, 
            user_repo: UserRepository,
            user_token_repo: UserTokenRepository,
            hh_token_repo: HeadHunterTokenRepository,
            state_manager: StateManager,
            hh_auth_service: HHOAuthService,
        ):
        self.session = session
        self.user_repo = user_repo
        self.user_token_repo = user_token_repo
        self.hh_token_repo = hh_token_repo
        self.state_manager = state_manager
        self.hh_auth_service = hh_auth_service
        
        self.hh_client = HHAsyncClient
    
    async def start_auth(
            self, state: str,
            notify_url: str = None,
            interface_redirect_url: str = None
        ):
        if notify_url:
            value_map = {"notify_url": notify_url}
        if interface_redirect_url:
            value_map = {"interface_redirect_url": interface_redirect_url}
        
        self.state_manager.set_state_hash_ex(state, value_map)

        return await self.hh_auth_service.get_user_authorize_url(state)
    
    async def get_or_create_user(self, authorization_code: str, state: str) -> UserDTO:
        hh_oauth_tokens_dto = await self.authorize_user(authorization_code, state)
        hh_user_dto = await self.get_hh_user_info(hh_oauth_tokens_dto.access_token)
        
        user_dto = await self.user_repo.get(hh_user_id=hh_user_dto.id)
        if not user_dto:
            user_dto = await self.create_user_with_hh_token(hh_user_dto.id, hh_oauth_tokens_dto)
        else:
            user_dto = await self.update_user_hh_token(user_dto, hh_oauth_tokens_dto)
        
        return user_dto
    
    async def create_user_with_hh_token(self, hh_user_id: str, hh_oauth_tokens_dto: OauthTokenDTO):
        user_dto = await self.user_repo.create(
            UserCreateDTO(hh_user_id=hh_user_id)
        )

        self.hh_token_repo.create(
            TokenCreateDTO(
                user_id=user_dto.id
                **hh_oauth_tokens_dto
            )
        )

        await self.session.commit()
        user_dto = await self.user_repo.refresh(user_dto)

        return user_dto
    
    async def update_user_hh_token(
            self, user_dto: UserDTO,
            hh_oauth_tokens_dto: OauthTokenDTO
        ) -> TokenDTO:
        await self.hh_token_repo.update(
            user_dto.hh_token.id,
            TokenUpdateDTO(**hh_oauth_tokens_dto)
        )
        user_dto = await self.user_repo.refresh(user_dto)

        return user_dto
    
    async def authorize_user(
            self, authorization_code: str,
            state: str
        ) -> OauthTokenDTO:
        hh_oauth_tokens_dto = await self.hh_auth_service.authorize_user(
            authorization_code,
            state
        )

        return hh_oauth_tokens_dto
    
    async def get_hh_user_info(self, access_token: str) -> HeadHunterUserDTO:
        async with self.hh_client() as client:
            hh_user_data = await client.make_me_request(access_token)
            
        return HeadHunterUserDTO(**hh_user_data)




