from injector import inject

from packages.shared.domain.models.reminder.reminder_if import IFReminderRepository
from packages.shared.interactor.reminder.get_by_note_id.reminder_get_by_note_id_input_if import (
    IFReminderGetbynoteidInputData,
)
from packages.shared.interactor.reminder.get_by_note_id.reminder_get_by_note_id_use_case import (
    IFReminderGetbynoteidUseCase,
)


class ReminderGetbynoteidInteractor(IFReminderGetbynoteidUseCase):
    @inject
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        self.__reminder_repository = reminder_repository

    async def handle(self, input_data: IFReminderGetbynoteidInputData):
        return await self.__reminder_repository.get_by_note_id(**input_data)
