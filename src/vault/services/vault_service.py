from ..interfaces.vault_repository_interface import IVaultRepository
from ..interfaces.vault_service_interface import IVaultService
from thefuzz import fuzz

class VaultService(IVaultService):
    """
    Implements all business logic for managing credentials.
    Supports adding, updating, deleting, listing, searching credentials,
    and changing the master password. Uses a repository for data persistence.
    """

    def __init__(self, repository: IVaultRepository, master_password: str):
        self.repo = repository
        self.password = master_password
        self.credentials = self.repo.load_data(self.password)

    def _save_credentials(self):
        self.repo.save_data(self.credentials, self.password)

    def add_credential(self, service, username, password):
        key = service.lower()
        if key in self.credentials:
            return False
        
        self.credentials[key] = {
            "service_name": service,
            "username": username,
            "password": password
        }

        self._save_credentials()
        return True

    def get_credential(self, service):
        return self.credentials.get(service.lower())

    def list_all_credentials(self):
        return self.credentials

    def delete_credential(self, service):
        key = service.lower()

        if self.credentials.pop(key, None):
            self._save_credentials()
            return True
        
        return False

    def update_credential(self, service, new_username=None, new_password=None):
        key = service.lower()
        if key not in self.credentials:
            return False
        
        cred = self.credentials[key]

        if new_username:
            cred['username'] = new_username
        if new_password:
            cred['password'] = new_password

        self._save_credentials()
        return True

    def search_credentials(self, query):
        all_creds = self.repo.load_data(self.password)
        matches = {}
        
        for service_name, data in all_creds.items():
            score = fuzz.partial_ratio(query.lower(), service_name.lower())

            if score > 60:
                matches[service_name] = data

        return matches

    def change_master_password(self, new_password) -> None:
        self.repo.rotate_encryption(self.credentials, new_password)
        self.password = new_password
        return True
    
    def import_credentials(self, new_data: dict) -> tuple[bool, int]:
        count = 0

        for key, details in new_data.items():
            if isinstance(details, dict) and 'username' in details and 'password' in details:
                self.credentials[key] = details
                count+=1

        if count > 0:
            self._save_credentials()
            return True, count
        return False, 0

    
