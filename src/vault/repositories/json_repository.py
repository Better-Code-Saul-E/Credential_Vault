import json
import os
from cryptography.fernet import InvalidToken
from ..interfaces.vault_repository_interface import IVaultRepository
from ..interfaces.data_migrator_interface import IDataMigrator
from ..interfaces.encryption_interface import IDataEncryptor

class JsonRepository(IVaultRepository):
    """
    Responsible for reading and writing vault data to a JSON file.
    Supports encryption, decryption, and migration of data via injected services.
    """


    def __init__(self, filepath: str, encryptor: IDataEncryptor, migrator: IDataMigrator = None):
        self.filepath = filepath
        self.encryptor = encryptor
        self.migrator = migrator
        self._salt = None

    def _load_salt(self) -> bytes:
        try:
            with open(self.filepath, 'rb') as f:
                return f.read(16)
        except (IOError, FileNotFoundError):
            return os.urandom(16)

    def load_data(self, password: str) -> dict:
        self._salt = self._load_salt()

        try:
            with open(self.filepath, 'rb') as f:
                f.seek(16)
                encrypted_data = f.read()

                if not encrypted_data:
                    return {}
                
                data_str = self.encryptor.decrypt(self._salt + encrypted_data, password)
                data = json.loads(data_str)

                if self.migrator:
                    data = self.migrator.migrate(data)
                    
                return data

        except (IOError, FileNotFoundError):
            return {}
        
        except InvalidToken:
            raise ValueError("Failed to decrypt vault: Bad password or corrupt file.")

    def save_data(self, data: dict, password: str) -> None:
        if not self._salt:
            self._salt = os.urandom(16)

        json_str = json.dumps(data)
        encrypted_data = self.encryptor.encrypt(json_str, password)

        with open(self.filepath, 'wb') as f:
            f.write(encrypted_data)

    def rotate_encryption(self, data: dict, new_password: str) -> None:
        self._salt = os.urandom(16)
        self.save_data(data, new_password)
