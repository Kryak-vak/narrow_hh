import secrets
from urllib.parse import urlencode

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.hh.auth.dto import OauthTokensDTO
from app.infrastructure.clients import HHAsyncClient
from app.infrastructure.database import RedisStateRepository
from app.infrastructure.database.users.repositories import HeadHunterTokenRepository


class HHOAuthService():
    def __init__(
            self,
            client_id: str, secret_key: str,
            redirect_uri: str,
            session: AsyncSession,
            state_repo: RedisStateRepository,
            hh_token_repo: HeadHunterTokenRepository
        ) -> None:
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri

        self.state_repo = state_repo
        
        self.session = session
        self.hh_token_repo = hh_token_repo
        self.hh_authorize_url = 'https://hh.ru/oauth/authorize'
        self.hh_token_url = 'https://api.hh.ru/token'
        self.hh_client = HHAsyncClient
    
    async def create_authorize_url(self):
        state = await self.generate_state()

        query = urlencode({
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state
        })

        return f"{self.hh_authorize_url}?{query}"
    
    async def get_tokens(self, authorization_code: str, state: str) -> str:
        await self.validate_state_and_get_user(state)
        
        tokens_data = await self.make_token_request(authorization_code)
        tokens_dto = OauthTokensDTO(**tokens_data)
        
        return tokens_dto
    
    async def make_token_request(self, authorization_code: str):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.secret_key,
            "redirect_uri": self.redirect_uri,
            "code": authorization_code,
        }

        async with self.hh_client() as client:
            token_response = await client.post(
                self.hh_token_url,
                headers=headers,
                data=data,
            )

        token_data = token_response.json()

        return token_data

    async def generate_state(self) -> str:
        state = secrets.token_urlsafe(16)
        await self.state_repo.create_ex(state)

        return state
    
    async def validate_state_and_get_user(self, state: str) -> int:
        await self.state_repo.get(state)
        # if not telegram_id:
            # raise RuntimeError('Invalid or expired state')
        
        await self.state_repo.delete(state)

        # return int(telegram_id)

        