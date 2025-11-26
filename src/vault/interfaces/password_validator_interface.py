from abc import ABC, abstractmethod
from typing import Tuple, List

class IPasswordValidator(ABC):
    """
    Specifies methods for password hashing and verification for authentication purposes.
    """

    @abstractmethod
    def validate_password(self, password: str) -> Tuple[int, List[str]]: 
        pass
    
    @abstractmethod
    def format_password_strength(self, score: int, feedback: List[str]) -> str: 
        pass
