import secrets
import string

class PasswordGenerator:
    @staticmethod
    def generate(length: int = 16, use_symbols: bool = True, use_numbers: bool = True) -> str:
        
        min_length = 1 + int(use_symbols) + int(use_numbers)
        if length < min_length:
            raise ValueError(f"Length {length} is too short for the requested constraints.")
        
        secure_random = secrets.SystemRandom()
        password_chars = []
        
        chars = string.ascii_letters
        password_chars.append(secure_random.choice(string.ascii_letters))

        if use_numbers:
            chars += string.digits
            password_chars.append(secure_random.choice(string.digits))

        if use_symbols:
            chars += string.punctuation
            password_chars.append(secure_random.choice(string.punctuation))
        
        while len(password_chars) < length:
            password_chars.append(secure_random.choice(chars))

        secure_random.shuffle(password_chars)

        return ''.join(password_chars)