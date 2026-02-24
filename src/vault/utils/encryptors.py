import os
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from ..interfaces.encryption_interface import IDataEncryptor, IPasswordHasher

class FernetDataEncryptor(IDataEncryptor):
    """
    Handles symmetric encryption for the Vault data.
    """
    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt(self, data: str, password: str) -> bytes:
        salt = os.urandom(16)
        key = self.derive_key(password, salt)
        f = Fernet(key)

        encrypted_data = f.encrypt(data.encode('utf-8'))
        return salt + encrypted_data

    def decrypt(self, encrypted_data_with_salt: bytes, password: str) -> str:
        salt = encrypted_data_with_salt[:16]
        key = self.derive_key(password, salt)

        f = Fernet(key)
        encrypted_data = encrypted_data_with_salt[16:]
        decrypted_data = f.decrypt(encrypted_data)

        return decrypted_data.decode('utf-8')


class Pbkdf2PasswordHasher(IPasswordHasher):
    """
    Handles one-way hashing for the Master Password.
    """
    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        return (salt + password_hash).hex()

    def verify_password(self, password_attempt: str, stored_hex_hash: str) -> bool:
        try:
            stored_bytes = bytes.fromhex(stored_hex_hash)
            salt = stored_bytes[:16]
            stored_hash = stored_bytes[16:]
            
            attempt_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password_attempt.encode('utf-8'),
                salt,
                100000
            )
            return hmac.compare_digest(attempt_hash, stored_hash)
        
        except (ValueError, TypeError):
            return False