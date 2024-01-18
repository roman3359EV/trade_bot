from pydantic_settings import BaseSettings


class StockSettings(BaseSettings):
    domain: str = 'https://api.exmo.me/v1.1'
    order_book: str = '/order_book'
