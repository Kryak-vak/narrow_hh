import httpx

from config.hh import hh_config


class HHAsyncClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        default_headers = {
            "User-Agent": f"{hh_config.app_name}/1.0 ({hh_config.contact_email})"
        }
        
        headers = kwargs.pop("headers", {})
        headers = {**default_headers, **headers}

        super().__init__(headers=headers, *args, **kwargs)
