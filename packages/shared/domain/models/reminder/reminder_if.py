from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from packages.shared.domain.models.shared.user import Reminder


class IFReminderRepository(ABC):
    @abstractmethod
    async def get_by_note_id(self, note_id: str) -> Reminder | None:
        ...

    @abstractmethod
    async def delete(self, note_id: str) -> None:
        ...

    @abstractmethod
    async def get_not_done_lists(self) -> list[Reminder]:
        ...

    @abstractmethod
    async def get_lists(self, user_id: str) -> list[Reminder]:
        ...

    @abstractmethod
    async def create(self, title: str, user_id: str, note_id: str) -> Reminder:
        ...
