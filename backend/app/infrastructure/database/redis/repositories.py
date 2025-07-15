from redis import Redis

from app.infrastructure.database.base.repositories import AbstractRedisRepository
from config.redis import redis_config


class RedisStateRepository(AbstractRedisRepository):
    def __init__(self, redis_client: Redis) -> None:
        self._state_key_prefix = "oauth_state:"

        super().__init__(redis_client=redis_client)
    
    def _state_to_key(self, state: str) -> str:
        return f"{self._state_key_prefix}{state}"

    async def create_ex(
            self, state: str,
            value: str = "ok",
            exp: int = redis_config.state_exp
        ) -> None:
        state_key = self._state_to_key(state)
        await super().create_ex(state_key, value, exp)
    
    async def get(self, state: str) -> str | None:
        state_key = self._state_to_key(state)
        return await super().get(state_key)
    
    async def delete(self, state: str) -> None:
        state_key = self._state_to_key(state)
        await super().delete(state_key)