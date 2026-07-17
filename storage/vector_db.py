"""
Vector Database Module

Stores and retrieves OCR text embeddings
using ChromaDB.
"""

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


class VectorDatabase:
    """
    Handles vector database operations.
    """

    def __init__(self, persist_directory="vector_db"):

        self.persist_directory = persist_directory

        self.embedding_model = embedding_model


    def create_database(self, text):

        chunks = text_splitter.split_text(text)

        database = Chroma.from_texts(
            texts=chunks,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory
        )

        database.persist()

        return database


    def load_database(self):

        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )


    def similarity_search(self, query, k=3):

        database = self.load_database()

        results = database.similarity_search(
            query=query,
            k=k
        )

        return results


    def add_text(self, text):

        database = self.load_database()

        chunks = text_splitter.split_text(text)

        database.add_texts(chunks)

        database.persist()