from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.domain.models.shared.user import User


class IFUserRepository(ABC):
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> User | None:
        ...

    @abstractmethod
    async def create(self, user_id: str) -> User:
        ...
