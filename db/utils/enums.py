from enum import Enum


class OrderStatusEnum(str, Enum):
    ACCEPTED = 'Принят'
    COOKING = 'Готовится'
    PACKING = 'Собирается'
    READY = 'Готов к выдаче'