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


class DishTaskCreate(BaseModel):
    name: str = Field(...)
    position: int = Field(...)
    time: int = Field(default=60)


class DishTask(DishTaskCreate):
    id: int = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'Cutting vegetables',
                'position': 2,
                'time': 120
            }
        }


class Dish(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    ingredients: Optional[List[Ingredient]]
    tasks: Optional[List[DishTask]]
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
                ],
                'tasks': [
                    {
                        'id': 2,
                        'name': 'Roasting bread',
                        'position': 1,
                        'time': 90
                    },
                    {
                        'id': 1,
                        'name': 'Cutting vegetables',
                        'position': 2,
                        'time': 120
                    },
                ],
                'price': 500.0
            }
        }


class DishCreate(BaseModel):
    name: str = Field(...)
    ingredients: Optional[List[Ingredient]]
    tasks: Optional[List[DishTask]]
    price: Decimal = Field(default=0.0)


class IngredientCreate(BaseModel):
    name: str = Field(...)
