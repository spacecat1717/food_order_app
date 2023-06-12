import asyncio
from typing import List, Optional

from sqlalchemy import String, Column, Table, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.mixins.crud_mixin import CRUDMixin


# TODO: надо нормальное имя для нее придумать
relation_table = Table(
    'relation_table',
    Base.metadata,
    Column('dish_id', ForeignKey('dishes.id')),
    Column('ingredient_id', ForeignKey('ingredients.id'))
)

dish_task_table = Table(
    'dish_task_table',
    Base.metadata,
    Column('dish.id', ForeignKey('dishes.id')),
    Column('dishtask.id', ForeignKey('dish_tasks.id'))
)


class Dish(Base, CRUDMixin):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    ingredients: Mapped[Optional[List["Ingredient"]]] = relationship(secondary=relation_table, back_populates='dishes',
                                                                     lazy='joined')
    tasks: Mapped[Optional[List["DishTask"]]] = relationship(secondary=dish_task_table, back_populates='dishes',
                                                             lazy='joined')
    price: Mapped[int] = mapped_column(Numeric, default=300)


class Ingredient(Base, CRUDMixin):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    dishes: Mapped[Optional[List["Dish"]]] = relationship(secondary=relation_table, back_populates='ingredients')


class DishTask(Base, CRUDMixin):
    __tablename__ = 'dish_tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128))
    dishes: Mapped[Optional[List["Dish"]]] = relationship(secondary=dish_task_table, back_populates='tasks')
    position: Mapped[int] = mapped_column(Integer)
    time: Mapped[int] = mapped_column(Integer)

    async def execute(self) -> str:
        # временная штука для симуляции какого то действия, можно доработать
        await asyncio.sleep(self.time)
        return f'{self.__class__.__name__} {self.name} done!'
