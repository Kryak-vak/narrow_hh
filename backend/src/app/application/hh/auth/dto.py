from pydantic import BaseModel


class OauthTokenDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_in: int


class HeadHunterUserDTO(BaseModel):
    id: str
