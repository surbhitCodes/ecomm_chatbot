"""
Main program to activate API (FastAPI) and run backend (use this with uvicorn)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.setup_vector_db import populate_vector_db
import logging
from api.endpoints import technical_support, project_planning, queries

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executes logic during app startup and shutdown.
    """
    logger.info("Starting up the application...")
    try:
        populate_vector_db() 
        logger.info("Vector db updated successfully...")
    except Exception as e:
        logger.error(f"Error updating vector db: {e}")
    yield  
    logger.info("Shutting down the application...")


app = FastAPI(
    lifespan=lifespan,
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
