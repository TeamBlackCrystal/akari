from injector import Binder, Module

from src.domain.models.notfound_fixed.notfound_fixed_if import IFNotfoundFixedRepository
from src.domain.models.notfound_fixed.notfound_fixed_repository import NotFoundFixedRepository
from src.interactor.notfound_fixed.complete.notfound_fixed_complete import NotfoundFixedCompleteInteractor
from src.interactor.notfound_fixed.complete.notfound_fixed_complete_use_case import IFNotfoundFixedCompleteUseCase
from src.interactor.notfound_fixed.find_by_user_id.notfound_fixed_find_by_user_id import NotfoundFixedFindByUserIdInteractor
from src.interactor.notfound_fixed.find_by_user_id.notfound_fixed_find_by_user_id_use_case import IFNotfoundFixedFindByUserIdUseCase


class NotfoundFixedModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IFNotfoundFixedRepository, NotFoundFixedRepository)
        binder.bind(IFNotfoundFixedCompleteUseCase, NotfoundFixedCompleteInteractor)
        binder.bind(IFNotfoundFixedFindByUserIdUseCase, NotfoundFixedFindByUserIdInteractor)