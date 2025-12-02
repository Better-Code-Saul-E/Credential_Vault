import os
import sys
import argparse

# --- 1. Tools & Utilities ---
from .utils.encryptors import FernetDataEncryptor, Pbkdf2PasswordHasher
from .utils.password_validator import PasswordStrength
from .utils.clipboard import SystemClipboard
from .views.console_view import ConsoleView

# --- 2. Services & Repositories ---
from .repositories.file_master_hash_repository import FileMasterHashRepository
from .repositories.json_repository import JsonRepository
from .services.authentication_service import AuthenticationService
from .services.vault_service import VaultService
from .services.configuration_service import ConfigurationService
from .services.credential_input_service import CredentialInputService
from .services.vault_transfer_service import VaultTransferService


# --- 3. Controllers ---
from .controllers.vault_controller import VaultController
from .controllers.authentication_controller import AuthenticationController

def ensure_data_directory(data_dir: str):
    os.makedirs(data_dir, exist_ok=True)

def setup_tools() -> tuple[FernetDataEncryptor, Pbkdf2PasswordHasher, SystemClipboard, ConsoleView, PasswordStrength]:
    """Instantiate tools and utility objects."""
    encryptor = FernetDataEncryptor()
    hasher = Pbkdf2PasswordHasher()
    clipboard = SystemClipboard()
    view = ConsoleView()
    validator = PasswordStrength()  # Stateless
    return encryptor, hasher, clipboard, view, validator

# Find this function in src/vault/app.py
def setup_services(hash_file: str, config_file: str, data_dir: str, hasher: Pbkdf2PasswordHasher) -> tuple[AuthenticationService, ConfigurationService]:
    """Instantiate main services."""

    hash_repo = FileMasterHashRepository(hash_file)
    auth_service = AuthenticationService(repo=hash_repo, hasher=hasher)
    config_service = ConfigurationService(config_file, data_dir) 
    
    return auth_service, config_service

def bootstrap_controllers(auth_service: AuthenticationService, config_service: ConfigurationService, view: ConsoleView,
                          encryptor: FernetDataEncryptor, clipboard: SystemClipboard, validator: PasswordStrength,
                          user_password: str, vault_path: str) -> VaultController:
    """Build VaultController with all dependencies."""
    
    repository = JsonRepository(vault_path, encryptor)
    vault_service = VaultService(repository, user_password)
    credential_input_service = CredentialInputService(io=view, password_validator=validator)
    transfer_service = VaultTransferService(vault_service)

    vault_controller = VaultController(
        service=vault_service,
        io=view,
        clipboard=clipboard,
        config_service=config_service,
        auth_service=auth_service,
        transfer_service=transfer_service,
        credential_input=credential_input_service
    )

    return vault_controller

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A command-line credential vault.")
    
    subparsers = parser.add_subparsers(dest="command", required=False, help="Action to perform.")

    subcommands = [
        ('add', 'Add a new credential.', 'service'),
        ('get', 'Get password for a service.', 'service'),
        ('delete', 'Delete a credential.', 'service'),
        ('update', 'Update a credential.', 'service'),
        ('search', 'Search for credentials.', 'query'),
        ('switch', 'Switch the active vault.', 'vault_name'),
        ('export', 'Export decrypted vault to JSON.', 'filepath'),
        ('import', 'Import credentials from JSON.', 'filepath'),
    ]

    for cmd, help_text, arg_name in subcommands:
        sp = subparsers.add_parser(cmd, help=help_text)
        sp.add_argument(arg_name, type=str, help=f"The {arg_name}.")

    subparsers.add_parser('view', help='View all credentials.')
    subparsers.add_parser('passwd', help='Change the master password.')
    
    parser.add_argument('-f', '--file', type=str, metavar='FILEPATH', help='Specify a custom vault file path.')
    return parser

def route_command(args, vault_controller: VaultController, parser: argparse.ArgumentParser):
    """Dispatch commands to the VaultController."""
    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'add':
            vault_controller.add_entry(args.service)
        elif args.command == 'view':
            vault_controller.view_all_entrys()
        elif args.command == 'get':
            vault_controller.get_entry(args.service)
        elif args.command == 'delete':
            vault_controller.delete_entry(args.service)
        elif args.command == 'update':
            vault_controller.update_entry(args.service)
        elif args.command == 'search':
            vault_controller.find_entry(args.query)
        elif args.command == 'switch':
            vault_controller.switch_active_vault(args.vault_name)
        elif args.command == 'passwd':
            vault_controller.change_password()
        elif args.command == 'export':
            vault_controller.export_vault(args.filepath) 
        elif args.command == 'import':
            vault_controller.import_vault(args.filepath)
    except Exception as e:
        vault_controller.io.show_error(f"An unexpected error occurred: {e}")









# -------------------------------
# Main Run Function
# -------------------------------

def run():
    BASE_DIR = os.getcwd()
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    HASH_FILE = os.path.join(DATA_DIR, 'master.hash')
    CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

    ensure_data_directory(DATA_DIR)

    # 1. Setup Tools & Services
    encryptor, hasher, clipboard, view, validator = setup_tools()
    auth_service, config_service = setup_services(HASH_FILE, CONFIG_FILE, DATA_DIR, hasher)

    # 2. Parse Arguments EARLY
    parser = create_parser()
    args = parser.parse_args()

    # 3. Special Case: Switch (No Auth Required)
    if args.command == 'switch':
        new_path = config_service.set_active_vault(args.vault_name)
        
        # Manually construct header/success since we don't have a controller yet
        vault_name = os.path.basename(new_path)
        clean_name = os.path.splitext(vault_name)[0].capitalize()
        
        view.show_header(clean_name)
        view.show_success(f"Switched active vault to: {new_path}")
        return 

    # 4. Authentication Phase (Only if not switching)
    auth_controller = AuthenticationController(auth_service, view, config_service)
    user_password = auth_controller.authenticate_user()
    if not user_password:
        sys.exit(1)

    # 5. Determine Vault Path
    vault_path = args.file if args.file else config_service.get_active_vault()

    # 6. Bootstrap Vault Controller (Now that we have the password)
    vault_controller = bootstrap_controllers(
        auth_service=auth_service,
        config_service=config_service,
        view=view,
        encryptor=encryptor,
        clipboard=clipboard,
        validator=validator,
        user_password=user_password,
        vault_path=vault_path
    )

    # 7. Route Command
    route_command(args, vault_controller, parser)

if __name__ == "__main__":
    run()
