# backend/api/endpoints/__init__.py

from .queries import router as queries_router
from .project_planning import router as project_planning_router
from .technical_support import router as technical_support_router

__all__ = ["queries_router", "project_planning_router", "technical_support_router"]
