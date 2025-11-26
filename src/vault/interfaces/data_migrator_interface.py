# interfaces/migration_interface.py
from abc import ABC, abstractmethod

class IDataMigrator(ABC):
    """
    Defines a contract to migrate legacy vault data to the current format.
    """

    @abstractmethod
    def migrate(self, data: dict) -> dict:
        pass
