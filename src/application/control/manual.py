from abc import ABC

from src.application.control.base import Base
from src.domain.account.order import Order
from src.domain.personal.user import User
from src.infrastructure.database.transaction import transaction
from src.infrastructure.telegram.telegram import sync_send_message, sync_send_message_with_actions


class Manual(Base, ABC):
    def __init__(self, user: User, individual_session=None):
        super().__init__(user, individual_session)
        self.action = None

    async def action_buy(self, order: Order) -> None:
        self.action = 'buy'
        await self.telegram.send_message_with_actions(self.__attempt_message(order), self.action, self.__attempt_buy_action(order))

    async def action_sell(self, order: Order) -> None:
        self.action = 'sell'
        await self.telegram.send_message_with_actions(self.__attempt_message(order), self.action, self.__attempt_sell_action(order))

    def __attempt_message(self, order: Order) -> str:
        usdt = order.sell_amount if self.action == 'sell' else order.buy_amount
        return f"Are you {self.action} {order.quantity} {order.pair.split('_')[0]} on {usdt} USDT?"

    def __attempt_buy_action(self, order: Order) -> str:
        return f"{self.config.app_host}/api/v1/control/buy/{order.pair}?user_id={order.user_id}"

    def __attempt_sell_action(self, order: Order) -> str:
        return f"{self.config.app_host}/api/v1/control/sell?order_id={order.id}&user_id={order.user_id}"

    @transaction
    async def manual_buy(self, pair: str) -> None:
        state = await self._get_next_state(pair)
        buy_amount = self._get_buy_amount(state)
        quantity = self._get_quantity(state)

        order = Order(
            pair=pair,
            quantity=quantity,
            buy_amount=buy_amount,
            buy_price=state.ask_price,
            type_control=self.config.manual_type,
            user_id=self.user.id
        )

        await self.buy(order)
        sync_send_message.delay(self.user.telegram_id, self._buy_message(order))

    @transaction
    async def manual_sell(self, order_id: int) -> None:
        open_order = await self.order_repository.get(order_id=order_id)
        state = await self._get_next_state(open_order.pair)

        order = Order(
            id=open_order.id,
            pair=open_order.pair,
            quantity=open_order.quantity,
            buy_amount=open_order.buy_amount,
            buy_price=open_order.buy_price,
            sell_amount=open_order.quantity * state.bid_price,
            sell_price=state.bid_price,
            profit=open_order.quantity * (state.bid_price - open_order.buy_price),
            user_id=self.user.id
        )

        await self.sell(order)
        sync_send_message.delay(self.user.telegram_id, self._sell_message(order))

    async def _get_previous_state(self, pair: str) -> Order | None:
        return await self.order_repository.filter_one(pair=pair, user_id=self.user.id, profit=0, type_control=self.config.manual_type)