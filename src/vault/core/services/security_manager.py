from .cryptography_handler import CryptoHandler
import os

class SecurityManager:
    def __init__(self, hash_file='master.hash'):
        self.hash_file = hash_file
        self.cryptography_handler = CryptoHandler()
        
    def hash_file_exists(self):
        return os.path.exists(self.hash_file)
    
    def create_master_hash(self, password):
        try:
            hashed_password_hex = self.cryptography_handler.hash_password(password)
            
            with open(self.hash_file, 'w') as f:
                f.write(hashed_password_hex)
            return True
        
        except Exception:
            return False    
    
    def verify_password(self, password_attempt):
        stored_hex_hash = self.read_hash()
        if not stored_hex_hash:
            return False
        
        return self.cryptography_handler.verify_hashed_password(
            password_attempt,
            stored_hex_hash
        )
        
        
        
        
    
    def read_hash(self):
        try:
            with open(self.hash_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    