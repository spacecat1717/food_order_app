from typing import List, Optional, Any

from sqlalchemy import String, ForeignKey, Integer, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    comment: Mapped[str] = mapped_column(String(256))
    created: Mapped[Any] = mapped_column(DateTime(timezone=True))
    closed: Mapped[Any] = mapped_column(DateTime(timezone=True))
    items: Mapped[Optional[List["OrderItem"]]] = relationship()


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    dish: Mapped[int] = mapped_column(ForeignKey('dishes.id'))
    quantity: Mapped[int] = mapped_column(Integer)
    total: Mapped[Numeric] = mapped_column(Numeric)

