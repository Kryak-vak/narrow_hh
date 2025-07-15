from pydantic import BaseModel


class OauthTokensDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_in: int


class HHUserDTO(BaseModel):
    id: str
