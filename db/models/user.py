from sqlalchemy import String
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

