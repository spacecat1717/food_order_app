from typing import List, Optional

from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import Base


# TODO: надо нормальное имя для нее придумать
relation_table = Table(
    'relation_table',
    Base.metadata,
    Column('dish_id', ForeignKey('dishes.id')),
    Column('ingredient_id', ForeignKey('ingredients.id'))
)


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    ingredients: Mapped[Optional[List["Ingredient"]]] = relationship(secondary=relation_table, back_populates='dishes')


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    dishes: Mapped[Optional[List["Dish"]]] = relationship(secondary=relation_table, back_populates='ingredients')

