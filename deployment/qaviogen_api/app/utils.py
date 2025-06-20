"""
Utility functions for Q-AVIOGEN FastAPI Service

This module provides common utility functions used throughout the API,
including logging, validation, file management, and system operations.
"""

import asyncio
import logging
import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any, Optional, Union

import psutil
from fastapi import HTTPException

from .models import VideoGenerationRequest


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('qaviogen_api.log')
        ]
    )
    
    # Create specific logger for our app
    logger = logging.getLogger('qaviogen_api')
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'qaviogen_api.{name}')


async def validate_request(request: VideoGenerationRequest) -> None:
    """Validate video generation request
    
    Args:
        request: Video generation request to validate
        
    Raises:
        HTTPException: If validation fails
    """
    logger = get_logger(__name__)
    
    try:
        # Validate procedure text
        if not request.procedure_text or len(request.procedure_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Procedure text must be at least 10 characters long"
            )
        
        # Validate avatar configuration
        if not request.avatar.model_path:
            raise HTTPException(
                status_code=400,
                detail="Avatar model path is required"
            )
        
        # Validate voice configuration
        if not request.voice.voice_file and not request.voice.voice_id:
            raise HTTPException(
                status_code=400,
                detail="Either voice file or voice ID must be provided"
            )
        
        # Validate render settings
        if request.render.resolution_x < 480 or request.render.resolution_y < 270:
            raise HTTPException(
                status_code=400,
                detail="Minimum resolution is 480x270"
            )
        
        if request.render.fps < 24 or request.render.fps > 60:
            raise HTTPException(
                status_code=400,
                detail="FPS must be between 24 and 60"
            )
        
        # Validate project name
        if not request.project_name or len(request.project_name.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Project name is required"
            )
        
        logger.info(f"Request validation passed for project: {request.project_name}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Request validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Request validation failed: {str(e)}"
        )


async def validate_file_path(file_path: str) -> None:
    """Validate that a file path exists and is accessible
    
    Args:
        file_path: Path to validate
        
    Raises:
        HTTPException: If file is not found or not accessible
    """
    if not file_path:
        return
    
    path = Path(file_path)
    
    # Handle relative paths - make them relative to Q-AVIOGEN root
    if not path.is_absolute():
        qaviogen_root = Path(__file__).parent.parent.parent.parent
        path = qaviogen_root / file_path
    
    if not path.exists():
        raise HTTPException(
            status_code=400,
            detail=f"File not found: {file_path}"
        )
    
    if not path.is_file():
        raise HTTPException(
            status_code=400,
            detail=f"Path is not a file: {file_path}"
        )
    
    # Check if file is readable
    try:
        with open(path, 'rb') as f:
            f.read(1)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"File not accessible: {file_path} - {str(e)}"
        )


def ensure_directory(directory: Union[str, Path]) -> None:
    """Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path to ensure
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)


def cleanup_old_files(directory: Union[str, Path], max_age_hours: int = 24) -> int:
    """Clean up old files in a directory
    
    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files to keep (in hours)
        
    Returns:
        Number of files deleted
    """
    logger = get_logger(__name__)
    
    directory = Path(directory)
    if not directory.exists():
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    try:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                        logger.debug(f"Deleted old file: {file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to delete file {file_path}: {e}")
        
        # Remove empty directories
        for dir_path in directory.rglob('*'):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                try:
                    dir_path.rmdir()
                    logger.debug(f"Removed empty directory: {dir_path}")
                except Exception as e:
                    logger.warning(f"Failed to remove directory {dir_path}: {e}")
    
    except Exception as e:
        logger.error(f"Error during cleanup of {directory}: {e}")
    
    if deleted_count > 0:
        logger.info(f"Cleaned up {deleted_count} old files from {directory}")
    
    return deleted_count


def get_system_stats() -> Dict[str, Any]:
    """Get current system statistics
    
    Returns:
        Dictionary with system stats
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "memory_total": memory.total,
            "memory_available": memory.available,
            "disk_usage": disk.percent,
            "disk_total": disk.total,
            "disk_free": disk.free,
            "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
        }
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error getting system stats: {e}")
        return {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0,
            "error": str(e)
        }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    size_index = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and size_index < len(size_names) - 1:
        size /= 1024.0
        size_index += 1
    
    return f"{size:.1f} {size_names[size_index]}"


def calculate_estimated_duration(request: VideoGenerationRequest) -> int:
    """Calculate estimated video generation duration
    
    Args:
        request: Video generation request
        
    Returns:
        Estimated duration in seconds
    """
    # Base time factors
    base_time = 60  # 1 minute base
    
    # Resolution factor
    resolution_factor = (request.render.resolution_x * request.render.resolution_y) / (1920 * 1080)
    
    # Quality factor
    quality_factors = {
        "low": 0.5,
        "medium": 1.0,
        "high": 1.5,
        "ultra": 2.5
    }
    quality_factor = quality_factors.get(request.render.quality, 1.0)
    
    # FPS factor
    fps_factor = request.render.fps / 30.0
    
    # Samples factor
    samples_factor = request.render.samples / 128.0
    
    # Text length factor (estimate video duration from text)
    words_per_minute = 150  # Average speaking rate
    word_count = len(request.procedure_text.split())
    video_duration_minutes = max(1, word_count / words_per_minute)
    
    # Calculate estimated render time
    estimated_seconds = (
        base_time * 
        resolution_factor * 
        quality_factor * 
        fps_factor * 
        samples_factor * 
        video_duration_minutes
    )
    
    return int(estimated_seconds)


async def check_system_requirements() -> Dict[str, bool]:
    """Check if system meets minimum requirements
    
    Returns:
        Dictionary with requirement checks
    """
    logger = get_logger(__name__)
    
    requirements = {
        "sufficient_memory": False,
        "sufficient_disk": False,
        "blender_available": False,
        "ffmpeg_available": False,
        "python_version": False
    }
    
    try:
        # Check memory (minimum 4GB)
        memory = psutil.virtual_memory()
        requirements["sufficient_memory"] = memory.available > 4 * 1024 * 1024 * 1024
        
        # Check disk space (minimum 10GB free)
        disk = psutil.disk_usage('/')
        requirements["sufficient_disk"] = disk.free > 10 * 1024 * 1024 * 1024
        
        # Check if Blender is available
        try:
            result = await asyncio.create_subprocess_exec(
                "blender", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            requirements["blender_available"] = result.returncode == 0
        except Exception:
            requirements["blender_available"] = False
        
        # Check if FFmpeg is available
        try:
            result = await asyncio.create_subprocess_exec(
                "ffmpeg", "-version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            requirements["ffmpeg_available"] = result.returncode == 0
        except Exception:
            requirements["ffmpeg_available"] = False
        
        # Check Python version (minimum 3.8)
        import sys
        requirements["python_version"] = sys.version_info >= (3, 8)
        
    except Exception as e:
        logger.error(f"Error checking system requirements: {e}")
    
    return requirements


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be safe for filesystem
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename


class ProgressTracker:
    """Track progress of long-running operations"""
    
    def __init__(self, total_steps: int):
        """Initialize progress tracker
        
        Args:
            total_steps: Total number of steps in operation
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        self.step_times = []
    
    def update(self, step: int, message: str = "") -> Dict[str, Any]:
        """Update progress
        
        Args:
            step: Current step number
            message: Optional progress message
            
        Returns:
            Progress information
        """
        self.current_step = step
        current_time = time.time()
        self.step_times.append(current_time)
        
        # Calculate progress percentage
        progress_percent = min(100, int((step / self.total_steps) * 100))
        
        # Calculate elapsed time
        elapsed_time = current_time - self.start_time
        
        # Estimate remaining time
        if step > 0:
            avg_time_per_step = elapsed_time / step
            remaining_steps = self.total_steps - step
            estimated_remaining = avg_time_per_step * remaining_steps
        else:
            estimated_remaining = 0
        
        return {
            "progress": progress_percent,
            "current_step": step,
            "total_steps": self.total_steps,
            "message": message,
            "elapsed_time": elapsed_time,
            "estimated_remaining": estimated_remaining
        }
    
    def complete(self) -> Dict[str, Any]:
        """Mark operation as complete
        
        Returns:
            Completion information
        """
        return self.update(self.total_steps, "Operation completed")


def parse_time_duration(duration_str: str) -> int:
    """Parse time duration string to seconds
    
    Args:
        duration_str: Duration string (e.g., "1h30m", "45m", "120s")
        
    Returns:
        Duration in seconds
    """
    duration_str = duration_str.lower().strip()
    
    if not duration_str:
        return 0
    
    total_seconds = 0
    current_number = ""
    
    for char in duration_str:
        if char.isdigit():
            current_number += char
        elif char in ['h', 'm', 's']:
            if current_number:
                value = int(current_number)
                if char == 'h':
                    total_seconds += value * 3600
                elif char == 'm':
                    total_seconds += value * 60
                elif char == 's':
                    total_seconds += value
                current_number = ""
    
    # If there's a remaining number without unit, assume seconds
    if current_number:
        total_seconds += int(current_number)
    
    return total_seconds
