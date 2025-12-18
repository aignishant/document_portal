CONFIG_DIR = "config"

CONFIG_FILE = "config.yaml"

COMPONENT_DOCUMENT_ANALYSIS = "DocumentAnalysis"

LLM_PROVIDER_GOOGLE = "google"

MSG_DOC_ANALYSIS_INIT = "DocumentAnalysis initialized"

ERR_DOC_ANALYSIS_INIT = (
    "Failed to initialize DocumentAnalysis" "Failed to initialize DocumentAnalysis"
)

ENV_DATA_STORAGE_PATH = "DATA_STORAGE_PATH"

DIR_DATA = "data"

DIR_DOCUMENT_ANALYSIS = "document_analysis"

MSG_DOC_HANDLER_INIT = "DocumentHandler initialized with session_id"

ERR_DOC_HANDLER_INIT = "Failed to initialize DocumentHandler"

ERR_INVALID_FILE_OBJ = (
    "Provided file object must have 'path' and 'getbuffer' attributes"
)

ERR_PDF_NOT_FOUND = "PDF file not found at path"

MSG_PDF_SAVED = "PDF saved to"

ERR_PDF_SAVE = "Failed to save PDF"

ERR_PDF_READ = "Failed to read PDF"

FITZ_TEXT_MODE = "text"

KEY_FAISS_DB = "faiss_db"

KEY_EMBEDDING_MODEL = "embedding_model"

KEY_RETRIEVER = "retriever"

KEY_LLM = "llm"

KEY_PROVIDER = "provider"

KEY_MODEL_NAME = "model_name"

LLM_PROVIDER_GROQ = "groq"

MSG_START_CONFIG_VAL = "--- Starting Configuration Validation ---"

MSG_CONFIG_FILE_NOT_FOUND = "❌ Config file not found at"

MSG_CONFIG_FILE_FOUND = "✅ Config file found at"

MSG_ENV_NOT_FOUND = (
    "⚠️ .env file not found or empty (this might be expected if env vars are "
    "set otherwise)"
)

MSG_ENV_LOADED = "✅ Client environment variables loaded"

MSG_CONFIG_YAML_LOADED = "✅ Config YAML loaded successfully"

ERR_YAML_PARSE = "❌ Failed to parse YAML"

ERR_MISSING_KEY = "❌ Missing required key in config"

MSG_KEY_PRESENT = "✅ Key '{}' present"

MSG_TEST_GOOGLE_EMB = "Testing Google Embeddings ({})..."

MSG_GOOGLE_EMB_WORKING = "✅ Google Embeddings working"

ERR_GOOGLE_EMB_EMPTY = "❌ Google Embeddings returned empty result"

MSG_SKIP_EMB_TEST = "ℹ️ Skipping Embedding test (Provider: {})"

ERR_GOOGLE_EMB_FAIL = "❌ Google Embeddings Failed"

MSG_TEST_GROQ_LLM = "Testing Groq LLM ({})..."

MSG_GROQ_LLM_WORKING = "✅ Groq LLM working. Response: {}"

ERR_GROQ_LLM_EMPTY = "❌ Groq LLM returned empty response"

MSG_SKIP_GROQ_TEST = "ℹ️ Skipping Groq LLM test"

ERR_GROQ_LLM_FAIL = "❌ Groq LLM Failed"

MSG_TEST_GOOGLE_LLM = "Testing Google LLM ({})..."

MSG_GOOGLE_LLM_WORKING = "✅ Google LLM working. Response: {}"

ERR_GOOGLE_LLM_EMPTY = "❌ Google LLM returned empty response"

MSG_SKIP_GOOGLE_TEST = "ℹ️ Skipping Google LLM test"

ERR_GOOGLE_LLM_FAIL = "❌ Google LLM Failed"

MSG_VAL_COMPLETE = "--- Validation Complete ---"

TEST_QUERY = "dataset"

TEST_PROMPT = "Say 'Hello'"
