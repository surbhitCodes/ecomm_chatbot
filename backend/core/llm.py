"""
Program for loading responses from OpenAI using RAG via vectorstore (chroma)
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from core.config import settings
import logging
import chromadb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_qa_chain(retriever=None):
    """
    Getter for qa chain, via chroma based query retriever 
    """
    try:
        if retriever is None:
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
    Getter for query retriever from vectorstore using OpenAI embeddings
    """
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)
    persist_directory = "./chroma_db"

    # initialize vectorstore
    vectorstore = Chroma(
        client=chromadb.PersistentClient(path=persist_directory),
        embedding_function=embeddings,
        collection_name="materials"
    )
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
