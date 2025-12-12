import os
import sys
from typing import Any, Dict

# Ensure we can import ai_common if it's installed in the venv
# If ai-common is a subdirectory and not installed, we might need to append it to path
# But since we installed it in the previous steps via headers, standard import
# should work. Just in case, we add the current directory to path.
sys.path.append(os.getcwd())

from ai_common.logger.custom_logger import logger  # noqa: E402
from ai_common.model_loader import (  # noqa: E402
    ApiKeyManager,
    BaseProvider,
    ModelLoader,
)


# --- 1. Custom Provider Implementation ---
class DummyProvider(BaseProvider):
    """
    A dummy provider that returns string objects instead of real models.
    Useful for testing or when actual model access isn't required.
    """

    def load_llm(self, api_key_mgr: ApiKeyManager, config: Dict[str, Any], **kwargs):
        model_name = kwargs.get("model_name", "default-dummy")
        return f"DummyLLM(model={model_name})"

    def load_embedding(
        self, api_key_mgr: ApiKeyManager, config: Dict[str, Any], **kwargs
    ):
        return "DummyEmbeddings()"


# --- 2. Usage Examples Classes ---


class StandardUsage:
    """
    Demonstrates how to use the built-in providers (Google, Groq) using a config file.
    """

    def __init__(self):
        # Load configuration from yaml file
        config_path = "example_config.yaml"

        if not os.path.exists(config_path):
            logger.warning(f"Config file not found at {config_path}")

        logger.info(f"Loading config from: {config_path}")
        self.loader = ModelLoader(config_path=config_path)

    def run(self):
        logger.info("--- Running Standard Usage Example ---")

        # Google LLM
        try:
            # Note: Expects GOOGLE_API_KEY to be set
            llm = self.loader.load_llm(provider="google")
            logger.info(f"Loaded Standard LLM (Google): {type(llm)}")
        except Exception as e:
            logger.warning(f"Standard LLM (Google) skipped or failed: {e}")

        # Google Embeddings
        try:
            embeddings = self.loader.load_embeddings(provider="google")
            logger.info(f"Loaded Standard Embeddings (Google): {type(embeddings)}")
        except Exception as e:
            logger.warning(f"Standard Embeddings (Google) skipped or failed: {e}")


class CustomUsage:
    """
    Demonstrates how to register and use a custom provider.
    """

    def __init__(self):
        # Init loader (config is optional if provider doesn't strictly need it)
        self.loader = ModelLoader()

    def run(self):
        logger.info("--- Running Custom Usage Example ---")

        # 1. Register the custom provider
        self.loader.register_provider("dummy", DummyProvider())
        logger.info("Registered 'dummy' provider.")

        # 2. Use it to load LLM
        # We can pass ad-hoc arguments supported by the provider
        my_llm = self.loader.load_llm(provider="dummy", model_name="my-test-model")
        logger.info(f"Loaded Custom LLM: {my_llm}")

        # 3. Use it to load Embeddings
        my_emb = self.loader.load_embeddings(provider="dummy")
        logger.info(f"Loaded Custom Embeddings: {my_emb}")


def main():
    # Execute Standard Usage
    try:
        standard_demo = StandardUsage()
        standard_demo.run()
    except Exception as e:
        logger.error(f"Standard usage failed: {e}")

    # Execute Custom Usage
    try:
        custom_demo = CustomUsage()
        custom_demo.run()
    except Exception as e:
        logger.error(f"Custom usage failed: {e}")


if __name__ == "__main__":
    main()
