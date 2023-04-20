from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from packages.shared.domain.models.shared.user import Reminder
from packages.shared.domain.models.reminder.reminder_if import IFReminderRepository
from src.db import Session


class ReminderRepository(IFReminderRepository):
    async def get_by_note_id(self, note_id: str) -> Reminder | None:
        async with Session() as session:
            async with session.begin():
                search_reminder = await session.execute(
                    select(Reminder)
                    .where(Reminder.note_id == note_id)
                    .options(joinedload(Reminder.user))
                )
        return search_reminder.scalar_one_or_none()

    async def delete(self, note_id: str) -> None:
        async with Session() as session:
            async with session.begin():
                await session.execute(
                    delete(Reminder).where(Reminder.note_id == note_id)
                )

    async def get_not_done_lists(self) -> list[Reminder]:
        async with Session() as session:
            async with session.begin():
                search_reminder = await session.execute(
                    select(Reminder)
                    .where(Reminder.is_done.is_(False))
                    .options(joinedload(Reminder.user))
                    .filter()
                )
        return [i for i in search_reminder.scalars()]

    async def get_lists(self, user_id: str) -> list[Reminder]:
        async with Session() as session:
            async with session.begin():
                search_reminder = await session.execute(
                    select(Reminder)
                    .where(Reminder.user_id == user_id)
                    .options(joinedload(Reminder.user))
                    .filter()
                )
        return [i for i in search_reminder.scalars()]

    async def create(self, title: str, user_id: str, note_id: str) -> Reminder:
        create_reminder = Reminder(title=title, user_id=user_id, note_id=note_id)
        async with Session() as session:
            async with session.begin():
                session.add(create_reminder)

        return create_reminder
