from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.user import User

class IFAvatarFixService(ABC):
    @abstractmethod
    async def complete(self, user_id: str):
        ...
        
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> User | None:
        ...