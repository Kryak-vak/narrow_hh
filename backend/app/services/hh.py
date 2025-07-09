import secrets
from urllib.parse import urlencode

from httpx import AsyncClient
from redis.asyncio import Redis

from app.infrastructure.clients import HHAsyncClient


class HHAuthService():
    def __init__(
            self, redis: Redis,
            client_id: str, secret_key: str,
            redirect_uri: str, state_exp: int
        ) -> None:
        self.redis = redis
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.state_exp = state_exp

        self.hh_authorize_url = 'https://hh.ru/oauth/authorize'
        self.hh_token_url = 'https://api.hh.ru/token'
        self.hh_client = HHAsyncClient
    
    async def create_authorize_url(self, telegram_user_id: int):
        state = await self.generate_state(telegram_user_id)

        query = urlencode({
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state
        })

        return f"{self.hh_authorize_url}?{query}"
    
    async def get_tokens(self, authorization_code: str, state: str) -> str:
        telegram_user_id = await self.validate_state_and_get_user(state)
        
        token_data = await self.make_token_request(authorization_code)
        
        return token_data
    
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

    async def generate_state(self, telegram_user_id: int) -> str:
        state = secrets.token_urlsafe(16)
        await self.redis.setex(f"oauth_state:{state}", self.state_exp, telegram_user_id)

        return state
    
    async def validate_state_and_get_user(self, state: str) -> int:
        telegram_user_id = await self.redis.get(f"oauth_state:{state}")
        if not telegram_user_id:
            raise RuntimeError('Invalid or expired state')
        
        await self.redis.delete(f"oauth_state:{state}")

        return int(telegram_user_id)

        