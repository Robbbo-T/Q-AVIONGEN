"""
Q-AVIOGEN FastAPI Service

Enterprise-ready REST API for Q-AVIOGEN Avatar Video Generator.
This package provides a scalable, containerized API for generating
animated aeronautical documentation videos with personalized avatars
and real voice narration.

Author: Amedeo Pelliccia
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Amedeo Pelliccia"
__email__ = "your.email@domain.com"
__license__ = "MIT"

from .config import settings
from .models import (
    VideoGenerationRequest,
    VideoGenerationResponse,
    JobStatusResponse,
    HealthResponse,
    ErrorResponse
)

__all__ = [
    "settings",
    "VideoGenerationRequest",
    "VideoGenerationResponse", 
    "JobStatusResponse",
    "HealthResponse",
    "ErrorResponse"
]
