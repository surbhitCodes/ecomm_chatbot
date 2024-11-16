from fastapi import APIRouter, HTTPException, Depends
from backend.api.dependencies import verify_api_key
from backend.models.schemas import ProjectDescription, MaterialEstimate
from backend.core.llm import get_qa_chain

router = APIRouter(
    prefix="/project-planning",
    tags=["Project Planning Assistant"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/estimate", response_model=MaterialEstimate)
def estimate_materials(project: ProjectDescription):
    try:
        # Implement the logic using LangChain's RetrievalQA or custom chains
        qa = get_qa_chain()
        query = f"Estimate the materials and cost for the following project: {project.description}"
        result = qa.run(query)
        
        # Process result to fit MaterialEstimate schema
        # This is a placeholder and should be replaced with actual parsing logic
        return MaterialEstimate(
            materials=["2x4 Lumber", "Concrete"],
            total_cost=1500.0,
            details=result['result']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
