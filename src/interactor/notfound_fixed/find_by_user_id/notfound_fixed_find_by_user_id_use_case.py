from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from src.interface.usecase_if import IFUseCase
from src.interactor.notfound_fixed.find_by_user_id.notfound_fixed_find_by_user_id_input_if import IFNotfoundFixedFindByUserIdInputData

if TYPE_CHECKING:
    from src.domain.models.shared.user import User
    

class IFNotfoundFixedFindByUserIdUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self, input_data: IFNotfoundFixedFindByUserIdInputData) -> User | None:
        ...
