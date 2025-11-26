from ..interfaces.encryption_interface import IPasswordHasher
from ..interfaces.master_hash_repository_interface import IMasterHashRepository


class AuthenticationService:
    """
    Handles master password verification and creation.
    Delegates hashing to an injected IPasswordHasher implementation.
    Delegates storage to an IMasterHashRepository implementation.
    """

    def __init__(self, repo: IMasterHashRepository, hasher: IPasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def create_master_hash(self, password: str) -> bool:
        hashed = self.hasher.hash_password(password)
        return self.repo.save_hash(hashed)

    def verify_password(self, password_attempt: str) -> bool:
        stored_hash = self.repo.load_hash()
        if stored_hash is None:
            return False

        return self.hasher.verify_password(password_attempt, stored_hash)