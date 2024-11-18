"""
Program to extract environment variables
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    Extracting the needed environment variables
    """
    OPENAI_KEY: str = Field(..., env='OPENAI_KEY')
    API_KEY: str = Field(..., env='API_KEY')


settings = Settings()

# print("Loaded Settings:", settings.model_dump()) # for debugging
