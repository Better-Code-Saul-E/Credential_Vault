from abc import ABC, abstractmethod
from typing import Optional, Dict
from ..models.credential import Credential

class IVaultService(ABC):
    """
    Defines the contract for VaultService implementations.
    Specifies methods for managing credentials without dictating storage details.
    """
    
    @abstractmethod
    def add_credential(self, credential: Credential) -> bool:
        pass

    @abstractmethod
    def list_all_credentials(self) -> Dict[str, Credential]:
        pass

    @abstractmethod
    def get_credential(self, service_name: str) -> Optional[Credential]:
        pass

    @abstractmethod
    def update_credential(self, credential: Credential) -> bool:
        pass

    @abstractmethod
    def delete_credential(self, service_name: str) -> bool:
        pass

    @abstractmethod
    def search_credentials(self, query: str) -> Dict[str, Credential]:
        pass

    @abstractmethod
    def change_master_password(self, new_password: str) -> tuple[int, list[str]]:
        pass

    @abstractmethod
    def import_credentials(self, new_data: dict) -> tuple[bool, int]:
        pass