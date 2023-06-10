from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import String, ForeignKey, Integer, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.mixins.crud_mixin import CRUDMixin
from db.models.base import Base
from db.utils.enums import OrderStatusEnum, DishStatusEnum


class Order(Base, CRUDMixin):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    comment: Mapped[str] = mapped_column(String(256))
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    closed: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), default=OrderStatusEnum.ACCEPTED)
    items: Mapped[Optional[List["OrderItem"]]] = relationship(lazy='joined')
    total: Mapped[Decimal] = mapped_column(default=0.0)


class OrderItem(Base, CRUDMixin):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    dish: Mapped[int] = mapped_column(ForeignKey('dishes.id'))
    quantity: Mapped[int] = mapped_column(Integer)
    total: Mapped[Decimal] = mapped_column(Numeric)
    status: Mapped[str] = mapped_column(String(32), default=DishStatusEnum.QUEUE)


