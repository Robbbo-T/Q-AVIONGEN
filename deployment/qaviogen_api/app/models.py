"""
Pydantic models for Q-AVIOGEN FastAPI service

This module defines all the request and response models used by the API,
ensuring type safety and automatic validation.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
import json


class JobStatusEnum(str, Enum):
    """Job status enumeration"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AvatarConfig(BaseModel):
    """Avatar configuration model"""
    model_path: str = Field(..., description="Path to the avatar Blender model")
    face_texture: Optional[str] = Field(None, description="Path to face texture")
    animation_style: str = Field("professional", description="Animation style")
    enable_lip_sync: bool = Field(True, description="Enable lip synchronization")
    gesture_intensity: float = Field(0.5, ge=0.0, le=1.0, description="Gesture intensity")


class VoiceConfig(BaseModel):
    """Voice configuration model"""
    voice_file: Optional[str] = Field(None, description="Path to voice audio file")
    voice_id: Optional[str] = Field(None, description="TTS voice ID")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Speech speed")
    pitch: float = Field(1.0, ge=0.5, le=2.0, description="Voice pitch")
    volume: float = Field(1.0, ge=0.0, le=1.0, description="Audio volume")


class RenderSettings(BaseModel):
    """Render settings model"""
    resolution_x: int = Field(1920, ge=480, le=4096, description="Video width")
    resolution_y: int = Field(1080, ge=270, le=2160, description="Video height")
    fps: int = Field(30, ge=24, le=60, description="Frames per second")
    quality: str = Field("high", description="Render quality: low, medium, high, ultra")
    samples: int = Field(128, ge=32, le=512, description="Render samples")
    enable_denoising: bool = Field(True, description="Enable AI denoising")


class CameraConfig(BaseModel):
    """Camera configuration model"""
    position: List[float] = Field([0, 0, 5], description="Camera position [x, y, z]")
    rotation: List[float] = Field([0, 0, 0], description="Camera rotation [x, y, z]")
    focal_length: float = Field(50.0, ge=10.0, le=200.0, description="Focal length in mm")
    tracking_target: Optional[str] = Field(None, description="Object to track")


class SceneConfig(BaseModel):
    """Scene configuration model"""
    background_hdri: Optional[str] = Field(None, description="Path to HDRI background")
    lighting_setup: str = Field("studio", description="Lighting setup type")
    environment_intensity: float = Field(1.0, ge=0.0, le=5.0, description="Environment intensity")
    props: List[Dict[str, Any]] = Field(default_factory=list, description="Scene props")


class VideoGenerationRequest(BaseModel):
    """Main video generation request model"""
    project_name: str = Field(..., min_length=1, max_length=100, description="Project name")
    procedure_text: str = Field(..., min_length=10, description="Procedure text to narrate")
    
    # Avatar configuration
    avatar: AvatarConfig = Field(..., description="Avatar configuration")
    
    # Voice configuration
    voice: VoiceConfig = Field(..., description="Voice configuration")
    
    # Render settings
    render: RenderSettings = Field(default_factory=RenderSettings, description="Render settings")
    
    # Camera configuration
    camera: CameraConfig = Field(default_factory=CameraConfig, description="Camera configuration")
    
    # Scene configuration
    scene: SceneConfig = Field(default_factory=SceneConfig, description="Scene configuration")
    
    # Output settings
    output_format: str = Field("mp4", description="Output video format")
    output_quality: str = Field("high", description="Output quality")
    
    # Optional metadata
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @validator('procedure_text')
    def validate_procedure_text(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Procedure text must be at least 10 characters long')
        return v.strip()
    
    @validator('avatar')
    def validate_avatar(cls, v):
        if not v.model_path:
            raise ValueError('Avatar model path is required')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "project_name": "ATA_32-11-00_Nosegear_Inspection",
                "procedure_text": "Welcome to the nose gear inspection procedure. Today we will examine the aircraft nose landing gear assembly following ATA 32-11-00 specifications.",
                "avatar": {
                    "model_path": "/assets/avatars/amedeo/avatar_model.blend",
                    "face_texture": "/assets/avatars/amedeo/face_texture.png",
                    "animation_style": "professional",
                    "enable_lip_sync": True,
                    "gesture_intensity": 0.7
                },
                "voice": {
                    "voice_file": "/assets/audio/amedeo_voice_48k.wav",
                    "speed": 1.0,
                    "pitch": 1.0,
                    "volume": 0.8
                },
                "render": {
                    "resolution_x": 1920,
                    "resolution_y": 1080,
                    "fps": 30,
                    "quality": "high",
                    "samples": 128,
                    "enable_denoising": True
                },
                "output_format": "mp4",
                "output_quality": "high"
            }
        }


class VideoGenerationResponse(BaseModel):
    """Video generation response model"""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatusEnum = Field(..., description="Current job status")
    message: str = Field(..., description="Status message")
    estimated_duration: Optional[int] = Field(None, description="Estimated completion time in seconds")


class JobStatusResponse(BaseModel):
    """Job status response model"""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatusEnum = Field(..., description="Current job status")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    message: str = Field(..., description="Current status message")
    output_file: Optional[str] = Field(None, description="Path to output file (if completed)")
    error: Optional[str] = Field(None, description="Error message (if failed)")
    created_at: float = Field(..., description="Job creation timestamp")
    started_at: Optional[float] = Field(None, description="Job start timestamp")
    completed_at: Optional[float] = Field(None, description="Job completion timestamp")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    timestamp: float = Field(..., description="Current timestamp")
    active_jobs: int = Field(..., description="Number of active jobs")
    system_info: Optional[Dict[str, Any]] = Field(None, description="System information")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    timestamp: Optional[float] = Field(None, description="Error timestamp")
    job_id: Optional[str] = Field(None, description="Related job ID if applicable")


class JobCancellationResponse(BaseModel):
    """Job cancellation response model"""
    job_id: str = Field(..., description="Cancelled job ID")
    message: str = Field(..., description="Cancellation message")
    timestamp: float = Field(..., description="Cancellation timestamp")


class BatchJobRequest(BaseModel):
    """Batch job request model for multiple video generations"""
    jobs: List[VideoGenerationRequest] = Field(..., min_items=1, max_items=10, description="List of video generation requests")
    batch_name: Optional[str] = Field(None, description="Optional batch name")
    priority: int = Field(0, ge=0, le=10, description="Batch priority (higher = more priority)")


class BatchJobResponse(BaseModel):
    """Batch job response model"""
    batch_id: str = Field(..., description="Unique batch identifier")
    job_ids: List[str] = Field(..., description="List of individual job IDs")
    status: str = Field(..., description="Batch status")
    message: str = Field(..., description="Status message")


class SystemStatsResponse(BaseModel):
    """System statistics response model"""
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    active_jobs: int = Field(..., description="Number of active jobs")
    total_jobs_processed: int = Field(..., description="Total jobs processed since startup")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


# Legacy support models for backward compatibility
class LegacySceneConfig(BaseModel):
    """Legacy scene configuration for backward compatibility"""
    scene_name: str
    instructor_name: str
    procedure_steps: List[str]
    avatar_model: str
    voice_settings: Dict[str, Any]
    
    def to_modern_request(self) -> VideoGenerationRequest:
        """Convert legacy config to modern request format"""
        return VideoGenerationRequest(
            project_name=self.scene_name,
            procedure_text=" ".join(self.procedure_steps),
            avatar=AvatarConfig(
                model_path=self.avatar_model,
                animation_style="professional"
            ),
            voice=VoiceConfig(**self.voice_settings)
        )


# Type aliases for convenience
JobStatus = JobStatusEnum
JobID = str
Timestamp = float
