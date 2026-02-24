import pytest
from unittest.mock import patch, MagicMock
from src.vault.utils.clipboard import SystemClipboard

@patch('src.vault.utils.clipboard.pyperclip.copy')
def test_copy_to_clipboard(mock_pyperclip_copy: MagicMock):
    clipboard = SystemClipboard()
    password = "TestPassword123!"

    clipboard.copy_to_clipboard(password)

    mock_pyperclip_copy.assert_called_once_with(password)

