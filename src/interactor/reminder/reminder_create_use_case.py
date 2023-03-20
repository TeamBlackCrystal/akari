from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from src.interface.usecase_if import IFUseCase

if TYPE_CHECKING:
    from src.domain.models.reminder.reminder_if import IFReminderRepository
    from src.domain.models.shared.user import Reminder
    from src.interactor.reminder.create_reminder_input import IReminderCreateInputData


class IFReminderCreateUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        pass

    @abstractmethod
    async def handle(self, input_data: IReminderCreateInputData) -> Reminder:
        pass
