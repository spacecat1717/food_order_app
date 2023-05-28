from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'lettuce'
            }
        }


class Dish(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    ingredients: Optional[List[Ingredient]]
    price: Decimal = Field(default=0.0)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'burger',
                'ingredients': [
                    {
                    'id': 1,
                    'name': 'lettuce'
                    },
                    {
                        'id': 2,
                        'name': 'tomato'
                    },
                    {
                        'id': 3,
                        'name': 'sauce'
                    }
                ]
            }
        }


class DishCreate(BaseModel):
    name: str = Field(...)
    ingredients: Optional[List[Ingredient]]
    price: Decimal = Field(default=0.0)


class IngredientCreate(BaseModel):
    name: str = Field(...)
