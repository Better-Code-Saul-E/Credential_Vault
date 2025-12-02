from abc import ABC, abstractmethod

"""
Defines encryption/decryption operations and key derivation for secure vault storage.
"""

class IDataEncryptor(ABC):
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
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password_attempt: str, stored_hash: str) -> bool:
        pass