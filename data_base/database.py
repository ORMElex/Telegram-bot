from .dbmodels import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine('sqlite+aiosqlite:///mydatabase.sqlite3')

async_session = async_sessionmaker(engine, class_=AsyncSession)