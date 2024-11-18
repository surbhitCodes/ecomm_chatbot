"""
Core program for infromation retreival using the RAG model from OpenAI LLM, using langchain
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from core.config import settings
import logging

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_qa_chain(retriever=None):
    """
    Build QA chain for information retrieval over RAG model
    """
    try:
        if retriever is None: # create default retriever
            retriever = get_retriever()
            
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=settings.OPENAI_KEY, temperature=0),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        logger.info("QA chain successfully initialized")
        return qa
    except Exception as e:
        logger.error(f"Failed to initialize QA chain: {e}")
        raise


def get_retriever():
    """
    Using the embedding create a vectorstore retreiver, 
    using k=5 top basis similarity
    """
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") # giving erroneous results
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
