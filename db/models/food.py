import asyncio
from typing import List

from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from db.session import async_session, engine


class Base(DeclarativeBase):
    pass

# надо нормальное имя для нее придумать
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
    ingredients: Mapped[List["Ingredient"]] = relationship(secondary=relation_table, back_populates='dishes')


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    dishes: Mapped[List["Dish"]] = relationship(secondary=relation_table, back_populates='ingredients')

