from abc import ABC, abstractmethod
from typing import Tuple, List
from ..models.password_strength_result import PasswordStrengthResult

class IPasswordValidator(ABC):
    """
    Specifies methods for password hashing and verification for authentication purposes.
    """

    @abstractmethod
    def validate_password_requirements(self, password: str) -> Tuple[PasswordStrengthResult, List[str]]: 
        pass
    