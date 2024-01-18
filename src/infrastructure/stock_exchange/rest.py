import aiohttp

from src.config.stock import StockSettings
from src.infrastructure.stock_exchange.dto.order_book_dto import RestOrderBookDto


class Rest:
    def __init__(self):
        self.config = StockSettings()

    async def get_order_book(self, pair: str) -> RestOrderBookDto | None:
        data = {
            'pair': pair,
            'limit': 1
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.config.domain}{self.config.order_book}", data=data) as response:
                response = await response.json()
                return RestOrderBookDto(pair, response)
