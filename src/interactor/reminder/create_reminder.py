from injector import inject

from src.domain.models.reminder.reminder_if import IFReminderRepository
from src.interactor.reminder.create_reminder_input import IReminderCreateInputData
from src.interactor.reminder.reminder_create_use_case import IFReminderCreateUseCase


class CreateReminderInteractor(IFReminderCreateUseCase):
    @inject
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        self.__reminder_repository = reminder_repository

    async def handle(self, input_data: IReminderCreateInputData):
        return await self.__reminder_repository.create(**input_data)
