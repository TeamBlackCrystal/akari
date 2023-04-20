from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from packages.shared.domain.models.user.user_if import IFUserRepository
from packages.shared.interactor.user.create.user_create_input import IUserCreateInputData
from packages.shared.interface.usecase_if import IFUseCase

if TYPE_CHECKING:
    from packages.shared.domain.models.shared.user import User


class IFUserCreateUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, reminder_repository: IFUserRepository) -> None:
        pass

    @abstractmethod
    async def handle(self, input_data: IUserCreateInputData) -> User:
        pass
