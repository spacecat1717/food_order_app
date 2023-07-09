from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import food
from db.models.food import Dish, Ingredient, DishTask
from db.utils.utils import get_async_session
from routers.utils import create_nested_models_list, raise_not_found

dishes_router = APIRouter(prefix="/dishes")


@dishes_router.get('/', response_model=List[food.Dish], tags=['dishes'])
async def get_all_dishes(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    :param request:
    :param session: AsyncSession for db
    :return: List of all dishes
    """
    dishes = await Dish.get_all(session)
    for dish in dishes:
        dish.url = str(request.url_for('get_dish', dish_id=dish.id))
    return dishes


async def get_dish_nested_links(dish: Dish, request: Request):
    for ing in dish.ingredients:
        ing.url = str(request.url_for('get_ingredient', ing_id=ing.id))
    for task in dish.tasks:
        task.url = str(request.url_for('get_dish_task', task_id=task.id))
    return dish


@dishes_router.get('/{dish_id}', response_model=food.Dish, tags=['dish'])
async def get_dish(request: Request, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param request: Request obj
    :param dish_id: identifier of required dish
    :param session: AsyncSession for db
    :return: required dish data
    """
    dish = await Dish.get_by_id(session, dish_id)
    if not dish:
        await raise_not_found(request)
        return
    return await get_dish_nested_links(dish, request)


@dishes_router.post('/', response_model=food.Dish, status_code=201, tags=['dish'])
async def create_dish(request: food.DishCreate, session: AsyncSession = Depends(get_async_session)):
    """
    :param request: dish schema
    :param session: AsyncSession for db
    :return: created dish data
    """
    if await Dish.get_by_name(session, request.name):
        raise HTTPException(status_code=400, detail='This dish already exists!')
    ingredients = await create_nested_models_list(Ingredient, request.ingredients, session)
    tasks = await create_nested_models_list(DishTask, request.tasks, session)
    return await Dish.create(session, name=request.name, ingredients=ingredients, tasks=tasks, price=request.price)


@dishes_router.put('/{dish_id}/change_price', response_model=food.Dish, tags=['dish'])
async def update_price(dish_id: int, request: Request, price: Decimal, session: AsyncSession = Depends(get_async_session)):
    """
    :param request: Request obj
    :param dish_id: id of dish change to
    :param price: new price
    :param session: AsyncSession for db
    :return: changed dish
    """
    dish = await Dish.get_by_id(session, dish_id)
    await dish.update(session, price=price)
    await get_dish_nested_links(dish, request)
    return dish


@dishes_router.put('/{dish_id}/change_ingredients', response_model=food.Dish, tags=['dish'])
async def update_ingredients(dish_id: int, request: Request, ingredients: List[food.Ingredient],
                             session: AsyncSession = Depends(get_async_session)):
    """
    :param request: Request obj
    :param dish_id: id of dish change to
    :param ingredients: list of new ingredients
    :param session: AsyncSession for db
    :return: changed dish
    """
    dish = await Dish.get_by_id(session, dish_id)
    new_ingredients = [await Ingredient.get_by_id(session, ing.id) for ing in ingredients]
    await dish.update(session, ingredients=new_ingredients)
    await get_dish_nested_links(dish, request)
    return dish


@dishes_router.put('/{dish_id}/change_tasks', response_model=food.Dish, tags=['dish'])
async def update_dish_tasks(dish_id: int, request:Request, tasks: List[food.DishTask],
                            session: AsyncSession = Depends(get_async_session)):
    """
    :param request: Request obj
    :param dish_id: id if Dish change to
    :param tasks: list of new tasks
    :param session: AsyncSession for db
    :return: changed Dish
    """
    dish = await Dish.get_by_id(session, dish_id)
    new_tasks = [await DishTask.get_by_id(session, task.id) for task in tasks]
    await dish.update(session, tasks=new_tasks)
    await get_dish_nested_links(dish, request)
    return dish


@dishes_router.delete('/{dish_id}', tags=['dish'])
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param dish_id: id of a dish delete to
    :param session: AsyncSession for db
    :return: status
    """
    dish = await Dish.get_by_id(session, dish_id)
    await dish.delete(session)
    return {'status': 'ok'}
