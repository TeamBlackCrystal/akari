from injector import Injector

from packages.shared.injector.notfound_fixed_module import NotfoundFixedModule
from packages.shared.injector.reminder_module import ReminderModule
from packages.shared.injector.user_module import UserModule


injector = Injector([UserModule, ReminderModule, NotfoundFixedModule])
