from fastapi import FastAPI

from routers.dishes import dishes_router
from routers.ingredients import ing_router

app = FastAPI(title='Food order app with queues')

app.include_router(dishes_router)
app.include_router(ing_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

