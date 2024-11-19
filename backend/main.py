"""
Main program to activate API (FastAPI) and run backend (use this with uvicorn)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from api.endpoints import technical_support, project_planning, queries

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Arbor Test Project API",
    description="LLM-powered assistant for contractors and builders.",
    version="1.0.0",
)

# CORS config
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

# include API routers
app.include_router(technical_support.router)
app.include_router(project_planning.router)
app.include_router(queries.router)
