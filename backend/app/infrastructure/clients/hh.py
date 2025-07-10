import httpx

from core.config import settings


class HHAsyncClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        default_headers = {
            "User-Agent": f"{settings.HH_APP_NAME}/1.0 ({settings.HH_CONTACT_EMAIL})"
        }
        
        headers = kwargs.pop("headers", {})
        headers = {**default_headers, **headers}

        super().__init__(headers=headers, *args, **kwargs)