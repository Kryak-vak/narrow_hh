from redis.asyncio.client import Redis

from src.app.infrastructure.database.base.repositories import AbstractRedisRepository
from src.config.redis import redis_config


class RedisStateRepository(AbstractRedisRepository):
    def __init__(self, redis_client: Redis) -> None:
        super().__init__(
            redis_client=redis_client,
            key_namespace="oauth_state:",
            default_exp=redis_config.state_exp
        )