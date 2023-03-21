
from injector import inject

from src.domain.models.reminder.reminder_if import IFReminderRepository
from src.interactor.reminder.delete.reminder_delete_input_if import IFReminderDeleteInputData
from src.interactor.reminder.delete.reminder_delete_use_case import IFReminderDeleteUseCase


class ReminderDeleteInteractor(IFReminderDeleteUseCase):
    @inject
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        self.__reminder_repository = reminder_repository

    async def handle(self, input_data: IFReminderDeleteInputData):
        return await self.__reminder_repository.delete(**input_data)
