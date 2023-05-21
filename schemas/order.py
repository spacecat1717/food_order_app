from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from schemas.food import Dish


class OrderItem(BaseModel):
    id: int = Field(...)
    dish: Dish = Field(...)
    quantity: int = Field(default=0)
    total: Decimal = Field(default=0.0)

    class Config:
        schema_extra = {
            'example': {
                'dish': {
                    'id': 1,
                    'name': 'burger',
                    'ingredients': [
                        {
                            'name': 'lettuce'
                        },
                        {
                            'name': 'tomato'
                        },
                        {
                            'name': 'sauce'
                        }
                    ]
                },
                'quantity': 1,
                'total': 300.0
            }
        }


class Order(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    comment: str = Field(max_length=256)
    created: datetime = Field(...)
    closed: datetime = Field(default=None)
    status: str = Field(...)
    items: Optional[List[OrderItem]]
    total: Decimal = Field(default=0.0)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'John',
                'comment': 'More sause please',
                # TODO: проверить, что datetime будет нормально работать
                'created': '2023-05-10 22:53:47.503971',
                'closed':  None,
                'status': 'Готов к выдаче',
                'items': [
                    {
                        'dish': {
                            'name': 'burger',
                            'ingredients': [
                                {
                                    'name': 'lettuce'
                                },
                                {
                                    'name': 'tomato'
                                },
                                {
                                    'name': 'sauce'
                                }
                            ]
                        },
                        'quantity': 1,
                        'total': 300.0
                    },
                    {
                        'dish': {
                            'name': 'cola',
                            'ingredients': [
                                {
                                    'name': 'coca-cola'
                                }
                            ]
                        },
                        'quantity': 1,
                        'total': 150.0
                    },
                ],
                'total': 450.0
            }
        }

