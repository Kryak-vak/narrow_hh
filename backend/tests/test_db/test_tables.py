
import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine

from src.app.infrastructure.database.migrations import Base


@pytest.fixture(scope="module")
def table_names() -> list[str]:
    return list(Base.metadata.tables)


@pytest.mark.asyncio
async def test_migrations_applied(engine: AsyncEngine, table_names: list[str]):
    async with engine.connect() as connection:
        for table_name in table_names:
            result = await connection.execute(
                sqlalchemy.text(
                    f"SELECT to_regclass('public.{table_name}')"
                )
            )
            
            found_table = result.scalar()
            assert found_table == table_name, f"Table '{table_name}' not found in DB"
