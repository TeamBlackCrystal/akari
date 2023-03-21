from sqlalchemy import select
from src.domain.models.shared.user import Reminder
from src.domain.models.reminder.reminder_if import IFReminderRepository
from src.db import session


class ReminderRepository(IFReminderRepository):
    async def get_not_done_lists(self) -> list[Reminder]:
        async with session() as _session:
            async with _session.begin():
                search_reminder = await _session.execute(
                    select(Reminder).where(Reminder.is_done.is_(False))
                )
        return [i for i in search_reminder.scalars()]

    async def get_lists(self, user_id: str) -> list[Reminder]:
        async with session() as _session:
            async with _session.begin():
                search_reminder = await _session.execute(
                    select(Reminder).where(Reminder.user_id == user_id)
                )
        return [i for i in search_reminder.scalars()]

    async def create(self, title: str, user_id: str, note_id: str) -> Reminder:
        create_reminder = Reminder(title=title, user_id=user_id, note_id=note_id)
        async with session() as _session:
            async with _session.begin():
                _session.add(create_reminder)

        return create_reminder
