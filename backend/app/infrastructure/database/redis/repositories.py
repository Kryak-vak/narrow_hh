from redis import Redis

from config.redis import redis_config


class RedisStateRepository:
    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client
        self._state_key_prefix = "oauth_state:"
    
    def _state_to_key(self, state: str) -> str:
        return f"{self._state_key_prefix}{state}"

    async def create_ex(self, state: str, value: str, exp: int = redis_config.state_exp) -> None:
        state_key = self._state_to_key(state)
        await self.redis_client.setex(state_key, exp, value)
    
    async def get(self, state: str) -> str | None:
        state_key = self._state_to_key(state)
        value = await self.redis_client.get(state_key)

        return value
    
    async def delete(self, state: str) -> None:
        state_key = self._state_to_key(state)
        await self.redis_client.delete(state_key)