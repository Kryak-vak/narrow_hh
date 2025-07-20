from uuid import UUID

from pydantic import BaseModel, ConfigDict


# User DTO's
class UserBaseDTO(BaseModel):
    hh_user_id: str


class UserDTO(UserBaseDTO):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(UserBaseDTO):
    pass


class UserUpdateDTO(UserBaseDTO):
    pass


# UserToken DTO's
class UserRefreshTokenBaseDTO(BaseModel):
    id: str
    user_id: UUID


class UserRefreshTokenDTO(UserRefreshTokenBaseDTO):
    is_blacklisted: bool = False


class UserRefreshTokenCreateDTO(UserRefreshTokenBaseDTO):
    pass


class UserRefreshTokenUpdateDTO(BaseModel):
    is_blacklisted: bool = False


# HeadHunterToken DTO's
class HeadHunterTokenBaseDTO(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class HeadHunterTokenNestedDTO(BaseModel):
    id: int


class HeadHunterTokenDTO(HeadHunterTokenBaseDTO):
    id: int
    user_id: UUID


class HeadHunterTokenCreateDTO(HeadHunterTokenBaseDTO):
    user_id: UUID


class HeadHunterTokenUpdateDTO(BaseModel):
    access_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    refresh_token: str | None = None


UserDTO.model_rebuild()
