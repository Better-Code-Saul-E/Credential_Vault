from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import hashlib
import base64
import hmac
import os

class CryptoHandler:

    def __init__(self, key_file='data/secret.key'):
        self.key_file = key_file

    def encrypt(self, data, password):
        salt = os.urandom(16)
        key = self.get_key_from_password(password, salt)
        f = Fernet(key)
        
        encrypted_data = f.encrypt(data.encode('utf-8'))
        return salt + encrypted_data
    
    def decrypt(self, data_encrypted_with_salt, password):
        salt = data_encrypted_with_salt[:16]
        encrypted_data = data_encrypted_with_salt[16:]
        key = self.get_key_from_password(password, salt)
        f = Fernet(key)
        
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')

    def hash_password(self, password):
        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ) 
        return (salt + password_hash).hex()
        
    def verify_hashed_password(self, password_attempt, stored_hex_hash):
        try:
            stored_hash_bytes = bytes.fromhex(stored_hex_hash)
            
            salt = stored_hash_bytes[:16]
            stored_hash = stored_hash_bytes[16:]
            
            attempt_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password_attempt.encode('utf-8'),
                salt,
                100000
            )   
            
            return hmac.compare_digest(attempt_hash, stored_hash)
        except(ValueError, TypeError):
            return False



    
    def get_key_from_password(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
    
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
        
    
