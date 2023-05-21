from typing import List, Optional

from sqlalchemy import select
from sqlalchemy import String, Column, Table, ForeignKey, Numeric
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.mixins.crud_mixin import CRUDMixin
from db.utils.utils import get_async_session


# TODO: надо нормальное имя для нее придумать
relation_table = Table(
    'relation_table',
    Base.metadata,
    Column('dish_id', ForeignKey('dishes.id')),
    Column('ingredient_id', ForeignKey('ingredients.id'))
)


class Dish(Base, CRUDMixin):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    ingredients: Mapped[Optional[List["Ingredient"]]] = relationship(secondary=relation_table, back_populates='dishes',
                                                                     lazy='joined')
    price: Mapped[int] = mapped_column(Numeric, default=300)


class Ingredient(Base, CRUDMixin):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    dishes: Mapped[Optional[List["Dish"]]] = relationship(secondary=relation_table, back_populates='ingredients')

