from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.order import Order, OrderItem
from db.utils.utils import get_async_session
from schemas import order
from schemas import user as us
from routers.utils import QuantityEnum
from routers.user import get_current_user


order_router = APIRouter(prefix='/order')

instance = order.OrderCreate()


async def is_item_added(item: order.OrderItem) -> bool:
    if instance.items and item in instance.items:
        return True
    else:
        return False

# TODO: need refactor
async def increment_quantity(item_id: int):
    for item in instance.items:
        if item.id == item_id:
            item.quantity += 1
            item.total = item.total * 2

# TODO: need refactor
async def decrement_quantity(item_id: int):
    for item in instance.items:
        if item.id == item_id:
            item.total = item.total // 2
            if item.quantity > 1:
                item.quantity -= 1
            else:
                instance.items.remove(item)


@order_router.get('/', response_model=order.OrderCreate, tags=['order'])
async def get_order() -> order.OrderCreate:
    return instance


@order_router.post('/create', status_code=201, tags=['order'])
async def add_item(item: order.OrderItem) -> dict:
    if await is_item_added(item):
        await increment_quantity(item.id)
    item.id = len(instance.items) + 1
    instance.items.append(item)
    return {'status': 'ok', 'data': f'Item {item.dish.name} has been added successfully'}


@order_router.delete('/delete', status_code=201, tags=['order'])
async def delete_item(item: order.OrderItem) -> dict:
    if not await is_item_added(item):
        raise HTTPException(status_code=400, detail=f'Item {item.dish.name} is not in your order and cannot be deleted')
    instance.items.remove(item)
    return {'status': 'ok', 'data': f'Item {item.dish.name} has been deleted successfully'}


@order_router.post('/change_quantity', tags=['order'])
async def change_quantity(item_id: int, type: int):
    match type:
        case QuantityEnum.INCREMENT:
            await increment_quantity(item_id)
        case QuantityEnum.DECREMENT:
            await decrement_quantity(item_id)
    return {'status': 'ok', 'data': 'Quantity of has been changed successfully'}


@order_router.get('/save', response_model=order.Order, tags=['order'])
async def save_order(request: Request, user: Annotated[us.User, Depends(get_current_user)],
                     session: AsyncSession = Depends(get_async_session)):
    order = await Order.create(session)
    return order
