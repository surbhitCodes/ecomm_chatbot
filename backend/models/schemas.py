from pydantic import BaseModel
from typing import List, Optional

# Intelligent Material Queries
class QueryRequest(BaseModel):
    session_id: Optional[str] = None
    query: str

class QueryResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[str]

# Project Planning Assistant
class ProjectDescription(BaseModel):
    description: str

class MaterialEstimate(BaseModel):
    materials: List[str]
    total_cost: float
    details: str

# Technical Support
class TechnicalQuery(BaseModel):
    session_id: Optional[str] = None
    question: str

class TechnicalResponse(BaseModel):
    session_id: str
    answer: str
    references: List[str]
