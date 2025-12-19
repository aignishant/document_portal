from AIFoundationKit.rag.model_loader import ModelLoader
try:
    loader = ModelLoader()
    print("Attempting to load Groq embeddings...")
    embedding_model = loader.load_embeddings(provider="groq")
    print(f"Result type: {type(embedding_model)}")
    print(f"Result: {embedding_model}")

except Exception as e:
    print(f"ERROR: {e}")
