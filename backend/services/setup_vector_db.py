"""
Program to setup up vector stores using Chroma, using OpenAI/HF embeddings
"""

import chromadb
from chromadb.utils import embedding_functions
from data.materials_data import materials_data
from core.config import settings
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


def get_chroma_client():
    """
    Initialize chroma db (vectorstore)
    """
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )
    return client


def create_collection(client, name="materials"):
    """
    Create or retrieve chroma collection with the embedding function
    """
    
    # HF miniLM works fastest, more conversational and free
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") 
    # embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    # embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=settings.OPENAI_KEY)
    if name not in [collection.name for collection in client.list_collections()]:
        return client.create_collection(name=name, embedding_function=embedding_function)
    return client.get_collection(name=name, embedding_function=embedding_function)


logger = logging.getLogger(__name__)


def populate_vector_db():
    """
    Load materials_data into vector store by Chroma
    """
    logger.info("Starting vector store population...")
    try:
        
        # HF miniLM works fastest, more conversational and free
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") 
        #embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)
        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )

        documents = []
        metadatas = []
        ids = []

        # load product catalog
        for product in materials_data["product_catalog"]:
            text = f"Product: {product['name']}\nSpecifications: {product['specifications']}\nApplications: {', '.join(product['applications'])}\nTechnical Details: {product['technical_details']}"
            documents.append(text)
            metadatas.append({"id": product["id"], "title": product["name"]})
            ids.append(product["id"])
            logger.info(f"Processed product: {product['id']}")

        # load technical documents
        for doc in materials_data["technical_documents"]:
            text = f"Technical Document: {doc['title']}\nContent: {doc['content']}"
            documents.append(text)
            metadatas.append({"id": doc["id"], "title": doc["title"]})
            ids.append(doc["id"])
            logger.info(f"Processed technical document: {doc['id']}")

        # load vector store
        vectorstore.add_texts(texts=documents, metadatas=metadatas, ids=ids)
        logger.info(f"Added {len(documents)} documents to the vector store.")

    except Exception as e:
        logger.error(f"Error populating vector store: {e}")
