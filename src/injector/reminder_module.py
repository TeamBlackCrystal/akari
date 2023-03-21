from injector import Binder, Module
from src.domain.models.reminder.reminder_if import IFReminderRepository
from src.domain.models.reminder.reminder_repository import ReminderRepository
from src.interactor.reminder.create_reminder import CreateReminderInteractor
from src.interactor.reminder.delete.reminder_delete import ReminderDeleteInteractor
from src.interactor.reminder.delete.reminder_delete_use_case import (
    IFReminderDeleteUseCase,
)
from src.interactor.reminder.get_by_note_id.reminder_get_by_note_id import (
    ReminderGetbynoteidInteractor,
)
from src.interactor.reminder.get_by_note_id.reminder_get_by_note_id_use_case import (
    IFReminderGetbynoteidUseCase,
)
from src.interactor.reminder.get_lists.reminder_get_lists import (
    ReminderGetListsInteractor,
)
from src.interactor.reminder.get_lists.reminder_get_lists_use_case import (
    IFReminderGetListsUseCase,
)
from src.interactor.reminder.get_not_done_lists.reminder_get_not_done_lists import (
    ReminderGetnotdonelistsInteractor,
)
from src.interactor.reminder.get_not_done_lists.reminder_get_not_done_lists_use_case import (
    IFReminderGetnotdonelistsUseCase,
)
from src.interactor.reminder.reminder_create_use_case import IFReminderCreateUseCase


class ReminderModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFReminderRepository, ReminderRepository)
        binder.bind(IFReminderCreateUseCase, CreateReminderInteractor)
        binder.bind(IFReminderGetListsUseCase, ReminderGetListsInteractor)
        binder.bind(IFReminderGetnotdonelistsUseCase, ReminderGetnotdonelistsInteractor)
        binder.bind(IFReminderDeleteUseCase, ReminderDeleteInteractor)
        binder.bind(IFReminderGetbynoteidUseCase, ReminderGetbynoteidInteractor)
