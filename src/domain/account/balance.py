class Balance:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.usdt = kwargs.get('usdt')
        self.btc = kwargs.get('btc')
        self.eth = kwargs.get('eth')
