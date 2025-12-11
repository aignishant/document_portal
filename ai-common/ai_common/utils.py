import yaml
import os
from typing import Dict, Any
from ai_common.exception.custom_exception import ConfigException

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: The configuration as a dictionary.

    Raises:
        ConfigException: If the config file does not exist or if there is an error parsing the YAML file.
    """
    if not os.path.exists(config_path):
        raise ConfigException(f"Config file not found: {config_path}")

    with open(config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            raise ConfigException(f"Error parsing YAML file: {e}")
