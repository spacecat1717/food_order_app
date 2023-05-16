from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str = Field(...)

    class Config:
        schema_extra = {
            'example': {
                'name': 'lettuce'
            }
        }


class Dish(BaseModel):
    name: str = Field(...)
    ingredients: List[Ingredient] | None = None
    price: Decimal = Field(default=0.0)

    class Config:
        schema_extra = {
            'example': {
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
