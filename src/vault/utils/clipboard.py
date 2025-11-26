import pyperclip
from ..interfaces.user_io_interface import IClipboard

class SystemClipboard(IClipboard):
    def copy_to_clipboard(self, text: str):
        pyperclip.copy(text)