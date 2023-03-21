from injector import Module, Binder

from src.domain.models.user.user_if import IFUserRepository
from src.domain.models.user.user_repository import UserRepository
from src.interactor.user.create.user_create_interactor import UserCreateInteractor
from src.interactor.user.create.user_create_use_case import IFUserCreateUseCase
from src.interactor.user.get_by_misskey_id.user_get_by_misskey_id import UserGetbymisskeyidInteractor
from src.interactor.user.get_by_misskey_id.user_get_by_misskey_id_use_case import IFUserGetbymisskeyidUseCase


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFUserRepository, UserRepository)
        binder.bind(IFUserCreateUseCase, UserCreateInteractor)
        binder.bind(IFUserGetbymisskeyidUseCase, UserGetbymisskeyidInteractor)
        
