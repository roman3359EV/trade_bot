from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config.database import DatabaseSettings

async_engine: AsyncEngine = create_async_engine(DatabaseSettings().sqlalchemy_database_url_async)
session: AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)()

Base = declarative_base()