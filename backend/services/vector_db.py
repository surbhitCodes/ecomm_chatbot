# backend/services/vector_db.py

import chromadb
from chromadb.config import Settings
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from backend.data.materials_data import materials_data
from backend.core.config import settings

def get_chroma_client():
    client = chromadb.Client(Settings(
        chroma_db_impl="sqlite",
        persist_directory="./chroma_db"
    ))
    return client

def create_collection(client, name="materials"):
    if name not in client.list_collections():
        return client.create_collection(name=name)
    return client.get_collection(name=name)

def add_documents(collection, documents, embeddings):
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(documents))]
    )

def populate_vector_db():
    client = get_chroma_client()
    collection = create_collection(client)

    documents = []
    for product in materials_data['product_catalog']:
        text = f"{product['name']}: {product['specifications']}"
        documents.append(text)
    
    embeddings = get_embeddings().embed_documents(documents)
    add_documents(collection, documents, embeddings)
    client.persist()

def get_embeddings():
    
    # return OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
