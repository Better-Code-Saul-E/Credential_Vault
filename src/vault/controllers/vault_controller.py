import os
from ..models.credential import Credential
from ..services.vault_service import IVaultService
from ..services.configuration_service import ConfigurationService
from ..services.authentication_service import AuthenticationService
from ..interfaces.user_io_interface import IUserIO, IClipboard
from ..services.credential_input_service import CredentialInputService


class VaultController:
    """
    Handles user interactions with the vault, including adding, viewing, updating, deleting,
    and searching credentials. Delegates business logic to VaultService and handles clipboard operations.
    """


    def __init__(self, 
                 service: IVaultService, 
                 io: IUserIO,
                 clipboard: IClipboard,
                 config_service: ConfigurationService, 
                 auth_service: AuthenticationService,
                 credential_input: CredentialInputService):
        self.service = service
        self.io = io
        self.clipboard = clipboard
        self.config = config_service
        self.auth = auth_service
        self.credential_input = credential_input

    def _get_vault_name(self):
        """Gets the clean name of the current vault (e.g. 'Work')."""
        full_path = self.config.get_active_vault()
        filename = os.path.basename(full_path)
        # Removes .json and capitalizes the first letter
        return os.path.splitext(filename)[0].capitalize()
       
    def add_entry(self, service_name):
        self.io.show_header(self._get_vault_name())
        # FIX: Removed extra ()
        username = self.io.get_input(f"Enter username for {service_name}: ")
        password = self.credential_input.get_valid_password()

        cred = Credential(service_name, username, password)
        
        if self.service.add_credential(cred.service_name, cred.username, cred.password):
            self.io.show_success(f"Credential for {service_name} added.")
        else:
            self.io.show_error(f"Service {service_name} already exists.")

    def view_all_entrys(self):
        self.io.show_header(self._get_vault_name())
        data = self.service.list_all_credentials()
        self.io.show_credential_list(data)

    def get_entry(self, service_name):
        self.io.show_header(self._get_vault_name())
        cred_dict = self.service.get_credential(service_name)
        if cred_dict:
            self.clipboard.copy_to_clipboard(cred_dict['password'])
            self.io.show_success(f"Password for {cred_dict['service_name']} copied to clipboard.")
        else:
            self.io.show_warning(f"Service {service_name} not found.")

    def delete_entry(self, service_name):
        self.io.show_header(self._get_vault_name())
        if self.service.delete_credential(service_name):
            self.io.show_success(f"Credential for {service_name} deleted.")
        else:
            self.io.show_warning(f"Service {service_name} not found.")

    def update_entry(self, service_name):
        self.io.show_header(self._get_vault_name())
        if not self.service.get_credential(service_name):
            self.io.show_warning(f"Service {service_name} not found.")
            return

        self.io.show_info(f"Updating {service_name}. Press Enter to keep current values.")
        
        # FIX: Removed extra () and use injected IO
        new_user = self.io.get_input("New username: ")
        new_pass = self.io.get_password("New password: ")

        final_user = new_user if new_user else None
        final_pass = new_pass if new_pass else None

        if self.service.update_credential(service_name, final_user, final_pass):
            self.io.show_success(f"Updated {service_name}.")
        else:
            self.io.show_error("Update failed.")

    def find_entry(self, query):
        self.io.show_header(self._get_vault_name())
        matches = self.service.search_credentials(query)
        self.io.show_search_results(matches, query)

    def switch_active_vault(self, vault_name):
        new_path = self.config.set_active_vault(vault_name)

        self.io.show_header(self._get_vault_name())
        self.io.show_success(f"Switched active vault to: {new_path}")

    def change_password(self):
        self.io.show_header(self._get_vault_name())
        # FIX: Use injected IO
        new_pass = self.io.get_password("Enter NEW master password: ")
        confirm = self.io.get_password("Confirm NEW master password: ")

        if new_pass != confirm:
            self.io.show_error("Passwords do not match.")
            return

        self.service.change_master_password(new_pass)
        self.auth.create_master_hash(new_pass)
        
        self.io.show_success("Master password changed successfully.")
    
    