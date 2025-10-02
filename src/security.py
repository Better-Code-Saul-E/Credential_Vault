from src.cryptography_handler import CryptoHandler
from rich import print as rich_print
from rich.panel import Panel
import getpass
import os

class SecurityManager:
    def __init__(self, hash_file='master.hash'):
        self.hash_file = hash_file
        self.cryptography = CryptoHandler()
    
    def setup_master_password(self):
        rich_print(Panel.fit("[yellow]--- First-Time Setup: Master Password ---[/yellow]"))    
        rich_print("\n[italic dim]Your typing will be hidden for security.[/italic dim]\n")

        password = getpass.getpass("Create a new master password: ")
        password_confirm = getpass.getpass("Confirm master password: ")

        if password != password_confirm:
            rich_print("\n[bold red] Passwords do not match. Please try again.[/bold red]\n")    
            return False
        
        hashed_password = self.cryptography.hash_password(password)
        with open(self.hash_file, 'w') as f:
            f.write(hashed_password)

        rich_print("\n[green] Master password has been set up successfully![/green]\n")
        return True
    
    def verify_master_password(self):
        if not os.path.exists(self.hash_file):
            rich_print("\n[yellow] No master password found. Starting first-time setup.. [/yellow]\n")
            if not self.setup_master_password():
                return False
        
        try:
            with open(self.hash_file, 'r') as f:
                stored_hash = f.read().strip()
        except FileNotFoundError:
            return False
        
        rich_print("\n[bold] Enter master password:[/bold]\n", end="")
        user_password = getpass.getpass(" ")
        user_password_hash = self.cryptography.hash_password(user_password)

        if user_password_hash == stored_hash:
            return user_password
        else:
            return None


