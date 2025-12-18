# Document Portal

Document Portal is a comprehensive Generative AI application designed to facilitate advanced document interaction and analysis. It allows users to chat with single or multiple documents, compare documents, and perform in-depth document analysis using state-of-the-art LLMs.

## Features

- **Single Document Chat**: Upload a document (PDF, Text) and ask questions specific to its content.
- **Multi-Document Chat**: Creating a knowledge base from multiple documents and query across them.
- **Document Comparison**: Compare two documents to identify differences, similarities, and key insights.
- **Document Analysis**: Perform detailed analysis on documents to extract structured information.
- **Screenshot to Document**: A utility tool to capture screenshots and compile them into a document (Docx).
- **Extensible Architecture**: Built with a modular design (Standardized `ai-common` library) supporting various LLM providers (Google Gemini, Groq, DeepSeek).

## Prerequisites

- **OS**: Linux (tested on Ubuntu)
- **Python**: 3.10 or higher
- **Conda** (recommended for environment management)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd document_portal
```

### 2. Environment Setup

It is recommended to use Conda to create an isolated environment.

```bash
# Create a new conda environment
conda create -p myvenv python=3.10 -y

# Activate the environment
conda activate ./myvenv
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory. You can use the provided template or set the variables directly.

```bash
# Example .env content
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
DATA_STORAGE_PATH=/path/to/your/data/storage
```

**Key Variables:**
- `DATA_STORAGE_PATH`: Directory where uploaded files and vector stores will be saved.
- `GOOGLE_API_KEY`: API key for Google Gemini models.
- `GROQ_API_KEY`: API key for Groq models.

### Application Config

The application uses `config/config.yaml` for model and provider configurations. Ensure this file exists and is correctly configured for your preferred default models.

## Usage

### Running the Web Application

The Document Portal features a Streamlit-based user interface.

```bash
streamlit run app.py
```

Navigate to the provided URL (usually `http://localhost:8501`) in your browser.

### Using the Screenshot Tool

A utility script `screenshot_to_doc.py` is available to capture screen regions and save them to a Word document.

```bash
# Run the screenshot tool
python screenshot_to_doc.py
```

### Testing

To verify the document handler functionality, you can run the provided test script:

```bash
./run_test_doc_handler.sh
```

## detailed Project Structure

- `src/`: Core application source code.
    - `src/single_doc_chat/`: Logic for single document interaction.
    - `src/multi_doc_chat/`: Logic for multi-document RAG.
    - `src/document_comparison/`: Logic for comparing documents.
    - `src/document_analysier/`: Logic for document analysis.
    - `src/constants.py`: Application-wide constants.
- `app.py`: Main Streamlit application entry point.
- `config/`: Configuration files.
- `tests/`: Unit and integration tests.