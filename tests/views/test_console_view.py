import builtins
import getpass
import pytest
from src.vault.views.console_view import ConsoleView


@pytest.fixture
def console_view():
    return ConsoleView()

def test_console_input(console_view, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test_user')
    user_input = console_view.get_input("Who is accessing this application: ")

    assert user_input == "test_user"

def test_getpass_input(console_view, monkeypatch):
    monkeypatch.setattr('getpass.getpass', lambda _: 'test_password')
    user_password = console_view.get_password("Enter your password: ")

    assert user_password == "test_password"

@pytest.mark.parametrize("view_operation", [
    ("show_message"),
    ("show_error"),
    ("show_success"),
    ("show_info"),
    ("show_warning")
])
def test_console_view_output(view_operation, console_view, capsys):
    operation = getattr(console_view, view_operation)
    operation("test text to print")
    captured = capsys.readouterr()

    assert "test text to print" in captured.out

def test_empty_vault_output(console_view, capsys):
    console_view.show_credential_list({})
    captured = capsys.readouterr()

    assert "Vault is empty." in captured.out

def test_filled_vault_output(console_view, capsys):
    console_view.show_credential_list({
    "apple": {
        "service_name": "apple",
        "username": "steve homeless",
        "password": "appleBest"
    }})
    captured = capsys.readouterr()

    assert "apple" in captured.out
    assert "steve homeless" in captured.out

def test_empty_credential_search(console_view, capsys):
    console_view.show_search_results({}, "apple")
    captured = capsys.readouterr()

    assert "No credentials found containing 'apple'." in captured.out

def test_successful_credential_search(console_view, capsys):
    console_view.show_search_results({
    "apple": {
        "service_name": "apple",
        "username": "steve homeless",
        "password": "appleBest"
    }}, "apple")
    captured = capsys.readouterr()

    assert "apple" in captured.out

def test_empty_log_audit(console_view, capsys):
    console_view.show_audit_table([])
    captured = capsys.readouterr()

    assert "No audit history found." in captured.out

def test_populated_log_audit(console_view, capsys):
    console_view.show_audit_table([
    {"timestamp": "2026-02-18 11:12:33", "action": "LOGIN_SUCCESS", "details": "User authenticated successfully"},
    {"timestamp": "2026-02-18 11:13:19", "action": "DELETE", "details": "Deleted credential: google"},
    {"timestamp": "2026-02-18 11:13:30", "action": "IMPORT", "details": "Imported 2 items from backup.json"},
    {"timestamp": "2026-02-18 11:45:00", "action": "LOGIN_FAIL", "details": "Invalid master password attempt"}
    ])
    captured = capsys.readouterr()

    assert "2026-02-18 11:12:33" in captured.out
    assert "Deleted credential: google" in captured.out
    assert "LOGIN_FAIL" in captured.out