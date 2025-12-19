from AIFoundationKit.rag.model_loader import ModelLoader
try:
    loader = ModelLoader()
    embedding_model = loader.load_embeddings()
    print(f"Result type: {type(embedding_model)}")
    print(f"Result: {embedding_model}")

    if embedding_model is not None:
        print("SUCCESS: load_embeddings returned an object.")
    else:
        print("FAILURE: load_embeddings returned None.")

except Exception as e:
    print(f"ERROR: {e}")
