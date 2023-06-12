from fastapi import FastAPI

from routers.dishes import dishes_router
from routers.ingredients import ing_router
from routers.user import user_router
from routers.dish_tasks import dish_task_router

app = FastAPI(title='Food order app with queues')

app.include_router(dishes_router)
app.include_router(ing_router)
app.include_router(user_router)
app.include_router(dish_task_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

