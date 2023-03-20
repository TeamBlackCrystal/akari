from injector import Injector
from src.injector.reminder_module import ReminderModule

from src.injector.user_module import UserModule

injector = Injector([UserModule, ReminderModule])
