from abc import ABC, abstractmethod

class IVaultRepository(ABC):    
    """
    Defines the contract for data repositories.
    Specifies methods to load, save, and rotate encryption of vault data.
    """

    @abstractmethod
    def load_data(self, password: str) -> dict:
        pass

    @abstractmethod
    def save_data(self, data: dict, password: str) -> None:
        pass

    @abstractmethod
    def rotate_encryption(self, data: dict, new_password: str) -> None:
        pass