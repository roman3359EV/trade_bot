from abc import ABC

from src.application.control.base import Base
from src.domain.account.order import Order
from src.domain.personal.user import User
from src.infrastructure.telegram.telegram import sync_send_message


class Automatic(Base, ABC):
    def __init__(self, user: User, individual_session=None):
        super().__init__(user, individual_session)

    async def action_buy(self, order: Order) -> None:
        await self.buy(order)
        await self.telegram.send_message(self._buy_message(order))

    async def action_sell(self, order: Order) -> None:
        await self.sell(order)
        await self.telegram.send_message(self._sell_message(order))

    async def _get_previous_state(self, pair: str) -> Order | None:
        return await self.order_repository.filter_one(pair=pair, user_id=self.user.id, profit=0, type_control=self.config.automatic_type)
