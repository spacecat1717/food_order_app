from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from db.mixins.crud_mixin import CRUDMixin
from db.models.base import Base


class User(Base, CRUDMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    full_name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[str] = mapped_column(String(128))

    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str):
        query = select(cls).where(cls.username == name)
        result = await session.execute(query)
        return result.scalars().first()

