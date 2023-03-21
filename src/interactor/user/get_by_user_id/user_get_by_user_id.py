from injector import inject

from src.domain.models.user.user_if import IFUserRepository
from src.interactor.user.get_by_user_id.user_get_by_user_id_input_if import (
    IFUserGetbyuseridInputData,
)
from src.interactor.user.get_by_user_id.user_get_by_user_id_use_case import (
    IFUserGetbyuseridUseCase,
)


class UserGetbyuseridInteractor(IFUserGetbyuseridUseCase):
    @inject
    def __init__(self, user_repository: IFUserRepository) -> None:
        self.__user_repository = user_repository

    async def handle(self, input_data: IFUserGetbyuseridInputData):
        return await self.__user_repository.find_by_user_id(**input_data)
