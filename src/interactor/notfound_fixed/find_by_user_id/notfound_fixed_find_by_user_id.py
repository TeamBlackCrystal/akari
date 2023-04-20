from __future__ import annotations

from typing import TYPE_CHECKING
from injector import inject

from src.domain.models.notfound_fixed.notfound_fixed_if import IFNotfoundFixedRepository
from src.interactor.notfound_fixed.find_by_user_id.notfound_fixed_find_by_user_id_input_if import IFNotfoundFixedFindByUserIdInputData
from src.interactor.notfound_fixed.find_by_user_id.notfound_fixed_find_by_user_id_use_case import IFNotfoundFixedFindByUserIdUseCase

if TYPE_CHECKING:
    from src.domain.models.shared.user import User
    

class NotfoundFixedFindByUserIdInteractor(IFNotfoundFixedFindByUserIdUseCase):
    @inject
    def __init__(self, notfound_fixed_repository: IFNotfoundFixedRepository
) -> None:
        self.__notfound_fixed_repository = notfound_fixed_repository

    async def handle(self, input_data: IFNotfoundFixedFindByUserIdInputData) -> User | None:
        return await self.__notfound_fixed_repository.find_by_user_id(**input_data)
