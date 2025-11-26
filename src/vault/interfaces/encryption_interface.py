from abc import ABC, abstractmethod

class IDataEncryptor(ABC):
    """
    Defines encryption/decryption operations and key derivation for secure vault storage.
    """


    @abstractmethod
    def encrypt(self, data: str, password: str) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, encrypted_data: bytes, password: str) -> str:
        pass
    
    @abstractmethod
    def derive_key(self, password: str, salt: bytes) -> bytes:
        pass

class IPasswordHasher(ABC):
    """Contract for checking user login (Auth layer)."""
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password_attempt: str, stored_hash: str) -> bool:
        pass