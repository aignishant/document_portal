import os
import yaml
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

def validate_config():
    print("--- Starting Configuration Validation ---")
    
    # 1. Check Config File Existence
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ Config file not found at {config_path}")
        return
    print(f"✅ Config file found at {config_path}")

    # 2. Check .env content (blindly, just checking if we can load it)
    if not load_dotenv():
        print("⚠️ .env file not found or empty (this might be expected if env vars are set otherwise)")
    else:
        print("✅ Client environment variables loaded")

    # 3. Load Config
    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
            print("✅ Config YAML loaded successfully")
        except yaml.YAMLError as e:
            print(f"❌ Failed to parse YAML: {e}")
            return

    # 4. Validate Structure (Basic checks)
    required_keys = ["faiss_db", "embedding_model", "retriever", "llm"]
    for key in required_keys:
        if key not in config:
            print(f"❌ Missing required key in config: {key}")
        else:
            print(f"✅ Key '{key}' present")

    # 5. Validate Embedding Model (Google)
    try:
        emb_config = config.get("embedding_model", {})
        if emb_config.get("provider") == "google":
            model = emb_config.get("model_name")
            print(f"Testing Google Embeddings ({model})...")
            
            embeddings = GoogleGenerativeAIEmbeddings(model=model)
            # Try to embed a simple string
            res = embeddings.embed_query("dataset")
            if res and len(res) > 0:
                 print("✅ Google Embeddings working")
            else:
                 print("❌ Google Embeddings returned empty result")
        else:
             print(f"ℹ️ Skipping Embedding test (Provider: {emb_config.get('provider')})")
    except Exception as e:
        print(f"❌ Google Embeddings Failed: {e}")

    # 6. Validate LLM (Groq)
    try:
        llm_config = config.get("llm", {}).get("groq", {})
        if llm_config.get("provider") == "groq":
            model = llm_config.get("model_name")
            print(f"Testing Groq LLM ({model})...")
            
            chat = ChatGroq(model=model, temperature=0)
            res = chat.invoke("Say 'Hello'")
            if res:
                print(f"✅ Groq LLM working. Response: {res.content}")
            else:
                print("❌ Groq LLM returned empty response")
        else:
             print("ℹ️ Skipping Groq LLM test")
    except Exception as e:
        print(f"❌ Groq LLM Failed: {e}")

    # 7. Validate LLM (Google)
    try:
        llm_config = config.get("llm", {}).get("google", {})
        if llm_config.get("provider") == "google":
            model = llm_config.get("model_name")
            print(f"Testing Google LLM ({model})...")
            
            chat = ChatGoogleGenerativeAI(model=model, temperature=0, max_output_tokens=1024)
            res = chat.invoke("Say 'Hello'")
            if res:
                 print(f"✅ Google LLM working. Response: {res.content}")
            else:
                 print("❌ Google LLM returned empty response")
        else:
             print("ℹ️ Skipping Google LLM test")
    except Exception as e:
        print(f"❌ Google LLM Failed: {e}")

    print("--- Validation Complete ---")

if __name__ == "__main__":
    validate_config()
