import asyncio
from decimal import Decimal

from db.models.food import Dish, Ingredient
from db.utils.utils import get_async_session


async def main():
    async with await get_async_session() as session:
        ham = await Ingredient.create(session=session, name='ham')
        bread = await Ingredient.create(session=session, name='bread')
        cheese = await Ingredient.create(session=session, name='cheddar cheese')
        sauce = await Ingredient.create(session=session, name='sandwich sauce')
        lettuce = await Ingredient.get_by_name(session=session, name='lettuce')
        sandwich = await Dish.create(session=session,
                               name='ham sandwich',
                               ingredients=[ham, bread, sauce, lettuce, cheese],
                               price=Decimal(150.5)
                               )
        print(await Dish.get_by_name(session=session, name='ham sandwich'))


async def get_sandwich():
    async with await get_async_session() as session:
        sandwich = await Dish.get_by_name(session=session, name='ham sandwich')
        print('RES:', sandwich.ingredients[0].name)


async def get_all_dishes():
    async with await get_async_session() as session:
        dishes = await Dish.get_all(session=session)
        print(dishes[1].ingredients[2].name)


if __name__ == '__main__':
    asyncio.run(get_all_dishes())
