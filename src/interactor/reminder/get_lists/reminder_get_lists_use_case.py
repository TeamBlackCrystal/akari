from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from src.interface.usecase_if import IFUseCase

if TYPE_CHECKING:
    from src.domain.models.reminder.reminder_if import IFReminderRepository
    from src.domain.models.shared.user import Reminder
    from src.interactor.reminder.get_lists.reminder_get_lists_input import (
        IReminderGetListsInputData,
    )


class IFReminderGetListsUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        pass

    @abstractmethod
    async def handle(self, input_data: IReminderGetListsInputData) -> Reminder:
        pass
