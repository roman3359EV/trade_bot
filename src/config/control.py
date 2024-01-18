from pydantic_settings import BaseSettings


class ControlSettings(BaseSettings):
    pairs_buy: tuple = ('BTC_USDT', 'ETH_USDT',)
    pairs_sell: tuple = ('USDT_BTC', 'USDT_BTC',)
    up_percent: float = 1.0
    down_percent: float = 10.0
    default_buy: float = 10.0
    automatic_type: int = 1
    manual_type: int = 2
    app_host: str = 'https://tradebot.com'
