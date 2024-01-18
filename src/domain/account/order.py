class Order:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get('id')
        self.pair: str = kwargs.get('pair')
        self.quantity: float = kwargs.get('quantity')
        self.buy_amount: float = kwargs.get('buy_amount')
        self.buy_price: float = kwargs.get('buy_price')
        self.sell_amount: float = kwargs.get('sell_amount', 0)
        self.sell_price: float = kwargs.get('sell_price', 0)
        self.type_control: int = kwargs.get('type_control', 1)
        self.profit: float = kwargs.get('profit', 0)
        self.user_id: int = kwargs.get('user_id')
