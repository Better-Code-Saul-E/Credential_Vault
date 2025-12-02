import json
from ..interfaces.vault_service_interface import IVaultService

class VaultTransferService:
    def __init__(self, vault: IVaultService):
        self.vault = vault

    def export_to_file(self, filepath: str):
        data = self.vault.list_all_credentials()

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
        return True

    def import_from_file(self, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)

        success, count = self.vault.import_credentials(data)
        return success, count
