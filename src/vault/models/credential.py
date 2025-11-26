from dataclasses import dataclass

@dataclass
class Credential:
    """
        Represents a single stored credential in the vault
    
        Attributes:
        service_name: The name of the service (e.g., 'GitHub')
        username: The username or email for the account
        password: The associated password or secret
    """
        
    service_name: str
    username: str
    password: str