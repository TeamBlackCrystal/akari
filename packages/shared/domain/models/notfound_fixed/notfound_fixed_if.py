from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packages.shared.domain.models.shared.user import User

class IFNotfoundFixedRepository(ABC):
    @abstractmethod
    async def complete(self, user_id: str):
        ...
        
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> User | None:
        ...