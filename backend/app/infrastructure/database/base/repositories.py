from abc import ABC
from typing import Generic
from uuid import UUID

from redis import Redis
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common_types import CreateDTOType, ReadDTOType, UpdateDTOType
from app.infrastructure.database.base.models import ModelType


class AbstractSQLAlchemyRepository(
        ABC, Generic[ModelType, ReadDTOType, CreateDTOType, UpdateDTOType]
    ):
    model: type[ModelType]
    read_dto: type[ReadDTOType]

    def __init__(self, session: AsyncSession):
        self._session = session
    
    def _to_dto(self, model: ModelType, from_attributes: bool = True) -> ReadDTOType:
        return self.read_dto.model_validate(model, from_attributes=from_attributes)

    async def create(self, create_dto: CreateDTOType) -> ReadDTOType:
        stmt = insert(self.model).values(create_dto.model_dump()).returning(self.model)
        result = await self._session.scalar(stmt)
        return self._to_dto(result)

    async def update(self, pk: int | UUID, update_dto: UpdateDTOType) -> ReadDTOType:
        stmt = (
            update(self.model)
            .where(self.model.id == pk)  # type: ignore[attr-defined]
            .values(update_dto.model_dump(exclude_none=True))
            .returning(self.model)
        )
        result = await self._session.scalar(stmt)
        return self._to_dto(result)

    async def get(self, **kwargs: str | UUID) -> ReadDTOType:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self._session.scalar(stmt)
        return self._to_dto(result) if result else None

    async def filter(self, **kwargs: str | UUID) -> list[ReadDTOType]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self._session.scalars(stmt)
        return [
            self._to_dto(instance)
            for instance in result.all()
        ]

    async def delete(self, pk: int | UUID) -> None:
        stmt = delete(self.model).where(self.model.id == pk)  # type: ignore[attr-defined]
        await self._session.scalar(stmt)


class AbstractRedisRepository:
    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client
    
    async def create(self, key: str, value) -> None:
        await self.redis_client.set(key, value)

    async def create_ex(
            self, key: str,
            value: str = "ok",
            exp: int = 300
        ) -> None:
        await self.redis_client.setex(key, exp, value)
    
    async def get(self, key: str) -> str | None:
        return await self.redis_client.get(key)
    
    async def delete(self, key: str) -> None:
        await self.redis_client.delete(key)
