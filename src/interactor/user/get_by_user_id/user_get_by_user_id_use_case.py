from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from src.interface.usecase_if import IFUseCase
from src.interactor.user.get_by_user_id.user_get_by_user_id_input_if import (
    IFUserGetbyuseridInputData,
)

if TYPE_CHECKING:
    from src.domain.models.shared.user import User


class IFUserGetbyuseridUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self, input_data: IFUserGetbyuseridInputData) -> User:
        ...
