from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Float, Boolean
from src.config.control import ControlSettings
from src.infrastructure.database.session import Base

control = ControlSettings()


class UserTable(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    telegram_id = Column(String, nullable=False, default='')


class OrderTable(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    pair = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    buy_amount = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_amount = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    type_control = Column(Integer, nullable=False, default=control.automatic_type)
    profit = Column(Float, nullable=False, default=0)

    user_id = Column(ForeignKey(UserTable.id), nullable=False)


class BalanceTable(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True)
    usdt = Column(Float, nullable=False, default=0)
    btc = Column(Float, nullable=False, default=0)
    eth = Column(Float, nullable=False, default=0)

    user_id = Column(ForeignKey(UserTable.id), nullable=False)
