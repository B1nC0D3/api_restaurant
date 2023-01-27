from abc import ABC, abstractmethod
from typing import Any


class AbstractOperations(ABC):

    @abstractmethod
    async def get(self, *args) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, *args) -> list[Any | None]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args) -> Any | None:
        raise NotImplementedError
