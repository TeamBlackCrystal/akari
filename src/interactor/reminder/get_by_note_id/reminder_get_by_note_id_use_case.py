from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from src.interface.usecase_if import IFUseCase
from src.interactor.reminder.get_by_note_id.reminder_get_by_note_id_input_if import (
    IFReminderGetbynoteidInputData,
)

if TYPE_CHECKING:
    from src.domain.models.shared.user import Reminder


class IFReminderGetbynoteidUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self, input_data: IFReminderGetbynoteidInputData) -> Reminder:
        ...
