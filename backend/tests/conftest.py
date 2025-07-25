from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
import pytest_asyncio
from alembic import config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

BASE_PATH = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def db() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer(
        image="postgres:17-alpine",
        driver="asyncpg"
    ) as db:
        yield db


@pytest_asyncio.fixture(scope="session")
async def engine(db: PostgresContainer) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        db.get_connection_url(),                      
        poolclass=NullPool,
    )
    
    await run_migrations_programmatically(engine)

    yield engine

    await engine.dispose()


async def run_migrations_programmatically(engine: AsyncEngine) -> None:
    alembic_test_env_path = BASE_PATH / "tests/alembic_test_env/"

    alembic_cfg = config.Config()
    alembic_cfg.set_main_option("script_location", str(alembic_test_env_path))
    script = ScriptDirectory.from_config(alembic_cfg)

    def do_run_migrations_sync(connection):
        def upgrade_to_head_fn(rev, context):
            return script._upgrade_revs("head", rev)

        ec = EnvironmentContext(
            alembic_cfg,
            script,
            connection=connection,
            fn=upgrade_to_head_fn,
        )
        ec.configure(
            connection=connection, fn=upgrade_to_head_fn
        )

        ec.run_migrations()

    async with engine.begin() as connection:
        await connection.run_sync(do_run_migrations_sync)


@pytest_asyncio.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        yield session
