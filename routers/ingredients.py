from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import food
from db.models.food import Ingredient
from db.utils.utils import get_async_session


ing_router = APIRouter(prefix='/ingredients')


@ing_router.get('/', response_model=List[food.Ingredient], tags=['ingredients'])
async def get_all_ingredients(session: AsyncSession = Depends(get_async_session)):
    """
    :param session: AsyncSession for db
    :return: List of all ingredients
    """
    return await Ingredient.get_all(session)


@ing_router.get('/{ing_id}', response_model=food.Ingredient, tags=['ingredient'])
async def get_ingredient(ing_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param ing_id: id of required ingredient
    :param session: AsyncSession for db
    :return: required ingredient
    """
    return await Ingredient.get_by_id(session, ing_id)


@ing_router.post('/', response_model=food.Ingredient, tags=['ingredient'])
async def create_ingredient(request: food.IngredientCreate, session: AsyncSession = Depends(get_async_session)):
    """
    :param request: ingredient schema
    :param session: AsyncSession for db
    :return: new ingredient
    """
    return await Ingredient.create(session, **request.dict())


@ing_router.delete('/{ing_id}', tags=['ingredient'])
async def delete_ingredient(ing_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param ing_id: id of an ingredient delete to
    :param session: AsyncSession for db
    :return: status
    """
    ing = await Ingredient.get_by_id(session, ing_id)
    await ing.delete(session)
    return {'status': 'ok'}
