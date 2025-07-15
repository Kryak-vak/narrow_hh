import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.hh.auth.dto import HHUserDTO, OauthTokensDTO
from app.infrastructure.clients import HHAsyncClient
from app.infrastructure.database import RedisStateRepository
from app.infrastructure.database.users.repositories import HeadHunterTokenRepository


class HHOAuthService():
    def __init__(
            self, session: AsyncSession,
            state_repo: RedisStateRepository,
            hh_token_repo: HeadHunterTokenRepository
        ) -> None:
        self.session = session
        self.state_repo = state_repo

        self.hh_token_repo = hh_token_repo
        self.hh_client = HHAsyncClient
    
    async def get_user_authorize_url(self) -> str:
        state = await self.generate_state()
        return self.hh_client.create_user_authorize_url(state)
    
    async def authorize_user(
            self, authorization_code: str, state: str
        ) -> tuple[HHUserDTO, OauthTokensDTO]:
        await self.validate_state(state)

        hh_tokens_dto = await self.get_hh_tokens(authorization_code)
        hh_user_dto = await self.get_hh_user_info(hh_tokens_dto.access_token)

        return hh_user_dto, hh_tokens_dto
    
    async def get_hh_tokens(self, authorization_code: str) -> OauthTokensDTO:
        async with self.hh_client() as client:
            tokens_data = await client.make_token_request(authorization_code)
        
        return OauthTokensDTO(**tokens_data)
    
    async def get_hh_user_info(self, access_token: str) -> HHUserDTO:
        async with self.hh_client() as client:
            hh_user_data = await client.make_me_request(access_token)
            
        return HHUserDTO(**hh_user_data)

    async def generate_state(self) -> str:
        state = secrets.token_urlsafe(16)
        await self.state_repo.create_ex(state)

        return state
    
    async def validate_state(self, state: str) -> int:
        result = await self.state_repo.get(state)

        if not result:
            raise RuntimeError('CSRF protection failed')  # TODO change to custom app exception
        
        await self.state_repo.delete(state)

        