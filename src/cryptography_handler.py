from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64

class CryptoHandler:

    def hash_password(self, password):
        hashed = hashlib.sha256()
        hashed.update(password.encode('utf-8'))
        return hashed.hexdigest()
    
    def derive_key(self, password, salt):

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

