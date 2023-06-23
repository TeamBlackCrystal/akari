from injector import Injector
from src.avatar_fix.avatar_fix_module import AvatarFixModule
from src.reminder.remidner_module import ReminderModule

from src.user.user_module import UserModule


injector = Injector(modules=[UserModule, AvatarFixModule, ReminderModule])