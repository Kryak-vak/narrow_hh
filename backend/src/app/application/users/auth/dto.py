from enum import StrEnum

from pydantic import BaseModel


class JWTPairDTO(BaseModel):
    access_token: str
    refresh_token: str


class JWTEntity(BaseModel):
    user_id: str
    type: "JWTType"
    expire: str


class JWTType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
