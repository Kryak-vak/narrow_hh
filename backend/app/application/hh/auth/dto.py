from pydantic import BaseModel

from app.application.common.dto import AbstractTokenBaseDTO


class OauthTokenDTO(AbstractTokenBaseDTO):
    pass


class HeadHunterUserDTO(BaseModel):
    id: str
