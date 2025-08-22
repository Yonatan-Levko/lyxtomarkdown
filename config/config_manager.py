import json
import os
from .settings import DEFAULT_CONFIG

class ConfigManager:
    """Manages loading and saving of application configuration."""
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.default_config = DEFAULT_CONFIG

    def load_config(self):
        """Loads configuration from the JSON file.

        If the file doesn't exist or is invalid, returns the default config.
        """
        if not os.path.exists(self.config_path):
            return self.default_config.copy()
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                # Ensure all keys from default are present
                for key, value in self.default_config["paths"].items():
                    if key not in config.get("paths", {}):
                        config["paths"][key] = value
                return config
        except (json.JSONDecodeError, IOError):
            return self.default_config.copy()

    def save_config(self, config_data):
        """Saves the given configuration data to the JSON file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=4)
        except IOError as e:
            # This should be logged properly in a real application
            print(f"Error saving configuration: {e}")
