from abc import ABC, abstractmethod
from .config import DatabaseConfigInterface

class DatabaseCreator(ABC):
    @abstractmethod
    def create(self, config: DatabaseConfigInterface) -> None:
        pass

class TableCreator(ABC):
    @abstractmethod
    def create(self, cursor) -> None:
        pass

class ViewCreator(ABC):
    @abstractmethod
    def create(self, cursor) -> None:
        pass

class FunctionCreator(ABC):
    @abstractmethod
    def create(self, cursor) -> None:
        pass
