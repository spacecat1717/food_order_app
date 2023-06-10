from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session, engine
from db.models.base import Base

# я пока хз куда это было бы правильно вынести, так что будет тут временно


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        return session
