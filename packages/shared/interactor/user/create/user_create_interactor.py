from injector import inject
from packages.shared.domain.models.user.user_repository import UserRepository

from packages.shared.interactor.user.create.user_create_input import IUserCreateInputData
from packages.shared.interactor.user.create.user_create_use_case import IFUserCreateUseCase


class UserCreateInteractor(IFUserCreateUseCase):
    @inject
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    async def handle(self, input_data: IUserCreateInputData):
        return await self.__user_repository.create(**input_data)