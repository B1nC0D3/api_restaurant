from abc import ABC, abstractmethod
from typing import Any


class AbstractOperations(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, *args, **kwargs) -> list[Any | None]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, name: int) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: int, data: Any) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
