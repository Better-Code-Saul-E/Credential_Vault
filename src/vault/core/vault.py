import json
import os

from cryptography.fernet import Fernet, InvalidToken

from .services.cryptography_handler import CryptoHandler


class Vault:
    def __init__(self, password, filepath='credentials.json'):
        self.filepath = filepath
        self.cryptography = CryptoHandler()
        self.salt = self._load_salt()
        self.key = self.cryptography.get_key_from_password(password, self.salt)

        try:
            self.credentials = self._load_credentials()
        except InvalidToken:
            raise ValueError("Failed to decrypt vault: Bad password or corrupt file!!!")
        except Exception as e:
            raise e
    
    def _load_salt(self):
        try: 
            with open(self.filepath, 'rb') as f:
                return f.read(16)
        except (IOError, FileNotFoundError):
            return os.urandom(16)
        
    def _load_credentials(self):
        try:
            with open(self.filepath, 'rb') as f:
                f.seek(16)
                encrypted_data = f.read()

                if not encrypted_data:
                    return {}
                
                fernet = Fernet(self.key)
                decrypted_data = fernet.decrypt(encrypted_data)
                data = json.loads(decrypted_data.decode())
            
                if isinstance(data, list):
                    new_data = {}
                    for item in data:
                        service_name = item.get('service')
                        
                        if service_name:
                            item.pop('service')
                            item['service_name'] = service_name
                            
                    self.credentials = new_data
                    self.save()
                    return new_data
                
                return data
        except (IOError, FileNotFoundError):
            return {}

    def save(self):
        fernet = Fernet(self.key)
        credentials_json = json.dumps(self.credentials, indent=4)
        encrypted_data = fernet.encrypt(credentials_json.encode())

        with open(self.filepath, 'wb') as f:
            f.write(self.salt)
            f.write(encrypted_data)

    def add_credential(self, service, username, password):
        service_key = service.lower()
        if service_key in self.credentials:
            return False
        
        self.credentials[service_key] = {
        "service_name": service,
        "username": username,
        "password": password
        }
        self.save()
        
        return True


    def list_all_credentials(self):
        return self.credentials
    
    def get_credential(self, service):
        service_key = service.lower()
        return self.credentials.get(service_key)

    def delete_credential(self, service):
        service_key = service.lower()
        deleted_service = self.credentials.pop(service_key, None)
        
        if deleted_service:
            self.save()
            return True
        
        return False

    def update_credential(self, service, new_username = None, new_password=None):
        service_key = service.lower()
        if service_key not in self.credentials:
            return False
        
        credential = self.credentials[service_key]
        
        if new_username:
            credential['username'] = new_username
        
        if new_password:
            credential['password'] = new_password
            
        self.save()
        return True
        
