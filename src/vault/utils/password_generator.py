import secrets
import string

class PasswordGenerator:
    @staticmethod
    def generate(length: int = 16, use_symbols: bool = True, use_numbers: bool = True) -> str:
        chars = string.ascii_letters

        if use_numbers:
            chars += string.digits

        if use_symbols:
            chars += string.punctuation
        
        return ''.join(secrets.choice(chars) for _ in range(length))