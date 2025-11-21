import pyperclip
import getpass

from rich import print as rich_print
from rich.table import Table
from rich.panel import Panel
import pyperclip
from ..core.services.configuration_manager import ConfigurationManager


def handle_command(vault, args, parser):
    """
    Dispatches the command to the appropriate 
    function based on the parsed arguments.
    """
    
    if args.command == 'add':
        handle_add(vault, args.service)
    elif args.command == 'get':
        handle_get(vault, args.service)
    elif args.command == 'delete':
        handle_delete(vault, args.service)
    elif args.command == 'update':
        handle_update(vault, args.service)
    elif args.command == 'view':
        handle_list_all(vault)
    elif args.command == 'search':
        handle_search(vault, args.query)
    elif args.command == 'switch':
        handle_switch(args.vault_name)
    else:
        parser.print_help()

def handle_list_all(vault):
    credentials = vault.list_all_credentials()
    
    if not credentials:
        rich_print("[yellow]Your vault is empty.[/yellow]")
        return

    table = Table(title="[bold cyan]Vault Contents[/bold cyan]", border_style="blue")
    table.add_column("Service", style="bold green", no_wrap=True)
    table.add_column("Username", style="magenta")
    
    for service_key in sorted(credentials.keys()):
        item = credentials[service_key]
        table.add_row(item['service_name'], item['username'])
        
    rich_print(table)  
    
def handle_add(vault, service):
    rich_print(f"[bold]Adding new credential for:[/] [green]{service}[/green]")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    success = vault.add_credential(service, username, password)

    if success:
        rich_print(f"[green] Credential for '[bold]{service}[/bold]' added successfully.[/green]")
    else:
        rich_print(f"[yellow] Service '[bold]{service}[/bold]' already exists. Use 'update' to change it.[/yellow]")
      
def handle_get(vault, service):
    credential = vault.get_credential(service)
    
    if credential:
        password = credential['password']
        pyperclip.copy(password)
        rich_print(f"[green] Password for '[bold]{credential['service_name']}[/bold]' copied to clipboard.[/green]")
    else:
        rich_print(f"[yellow] Service '[bold]{service}[/bold]' not found.[/yellow]")  

def handle_delete(vault, service):
    success = vault.delete_credential(service)
    
    if success:
        rich_print(f"[green] Credential for '[bold]{service}[/bold]' has been deleted.[/green]")
    else:
        rich_print(f"[yellow] Service '[bold]{service}[/bold]' not found.[/yellow]") 
        
        
def handle_update(vault, service):
    existing_credential = vault.get_credential(service)
    if not existing_credential:
        rich_print(f"[yellow] Service '[bold]{service}[/bold]' not found. Use 'add' to create it.[/yellow]")
        return

    rich_print(f"[bold cyan]--- Updating '{existing_credential['service_name']}' ---[/bold cyan]")
    rich_print(f"Current username: {existing_credential['username']}")
    
    new_username = input("Enter new username (or press Enter to keep current): ")
    new_password = getpass.getpass("Enter new password (or press Enter to keep current): ")

    if not new_username:
        new_username = None
    if not new_password:
        new_password = None

    if not new_username and not new_password:
        rich_print("[dim]No changes made.[/dim]")
        return

    success = vault.update_credential(service, new_username, new_password)
    
    if success:
        rich_print(f"[green] Credential for '[bold]{existing_credential['service_name']}[/bold]' has been updated.[/green]")
    else:
        rich_print(f"[red]Error updating credential.[/red]")

def handle_search(vault, query):
    matches = vault.search_credentials(query)

    if not matches:
        rich_print(f"[yellow]No credentials found containing '{query}'.[/yellow]")
        return
    
    table = Table(title=f"[bold cyan]Search Results: '{query}'[/bold cyan]", border_style="blue")
    table.add_column("Service", style="bold green", no_wrap=True)
    table.add_column("Username", style="magenta")

    for service_key in sorted(matches.keys()):
        item = matches[service_key]
        table.add_row(item['service_name'], item['username'])

    rich_print(table)

def handle_switch(vault_name):
    config_mgr = ConfigurationManager()
    new_path = config_mgr.set_active_vault(vault_name)
    rich_print(f"[green] Switched active vault to: [bold]{new_path}[/bold][/green]")