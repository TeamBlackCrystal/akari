from injector import Binder, Module

from src.avatar_fix.avatar_fix_interface import IFAvatarFixService
from src.avatar_fix.avatar_fix_service import AvatarFixService


class AvatarFixModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFAvatarFixService, AvatarFixService)
