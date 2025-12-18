import os

import yaml
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq

from src.constants import (
    CONFIG_DIR,
    CONFIG_FILE,
    ERR_GOOGLE_EMB_EMPTY,
    ERR_GOOGLE_EMB_FAIL,
    ERR_GOOGLE_LLM_EMPTY,
    ERR_GOOGLE_LLM_FAIL,
    ERR_GROQ_LLM_EMPTY,
    ERR_GROQ_LLM_FAIL,
    ERR_MISSING_KEY,
    ERR_YAML_PARSE,
    KEY_EMBEDDING_MODEL,
    KEY_FAISS_DB,
    KEY_LLM,
    KEY_MODEL_NAME,
    KEY_PROVIDER,
    KEY_RETRIEVER,
    LLM_PROVIDER_GOOGLE,
    LLM_PROVIDER_GROQ,
    MSG_CONFIG_FILE_FOUND,
    MSG_CONFIG_FILE_NOT_FOUND,
    MSG_CONFIG_YAML_LOADED,
    MSG_ENV_LOADED,
    MSG_ENV_NOT_FOUND,
    MSG_GOOGLE_EMB_WORKING,
    MSG_GOOGLE_LLM_WORKING,
    MSG_GROQ_LLM_WORKING,
    MSG_KEY_PRESENT,
    MSG_SKIP_EMB_TEST,
    MSG_SKIP_GOOGLE_TEST,
    MSG_SKIP_GROQ_TEST,
    MSG_START_CONFIG_VAL,
    MSG_TEST_GOOGLE_EMB,
    MSG_TEST_GOOGLE_LLM,
    MSG_TEST_GROQ_LLM,
    MSG_VAL_COMPLETE,
    TEST_PROMPT,
    TEST_QUERY,
)


def validate_config():

    print(MSG_START_CONFIG_VAL)

    config_path = os.path.join(CONFIG_DIR, CONFIG_FILE)

    if not os.path.exists(config_path):

        print(f"{MSG_CONFIG_FILE_NOT_FOUND} {config_path}")

        return

    print(f"{MSG_CONFIG_FILE_FOUND} {config_path}")

    if not load_dotenv():

        print(MSG_ENV_NOT_FOUND)

    else:

        print(MSG_ENV_LOADED)

    with open(config_path, "r") as f:

        try:

            config = yaml.safe_load(f)

            print(MSG_CONFIG_YAML_LOADED)

        except yaml.YAMLError as e:

            print(f"{ERR_YAML_PARSE}: {e}")

            return

    required_keys = [KEY_FAISS_DB, KEY_EMBEDDING_MODEL, KEY_RETRIEVER, KEY_LLM]

    for key in required_keys:

        if key not in config:

            print(f"{ERR_MISSING_KEY}: {key}")

        else:

            print(MSG_KEY_PRESENT.format(key))

    try:

        emb_config = config.get(KEY_EMBEDDING_MODEL, {})

        if emb_config.get(KEY_PROVIDER) == LLM_PROVIDER_GOOGLE:

            model = emb_config.get(KEY_MODEL_NAME)

            print(MSG_TEST_GOOGLE_EMB.format(model))

            embeddings = GoogleGenerativeAIEmbeddings(model=model)

            res = embeddings.embed_query(TEST_QUERY)

            if res and len(res) > 0:

                print(MSG_GOOGLE_EMB_WORKING)

            else:

                print(ERR_GOOGLE_EMB_EMPTY)

        else:

            print(MSG_SKIP_EMB_TEST.format(emb_config.get(KEY_PROVIDER)))

    except Exception as e:

        print(f"{ERR_GOOGLE_EMB_FAIL}: {e}")

    try:

        llm_config = config.get(KEY_LLM, {}).get(LLM_PROVIDER_GROQ, {})

        if llm_config.get(KEY_PROVIDER) == LLM_PROVIDER_GROQ:

            model = llm_config.get(KEY_MODEL_NAME)

            print(MSG_TEST_GROQ_LLM.format(model))

            chat = ChatGroq(model=model, temperature=0)

            res = chat.invoke(TEST_PROMPT)

            if res:

                print(MSG_GROQ_LLM_WORKING.format(res.content))

            else:

                print(ERR_GROQ_LLM_EMPTY)

        else:

            print(MSG_SKIP_GROQ_TEST)

    except Exception as e:

        print(f"{ERR_GROQ_LLM_FAIL}: {e}")

    try:

        llm_config = config.get(KEY_LLM, {}).get(LLM_PROVIDER_GOOGLE, {})

        if llm_config.get(KEY_PROVIDER) == LLM_PROVIDER_GOOGLE:

            model = llm_config.get(KEY_MODEL_NAME)

            print(MSG_TEST_GOOGLE_LLM.format(model))

            chat = ChatGoogleGenerativeAI(
                model=model, temperature=0, max_output_tokens=1024
            )

            res = chat.invoke(TEST_PROMPT)

            if res:

                print(MSG_GOOGLE_LLM_WORKING.format(res.content))

            else:

                print(ERR_GOOGLE_LLM_EMPTY)

        else:

            print(MSG_SKIP_GOOGLE_TEST)

    except Exception as e:

        print(f"{ERR_GOOGLE_LLM_FAIL}: {e}")

    print(MSG_VAL_COMPLETE)


if __name__ == "__main__":

    validate_config()
