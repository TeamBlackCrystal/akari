from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from packages.shared.interface.usecase_if import IFUseCase

if TYPE_CHECKING:
    from packages.shared.domain.models.shared.user import Reminder


class IFReminderGetnotdonelistsUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self) -> list[Reminder]:
        ...
