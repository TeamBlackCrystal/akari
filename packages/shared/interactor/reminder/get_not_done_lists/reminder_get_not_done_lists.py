from injector import inject

from packages.shared.domain.models.reminder.reminder_if import IFReminderRepository
from packages.shared.interactor.reminder.get_not_done_lists.reminder_get_not_done_lists_use_case import (
    IFReminderGetnotdonelistsUseCase,
)


class ReminderGetnotdonelistsInteractor(IFReminderGetnotdonelistsUseCase):
    @inject
    def __init__(self, reminder_repository: IFReminderRepository) -> None:
        self.__reminder_repository = reminder_repository

    async def handle(self):
        return await self.__reminder_repository.get_not_done_lists()
