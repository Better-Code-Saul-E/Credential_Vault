from abc import ABC, abstractmethod

class IMasterHashRepository(ABC):
    @abstractmethod
    def load_hash(self) -> str | None:
        pass

    @abstractmethod
    def save_hash(self, hashed: str) -> bool:
        pass
