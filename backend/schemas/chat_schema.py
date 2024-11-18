"""
Defining Response and Request Schema for each API endpoint
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    """
    Request schema for query endpoint
    """

    query: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    """
    Response schema for query endpoint
    """
    session_id: str
    answer: str
    sources: List[str]


class ProjectDescription(BaseModel):
    """
    Schema for item description
    """
    description: str


class MaterialEstimate(BaseModel):
    """
    Schema for item material estimate
    """
    materials: List[str]
    total_cost: float
    details: str


class TechnicalQuery(BaseModel):
    """
    Technical support request schema
    """
    question: str
    session_id: Optional[str] = None


class TechnicalResponse(BaseModel):
    """
    Technical support response schema
    """
    session_id: str = Field(..., description="Session ID of the conversation")
    answer: str = Field(..., description="Answer to the user's question")
    references: List[str] = Field(..., description="List of references used in the answer")
    conversation: List[str] = Field(..., description="Conversation history up to this point")


class PlanningQuery(BaseModel):
    """
    Planning query schema
    """
    project_description: str
    session_id: Optional[str] = None


class PlanningResponse(BaseModel):
    """
    Project planning response schema
    """
    session_id: str
    plan: str
    references: List[str]
