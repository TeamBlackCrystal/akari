
REPOSITORY_CLASS_NAME_TEMPLATE = "IF{}Repository"
REPOSITORY_TEMPLATE = """from __future__ import annotations

from abc import ABC, abstractmethod

class {}(ABC):
    ..."""

INPUT_DATA_CLASS_NAME_TEMPLATE = "IF{}{}InputData"
INPUT_DATA_TEMPLATE = """
from __future__ import annotations

from typing import TypedDict


class {}(TypedDict):
    ...
"""

USE_CASE_CLASS_NAME_TEMPLATE = "IF{}UseCase"
USE_CASE_TEMPLATE = """from __future__ import annotations

from abc import abstractmethod

from src.interface.usecase_if import IFUseCase
from {0} import {1}


class {2}(IFUseCase):
    @abstractmethod
    def __init__(self, repository) -> None:
        ...

    @abstractmethod
    async def handle(self, input_data: {1}):
        ...
"""

INTERACTOR_CLASS_NAME = "{0}Interactor"

INTERACTOR_TEMPLATE = """
from injector import inject

from {0} import {1}
from {2} import {3}
from {4} import {5}


class {6}({5}):
    @inject
    def __init__(self, {7}: {1}) -> None:
        self.__{7} = {7}

    async def handle(self, input_data: {3}):
        return None
"""