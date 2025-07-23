from abc import ABC
from typing import Any, Generic
from uuid import UUID

from redis.asyncio.client import Redis
from redis.typing import ExpiryT
from sqlalchemy import Select, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common_types import CreateDTOType, ReadDTOType, RedisHash, RedisPrimitive, UpdateDTOType
from src.app.infrastructure.database.base.models import ModelType


class AbstractSQLAlchemyRepository(
        ABC, Generic[ModelType, ReadDTOType, CreateDTOType, UpdateDTOType]
    ):
    model: type[ModelType]
    read_dto: type[ReadDTOType]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def refresh(self, read_dto: ReadDTOType) -> ReadDTOType:
        model_instance: ModelType = await self._session.get(self.model, read_dto.id)  # type: ignore[attr-defined]
        await self._session.refresh(model_instance)

        return self._to_dto(model_instance)

    async def create(self, create_dto: CreateDTOType) -> ReadDTOType:
        stmt = insert(self.model).values(create_dto.model_dump()).returning(self.model)
        result = await self._session.scalars(stmt)
        return self._to_dto(result.one())

    async def update(self, pk: int | UUID, update_dto: UpdateDTOType) -> ReadDTOType:
        stmt = (
            update(self.model)
            .where(self.model.id == pk)  # type: ignore[attr-defined]
            .values(update_dto.model_dump(exclude_none=True))
            .returning(self.model)
        )
        result = await self._session.scalars(stmt)
        return self._to_dto(result.one())

    async def get(self, *, with_related: bool = True, **kwargs: Any) -> ReadDTOType | None:
        stmt = select(self.model).filter_by(**kwargs)

        if with_related:
            stmt = self._apply_loader_options(stmt)
        
        result = await self._session.scalars(stmt)
        model_instance = result.one_or_none()

        return self._to_dto(model_instance) if model_instance else None

    async def filter(self, *, with_related: bool = True, **kwargs: Any) -> list[ReadDTOType]:
        stmt = select(self.model).filter_by(**kwargs)

        if with_related:
            stmt = self._apply_loader_options(stmt)
        
        result = await self._session.scalars(stmt)
        return [
            self._to_dto(instance)
            for instance in result.all()
        ]

    async def delete(self, pk: int | UUID) -> None:
        stmt = delete(self.model).where(self.model.id == pk)  # type: ignore[attr-defined]
        await self._session.execute(stmt)
    
    def _to_dto(self, model: ModelType, from_attributes: bool = True) -> ReadDTOType:
        return self.read_dto.model_validate(model, from_attributes=from_attributes)

    def _apply_loader_options(self, stmt: Select) -> Select:
        return stmt


class AbstractRedisRepository:
    def __init__(
            self, redis_client: Redis,
            key_namespace: str | None = None,
            default_exp: ExpiryT = 300
        ) -> None:
        self.key_namespace = key_namespace if key_namespace else ""
        self.redis_client: Redis = redis_client
        self.default_exp = default_exp
    
    def _add_namespace_to_key(self, key: str) -> str:
        return f"{self.key_namespace}{key}"
    
    async def create(
            self, key: str,
            value: RedisPrimitive = "ok",
            exp: ExpiryT | None = None
        ) -> None:
        key = self._add_namespace_to_key(key)
        await self.redis_client.set(name=key, value=value, ex=exp)
    
    async def create_ex(
            self, key: str,
            value: RedisPrimitive = "ok",
            exp: ExpiryT | None = None
        ) -> None:
        exp = exp if exp else self.default_exp
        await self.create(key=key, value=value, exp=exp)

    async def create_hash(
            self, key: str,
            mapping: RedisHash,
            exp: ExpiryT | None = None
        ) -> None:
        key = self._add_namespace_to_key(key)
        await self.redis_client.hset(key, mapping=mapping)  # type: ignore[reportGeneralTypeIssues]
        
        if exp:
            await self.redis_client.expire(key, exp)

    async def create_hash_ex(
            self, key: str,
            mapping: RedisHash,
            exp: ExpiryT | None = None
        ) -> None:
        exp = exp if exp else self.default_exp
        await self.create_hash(key=key, mapping=mapping, exp=exp)
    
    async def get(self, key: str) -> str | None:
        key = self._add_namespace_to_key(key)
        return await self.redis_client.get(key)
    
    async def delete(self, key: str) -> None:
        key = self._add_namespace_to_key(key)
        await self.redis_client.delete(key)
