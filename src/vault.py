from tabulate import tabulate
from cryptography.fernet import Fernet
from .cryptography_handler import CryptoHandler
from rich import print as rich_print
from rich.panel import Panel
import json
import os

class Vault:
    def __init__(self, password, filepath='credentials.json'):
        self.filepath = filepath
        self.cryptography = CryptoHandler()
        self.salt = self._load_salt()
        self.key = self.cryptography.derive_key(password, self.salt)
        self.credentials = self._load_credentials()
    
    def _load_salt(self):
        try: 
            with open(self.filepath, 'rb') as f:
                return f.read(16)
        except (IOError, FileNotFoundError):
            return os.urandom(16)
        
    def _load_credentials(self):
        try:
            with open(self.filepath, 'rb') as f:
                f.seek(16)
                encrypted_data = f.read()

                if not encrypted_data:
                    return []
                
                fernet = Fernet(self.key)
                decrypted_data = fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
                
        except (IOError, FileNotFoundError):
            return []

    def _save(self):
        fernet = Fernet(self.key)
        credentials_json = json.dumps(self.credentials, indent=4)
        encrypted_data = fernet.encrypt(credentials_json.encode())

        with open(self.filepath, 'wb') as f:
            f.write(self.salt)
            f.write(encrypted_data)

    def add(self, service, username, password):
        self.credentials.append(
        {
        "service": service,
        "username": username,
        "password": password
        })
        self._save()
    
        rich_print("\n[green] Crednetial added successfully![/green]\n")

    def view(self):
        if not self.credentials:
            print("Your vault is empty! - vault")
            return

        display_data = [
            {"service": cred["service"], "username": cred["username"]} 
            for cred in self.credentials
            ]

        table_string = tabulate(display_data, headers="keys", tablefmt="grid")
        rich_print(Panel(table_string, title="[bold cyan]Vault Contents[/bold cyan]", border_style="Blue"))

    def delete(self, service_to_delete):
        count = len(self.credentials)
        self.credentials = [
            cred for cred in self.credentials
            if cred['service'] != service_to_delete]

        if len(self.credentials) < count:
            self._save()
            rich_print(f"\n[green] Credential for '[bold]{service_to_delete}[/bold]' has been deleted.[/green]\n")
        else:
            rich_print(f"\n[yellow]No credential found for service '[bold]{service_to_delete}[/bold]'.[/yellow]\n")

    def get_password(self, service_to_find):
        for cred in self.credentials:
            if cred['service'].lower() == service_to_find.lower():
                return cred['password']
        
        return None

    def update_credential(self, service_to_update):
        for cred in self.credentials:
            if cred['service'].lower() == service_to_update.lower():
                rich_print(f"\n[bold cyan]=== Updating '{cred['service']}' ===[/bold cyan]\n")
                rich_print(f"Current username: {cred['username']}")

                new_username = input("Enter new username (or press Enter to keep current): ")
                if new_username:
                    cred['username'] = new_username

                new_password = input("Enter new password (or press Enter to keep current): ")
                if new_password:
                    cred['password'] = new_password 

                self._save()
                rich_print(f"\n[green] Credential for '[bold]{service_to_update}[/bold]' has been updated.[/green]\n")
                return
        
        print(f"\n[yellow] Service '[bold]{service_to_update}[/bold]' not found.[/yellow\n]")

