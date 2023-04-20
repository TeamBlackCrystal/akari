from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.orm import DeclarativeBase
from asyncio import current_task

engine = create_async_engine('sqlite+aiosqlite:///app.sqlite3')

Session = async_scoped_session(
    async_sessionmaker(engine, expire_on_commit=False), scopefunc=current_task
)


class Base(DeclarativeBase):
    pass
