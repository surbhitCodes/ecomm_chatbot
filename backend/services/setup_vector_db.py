"""
Program to setup vector stores using chroma, using openai/hf embeddings
"""

import chromadb
from chromadb.utils import embedding_functions
from langchain_huggingface import HuggingFaceEmbeddings
from data.materials_data import materials_data
from core.config import settings
from langchain_openai import OpenAIEmbeddings
import logging

# define the chroma-compatible HF wrapper
class HFWrapper:
    def __init__(self, model_name: str):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    def __call__(self, input: list[str]) -> list[list[float]]:
        """
        Chroma expects the embedding function to accept a list of strings and return a list of embedding vectors
        """
        return self.embeddings.embed_documents(input)

# initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    embedding_function = HFWrapper(model_name="sentence-transformers/all-MiniLM-L6-v2")
    existing_collections = [collection.name for collection in client.list_collections()]
    
    # delete collection if it exists to avoid dimensionality conflicts
    if name in existing_collections:
        client.delete_collection(name)
        logger.info(f"deleted existing collection: {name}")

    return client.create_collection(name=name, embedding_function=embedding_function)

def populate_vector_db():
    """
    Load materials_data into vector store by chroma
    """
    logger.info("starting vector store population...")
    try:
        # initialize embedding function via the wrapper
        embedding_function = HFWrapper(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # embedding_function = HFWrapper(model_name="sentence-transformers/mpnet-base-v2")
        # embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=settings.OPENAI_KEY)
        
        client = get_chroma_client()
        vectorstore = create_collection(client, name="materials")
        logger.info("created collection: materials")

        documents = []
        metadatas = []
        ids = []

        # process product catalog
        for product in materials_data.get("product_catalog", []):
            specs = '\n'.join([f"{k}: {v}" for k, v in product.get('specifications', {}).items()])
            tech_details = '\n'.join([f"{k}: {v}" for k, v in product.get('technical_details', {}).items()])
            price_history = '\n'.join([f"{entry['date']}: ${entry['price']}" for entry in product.get('price_history', [])])
            current_stock = '\n'.join([f"{k}: {v}" for k, v in product.get('current_stock', {}).items()])
            text = f"""product: {product.get('name')}
specifications:
{specs}
applications: {', '.join(product.get('applications', []))}
technical details:
{tech_details}
price history:
{price_history}
current stock:
{current_stock}
"""
            documents.append(text)
            metadatas.append({
                "id": product.get("id"),
                "title": product.get("name"),
                "category": product.get("category"),
                "manufacturer": product.get("manufacturer"),
            })
            ids.append(f"product-{product.get('id')}")
            logger.info(f"processed product: {product.get('id')}")

        # process technical documents
        for doc in materials_data.get("technical_documents", []):
            text = f"technical document: {doc.get('title')}\ncontent: {doc.get('content')}"
            documents.append(text)
            metadatas.append({
                "id": doc.get("id"),
                "title": doc.get("title"),
                "product_id": doc.get("product_id"),
            })
            ids.append(f"technical_document-{doc.get('id')}")
            logger.info(f"processed technical document: {doc.get('id')}")

        # process building codes
        for code in materials_data.get("building_codes", []):
            summary = code.get('summary', '').strip()
            text = f"building code: {code.get('title')}\njurisdiction: {code.get('jurisdiction')}\napplicable products: {', '.join(code.get('applicable_products', []))}\nsummary:\n{summary}"
            documents.append(text)
            metadatas.append({
                "id": code.get("code_id"),
                "title": code.get("title"),
                "jurisdiction": code.get("jurisdiction"),
                "applicable_products": ', '.join(code.get("applicable_products", [])),  # convert list to string
            })
            ids.append(f"building_code-{code.get('code_id')}")
            logger.info(f"processed building code: {code.get('code_id')}")

        # process installation guides
        for guide in materials_data.get("installation_guides", []):
            content = guide.get('content', '').strip()
            text = f"installation guide: {guide.get('title')}\nproduct_id: {guide.get('product_id')}\ncontent:\n{content}"
            documents.append(text)
            metadatas.append({
                "id": guide.get("guide_id"),
                "title": guide.get("title"),
                "product_id": guide.get("product_id"),
            })
            ids.append(f"installation_guide-{guide.get('guide_id')}")
            logger.info(f"processed installation guide: {guide.get('guide_id')}")

        # process safety documents
        for safety_doc in materials_data.get("safety_documents", []):
            content = safety_doc.get('content', '').strip()
            text = f"safety document: {safety_doc.get('title')}\nproduct_id: {safety_doc.get('product_id')}\ncontent:\n{content}"
            documents.append(text)
            metadatas.append({
                "id": safety_doc.get("doc_id"),
                "title": safety_doc.get("title"),
                "product_id": safety_doc.get("product_id"),
            })
            ids.append(f"safety_document-{safety_doc.get('doc_id')}")
            logger.info(f"processed safety document: {safety_doc.get('doc_id')}")

        # process material alternatives
        for alternative in materials_data.get("material_alternatives", []):
            primary_id = alternative.get("primary_product_id")
            for alt in alternative.get("alternatives", []):
                comparison = '\n'.join([f"{k}: {v}" for k, v in alt.get('comparison', {}).items()])
                text = f"material alternative for {primary_id}: {alt.get('name')}\ncomparison:\n{comparison}"
                documents.append(text)
                metadatas.append({
                    "id": alt.get("id"),
                    "name": alt.get("name"),
                    "primary_product_id": primary_id,
                })
                ids.append(f"material_alternative-{alt.get('id')}")
                logger.info(f"processed material alternative: {alt.get('id')}")

        # process typical queries with unique IDs
        for idx, query_entry in enumerate(materials_data.get("typical_queries", []), start=1):
            query = query_entry.get("query")
            context = query_entry.get("context", "")
            relevant_products = ', '.join(query_entry.get("relevant_products", []))  # convert list to string
            relevant_codes = ', '.join(query_entry.get("relevant_codes", []))  # convert list to string
            relevant_documents = ', '.join(query_entry.get("relevant_documents", [])) if "relevant_documents" in query_entry else ""
            key_points = '\n'.join([f"- {point}" for point in query_entry.get("key_points", [])])
            considerations = '\n'.join([f"- {cons}" for cons in query_entry.get("considerations", [])])
            
            text = f"typical query: {query}\ncontext: {context}\nrelevant products: {relevant_products}\nrelevant codes: {relevant_codes}"
            if relevant_documents:
                text += f"\nrelevant documents: {relevant_documents}"
            text += f"\nkey points:\n{key_points}"
            if considerations:
                text += f"\nconsiderations:\n{considerations}"
            
            documents.append(text)
            metadatas.append({
                "query": query,
                "context": context,
                "relevant_products": relevant_products,  # ensure primitive type
                "relevant_codes": relevant_codes,  # ensure primitive type
                "relevant_documents": relevant_documents,  # ensure primitive type
            })
            query_id = f"typical_query-{idx}"
            ids.append(query_id)
            logger.info(f"processed typical query: {query_id}")

        # verify all documents are strings and log their types
        for i, doc in enumerate(documents):
            if not isinstance(doc, str):
                logger.error(f"document at index {i} is not a string: {doc}")
                raise ValueError("all documents must be strings")
            else:
                logger.debug(f"document {i} is a string of length {len(doc)}.")

        # verify metadatas are dictionaries and log their keys
        for i, meta in enumerate(metadatas):
            if not isinstance(meta, dict):
                logger.error(f"metadata at index {i} is not a dict: {meta}")
                raise ValueError("all metadatas must be dictionaries")
            else:
                for key, value in meta.items():
                    if not isinstance(value, (str, int, float, bool, type(None))):
                        logger.error(f"invalid metadata value for key '{key}': {value}")
                        raise ValueError(f"metadata values must be primitives, got {value} of type {type(value)}")
                logger.debug(f"metadata {i} is a dict with keys: {list(meta.keys())}.")

        # verify ids are strings and log their values
        for i, id_ in enumerate(ids):
            if not isinstance(id_, str):
                logger.error(f"id at index {i} is not a string: {id_}")
                raise ValueError("all ids must be strings")
            else:
                logger.debug(f"id {i} is a string: {id_}.")

        # load vector store
        vectorstore.add(documents=documents, metadatas=metadatas, ids=ids)
        logger.info(f"added {len(documents)} documents to the vector store.")

    except Exception as e:
        logger.exception("error populating vector store")
