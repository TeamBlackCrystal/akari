from injector import Binder, Module

from src.reminder.reminder_interface import IFReminderService
from src.reminder.reminder_service import ReminderService


class ReminderModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFReminderService, ReminderService)
