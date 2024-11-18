"""
Mapping dependency and api_key verification
"""

from fastapi import Header, HTTPException, status
from typing import Optional
from core.config import settings


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Validate API key for added security
    :param x_api_key: supplied API key over the n/w
    :return: validated API key
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key missing"
        )
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return x_api_key
