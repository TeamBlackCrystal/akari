from injector import inject

from packages.shared.domain.models.reminder.reminder_if import IFReminderRepository
from packages.shared.interactor.reminder.get_lists.reminder_get_lists_input import (
    IReminderGetListsInputData,
)
from packages.shared.interactor.reminder.get_lists.reminder_get_lists_use_case import (
    IFReminderGetListsUseCase,
)


class ReminderGetListsInteractor(IFReminderGetListsUseCase):
    @inject
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        self.__reminder_repository = reminder_repository

    async def handle(self, input_data: IReminderGetListsInputData):
        return await self.__reminder_repository.get_lists(**input_data)
