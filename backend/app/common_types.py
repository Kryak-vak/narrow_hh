from typing import Dict, TypeVar, Union

from pydantic import BaseModel

ReadDTOType = TypeVar("ReadDTOType", bound=BaseModel)
CreateDTOType = TypeVar("CreateDTOType", bound=BaseModel)
UpdateDTOType = TypeVar("UpdateDTOType", bound=BaseModel)


RedisPrimitive = Union[str, int, float, bytes]
RedisHash = Dict[str, str]