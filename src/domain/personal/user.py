class User:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get('id')
        self.login: str = kwargs.get('login')
        self.password: str = kwargs.get('password')
        self.is_active: bool = kwargs.get('is_active', False)
        self.telegram_id: int = kwargs.get('telegram_id', 0)
