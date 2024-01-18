from src.domain.account.balance import Balance
from src.domain.personal.user import User
from src.infrastructure.database.repository import BaseRepository


class BalanceRepository(BaseRepository):
    def __init__(self, individual_session=None):
        super().__init__('Balance', individual_session)

    async def get(self, user: User) -> Balance:
        balance = await self._get('user_id', user.id)
        return Balance(**balance.__dict__) if balance is not None else None

    async def update(self, balance: Balance) -> int:
        return await self._update(**balance.__dict__)
