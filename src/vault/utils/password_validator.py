import re
from ..interfaces.password_validator_interface import IPasswordValidator

class PasswordStrength(IPasswordValidator):
    """
    Stateless password validator.
    Uses multiple methods for individual rules.
    """

    def _validate_min_length(self, password: str) -> tuple[bool, str]:
        return (len(password) >= 8, "Too short (min 8 chars)")

    def _validate_has_number(self, password: str) -> tuple[bool, str]:
        return (bool(re.search(r"\d", password)), "Add numbers")

    def _validate_mixed_case(self, password: str) -> tuple[bool, str]:
        return (bool(re.search(r"[A-Z]", password)) and bool(re.search(r"[a-z]", password)), "Mix uppercase & lowercase")

    def _validate_has_special_char(self, password: str) -> tuple[bool, str]:
        return (bool(re.search(r"[ !#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password)), "Add special chars (@, #, $, etc.)")

    def _validate_not_common(self, password: str) -> tuple[bool, str]:
        common = {"password", "admin"}
        return (password.lower() not in common, "Avoid common passwords")


    def validate_password(self, password: str) -> tuple[int, list[str]]:
        score = 0
        feedback = []

        for rule in [
            self._validate_min_length,
            self._validate_has_number,
            self._validate_mixed_case,
            self._validate_has_special_char,
            self._validate_not_common
        ]:

            passed, msg = rule(password)
            if passed:
                score += 1
            else:
                feedback.append(msg)

        return score, feedback

    def format_password_strength(self, score: int, feedback: list[str]) -> str:
        if score >= 4:
            return "[bold green]STRONG[/bold green]"
        elif score >= 2:
            return "[bold yellow]MEDIUM[/bold yellow]"
        else:
            return f"[bold red]WEAK[/bold red] ({', '.join(feedback)})"