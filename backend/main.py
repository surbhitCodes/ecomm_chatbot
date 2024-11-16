from fastapi import FastAPI
from backend.api.endpoints import queries, project_planning, technical_support
from backend.services.vector_db import populate_vector_db

app = FastAPI(
    title="Arbor Test Project API",
    description="LLM-powered assistant for contractors and builders.",
    version="1.0.0",
)

# Populate the vector database on startup
@app.on_event("startup")
def startup_event():
    populate_vector_db()

# Include API routers
app.include_router(queries.router)
app.include_router(project_planning.router)
app.include_router(technical_support.router)
