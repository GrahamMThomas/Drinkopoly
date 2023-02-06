from abc import ABC, abstractmethod


class Roller(ABC):
    @abstractmethod
    def Roll(self) -> int:
        pass
