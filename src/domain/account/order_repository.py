from src.domain.account.order import Order
from src.infrastructure.database.repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, individual_session=None):
        super().__init__('Order', individual_session)

    async def get(self, order_id: int) -> Order | None:
        order = await self._get('id', order_id)
        return Order(**order.__dict__) if order is not None else None

    async def filter_one(self, **kwargs) -> Order | None:
        return await self._filter_one(**kwargs)

    async def open(self, order: Order) -> int:
        return await self._create(**order.__dict__)

    async def close(self, order: Order) -> int:
        return await self._update(**order.__dict__)
