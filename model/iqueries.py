from abc import ABC, abstractmethod

class QueryInterface(ABC):
    @abstractmethod
    def execute(self)->None:
        pass
