import os
from ..services.authentication_service import AuthenticationService
from ..interfaces.user_io_interface import IUserIO
from ..services.configuration_service import ConfigurationService
from ..services.audit_service import AuditService


class AuthenticationController:
    """
    Manages user authentication flow including login and first-time setup.
    Delegates password verification to AuthenticationService and handles CLI input/output.
    """


    def __init__(self, auth_service: AuthenticationService, io: IUserIO, config_service: ConfigurationService, audit_service: AuditService):
        self.auth_service = auth_service
        self.io = io
        self.config = config_service
        self.audit = audit_service
    
    def _get_vault_name(self):
        full_path = self.config.get_active_vault()
        filename = os.path.basename(full_path)
        return os.path.splitext(filename)[0].capitalize()

    def _handle_first_time_setup(self):
        self.io.show_warning("No master password found. Starting first-time setup...")
        self.io.show_info("Your typing will be hidden for security.")

        try:
            password = self.io.get_password("Create a new master password: ")
            confirm = self.io.get_password("Confirm master password: ")
        except (KeyboardInterrupt, EOFError):
            self.io.show_error("Setup cancelled.")
            return None

        if password != confirm:
            self.io.show_error("Passwords do not match.")
            return None
        
        if not password:
            self.io.show_error("Password cannot be empty.")
            return None

        if self.auth_service.create_master_hash(password):
            self.io.show_success("Master password has been set up successfully!")
            return password
        else:
            self.io.show_error("Failed to save master password.")
            return None

    def _handle_login(self):
        try:
            password = self.io.get_password("Enter master password: ")

        except (KeyboardInterrupt, EOFError):
            self.audit.log_event("LOGIN_ABORT", "User cancelled login")
            self.io.show_error("Login cancelled.")
            return None

        if self.auth_service.verify_password(password):
            self.audit.log_event("LOGIN_SUCCESS", "User authenticated successfully") 
            self.io.show_success("Access granted")
            return password
        else:
            self.audit.log_event("LOGIN_FAILURE", "Incorrect master password attempt") 
            self.io.show_error("ACCESS DENIED")
            return None
    
    def authenticate_user(self) -> str | None:
        self.io.show_header(self._get_vault_name())

        if  self.auth_service.repo.load_hash() is None:
            self.audit.log_event("SETUP", "First time setup initiated")
            return self._handle_first_time_setup()
        else:
            return self._handle_login()