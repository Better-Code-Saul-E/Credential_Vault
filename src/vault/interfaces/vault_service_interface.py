from abc import ABC, abstractmethod
from typing import Optional, Dict


# Refactor Notes:
# - Use Credential as the dataclass for type safety (Dict[str, Credential]) in list_all_credentials, get_credential, search_credentials


class IVaultService(ABC):
    """
    Defines the contract for VaultService implementations.
    Specifies methods for managing credentials without dictating storage details.
    """
    
    @abstractmethod
    def add_credential(self, service_name: str, username: str, password: str) -> bool:
        pass

    @abstractmethod
    def list_all_credentials(self) -> Dict[str, dict]:
        pass

    @abstractmethod
    def get_credential(self, service_name: str) -> Optional[dict]:
        pass

    @abstractmethod
    def update_credential(self, service_name: str, username: str = None, password: str = None) -> bool:
        pass

    @abstractmethod
    def delete_credential(self, service_name: str) -> bool:
        pass

    @abstractmethod
    def search_credentials(self, query: str) -> Dict[str, dict]:
        pass

    @abstractmethod
    def change_master_password(self, new_password: str) -> bool:
        pass
