from fastapi import FastAPI

from routers.dishes import dishes_router

app = FastAPI(title='Food order app with queues')

app.include_router(dishes_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



# TODO: returns 422 code (something wrong with the schema
# @app.post('/dishes', response_model=food.Dish, status_code=201)
# async def create_dish(request: food.Dish, session: AsyncSession = Depends(get_async_session)):
#     if await Dish.get_by_name(session, request.name):
#         raise HTTPException(status_code=400, detail='This dish already exists!')
#     ingredients = []
#     for item in request.ingredients:
#         ingredients.append(await Ingredient.get_by_id(session, item.id))
#     return await Dish.create(session, name=request.name, ingredients=ingredients, price=request.price)
