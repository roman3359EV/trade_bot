from typing import Any
from sqlalchemy import Result, asc, delete, desc, func, select, update, Select

from src.infrastructure.database.session import session
from src.infrastructure.database.tables import BalanceTable, OrderTable, UserTable, Base


class BaseRepository:
    def __init__(self, schema_class, individual_session=None):
        self.schema_class = self.factory(schema_class)
        self.session = individual_session if individual_session is not None else session

    async def _create(self, **kwargs) -> int:
        schema = self.schema_class(**kwargs)

        self.session.add(schema)
        await self.session.flush()
        await self.session.refresh(schema)

        return schema.id

    async def _get(self, key: str, value: Any) -> Any:
        query = select(self.schema_class).where(getattr(self.schema_class, key) == value)
        result: Result = await self.session.execute(query)

        if not (result := result.scalars().one_or_none()):
            return None

        return result

    async def _filter_one(self, **kwargs):
        query = select(self.schema_class).filter_by(**kwargs)
        result: Result = await self.session.execute(query)

        if not (result := result.scalars().first()):
            return None

        return result

    async def _update(self, **kwargs):
        schema = self.schema_class(**kwargs)

        query = update(self.schema_class).where(getattr(self.schema_class, 'id') == kwargs['id']).values(kwargs)
        await self.session.execute(query)
        await self.session.flush()

        return schema.id

    async def _all(self):
        query = select(self.schema_class)
        result: Result = await self.session.execute(query)

        return result.scalars().all()

    @staticmethod
    def factory(schema_class: str) -> Base:
        return {
            'Balance': BalanceTable,
            'Order': OrderTable,
            'User': UserTable
        }[schema_class]
