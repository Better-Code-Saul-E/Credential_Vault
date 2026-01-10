import os
from ..models.credential import Credential
from ..services.vault_service import IVaultService
from ..services.configuration_service import ConfigurationService
from ..services.authentication_service import AuthenticationService
from ..interfaces.user_io_interface import IUserIO, IClipboard
from ..services.credential_input_service import CredentialInputService
from ..services.vault_transfer_service import VaultTransferService
from ..services.audit_service import AuditService

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
                 transfer_service: VaultTransferService,
                 credential_input: CredentialInputService,
                 audit_service: AuditService):
        self.service = service
        self.io = io
        self.clipboard = clipboard
        self.config = config_service
        self.auth = auth_service
        self.transfer = transfer_service
        self.credential_input = credential_input
        self.audit = audit_service

    def get_vault_name(self):
        full_path = self.config.get_active_vault()
        filename = os.path.basename(full_path)

        return os.path.splitext(filename)[0].capitalize()
       
    def add_entry(self, service_name):
        self.io.show_header(self.get_vault_name())
        username = self.io.get_input(f"Enter username for {service_name}: ")
        password = self.credential_input.get_valid_password()

        cred = Credential(service_name, username, password)
        
        if self.service.add_credential(cred.service_name, cred.username, cred.password):
            self.audit.log_event("ADD", f"Added credential: {service_name}")
            self.io.show_success(f"Credential for {service_name} added.")
        else:
            self.audit.log_event("ADD_FAIL", f"Failed to add {service_name} (Duplicate)")
            self.io.show_error(f"Service {service_name} already exists.")

    def view_all_entrys(self):
        self.audit.log_event("VIEW_ALL", "Viewed credential list")
        self.io.show_header(self.get_vault_name())
        data = self.service.list_all_credentials()
        self.io.show_credential_list(data)

    def get_entry(self, service_name):
        self.io.show_header(self.get_vault_name())
        cred_dict = self.service.get_credential(service_name)
        if cred_dict:
            self.clipboard.copy_to_clipboard(cred_dict['password'])
            self.audit.log_event("RETRIEVE", f"Copied password for: {service_name}")
            self.io.show_success(f"Password for {cred_dict['service_name']} copied to clipboard.")
        else:
            self.audit.log_event("RETRIEVE_FAIL", f"Service not found: {service_name}")
            self.io.show_warning(f"Service {service_name} not found.")

    def delete_entry(self, service_name):
        self.io.show_header(self.get_vault_name())
        if self.service.delete_credential(service_name):
            self.audit.log_event("DELETE", f"Deleted credential: {service_name}")
            self.io.show_success(f"Credential for {service_name} deleted.")
        else:
            self.audit.log_event("DELETE_FAIL", f"Service not found: {service_name}")
            self.io.show_warning(f"Service {service_name} not found.")

    def update_entry(self, service_name):
        self.io.show_header(self.get_vault_name())
        if not self.service.get_credential(service_name):
            self.io.show_warning(f"Service {service_name} not found.")
            return

        self.io.show_info(f"Updating {service_name}. Press Enter to keep current values.")
        
        new_user = self.io.get_input("New username: ")
        new_pass = self.io.get_password("New password: ")

        final_user = new_user if new_user else None
        final_pass = new_pass if new_pass else None

        if self.service.update_credential(service_name, final_user, final_pass):
            self.audit.log_event("UPDATE", f"UPDATE credential: {service_name}")
            self.io.show_success(f"Updated {service_name}.")
        else:
            self.audit.log_event("UPDATE_FAIL", f"Service not found: {service_name}")
            self.io.show_error("Update failed.")

    def find_entry(self, query):
        self.audit.log_event("SEARCH", f"Searched for: '{query}'")
        self.io.show_header(self.get_vault_name())
        matches = self.service.search_credentials(query)
        self.io.show_search_results(matches, query)

    def switch_active_vault(self, vault_name):
        new_path = self.config.set_active_vault(vault_name)
        clean_name = os.path.basename(new_path)

        self.audit.log_event("SWITCH_VAULT", f"Switched to vault: {clean_name}")
        self.io.show_header(self.get_vault_name())
        self.io.show_success(f"Switched active vault to: {new_path}")

    def change_password(self):
        self.io.show_header(self.get_vault_name())

        new_pass = self.io.get_password("Enter NEW master password: ")
        confirm = self.io.get_password("Confirm NEW master password: ")

        if new_pass != confirm:
            self.io.show_error("Passwords do not match.")
            return

        self.service.change_master_password(new_pass)
        self.auth.create_master_hash(new_pass)
        
        self.audit.log_event("MASTER_CHANGE", "Master password changed successfully")
        self.io.show_success("Master password changed successfully.")

    def export_vault(self, filepath):
        self.io.show_header(self.get_vault_name())
        self.io.show_warning(f"SECURITY RISK: You are about to save unencrypted passwords to '{filepath}'.")

        confirm = self.io.get_input("Are you sure you want to do this? (y/n): ")
        if confirm.lower() != 'y':
            self.io.show_error("Export cancelled.")
            return
        
        try:
            self.transfer.export_to_file(filepath)
            self.audit.log_event("EXPORT", f"Vault exported to: {filepath}")
            self.io.show_success("Vault exported successfully.")

        except Exception as e:
            self.audit.log_event("EXPORT_FAIL", f"Export error: {e}")
            self.io.show_error(f"Export failed: {e}")

    def import_vault(self, filepath):
        self.io.show_header(self.get_vault_name())
        
        if not os.path.exists(filepath):
            self.io.show_error(f"File '{filepath}' not found.")
            return

        try:
            success, count = self.transfer.import_from_file(filepath)
            
            if success:
                self.audit.log_event("IMPORT", f"Imported {count} items from {filepath}")
                self.io.show_success(f"Successfully imported {count} credentials.")
            else:
                self.audit.log_event("IMPORT_FAIL", f"No valid data in {filepath}")
                self.io.show_warning("No valid credentials found to import.")
    
        except Exception as e:
            self.audit.log_event("IMPORT_FAIL", f"Import error: {e}")
            self.io.show_error(f"Import failed: {e}")
    
    def show_audit_logs(self):
        self.audit.log_event("AUDIT_VIEW", "Accessed audit logs")
        self.io.show_header("Audit Logs")
        logs = self.audit.get_parsed_logs(20)
        self.io.show_audit_table(logs)

    
    