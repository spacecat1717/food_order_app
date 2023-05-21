from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'lettuce'
            }
        }


class Dish(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    ingredients: List[Ingredient] | None = None
    price: Decimal = Field(default=0.0)

    class Config:
        schema_extra = {
            'example': {
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
            }
        }
