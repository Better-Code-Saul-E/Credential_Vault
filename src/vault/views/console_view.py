import getpass
from rich import print as rich_print
from rich.table import Table
from rich.panel import Panel
from ..interfaces.user_io_interface import IUserIO


class ConsoleView(IUserIO):
    """
    Handles all terminal output formatting and user input.
    """
    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def get_password(self, prompt: str) -> str:
        return getpass.getpass(prompt)

    def show_header(self, vault_name="Default"):
        title = f"[bold cyan] Credential Vault : {vault_name} [/bold cyan]"
        rich_print(Panel.fit("=+~+="*2 + title + "=+~+="*2, border_style="blue"))

    def show_message(self, message: str):
        rich_print(message)

    def show_success(self, message: str):
        rich_print(f"\n[green]{message}[/green]\n")

    def show_error(self, message: str):
        rich_print(f"\n[bold red]{message}[/bold red]\n")

    def show_warning(self, message: str):
        rich_print(f"\n[yellow]{message}[/yellow]\n")

    def show_info(self, message: str):
        rich_print(f"[dim]{message}[/dim]")

    def show_credential_list(self, credentials: dict):
        if not credentials:
            self.show_warning("Vault is empty.")
            return

        table = Table(title="[bold cyan]Vault Contents[/bold cyan]", border_style="blue")
        table.add_column("Service", style="bold green", no_wrap=True)
        table.add_column("Username", style="magenta")
        
        for key in sorted(credentials.keys()):
            item = credentials[key]
            table.add_row(item['service_name'], item['username'])
        
        rich_print(table)

    def show_search_results(self, matches: dict, query: str):
        if not matches:
            self.show_warning(f"No credentials found containing '{query}'.")
            return

        table = Table(title=f"[bold cyan]Search Results: '{query}'[/bold cyan]", border_style="blue")
        table.add_column("Service", style="bold green", no_wrap=True)
        table.add_column("Username", style="magenta")
        
        for key in sorted(matches.keys()):
            item = matches[key]
            table.add_row(item['service_name'], item['username'])
            
        rich_print(table)

    def show_password_strength(self, formatted_score: str):
        rich_print(f"Password Strength: {formatted_score}")

    def show_audit_table(self, logs: list[dict]):
        if not logs:
            self.show_warning("No audit history found.")
            return

        table = Table(title="Audit Log History")

        table.add_column("Timestamp", style="cyan", no_wrap=True)
        table.add_column("Action", style="bold magenta")
        table.add_column("Details", style="white")

        for log in logs:
            action_style = "white"
            if "FAIL" in log['action']:
                action_style = "bold red"
            elif "DELETE" in log['action']:
                action_style = "red"
            elif "ADD" in log['action'] or "IMPORT" in log['action']:
                action_style = "green"
            elif "SWITCH" in log['action']:
                action_style = "yellow"

            table.add_row(
                log['timestamp'], 
                f"[{action_style}]{log['action']}[/{action_style}]", 
                log['details']
            )

        self.show_message(table)
        print()