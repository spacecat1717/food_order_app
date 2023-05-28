from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import food
from db.models.food import Dish
from db.utils.utils import get_async_session

dishes_router = APIRouter(prefix="/dishes", tags=['dish', 'dishes'])


@dishes_router.get('/', response_model=List[food.Dish])
async def get_all_dishes(session: AsyncSession = Depends(get_async_session)):
    """
    :param session: AsyncSession for db
    :return: List of all dishes
    """
    return await Dish.get_all(session)


@dishes_router.get('/{dish_id}', response_model=food.Dish)
async def get_dish(dish_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param dish_id: identifier of required dish
    :param session: AsyncSession for db
    :return: required dish data
    """
    return await Dish.get_by_id(session, dish_id)
