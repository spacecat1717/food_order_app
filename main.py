from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import food
from db.models.food import Dish, Ingredient
from db.utils.utils import get_async_session

app = FastAPI(title='Food order app with queues')

@app.get("/")
async def root():
    return {"message": "Hello World"}

# TODO: find the way to move endpoints to the different files


@app.get('/dishes', response_model=List[food.Dish])
async def get_all_dishes(session: AsyncSession = Depends(get_async_session)):
    """
    :param session: AsyncSession for db
    :return: List of all dishes
    """
    return await Dish.get_all(session)


@app.get('/dishes/{dish_id}', response_model=food.Dish)
async def get_dish(dish_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param dish_id: identifier of required dish
    :param session: AsyncSession for db
    :return: required dish data
    """
    return await Dish.get_by_id(session, dish_id)

# TODO: returns 422 code (something wrong with the schema
@app.post('/dishes', response_model=food.Dish, status_code=201)
async def create_dish(request: food.Dish, session: AsyncSession = Depends(get_async_session)):
    if await Dish.get_by_name(session, request.name):
        raise HTTPException(status_code=400, detail='This dish already exists!')
    ingredients = []
    for item in request.ingredients:
        ingredients.append(await Ingredient.get_by_id(session, item.id))
    return await Dish.create(session, name=request.name, ingredients=ingredients, price=request.price)
