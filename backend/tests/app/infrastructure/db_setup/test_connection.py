import asyncpg
import pytest
import sqlalchemy
from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from testcontainers.postgres import PostgresContainer


@pytest.mark.asyncio
async def test_db_connection(db: PostgresContainer):
    pure_conn_url = db.get_connection_url().replace("postgresql+asyncpg", "postgresql")
    connection: Connection = await asyncpg.connect(dsn=pure_conn_url)
    try:
        version = await connection.fetchval("SELECT version();")
    finally:
        await connection.close()

    assert "PostgreSQL" in str(version)


@pytest.mark.asyncio
async def test_engine_connection(engine: AsyncEngine):
    async with engine.connect() as connection:
        result = await connection.execute(sqlalchemy.text("SELECT version()"))
        version = result.fetchone()
    
    assert "PostgreSQL" in str(version)