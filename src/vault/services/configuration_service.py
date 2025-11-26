import json
import os


# Refactor Notes:
# - Add type hints for get_active_vault, set_active_vault


class ConfigurationService:
    """
    Manages application configuration such as the active vault.
    Handles loading, saving, and default values for configuration settings.
    """

    def __init__(self, config_path: str, data_dir: str):
        self.config_path = config_path
        self.data_dir = data_dir
        
        self.defaults = {
            "active_vault": os.path.join(data_dir, "credentials.json")
        }

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return self.defaults

        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
            
        except (IOError, json.JSONDecodeError):
            return self.defaults

    def _save_config(self, config):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)

            return True
        
        except IOError:
            return False

    def get_active_vault(self):
        config = self._load_config()
        return config.get("active_vault", self.defaults["active_vault"])

    def set_active_vault(self, vault_name):
        config = self._load_config()
        
        if os.path.sep in vault_name:
            path = vault_name

        else:
            filename = f"{vault_name}.json" if not vault_name.endswith('.json') else vault_name
            path = os.path.join(self.data_dir, filename)

        config["active_vault"] = path
        self._save_config(config)
        
        return path