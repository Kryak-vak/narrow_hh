from uuid import UUID

from pydantic import BaseModel, ConfigDict


# User DTO's
class UserDTO(BaseModel):
    id: UUID
    auth_profile: "TelegramProfileNestedDTO" | None = None
    token: "UserTokenNestedDTO" | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(BaseModel):
    pass


class UserUpdateDTO(BaseModel):
    pass


# TelegramProfile DTO's
class TelegramProfileBaseDTO(BaseModel):
    telegram_id: int


class TelegramProfileNestedDTO(TelegramProfileBaseDTO):
    id: int


class TelegramProfileDTO(TelegramProfileNestedDTO):
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)


class TelegramProfileCreateDTO(TelegramProfileBaseDTO):
    user_id: UUID


class TelegramProfileUpdateDTO(BaseModel):
    telegram_id: int | None = None


# UserToken DTO's
class UserTokenBaseDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_in: int


class UserTokenNestedDTO(UserTokenBaseDTO):
    id: int


class UserTokenDTO(UserTokenNestedDTO):
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)


class UserTokenCreateDTO(UserTokenBaseDTO):
    user_id: UUID


class UserTokenUpdateDTO(BaseModel):
    token_type: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None


BaseModel.model_rebuild()
