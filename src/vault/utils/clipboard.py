import pyperclip
import threading
from ..interfaces.user_io_interface import IClipboard

class SystemClipboard(IClipboard):
    def copy_to_clipboard(self, text: str):
        pyperclip.copy(text)

    def clear_clipboard(self):
        return pyperclip.copy("")

