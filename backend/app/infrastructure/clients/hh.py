from urllib.parse import urlencode

import httpx

from config.hh import hh_config


class HHAsyncClient(httpx.AsyncClient):
    authorize_url = "https://hh.ru/oauth/authorize"
    token_url = 'https://api.hh.ru/token'
    me_url = 'https://api.hh.ru/me'
    client_id = hh_config.client_id
    secret_key = hh_config.client_secret
    redirect_uri = hh_config.redirect_uri

    def __init__(self, *args, **kwargs) -> None:
        default_headers = {
            "User-Agent": f"{hh_config.app_name}/1.0 ({hh_config.contact_email})"
        }
        
        headers = kwargs.pop("headers", {})
        headers = {**default_headers, **headers}

        super().__init__(headers=headers, *args, **kwargs)
    
    @classmethod
    async def create_user_authorize_url(cls, state: str) -> str:
        query = urlencode({
            "response_type": "code",
            "client_id": cls.client_id,
            "redirect_uri": cls.redirect_uri,
            "state": state
        })

        return f"{cls.authorize_url}?{query}"

    async def make_token_request(self, authorization_code: str):
        headers = {
            **self.headers,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.secret_key,
            "redirect_uri": self.redirect_uri,
            "code": authorization_code,
        }

        response = await self.post(
            self.token_url,
            headers=headers,
            data=data,
        )

        return response.json()
    
    async def make_me_request(self, access_token: str):
        headers = {
            **self.headers,
            "Authorization": f"Bearer {access_token}"
        }

        response = await self.get(
            self.me_url,
            headers=headers
        )

        return response.json()