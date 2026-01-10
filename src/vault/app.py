import os
import sys
import argparse
import shlex

from .utils.encryptors import FernetDataEncryptor, Pbkdf2PasswordHasher
from .utils.password_validator import PasswordStrength
from .utils.clipboard import SystemClipboard
from .views.console_view import ConsoleView

from .repositories.file_master_hash_repository import FileMasterHashRepository
from .repositories.json_repository import JsonRepository
from .services.authentication_service import AuthenticationService
from .services.vault_service import VaultService
from .services.configuration_service import ConfigurationService
from .services.credential_input_service import CredentialInputService
from .services.vault_transfer_service import VaultTransferService
from .services.audit_service import AuditService

from .controllers.vault_controller import VaultController
from .controllers.authentication_controller import AuthenticationController

def ensure_data_directory(data_dir: str):
    os.makedirs(data_dir, exist_ok=True)

def setup_tools() -> tuple[FernetDataEncryptor, Pbkdf2PasswordHasher, SystemClipboard, ConsoleView, PasswordStrength]:
    encryptor = FernetDataEncryptor()
    hasher = Pbkdf2PasswordHasher()
    clipboard = SystemClipboard()
    view = ConsoleView()
    validator = PasswordStrength()  
    return encryptor, hasher, clipboard, view, validator

def setup_services(hash_file: str, config_file: str, data_dir: str, hasher: Pbkdf2PasswordHasher) -> tuple[AuthenticationService, ConfigurationService]:
    hash_repo = FileMasterHashRepository(hash_file)
    auth_service = AuthenticationService(repo=hash_repo, hasher=hasher)
    config_service = ConfigurationService(config_file, data_dir) 
    audit_servie = AuditService(data_dir)
    
    return auth_service, config_service, audit_servie

def bootstrap_controllers(auth_service: AuthenticationService, config_service: ConfigurationService, audit_service: AuditService,
                          view: ConsoleView, encryptor: FernetDataEncryptor, clipboard: SystemClipboard, 
                          validator: PasswordStrength, user_password: str, vault_path: str) -> VaultController:
    """Construct repositories, servicies, and controllers with their dependencies."""
    
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
        credential_input=credential_input_service,
        audit_service=audit_service
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

    subparsers.add_parser('audit', help='View audit logs.')
    subparsers.add_parser('view', help='View all credentials.')
    subparsers.add_parser('passwd', help='Change the master password.')
    
    parser.add_argument('-f', '--file', type=str, metavar='FILEPATH', help='Specify a custom vault file path.')
    return parser

def route_command(args, vault_controller: VaultController, parser: argparse.ArgumentParser):
    if not args.command:
        parser.print_help()
        return
    
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
    elif args.command == 'audit':
        vault_controller.show_audit_logs()





# -------------------------------
# Interactive Shell
# -------------------------------
def run_interactive_shell(controller: VaultController, view: ConsoleView):
    vault_name = controller.get_vault_name()
    view.show_header(f"{vault_name} [Session Active]")
    view.show_info("Type 'help' for commands, 'exit' to quit.")

    while True:
        try:
            user_input = view.get_input(f"vault({vault_name}) > ").strip()

            if not user_input:
                continue

            if user_input.lower() in ('exit', 'quit'):
                view.show_info("Closing session...")
                break

            if user_input.lower() == 'help':
                view.show_info("Commands: view, add, get, delete, update, search, passwd, export, import, exit")
                continue

            parts = shlex.split(user_input)
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd == 'view':
                controller.view_all_entrys()
            elif cmd == 'add' and len(args) >= 1:
                controller.add_entry(args[0])
            elif cmd == 'get' and len(args) >= 1:
                controller.get_entry(args[0])
            elif cmd == 'delete' and len(args) >= 1:
                controller.delete_entry(args[0])
            elif cmd == 'update' and len(args) >= 1:
                controller.update_entry(args[0])
            elif cmd == 'search' and len(args) >= 1:
                controller.find_entry(args[0])
            elif cmd == 'passwd':
                controller.change_password()
            elif cmd == 'export' and len(args) >= 1:
                controller.export_vault(args[0])
            elif cmd == 'import' and len(args) >= 1:
                controller.import_vault(args[0])
            elif cmd == 'audit':
                controller.show_audit_logs()
            elif cmd == 'switch':
                view.show_warning("Switching vaults requires restarting the session. Please 'exit' and run 'switch' command.")
            else:
                view.show_error(f"Unknown command or missing arguments: {cmd}")

        except KeyboardInterrupt:
            view.show_error("Type 'exit' to quit.")
        except Exception as e:
            view.show_error(f"Error: {e}")

# -------------------------------
# Main Run Function
# -------------------------------
def run():
    BASE_DIR = os.getcwd()
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    HASH_FILE = os.path.join(DATA_DIR, 'master.hash')
    CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

    ensure_data_directory(DATA_DIR)

    encryptor, hasher, clipboard, view, validator = setup_tools()
    auth_service, config_service, audit_service = setup_services(HASH_FILE, CONFIG_FILE, DATA_DIR, hasher)

    parser = create_parser()

    if len(sys.argv) == 1:
        interactive_mode = True
        args = None
    else:
        interactive_mode = False
        args = parser.parse_args()

    if not interactive_mode and args.command == 'switch':
        new_path = config_service.set_active_vault(args.vault_name)
        
        vault_name = os.path.basename(new_path)
        clean_name = os.path.splitext(vault_name)[0].capitalize()
        
        view.show_header(clean_name)
        view.show_success(f"Switched active vault to: {new_path}")
        return 

    auth_controller = AuthenticationController(auth_service, view, config_service, audit_service)
    user_password = auth_controller.authenticate_user()
    if not user_password:
        sys.exit(1)

    if interactive_mode:
        vault_path = config_service.get_active_vault()
    else:
        vault_path = args.file if args.file else config_service.get_active_vault()

    vault_controller = bootstrap_controllers(
        auth_service=auth_service,
        config_service=config_service,
        view=view,
        encryptor=encryptor,
        clipboard=clipboard,
        validator=validator,
        user_password=user_password,
        vault_path=vault_path,
        audit_service=audit_service
    )
    if interactive_mode:
        run_interactive_shell(vault_controller, view)
    else:
        if not args.command:
            parser.print_help()
            return
        route_command(args, vault_controller, parser)

if __name__ == "__main__":
    run()
