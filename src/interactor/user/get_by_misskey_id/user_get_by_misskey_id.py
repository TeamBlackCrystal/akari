
from injector import inject

from src.domain.models.user.user_if import IFUserRepository
from src.interactor.user.get_by_misskey_id.user_get_by_misskey_id_input_if import IFUserGetbymisskeyidInputData
from src.interactor.user.get_by_misskey_id.user_get_by_misskey_id_use_case import IFUserGetbymisskeyidUseCase


class UserGetbymisskeyidInteractor(IFUserGetbymisskeyidUseCase):
    @inject
    def __init__(self, user_repository: IFUserRepository) -> None:
        self.__user_repository = user_repository

    async def handle(self, input_data: IFUserGetbymisskeyidInputData):
        return await self.__user_repository.find_by_misskey_user_id(**input_data)
