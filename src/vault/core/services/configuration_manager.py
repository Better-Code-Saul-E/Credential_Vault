import json
import os

class ConfigurationManager:
    def __init__(self, config_file='data/config.json'):
        self.config_file = config_file
        self.defaults = {
            "active_vault": "data/credentials.json"
        }

    def _load_config(self):
        if not os.path.exists(self.config_file):
            return self.defaults

        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except(IOError, json.JSONDecodeError):
            return self.defaults

    def _save_config(self, config):
        try:
            with open(self.config_file, 'w') as f:
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
            path = os.path.join("data", filename)

        config["active_vault"] = path
        self._save_config(config)
        return path