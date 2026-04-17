from ..interfaces.user_io_interface import IUserIO
from ..interfaces.password_validator_interface import IPasswordValidator
from ..models.password_strength_result import PasswordStrengthResult

class CredentialInputService:
    """
    Handles secure user input for credentials, including password validation.
    Ensures passwords meet strength requirements before use.
    """


    def __init__(self, io: IUserIO, password_validator: IPasswordValidator):
        self.io = io
        self.validator = password_validator

    def get_valid_password(self) -> str:
        while True:
            password = self.io.get_password("Enter password: ")
            strength, feedback = self.validator.validate_password(password)
            self.io.show_password_strength(strength, feedback)

            if strength != PasswordStrengthResult.STRONG:
                confirm = self.io.get_input("Keep weak password? (y/n): ")

                if confirm.lower() != 'y':
                    continue
            
            confirm_password = self.io.get_password("Confirm password: ")
            if password != confirm_password:
                self.io.show_error("Passwords did not match. Please try again.")
                continue

            return password
    
    def get_optional_password(self) -> str | None:
        while True:
            password = self.io.get_password("New password: ")

            if not password: 
                return None

            strength, feedback = self.validator.validate_password(password)
            self.io.show_password_strength(strength, feedback)

            if strength != PasswordStrengthResult.STRONG:
                confirm = self.io.get_input("Keep weak password? (y/n): ")

                if confirm.lower() != 'y':
                    continue
            
            confirm_password = self.io.get_password("Confirm password: ")
            if password != confirm_password:
                self.io.show_error("Passwords did not match. Please try again.")
                continue

            return password
            
