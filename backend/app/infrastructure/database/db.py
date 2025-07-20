from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.database import database_config
from config.redis import redis_config

engine = create_async_engine(
    str(database_config.SQLALCHEMY_DATABASE_URI)
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)

redis_client = Redis(
    host=redis_config.host,
    port=redis_config.port,
    password=redis_config.password,
    decode_responses=True
)
