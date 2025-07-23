from typing import TypeVar

from pydantic import BaseModel

ReadDTOType = TypeVar("ReadDTOType", bound=BaseModel)
CreateDTOType = TypeVar("CreateDTOType", bound=BaseModel)
UpdateDTOType = TypeVar("UpdateDTOType", bound=BaseModel)


RedisPrimitive = str | int | float | bytes
RedisHash = dict[str, str]