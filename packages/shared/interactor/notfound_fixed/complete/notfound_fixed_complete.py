
from injector import inject

from packages.shared.domain.models.notfound_fixed.notfound_fixed_if import IFNotfoundFixedRepository
from packages.shared.interactor.notfound_fixed.complete.notfound_fixed_complete_input_if import IFNotfound_fixedCompleteInputData
from packages.shared.interactor.notfound_fixed.complete.notfound_fixed_complete_use_case import IFNotfoundFixedCompleteUseCase


class NotfoundFixedCompleteInteractor(IFNotfoundFixedCompleteUseCase):
    @inject
    def __init__(self, notfound_fixed_repository: IFNotfoundFixedRepository) -> None:
        self.__notfound_fixed_repository = notfound_fixed_repository

    async def handle(self, input_data: IFNotfound_fixedCompleteInputData):
        return await self.__notfound_fixed_repository.complete(**input_data)
