from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import AsyncSessionLocal


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
