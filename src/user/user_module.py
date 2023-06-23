from injector import Binder, Module

from src.user.user_interface import IFUserService
from src.user.user_service import UserService


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFUserService, UserService)
