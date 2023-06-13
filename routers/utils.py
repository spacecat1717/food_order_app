from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.food import Ingredient, DishTask
from schemas import food


async def create_nested_models_list(model: Union[Ingredient, DishTask],
                                    request_data: List[Union[food.Ingredient,
                                    food.DishTask, food.DishTaskCreate, food.IngredientCreate]], session: AsyncSession):
    models = []
    for item in request_data:
        try:
            instance = await model.get_by_id(session, item.id)
        except AttributeError:
            instance = None
        if not instance:
            instance = await model.create(session, **item.dict())
        models.append(instance)
    return models
