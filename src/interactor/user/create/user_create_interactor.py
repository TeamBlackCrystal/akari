from injector import inject
from src.domain.models.user.user_repository import UserRepository

from src.interactor.user.create.user_create_input import IUserCreateInputData
from src.interactor.user.create.user_create_use_case import IFUserCreateUseCase


class UserCreateInteractor(IFUserCreateUseCase):
    @inject
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    async def handle(self, input_data: IUserCreateInputData):
        return await self.__user_repository.create(**input_data)
