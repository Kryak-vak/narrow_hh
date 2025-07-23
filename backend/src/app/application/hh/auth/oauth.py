from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.hh.auth.dto import OauthTokenDTO
from src.app.infrastructure.clients import HHAsyncClient


class HHOAuthService():
    def __init__(
            self, session: AsyncSession,
        ) -> None:
        self.session = session
        self.hh_client = HHAsyncClient
    
    def get_user_authorize_url(self, state: str, redirect_uri: str) -> str:
        return self.hh_client.create_user_authorize_url(state, redirect_uri)
    
    async def authorize_user(
            self, authorization_code: str,
            redirect_uri: str,
        ) -> OauthTokenDTO:

        hh_oauth_tokens_dto = await self.get_tokens(authorization_code, redirect_uri)

        return hh_oauth_tokens_dto
    
    async def get_tokens(self, authorization_code: str, redirect_uri: str) -> OauthTokenDTO:
        async with self.hh_client() as client:
            oauth_tokens_data = await client.make_token_request(authorization_code, redirect_uri)
        
        return OauthTokenDTO(**oauth_tokens_data)

        