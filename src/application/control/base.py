from abc import ABC, abstractmethod

from src.config.control import ControlSettings
from src.domain.account.balance_repository import BalanceRepository
from src.domain.account.order import Order
from src.domain.account.order_repository import OrderRepository
from src.domain.personal.user import User
from src.infrastructure.stock_exchange.rest import Rest, RestOrderBookDto
from src.infrastructure.telegram.telegram import Telegram
from src.infrastructure.database.transaction import transaction


class Base(ABC):
    def __init__(self, user: User, individual_session=None):
        self.user = user
        self.session = individual_session
        self.balance_repository = BalanceRepository(individual_session)
        self.order_repository = OrderRepository(individual_session)
        self.config = ControlSettings()
        self.telegram = Telegram(self.user.telegram_id)
        self.stock_rest = Rest()

    @transaction
    async def solve(self, pair: str):
        previous_state = await self._get_previous_state(pair)
        next_state = await self._get_next_state(pair)

        if previous_state is None:
            buy_amount = self._get_buy_amount(next_state)
            quantity = self._get_quantity(next_state)
            order = Order(
                pair=pair,
                quantity=quantity,
                buy_amount=buy_amount,
                buy_price=next_state.ask_price,
                user_id=self.user.id
            )

            await self.action_buy(order)

            return

        trend = next_state.bid_price - previous_state.buy_price
        change_percent = abs(trend) / previous_state.buy_price * 100

        if (trend > 0 and change_percent > self.config.up_percent) or (trend < 0 and change_percent > self.config.down_percent):
            order = Order(
                id=previous_state.id,
                pair=pair,
                quantity=previous_state.quantity,
                buy_amount=previous_state.buy_amount,
                buy_price=previous_state.buy_price,
                sell_amount=previous_state.quantity * next_state.bid_price,
                sell_price=next_state.bid_price,
                profit=previous_state.quantity * (next_state.bid_price - previous_state.buy_price),
                user_id=self.user.id
            )

            await self.action_sell(order)

        return

    @abstractmethod
    async def action_buy(self, order: Order):
        """select control"""

    @abstractmethod
    async def action_sell(self, order: Order):
        """select control"""

    @abstractmethod
    def _get_previous_state(self, pair: str):
        """filter on previous state"""

    async def buy(self, order: Order) -> None:
        balance = await self.balance_repository.get(self.user)
        balance.usdt -= order.buy_amount
        balance.btc += order.quantity

        await self.order_repository.open(order)
        await self.balance_repository.update(balance)

    async def sell(self, order: Order) -> None:
        balance = await self.balance_repository.get(self.user)
        balance.usdt += order.quantity * order.sell_price
        balance.btc -= order.quantity

        await self.order_repository.close(order)
        await self.balance_repository.update(balance)

    async def _get_next_state(self, pair: str):
        return await self.stock_rest.get_order_book(pair)

    def _compare_order(self, minimal_ask: float):
        return self.config.default_buy <= minimal_ask

    def _get_buy_amount(self, state: RestOrderBookDto) -> float:
        return self.config.default_buy if self._compare_order(state.ask_amount) else state.ask_amount

    def _get_quantity(self, state: RestOrderBookDto) -> float:
        return float(self.config.default_buy / state.ask_price) if self._compare_order(state.ask_amount) else state.ask_quantity

    @staticmethod
    def _buy_message(order: Order) -> str:
        return f"Buy {order.quantity} {order.pair.split('_')[0]} on {order.buy_amount} USDT"

    @staticmethod
    def _sell_message(order: Order) -> str:
        return f"Sell {order.quantity} {order.pair.split('_')[0]} on {order.sell_amount} USDT"
