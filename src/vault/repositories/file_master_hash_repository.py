import os
from ..interfaces.master_hash_repository_interface import IMasterHashRepository


class FileMasterHashRepository(IMasterHashRepository):
    """
    Stores and retrieves the master password hash from a file.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def save_hash(self, hashed: str) -> bool:
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

            with open(self.filepath, "w") as f:
                f.write(hashed)
            return True
        
        except IOError:
            return False

    def load_hash(self) -> str | None:
        if not os.path.exists(self.filepath):
            return None
        
        try:
            with open(self.filepath, "r") as f:
                return f.read().strip()
            
        except IOError:
            return None
