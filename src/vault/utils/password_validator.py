import re
from ..models.password_strength_result import PasswordStrengthResult
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


    def validate_password(self, password: str) -> tuple[PasswordStrengthResult, list[str]]:
        score = 0
        feedback = []

        for rule in [
            self._validate_min_length,
            self._validate_has_number,
            self._validate_mixed_case,
            self._validate_has_special_char
        ]:

            passed, msg = rule(password)
            if passed:
                score += 1
            else:
                feedback.append(msg)

        if score >= 4:
            result = PasswordStrengthResult.STRONG
        elif score >= 2:
            result = PasswordStrengthResult.MEDIUM
        else:
            result = PasswordStrengthResult.WEAK

        return result, feedback
