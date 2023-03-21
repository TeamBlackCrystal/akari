from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.domain.models.shared.user import Reminder


class IFReminderRepository(ABC):
    async def get_not_done_lists(self) -> list[Reminder]:
        ...

    async def get_lists(self, user_id: str) -> list[Reminder]:
        ...

    @abstractmethod
    async def create(self, title: str, user_id: str, note_id: str) -> Reminder:
        ...
