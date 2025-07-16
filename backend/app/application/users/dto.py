from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.application.common.dto import AbstractTokenBaseDTO, AbstractTokenUpdateDTO


# User DTO's
class UserBaseDTO(BaseModel):
    hh_user_id: str


class UserDTO(UserBaseDTO):
    id: UUID
    hh_token: Optional["TokenNestedDTO"] = None
    token: Optional["TokenNestedDTO"] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(UserBaseDTO):
    pass


class UserUpdateDTO(UserBaseDTO):
    pass


# Token DTO's (for both HeadHunterToken and UserToken)
class TokenBaseDTO(AbstractTokenBaseDTO):
    pass


class TokenNestedDTO(TokenBaseDTO):
    id: int


class TokenDTO(TokenNestedDTO):
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)


class TokenCreateDTO(TokenBaseDTO):
    user_id: UUID


class TokenUpdateDTO(AbstractTokenUpdateDTO):
    pass


UserDTO.model_rebuild()
