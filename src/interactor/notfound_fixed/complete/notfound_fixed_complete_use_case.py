from __future__ import annotations

from abc import abstractmethod

from src.interface.usecase_if import IFUseCase
from src.interactor.notfound_fixed.complete.notfound_fixed_complete_input_if import IFNotfound_fixedCompleteInputData


class IFNotfoundFixedCompleteUseCase(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self, input_data: IFNotfound_fixedCompleteInputData):
        ...
