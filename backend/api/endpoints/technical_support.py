"""
Program to handle API endpoint for technical support queries
"""

from fastapi import APIRouter, HTTPException, Depends
from core.llm import get_qa_chain, get_retriever
from services.conversation import create_session, add_to_conversation, get_conversation
from api.dependencies import verify_api_key
from schemas.chat_schema import TechnicalQuery, TechnicalResponse
from services.prompt_builder import PromptBuilder  # Import the PromptBuilder class

router = APIRouter(
    prefix="/technical-support",
    tags=["Technical Support"],
    dependencies=[Depends(verify_api_key)]
)

# load the prompt builder
prompt_builder = PromptBuilder()

@router.post("/", response_model=TechnicalResponse)
def technical_support(query: TechnicalQuery):
    """
    Augment user query for RAG model over LLM and return response
    return: LLM response to augmented query
    """
    try:
        # session management
        session_id = query.session_id or create_session()
        add_to_conversation(session_id, f"User: {query.question}")

        # augment user prompt for better response
        prompt = prompt_builder.build_prompt(
            category="technical_support",
            context=query.question
        )

        # get qa chain using retriever for vectorstore
        retriever = get_retriever()
        qa = get_qa_chain(retriever=retriever)

        # get llm response over augmented query using RAG model from llm
        result = qa({"query": prompt})

        answer = result['result']
        source_documents = result.get('source_documents', [])

        # conversation update
        add_to_conversation(session_id, f"Assistant: {answer}")
        conversation_history = get_conversation(session_id)

        # get reference documents
        references = [doc.page_content for doc in source_documents]
        

        return TechnicalResponse(
            session_id=session_id,
            answer=answer,
            references=references,
            conversation=conversation_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
