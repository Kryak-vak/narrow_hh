from pydantic import BaseModel, HttpUrl


class AuthStartPayloadSchema(BaseModel):
    state: str
    redirect_url: HttpUrl


class AuthCallbackPayloadSchema(BaseModel):
    code: str
    state: str


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str