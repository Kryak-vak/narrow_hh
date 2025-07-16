from pydantic import BaseModel


class AbstractTokenBaseDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_in: int


class AbstractTokenUpdateDTO(BaseModel):
    token_type: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None