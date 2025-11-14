from rich import print as rich_print
from rich.panel import Panel
import getpass
import sys

from ..core.services.security_manager import SecurityManager


def handle_authentication(hash_path):
    security = SecurityManager(hash_file=hash_path)
    
    if not security.hash_file_exists():
        return prompt_for_new_password(security)
    else:
        return prompt_for_login(security)



def prompt_for_new_password(security_manager):
    rich_print(Panel.fit("[yellow]--- First-Time Setup: Master Password ---[/yellow]"))    
    rich_print("\n[italic dim]Your typing will be hidden for security.[/italic dim]\n")
    
    try: 
        password = getpass.getpass("Create a new master password")
        password_confirm = getpass.getpass("Confirm master password")
    except(KeyboardInterrupt, EOFError):
        rich_print("\n[bold red]Setup cancelled.[/bold red]")
        return None
    
    if not password:
        rich_print("\n[bold red]Password cannot be empty. Setup cancelled.[/bold red]\n")
        return None

    if password != password_confirm:
        rich_print("\n[bold red]Passwords do not match. Please try again.[/bold red]\n")    
        return None
    
    if security_manager.create_master_hash(password):
        rich_print("\n[green]Master password has been set up successfully![/green]\n")
        return password
    else:
        rich_print("\n[bold red]Failed to save master password.[/bold red]\n")
        return None
    
def prompt_for_login(security_manager):
    rich_print(Panel.fit("=+~+="*2+"[bold cyan] Credential Vault [/bold cyan]"+ "=+~+="*2, border_style="blue"))
    rich_print("\n[bold]Enter master password:[/bold]", end="")
    
    try:
        user_password = getpass.getpass(" ")
    except (KeyboardInterrupt, EOFError):
        rich_print("\n[bold red]Login cancelled.[/bold red]")
        return None
    
    if security_manager.verify_password(user_password):
        rich_print("[green]Access granted[/green]")
        return user_password
    else:
        rich_print("\nX [bold red] ACCESS DENIED [/bold red]X\n")
        return None
    
