class RestOrderBookDto:
    def __init__(self, pair, data):
        self.pair: str = pair
        self.ask: list = [float(item) for item in data[pair]['ask'][0]]
        self.bid: list = [float(item) for item in data[pair]['bid'][0]]

    @property
    def ask_price(self) -> float:
        return self.ask[0]

    @property
    def ask_quantity(self) -> float:
        return self.ask[1]

    @property
    def ask_amount(self) -> float:
        return self.ask[2]

    @property
    def bid_price(self) -> float:
        return self.bid[0]

    @property
    def bid_quantity(self) -> float:
        return self.bid[1]

    @property
    def bid_amount(self) -> float:
        return self.bid[2]
