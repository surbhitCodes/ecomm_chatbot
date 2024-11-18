"""
Program to handle API endpoint for project planning queries
"""

import logging
import time
from fastapi import APIRouter, HTTPException, Depends
from core.llm import get_qa_chain, get_retriever
from services.conversation import create_session, add_to_conversation, get_conversation
from api.dependencies import verify_api_key
from schemas.chat_schema import PlanningQuery, PlanningResponse
from services.prompt_builder import PromptBuilder  # Import PromptBuilder

router = APIRouter(
    prefix="/project-planning",
    tags=["Project Planning"],
    dependencies=[Depends(verify_api_key)]
)

logger = logging.getLogger(__name__)

# load the prompt builder
prompt_builder = PromptBuilder()

@router.post("/", response_model=PlanningResponse)
def project_planning(query: PlanningQuery):
    try:
        start = time.time()
        
        # session management
        session_id = query.session_id or create_session()
        add_to_conversation(session_id, f"User: {query.project_description}")

        # augment query with prompt
        prompt = prompt_builder.build_prompt(
            category="project_planning",
            context=query.project_description
        )

        # get vector store
        retriever = get_retriever()
        qa = get_qa_chain(retriever=retriever)

        # fetch answers for augmented prompt
        result = qa({"query": prompt})

        answer = result['result']
        source_documents = result.get('source_documents', [])

        # update to conversation
        add_to_conversation(session_id, f"Assistant: {answer}")
        conversation_history = get_conversation(session_id)

        # reference extraction
        references = [doc.page_content for doc in source_documents]  
        
        logger.info(f'Time taken: {(time.time()-start):.2f} seconds')      

        return PlanningResponse(
            session_id=session_id,
            plan=answer,
            references=references,
            conversation=conversation_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
