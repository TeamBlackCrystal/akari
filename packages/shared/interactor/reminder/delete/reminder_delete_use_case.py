from __future__ import annotations

from abc import abstractmethod

from packages.shared.interface.usecase_if import IFUseCase
from packages.shared.interactor.reminder.delete.reminder_delete_input_if import (
    IFReminderDeleteInputData,
)


class IFReminderDeleteUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self, input_data: IFReminderDeleteInputData):
        ...
