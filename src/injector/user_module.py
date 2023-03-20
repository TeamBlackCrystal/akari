from injector import Module, Binder

from src.domain.models.user.user_if import IUserCreateRepository
from src.domain.models.user.user_repository import UserRepository
from src.interactor.user.create.user_create_interactor import UserCreateInteractor
from src.interactor.user.create.user_create_use_case import IFUserCreateUseCase


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IUserCreateRepository, UserRepository)
        binder.bind(IFUserCreateUseCase, UserCreateInteractor)
