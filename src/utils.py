import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from AIFoundationKit.base.utils import generate_session_id
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


def _create_retriever(
    documents: List[Document],
    embedding_model: Any,
    faiss_index_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 300,
) -> BaseRetriever:
    """
    Create a retriever from documents.

    Args:
        documents (List[Document]): List of documents to process.
        embedding_model (Any): The embedding model to use.
        faiss_index_path (str): Path to save the FAISS index.
        chunk_size (int): Chunk size for splitting.
        chunk_overlap (int): Chunk overlap for splitting.

    Returns:
        BaseRetriever: The configured retriever.
    """
    # Flatten list of lists if necessary
    if documents and isinstance(documents[0], list):
        documents = [item for sublist in documents for item in sublist]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(
        documents=chunks, embedding=embedding_model
    )

    vectorstore.save_local(faiss_index_path)

    retriever = load_retriever_from_vectorstore(
        vectorstore, search_type="similarity", k=4
    )
    return retriever


def load_retriever_from_vectorstore(
    vectorstore: VectorStore,
    search_type: str = "similarity",
    k: int = 4,
    score_threshold: Optional[float] = None,
    filter: Optional[Dict[str, Any]] = None,
) -> BaseRetriever:
    """
    Load a retriever from a vectorstore with configurable search parameters.

    Args:
        vectorstore (VectorStore): The vectorstore to create a retriever from.
        search_type (str): The type of search to perform. Defaults to "similarity".
                           Options: "similarity", "mmr",
                           "similarity_score_threshold".
        k (int): The number of documents to return. Defaults to 4.
        score_threshold (Optional[float]): Minimum relevance threshold for
                                           similarity_score_threshold.
        filter (Optional[Dict[str, Any]]): Filter by document metadata.

    Returns:
        BaseRetriever: The configured retriever.
    """
    search_kwargs = {"k": k}

    if score_threshold is not None:
        search_kwargs["score_threshold"] = score_threshold
        if search_type == "similarity":
            search_type = "similarity_score_threshold"

    if filter is not None:
        search_kwargs["filter"] = filter

    retriever = vectorstore.as_retriever(
        search_type=search_type, search_kwargs=search_kwargs
    )

    return retriever


def ensure_directory_exists(
    directory: Union[str, Path], parents: bool = True, exist_ok: bool = True
) -> Path:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory (Union[str, Path]): The path to the directory.
        parents (bool): If True, any missing parents of this path are created as needed. Defaults to True.
        exist_ok (bool): If True, FileExistsError exceptions will be ignored. Defaults to True.

    Returns:
        Path: The Path object for the directory.
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=parents, exist_ok=exist_ok)
    return dir_path


def process_and_load_files(
    file_paths: List[str],
    data_dir: str,
    loader_cls: Type[BaseLoader] = PyPDFLoader,
    file_extension: str = ".pdf",
) -> List[List[Document]]:
    """
    Process files by saving them with a unique name and loading them.

    Args:
        file_paths (List[str]): List of paths to input files.
        data_dir (str): Directory to save the processed files.
        loader_cls (Type[BaseLoader]): Loader class to use for loading documents.
                                       Defaults to PyPDFLoader.
        file_extension (str): Extension to append to the unique filename.
                              Defaults to ".pdf".

    Returns:
        List[List[Document]]: A list of lists of loaded documents.
    """
    files = []
    for file_path in file_paths:
        unique_file_name = generate_session_id() + file_extension
        new_file_path = os.path.join(data_dir, unique_file_name)
        with open(new_file_path, "wb") as f:
            f.write(open(file_path, "rb").read())

        loader = loader_cls(new_file_path)
        documents = loader.load()
        files.append(documents)

    return files
