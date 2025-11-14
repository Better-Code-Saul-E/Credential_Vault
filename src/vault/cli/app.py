import argparse
import sys
import os

from rich import print as rich_print
from rich.panel import Panel

from .authentication import handle_authentication
from .handler import handle_command
from ..core.vault import Vault



def create_parser():
    parser = argparse.ArgumentParser(description="A command-line credential vault.")
    
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--add', type=str, metavar='SERVICE', help='Add a new credential for SERVICE.')
    group.add_argument('--get', type=str, metavar='SERVICE', help='Get the password for SERVICE.')
    group.add_argument('--delete', type=str, metavar='SERVICE', help='Delete the credential for SERVICE.')
    group.add_argument('--update', type=str, metavar='SERVICE', help='Update the credential for SERVICE.')
    
    group.add_argument('--view', action='store_true', help='View all credentials in the vault.')
    parser.add_argument('-f', '--file', type=str, metavar='FILEPATH', help='Specify a custom vault file path.')

    return parser

def run():
    
    data_dir = 'data'
    default_hash_file = os.path.join(data_dir,'master.hash')
    default_vault_file = os.path.join(data_dir, 'dredentials.json')
    
    os.makedirs(data_dir, exist_ok=True)
    
    user_password = handle_authentication(default_hash_file)
    if not user_password:
        sys.exit(1)
    
    parser = create_parser()
    args = parser.parse_args()

    filepath = args.file if args.file else default_vault_file
    try:
        my_vault = Vault(password=user_password, filepath=filepath)
    except ValueError as e:
        rich_print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        rich_print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        sys.exit(1)
    
    handle_command(my_vault, args, parser)