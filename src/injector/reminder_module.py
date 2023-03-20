from injector import Binder, Module
from src.domain.models.reminder.reminder_if import IFReminderRepository
from src.domain.models.reminder.reminder_repository import ReminderRepository
from src.interactor.reminder.create_reminder import CreateReminderInteractor
from src.interactor.reminder.get_lists.reminder_get_lists import ReminderGetListsInteractor
from src.interactor.reminder.get_lists.reminder_get_lists_use_case import IFReminderGetListsUseCase

from src.interactor.reminder.reminder_create_use_case import IFReminderCreateUseCase


class ReminderModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFReminderRepository, ReminderRepository)
        binder.bind(IFReminderCreateUseCase, CreateReminderInteractor)
        binder.bind(IFReminderGetListsUseCase, ReminderGetListsInteractor)