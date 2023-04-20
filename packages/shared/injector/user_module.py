from injector import Module, Binder

from packages.shared.domain.models.user.user_if import IFUserRepository
from packages.shared.domain.models.user.user_repository import UserRepository
from packages.shared.interactor.user.create.user_create_interactor import UserCreateInteractor
from packages.shared.interactor.user.create.user_create_use_case import IFUserCreateUseCase
from packages.shared.interactor.user.get_by_user_id.user_get_by_user_id import (
    UserGetbyuseridInteractor,
)
from packages.shared.interactor.user.get_by_user_id.user_get_by_user_id_use_case import (
    IFUserGetbyuseridUseCase,
)


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFUserRepository, UserRepository)
        binder.bind(IFUserCreateUseCase, UserCreateInteractor)
        binder.bind(IFUserGetbyuseridUseCase, UserGetbyuseridInteractor)
