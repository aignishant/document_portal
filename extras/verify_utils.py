import os
import sys

sys.path.append(os.path.abspath("ai-common"))

from AIFoundationKit.base.exception.custom_exception import (  # noqa: E402
    ConfigException,
)
from AIFoundationKit.base.utils import load_config  # noqa: E402


def test_load_config():

    config_path = "config/config.yaml"

    try:

        _ = load_config(config_path)

        print("Successfully loaded config.")

    except Exception as e:

        print(f"Failed to load existing config: {e}")

    try:

        load_config("non_existent_file.yaml")

    except ConfigException as e:

        print(f"Caught expected ConfigException for missing file: {e}")

    except Exception as e:

        print(f"Caught unexpected exception for missing file: {type(e).__name__}: {e}")


if __name__ == "__main__":

    test_load_config()
