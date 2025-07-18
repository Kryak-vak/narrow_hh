import secrets

from app.common_types import RedisHash, RedisPrimitive
from app.infrastructure.database import RedisStateRepository


class StateManager:
    def __init__(self, state_repo: RedisStateRepository) -> None:
        self.state_repo = state_repo

    async def generate_state(self) -> str:
        state = secrets.token_urlsafe(16)
        return state
    
    async def set_state_ex(self, state: str, value: RedisPrimitive = "ok", exp: int = None):
        await self.state_repo.create_ex(state, value, exp)
    
    async def set_state_hash_ex(self, state: str, value: RedisHash, exp: int = None):
        await self.state_repo.create_hash_ex(state, value, exp)
    
    async def validate_state(self, state: str) -> int:
        result = await self.state_repo.get(state)

        if not result:
            raise RuntimeError('CSRF protection failed')  # TODO change to custom app exception
        
        await self.state_repo.delete(state)





