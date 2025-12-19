from typing import Optional, Dict, Any
from langchain_core.vectorstores import VectorStore
from langchain_core.retrievers import BaseRetriever


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
        search_type=search_type,
        search_kwargs=search_kwargs
    )

    return retriever
