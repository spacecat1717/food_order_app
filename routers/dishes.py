from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import food
from db.models.food import Dish, Ingredient
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


@dishes_router.post('/', response_model=food.Dish, status_code=201)
async def create_dish(request: food.DishCreate, session: AsyncSession = Depends(get_async_session)):
    """
    :param request: dish schema
    :param session: AsyncSession for db
    :return: created dish data
    """
    if await Dish.get_by_name(session, request.name):
        raise HTTPException(status_code=400, detail='This dish already exists!')
    ingredients = []
    for item in request.ingredients:
        ingredients.append(await Ingredient.get_by_id(session, item.id))
    return await Dish.create(session, name=request.name, ingredients=ingredients, price=request.price)


@dishes_router.put('/{dish_id}/change_price', response_model=food.Dish)
async def update_price(dish_id: int, price: Decimal, session: AsyncSession = Depends(get_async_session)):
    """
    :param dish_id: id of dish change to
    :param price: new price
    :param session: AsyncSession for db
    :return: changed dish
    """
    dish = await Dish.get_by_id(session, dish_id)
    await dish.update(session, price=price)
    return dish


@dishes_router.put('/{dish_id}/change_ingredients', response_model=food.Dish)
async def update_ingredients(dish_id: int, ingredients: List[food.Ingredient],
                             session: AsyncSession = Depends(get_async_session)):
    """
    :param dish_id: id of dish change to
    :param ingredients: list of new ingredients
    :param session: AsyncSession for db
    :return: changed dish
    """
    dish = await Dish.get_by_id(session, dish_id)
    new_ingredients = [await Ingredient.get_by_id(session, i.id) for i in ingredients]
    await dish.update(session, ingredients=new_ingredients)
    return dish


@dishes_router.delete('/{dish_id}')
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param dish_id: id of a dish delete to
    :param session: AsyncSession for db
    :return: status
    """
    dish = await Dish.get_by_id(session, dish_id)
    await dish.delete(session)
    return {'status': 'ok'}
