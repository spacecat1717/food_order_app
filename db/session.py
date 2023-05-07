from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from db.settings.main import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
