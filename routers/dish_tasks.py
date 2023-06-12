from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import food
from db.models.food import DishTask
from db.utils.utils import get_async_session

dish_task_router = APIRouter(prefix='/dish_tasks')


@dish_task_router.get('/', response_model=List[food.DishTask], tags=['dish_tasks'])
async def get_all_dish_tasks(session: AsyncSession = Depends(get_async_session)):
    """
    :param session: AsyncSession for db
    :return: List of all dish_tasks
    """
    return await DishTask.get_all(session)


@dish_task_router.get('/{task_id}', response_model=food.DishTask, tags=['dish_task'])
async def get_dish_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param task_id: id for required DishTask
    :param session: AsyncSession for db
    :return: DishTask
    """
    return await DishTask.get_by_id(session, task_id)


@dish_task_router.post('/', response_model=food.DishTask, status_code=201, tags=['dish_task'])
async def create_dish_task(request: food.DishTaskCreate, session: AsyncSession = Depends(get_async_session)):
    """
    :param request: data of the new DishTask
    :param session: AsyncSession for db
    :return: created DishTask
    """
    return await DishTask.create(session, **request.dict())


@dish_task_router.put('/{task_id}/change_position', response_model=food.DishTask, tags=['dish_task'])
async def update_dish_task_position(task_id: int, position: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param task_id: id of DishTask change to
    :param position: new position in queue
    :param session: AsyncSession for db
    :return: changed DishTask
    """
    task = await DishTask.get_by_id(session, task_id)
    await task.update(session, position=position)
    return task


@dish_task_router.put('/{task_id}/change_time', response_model=food.DishTask, tags=['dish_task'])
async def update_dish_task_time(task_id: int, time: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param task_id: id of DishTask change to
    :param time: new execution time
    :param session: AsyncSession for db
    :return: changed DishTask
    """
    task = await DishTask.get_by_id(session, task_id)
    await task.update(session, time=time)
    return task


@dish_task_router.delete('/{task_id}', tags=['dish_task'])
async def delete_dish_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    :param task_id: id of DishTask delete to
    :param session: AsyncSession for db
    :return: status
    """
    task = await DishTask.get_by_id(session, task_id)
    await task.delete(session)
    return {'status': 'ok'}