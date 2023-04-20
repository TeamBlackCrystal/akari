from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from packages.shared.interface.usecase_if import IFUseCase

if TYPE_CHECKING:
    from packages.shared.domain.models.reminder.reminder_if import IFReminderRepository
    from packages.shared.domain.models.shared.user import Reminder
    from packages.shared.interactor.reminder.create_reminder_input import IReminderCreateInputData


class IFReminderCreateUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        pass

    @abstractmethod
    async def handle(self, input_data: IReminderCreateInputData) -> Reminder:
        pass
