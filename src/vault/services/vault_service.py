import os
import glob
from ..interfaces.vault_repository_interface import IVaultRepository
from ..interfaces.vault_service_interface import IVaultService
from ..models.credential import Credential
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
        export_data = {}
        for key, credential in self.credentials.items():
            export_data[key] = {
                "service_name": credential.service_name,
                "username": credential.username,
                "password": credential.password
            }

        self.repo.save_data(export_data, self.password)

    def add_credential(self, credential: Credential):
        key = credential.service_name.lower()
        if key in self.credentials:
            return False
        
        self.credentials[key] = credential

        self._save_credentials()
        return True

    def get_credential(self, service):
        credential = self.credentials.get(service.lower())
        return credential

    def list_all_credentials(self):
        return self.credentials

    def delete_credential(self, service):
        key = service.lower()

        if self.credentials.pop(key, None):
            self._save_credentials()
            return True
        
        return False

    def update_credential(self, credential: Credential):
        key = credential.service_name.lower()
        if key not in self.credentials:
            return False
        
        cred = self.credentials[key]

        if credential.username:
            cred.username = credential.username
        if credential.password:
            cred.password = credential.password

        self._save_credentials()
        return True

    def search_credentials(self, query):
        matches = {}
        
        for service, credential in self.credentials.items():
            score = fuzz.partial_ratio(query.lower(), credential.service_name.lower())

            if score > 60:
                matches[service] = credential

        return matches

    def change_master_password(self, new_password) -> None:
        current_vault_path = self.repo.filepath
        data_dir = os.path.dirname(current_vault_path)

        all_files = glob.glob(os.path.join(data_dir, "*.json"))

        success_count = 0
        
        for file_path in all_files:
            filename = os.path.basename(file_path)

            if filename == "config.json":
                continue

            try:
                temp_repo = self.repo.__class__(
                    filepath=file_path, 
                    encryptor=self.repo.encryptor,
                    migrator=getattr(self.repo, 'migrator', None) 
                )

                data = temp_repo.load_data(self.password)

                export_data = {}
                for k, cred in data.items():
                    export_data[k] = {
                        "service_name": cred.service_name,
                        "username": cred.username,
                        "password": cred.password
                    }
                
                temp_repo.save_data(export_data, new_password)
                
                print(f"Successfully re-encrypted vault: {filename}")
                success_count += 1

            except Exception as e:
                print(f"Skipping {filename} (Sync failed): {e}")

        self.password = new_password
        self._save_credentials()

        return True
    
    def import_credentials(self, new_data: dict) -> tuple[bool, int]:
        count = 0

        for key, details in new_data.items():
            if isinstance(details, dict) and 'username' in details and 'password' in details:
                service_name = details.get('service_name', key) 
                
                self.credentials[key] = Credential(
                    service_name=service_name,
                    username=details['username'],
                    password=details['password']
                )

                count+=1

        if count > 0:
            self._save_credentials()
            return True, count
        return False, 0

    
