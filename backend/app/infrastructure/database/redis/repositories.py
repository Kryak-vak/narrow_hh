from redis import Redis

from core.config import settings


class RedisStateRepository:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self._state_key_prefix = "oauth_state:"
    
    def _state_to_key(self, state: str) -> str:
        return f"{self._state_key_prefix}{state}"

    async def create_ex(self, state: str, value: str, exp: int = settings.STATE_EXP) -> None:
        state_key = self._state_to_key(state)
        await self.redis.setex(state_key, exp, value)
    
    async def get(self, state: str) -> str | None:
        state_key = self._state_to_key(state)
        value = await self.redis.get(state_key)

        return value
    
    async def delete(self, state: str) -> None:
        state_key = self._state_to_key(state)
        await self.redis.delete(state_key)