from redis import Redis


class RedisStateRepository:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def create_ex(self, key: str, value: str, exp: int) -> None:
        await self.redis.setex(key, exp, value)
    
    async def get(self, key: str) -> str | None:
        value = await self.redis.get(key)

        return value
    
    async def delete(self, key: str) -> None:
        await self.redis.delete(key)