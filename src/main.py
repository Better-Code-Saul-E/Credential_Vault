from .vault import Vault
from .security import SecurityManager
from rich import print as rich_print
from rich.panel import Panel
import argparse
import pyperclip

def main():
    rich_print(Panel.fit("=+~+="*2+"[bold cyan] Credential Vault [/bold cyan]"+ "=+~+="*2, border_style="blue"))

    security = SecurityManager(hash_file='data/master.hash')

    user_password = security.verify_master_password()
    if not user_password:
        rich_print("X [bold red] ACCESS DENIED [/bold red]X")
        return
    
    print("Access granted")

    parser = argparse.ArgumentParser(description="A command-line credential vault.")
    parser.add_argument('--view', action='store_true', help='View all credentials in the vault.')
    parser.add_argument('--add', action='store_true', help='Add a new credential')
    parser.add_argument('--delete', help='Delete a credential')
    parser.add_argument('--file', help='Specify a vault file to use (e.g., data/work.json).')
    parser.add_argument('--get', help='Get and copy the password for a specific service.')
    parser.add_argument('--update', help='Update the credentials for a specific service.')
    args = parser.parse_args()

    filepath = args.file if args.file else 'data/credentials.json'
    my_vault = Vault(password=user_password, filepath=filepath)

    if args.view:
        my_vault.view()
    elif args.add:
        service = input("Enter the service (e.g., Google, Netflix): ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        my_vault.add(service, username, password)
    elif args.delete:
        my_vault.delete(args.delete)
    elif args.get:
        password = my_vault.get_password(args.get)

        if password:
            pyperclip.copy(password)
            rich_print(f"[green] Password for '[bold]{args.get}[/bold]' copied to clipboard.[/green]")
        else:
            rich_print(f"[yellow] Service '[bold]{args.get}[/bold]' not found in the vault.[/yellow]")
    elif args.update:
        my_vault.update_credential(args.update)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()