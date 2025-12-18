import os
import sys
from typing import Any, Dict

sys.path.append(os.getcwd())

from AIFoundationKit.base.logger.custom_logger import logger  # noqa: E402
from AIFoundationKit.rag.model_loader import (  # noqa: E402
    ApiKeyManager,
    BaseProvider,
    ModelLoader,
)


class DummyProvider(BaseProvider):

    def load_llm(self, api_key_mgr: ApiKeyManager, config: Dict[str, Any], **kwargs):

        model_name = kwargs.get("model_name", "default-dummy")

        return f"DummyLLM(model={model_name})"

    def load_embedding(

        self, api_key_mgr: ApiKeyManager, config: Dict[str, Any], **kwargs

    ):

        return "DummyEmbeddings()"


class StandardUsage:

    def __init__(self):

        config_path = "example_config.yaml"

        if not os.path.exists(config_path):

            logger.warning(f"Config file not found at {config_path}")

        logger.info(f"Loading config from: {config_path}")

        self.loader = ModelLoader(config_path=config_path)

    def run(self):

        logger.info("--- Running Standard Usage Example ---")

        try:

            llm = self.loader.load_llm(provider="google")

            logger.info(f"Loaded Standard LLM (Google): {type(llm)}")

        except Exception as e:

            logger.warning(f"Standard LLM (Google) skipped or failed: {e}")

        try:

            embeddings = self.loader.load_embeddings(provider="google")

            logger.info(f"Loaded Standard Embeddings (Google): {type(embeddings)}")

        except Exception as e:

            logger.warning(f"Standard Embeddings (Google) skipped or failed: {e}")


class CustomUsage:

    def __init__(self):

        self.loader = ModelLoader()

    def run(self):

        logger.info("--- Running Custom Usage Example ---")

        self.loader.register_provider("dummy", DummyProvider())

        logger.info("Registered 'dummy' provider.")

        my_llm = self.loader.load_llm(provider="dummy", model_name="my-test-model")

        logger.info(f"Loaded Custom LLM: {my_llm}")

        my_emb = self.loader.load_embeddings(provider="dummy")

        logger.info(f"Loaded Custom Embeddings: {my_emb}")


def main():

    try:

        standard_demo = StandardUsage()

        standard_demo.run()

    except Exception as e:

        logger.error(f"Standard usage failed: {e}")

    try:

        custom_demo = CustomUsage()

        custom_demo.run()

    except Exception as e:

        logger.error(f"Custom usage failed: {e}")


if __name__ == "__main__":

    main()
