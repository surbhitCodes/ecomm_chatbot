"""
Program to handle API endpoint for general queries
"""


import time
import logging
from fastapi import APIRouter, HTTPException, Depends
from core.llm import get_qa_chain, get_retriever
from services.conversation import create_session, add_to_conversation, get_conversation
from api.dependencies import verify_api_key
from schemas.chat_schema import QueryRequest, QueryResponse
from services.prompt_builder import PromptBuilder  # Import PromptBuilder

router = APIRouter(
    prefix="/queries",
    tags=["Intelligent Material Queries"],
    dependencies=[Depends(verify_api_key)]
)

logger = logging.getLogger(__name__)

# load prompt builder
prompt_builder = PromptBuilder() 

@router.post("/", response_model=QueryResponse)
def material_query(request: QueryRequest):
    """
    Augment user query and get LLM response
    return: Query Response by LLM using RAG model
    """
    try:
        start=time.time()
        
        # session management
        session_id = request.session_id or create_session()
        add_to_conversation(session_id, f"User: {request.query}")

        # augment the prompt for improved response
        prompt = prompt_builder.build_prompt(
            category="queries",
            context=request.query
        )

        # get retreiver qa chain
        retriever = get_retriever()
        qa = get_qa_chain(retriever=retriever)

        # get response from llm using the qa chain and llm
        result = qa({"query": prompt})

        answer = result['result']
        source_documents = result.get('source_documents', [])

        # conversation update
        add_to_conversation(session_id, f"Assistant: {answer}")
        conversation_history = get_conversation(session_id)
        
        # source document extraction
        sources = [doc.page_content for doc in source_documents]
        
        
        logger.info(f'Time taken: {(time.time()-start):.2f} seconds')
        

        return QueryResponse(
            session_id=session_id,
            answer=answer,
            sources=sources,
            conversation=conversation_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
