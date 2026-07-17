"""
RAG (Retrieval-Augmented Generation)

This module stores OCR text into a vector database
and retrieves relevant information using semantic search.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


def create_vector_database(text, persist_directory="vector_db"):
    """
    Convert OCR text into embeddings
    and store them inside ChromaDB.
    """

    chunks = text_splitter.split_text(text)

    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    vector_db.persist()

    return vector_db


def load_vector_database(persist_directory="vector_db"):
    """
    Load an existing vector database.
    """

    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )


def search_document(query, persist_directory="vector_db", k=3):
    """
    Search the document semantically.

    Parameters
    ----------
    query : str
        User question.

    Returns
    -------
    list
        Most relevant document chunks.
    """

    database = load_vector_database(persist_directory)

    results = database.similarity_search(
        query=query,
        k=k
    )

    return results