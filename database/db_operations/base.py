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


class AbstractCache(ABC):

    @abstractmethod
    async def get(self, name: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str, data: Any) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
