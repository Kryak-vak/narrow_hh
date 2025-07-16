from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.csrf import StateManager
from app.application.hh.auth.dto import OauthTokenDTO
from app.infrastructure.clients import HHAsyncClient


class HHOAuthService():
    def __init__(
            self, session: AsyncSession,
            state_manager: StateManager
        ) -> None:
        self.session = session

        self.state_manager = state_manager
        self.hh_client = HHAsyncClient
    
    async def get_user_authorize_url(self, state: str) -> str:
        return self.hh_client.create_user_authorize_url(state)
    
    async def authorize_user(
            self, authorization_code: str, state: str
        ) -> OauthTokenDTO:
        await self.state_manager.validate_state(state)

        hh_oauth_tokens_dto = await self.get_tokens(authorization_code)

        return hh_oauth_tokens_dto
    
    async def get_tokens(self, authorization_code: str) -> OauthTokenDTO:
        async with self.hh_client() as client:
            oauth_tokens_data = await client.make_token_request(authorization_code)
        
        return OauthTokenDTO(**oauth_tokens_data)

        