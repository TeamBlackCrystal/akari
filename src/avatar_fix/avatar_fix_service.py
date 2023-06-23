from __future__ import annotations

from sqlalchemy import select

from packages.shared.db import Session
from src.entities.notfound_fixed import NotFoundFixed
from src.avatar_fix.avatar_fix_interface import IFAvatarFixService


class AvatarFixService(IFAvatarFixService):
    async def complete(self, user_id: str):
        async with Session() as session:
            async with session.begin():
                created_notfound_fixed = NotFoundFixed(user_id=user_id)
                session.add(created_notfound_fixed)

    async def find_by_user_id(self, user_id: str) -> NotFoundFixed | None:
        async with Session() as session:
            async with session.begin():
                search_reminder = await session.execute(select(NotFoundFixed).where(NotFoundFixed.user_id == user_id))
                return search_reminder.scalar_one_or_none()