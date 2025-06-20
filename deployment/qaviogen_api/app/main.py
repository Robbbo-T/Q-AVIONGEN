"""
Q-AVIOGEN FastAPI Service
Enterprise-ready REST API for Q-AVIOGEN Avatar Video Generator

This service provides a scalable, containerized API for generating
animated aeronautical documentation videos with personalized avatars
and real voice narration.

Author: Amedeo Pelliccia
Version: 1.0.0
License: MIT
"""

import asyncio
import logging
import os
import uuid
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from .models import (
    VideoGenerationRequest,
    VideoGenerationResponse,
    JobStatus,
    JobStatusResponse,
    HealthResponse,
    ErrorResponse
)
from .runner import VideoGenerationRunner
from .utils import setup_logging, validate_request, cleanup_old_files
from .config import Settings

# Initialize settings
settings = Settings()

# Setup logging
logger = setup_logging(settings.log_level)

# Job storage (in production, use Redis or database)
jobs: Dict[str, Dict] = {}

# Security
security = HTTPBearer(auto_error=False)


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token if authentication is enabled"""
    if not settings.enable_auth:
        return True
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    if credentials.credentials != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token"
        )
    
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Starting Q-AVIOGEN FastAPI Service")
    
    # Startup
    os.makedirs(settings.temp_dir, exist_ok=True)
    os.makedirs(settings.output_dir, exist_ok=True)
    
    # Start cleanup task
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Q-AVIOGEN FastAPI Service")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


async def periodic_cleanup():
    """Periodically clean up old files and jobs"""
    while True:
        try:
            await asyncio.sleep(settings.cleanup_interval)
            cleanup_old_files(settings.temp_dir, max_age_hours=24)
            cleanup_old_files(settings.output_dir, max_age_hours=48)
            
            # Clean up old job records
            current_time = asyncio.get_event_loop().time()
            expired_jobs = [
                job_id for job_id, job_data in jobs.items()
                if current_time - job_data.get('created_at', 0) > 86400  # 24 hours
            ]
            for job_id in expired_jobs:
                jobs.pop(job_id, None)
                
            logger.info(f"Cleanup completed. Removed {len(expired_jobs)} expired jobs")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Initialize FastAPI app
app = FastAPI(
    title="Q-AVIOGEN API",
    description="Enterprise REST API for Q-AVIOGEN Avatar Video Generator",
    version="1.0.0",
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    lifespan=lifespan
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred"
        ).dict()
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the Q-AVIOGEN API service"
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=asyncio.get_event_loop().time(),
        active_jobs=len([j for j in jobs.values() if j.get('status') == 'processing'])
    )


@app.post(
    "/generate",
    response_model=VideoGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate Video",
    description="Submit a video generation request and receive a job ID for tracking"
)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    _: bool = Depends(verify_token)
):
    """Generate avatar video based on configuration"""
    try:
        # Validate request
        await validate_request(request)
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job
        job_data = {
            'id': job_id,
            'status': 'queued',
            'request': request.dict(),
            'created_at': asyncio.get_event_loop().time(),
            'progress': 0,
            'message': 'Job queued for processing',
            'output_file': None,
            'error': None
        }
        
        jobs[job_id] = job_data
        
        # Start background processing
        background_tasks.add_task(process_video_generation, job_id, request)
        
        logger.info(f"📋 Video generation job {job_id} queued")
        
        return VideoGenerationResponse(
            job_id=job_id,
            status="queued",
            message="Video generation job has been queued"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting video generation job: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit job: {str(e)}"
        )


@app.get(
    "/jobs/{job_id}",
    response_model=JobStatusResponse,
    summary="Get Job Status",
    description="Get the current status and progress of a video generation job"
)
async def get_job_status(
    job_id: str,
    _: bool = Depends(verify_token)
):
    """Get job status and progress"""
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    job_data = jobs[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job_data['status'],
        progress=job_data['progress'],
        message=job_data['message'],
        output_file=job_data.get('output_file'),
        error=job_data.get('error'),
        created_at=job_data['created_at']
    )


@app.get(
    "/jobs",
    response_model=List[JobStatusResponse],
    summary="List Jobs",
    description="List all video generation jobs with their current status"
)
async def list_jobs(
    limit: int = 50,
    status_filter: Optional[str] = None,
    _: bool = Depends(verify_token)
):
    """List all jobs with optional filtering"""
    job_list = list(jobs.values())
    
    # Filter by status if provided
    if status_filter:
        job_list = [j for j in job_list if j['status'] == status_filter]
    
    # Sort by creation time (newest first)
    job_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Limit results
    job_list = job_list[:limit]
    
    return [
        JobStatusResponse(
            job_id=job['id'],
            status=job['status'],
            progress=job['progress'],
            message=job['message'],
            output_file=job.get('output_file'),
            error=job.get('error'),
            created_at=job['created_at']
        )
        for job in job_list
    ]


@app.get(
    "/download/{job_id}",
    summary="Download Video",
    description="Download the generated video file for a completed job"
)
async def download_video(
    job_id: str,
    _: bool = Depends(verify_token)
):
    """Download generated video file"""
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    job_data = jobs[job_id]
    
    if job_data['status'] != 'completed':
        raise HTTPException(
            status_code=400,
            detail="Job not completed"
        )
    
    output_file = job_data.get('output_file')
    if not output_file or not os.path.exists(output_file):
        raise HTTPException(
            status_code=404,
            detail="Output file not found"
        )
    
    return FileResponse(
        path=output_file,
        filename=f"qaviogen_video_{job_id}.mp4",
        media_type="video/mp4"
    )


@app.delete(
    "/jobs/{job_id}",
    summary="Cancel Job",
    description="Cancel a pending or running video generation job"
)
async def cancel_job(
    job_id: str,
    _: bool = Depends(verify_token)
):
    """Cancel a job"""
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    job_data = jobs[job_id]
    
    if job_data['status'] in ['completed', 'failed', 'cancelled']:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status: {job_data['status']}"
        )
    
    job_data['status'] = 'cancelled'
    job_data['message'] = 'Job cancelled by user'
    
    logger.info(f"🚫 Job {job_id} cancelled")
    
    return {"message": "Job cancelled successfully"}


async def process_video_generation(job_id: str, request: VideoGenerationRequest):
    """Background task to process video generation"""
    logger.info(f"🎬 Starting video generation for job {job_id}")
    
    try:
        # Update job status
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['message'] = 'Initializing video generation'
        jobs[job_id]['progress'] = 10
        
        # Initialize runner
        runner = VideoGenerationRunner(
            job_id=job_id,
            temp_dir=settings.temp_dir,
            output_dir=settings.output_dir
        )
        
        # Progress callback
        def update_progress(progress: int, message: str):
            if job_id in jobs:
                jobs[job_id]['progress'] = progress
                jobs[job_id]['message'] = message
                logger.info(f"📊 Job {job_id}: {progress}% - {message}")
        
        # Run generation
        output_file = await runner.generate_video(request, update_progress)
        
        # Update job completion
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['message'] = 'Video generation completed successfully'
        jobs[job_id]['output_file'] = output_file
        
        logger.info(f"✅ Video generation completed for job {job_id}")
        
    except Exception as e:
        logger.error(f"❌ Video generation failed for job {job_id}: {e}")
        
        if job_id in jobs:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = f'Video generation failed: {str(e)}'
            jobs[job_id]['error'] = str(e)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
