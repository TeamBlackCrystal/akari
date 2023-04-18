from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from src.interface.usecase_if import IFUseCase

if TYPE_CHECKING:
    from src.domain.models.shared.user import Reminder


class IFReminderGetnotdonelistsUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self) -> list[Reminder]:
        ...
