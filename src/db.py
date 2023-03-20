from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine('sqlite+aiosqlite:///app.sqlite3')

session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
