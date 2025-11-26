from abc import ABC, abstractmethod

class IClipboard(ABC):
    """
    Defines clipboard operations to allow copying data to system clipboard.
    """

    @abstractmethod
    def copy_to_clipboard(self, text: str):
        pass

class IUserIO(ABC):
    """
    Defines user input/output operations for console interactions.
    Abstracts CLI details from controllers.
    """

    @abstractmethod
    def get_input(self, prompt: str) -> str: 
        pass
    
    @abstractmethod
    def get_password(self, prompt: str) -> str: 
        pass
    
    @abstractmethod
    def show_header(self): 
        pass

    @abstractmethod
    def show_message(self, msg: str): 
        pass
    
    @abstractmethod
    def show_info(self, msg: str): 
        pass

    @abstractmethod
    def show_warning(self, msg: str): 
        pass
    
    @abstractmethod
    def show_error(self, msg: str): 
        pass
    
    @abstractmethod
    def show_success(self, msg: str): 
        pass

    @abstractmethod
    def show_credential_list(self, data: dict): 
        pass

    @abstractmethod
    def show_search_results(self, matches: dict, query: str): 
        pass

    @abstractmethod
    def show_password_strength(self, formatted_score: str): 
        pass


