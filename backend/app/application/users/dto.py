from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# User DTO's
class UserDTO(BaseModel):
    id: UUID
    token: Optional["HeadHunterTokenNestedDTO"] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(BaseModel):
    pass


class UserUpdateDTO(BaseModel):
    pass


# HeadHunterToken DTO's
class HeadHunterTokenBaseDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_in: int


class HeadHunterTokenNestedDTO(HeadHunterTokenBaseDTO):
    id: int


class HeadHunterTokenDTO(HeadHunterTokenNestedDTO):
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)


class HeadHunterTokenCreateDTO(HeadHunterTokenBaseDTO):
    user_id: UUID


class HeadHunterTokenUpdateDTO(BaseModel):
    token_type: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None


UserDTO.model_rebuild()
