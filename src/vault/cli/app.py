import argparse
import sys
import os

from rich import print as rich_print
from rich.panel import Panel

from .authentication import handle_authentication
from .handler import handle_command
from ..core.vault import Vault
from ..core.services.configuration_manager import ConfigurationManager


def create_parser():
    parser = argparse.ArgumentParser(description="A command-line credential vault.")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="The action to perform.")

    add_parser = subparsers.add_parser('add', help='Add a new credential.')
    add_parser.add_argument('service', type=str, help='The name of the service to add (e.g., "Google").')
    
    get_parser = subparsers.add_parser('get', help='Get the password for a service.')
    get_parser.add_argument('service', type=str, help='The name of the service to get.')
    

    delete_parser = subparsers.add_parser('delete', help='Delete a credential.')
    delete_parser.add_argument('service', type=str, help='The name of the service to delete.')
    
    update_parser = subparsers.add_parser('update', help='Update a credential.')
    update_parser.add_argument('service', type=str, help='The name of the service to update.')
    
    search_parser = subparsers.add_parser('search', help='Search for credentials.')
    search_parser.add_argument('query', type=str, help=('The search term (e.g., "google"),'))

    view_parser = subparsers.add_parser('view', help='View all credentials in the vault.')

    switch_parser = subparsers.add_parser('switch', help='Switch the active vault.')
    switch_parser.add_argument('vault_name', type=str, help='Name of the vault to switch to (e.g., "work").')

    parser.add_argument('-f', '--file', type=str, metavar='FILEPATH', help='Specify a custom vault file path.')

    return parser

def run():
    
    data_dir = 'data'
    default_hash_file = os.path.join(data_dir,'master.hash')
    os.makedirs(data_dir, exist_ok=True)
    
    user_password = handle_authentication(default_hash_file)
    if not user_password:
        sys.exit(1)
    
    parser = create_parser()
    args = parser.parse_args()
    config_mgr = ConfigurationManager()

    if args.file:
        filepath = args.file
    else:
        filepath = config_mgr.get_active_vault()

    try:
        my_vault = Vault(password=user_password, filepath=filepath)
    except ValueError as e:
        rich_print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        rich_print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        sys.exit(1)
    
    handle_command(my_vault, args, parser)