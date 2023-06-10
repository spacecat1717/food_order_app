from enum import Enum


class OrderStatusEnum(str, Enum):
    ACCEPTED = 'Принят'
    COOKING = 'Готовится'
    PACKING = 'Собирается'
    READY = 'Готов к выдаче'


class DishStatusEnum(str, Enum):
    QUEUE = 'В очереди'
    PREPARING = 'Подготовка ингредиентов'
    COOKING = 'Готовится'
    PACKING = 'Собирается'
    DONE = 'Готово'