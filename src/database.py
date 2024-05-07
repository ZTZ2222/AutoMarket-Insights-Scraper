from collections.abc import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.utils.logger.logging import AppLogger


logger = AppLogger().get_logger()

engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    future=True,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session
