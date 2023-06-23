from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.entities.user import User

class IFUserService(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        ...

    @abstractmethod
    async def create(self, misskey_id: str) -> User:
        ...
