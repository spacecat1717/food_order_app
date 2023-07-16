from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import String, ForeignKey, Integer, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.mixins.crud_mixin import CRUDMixin
from db.models.base import Base
from db.models.user import User
from db.utils.enums import OrderStatusEnum, DishStatusEnum


class Order(Base, CRUDMixin):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='orders')
    comment: Mapped[str] = mapped_column(String(256), default='')
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    closed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=OrderStatusEnum.ACCEPTED)
    items: Mapped[List["OrderItem"]] = relationship(back_populates='order', lazy='joined')
    total: Mapped[Decimal] = mapped_column(default=0.0)


class OrderItem(Base, CRUDMixin):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey('dishes.id'))
    dish: Mapped["Dish"] = relationship(lazy='joined')
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    order: Mapped["Order"] = relationship(back_populates='items')
    quantity: Mapped[int] = mapped_column(Integer)
    total: Mapped[Decimal] = mapped_column(Numeric)
    status: Mapped[str] = mapped_column(String(32), default=DishStatusEnum.QUEUE)
