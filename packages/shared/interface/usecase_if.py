from abc import ABC, abstractmethod


class IFUseCase(ABC):
    @abstractmethod
    async def handle(self):
        ...
