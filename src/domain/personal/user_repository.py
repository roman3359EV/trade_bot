from src.domain.personal.user import User
from src.infrastructure.database.repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, individual_session=None):
        super().__init__('User', individual_session)

    async def get(self, user_id: int) -> User:
        user = await self._get('id', user_id)
        return User(**user.__dict__) if user is not None else None

    async def update(self, user: User) -> int:
        return await self._update(**user.__dict__)

    async def all(self) -> list:
        return await self._all()
