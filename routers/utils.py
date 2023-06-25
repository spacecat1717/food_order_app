from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.food import Ingredient, DishTask
from schemas import food


async def create_nested_models_list(model: Ingredient | DishTask,
                                    request_data: List[food.Ingredient | food.DishTask | food.DishTaskCreate
                                                       | food.IngredientCreate], session: AsyncSession):
    """
    creates list of nested models for create_dish  endpoint
    :param model: type of model to get/create
    :param request_data: serialized data of request
    :param session: AsyncSession for DB
    :return: list of got/created models
    """
    models = []
    for item in request_data:
        try:
            instance = await model.get_by_id(session, item.id)
        except AttributeError:
            instance = await model.create(session, **item.dict())
        models.append(instance)
    return models
