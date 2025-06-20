"""
Video Generation Runner for Q-AVIOGEN FastAPI Service

This module handles the actual video generation process, integrating with
the existing Q-AVIOGEN core system and managing the rendering pipeline.
"""

import asyncio
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Callable, Dict, Any, Optional

from .models import VideoGenerationRequest
from .utils import get_logger, validate_file_path, ensure_directory

logger = get_logger(__name__)


class VideoGenerationRunner:
    """Handles video generation process"""
    
    def __init__(self, job_id: str, temp_dir: str, output_dir: str):
        """Initialize the runner
        
        Args:
            job_id: Unique job identifier
            temp_dir: Temporary directory for processing
            output_dir: Output directory for final videos
        """
        self.job_id = job_id
        self.temp_dir = Path(temp_dir)
        self.output_dir = Path(output_dir)
        self.job_temp_dir = self.temp_dir / job_id
        
        # Create job-specific temp directory
        ensure_directory(self.job_temp_dir)
        
        # Paths to Q-AVIOGEN core components (adjust based on your structure)
        self.qaviogen_root = Path(__file__).parent.parent.parent.parent
        self.core_path = self.qaviogen_root / "core"
        self.main_script = self.qaviogen_root / "main.py"
        
        logger.info(f"Initialized runner for job {job_id}")
    
    async def generate_video(
        self, 
        request: VideoGenerationRequest, 
        progress_callback: Callable[[int, str], None]
    ) -> str:
        """Generate video based on request
        
        Args:
            request: Video generation request
            progress_callback: Function to update progress
            
        Returns:
            Path to generated video file
        """
        try:
            progress_callback(10, "Preparing configuration")
            
            # Step 1: Create configuration file
            config_file = await self._create_config_file(request)
            progress_callback(20, "Configuration created")
            
            # Step 2: Validate assets
            await self._validate_assets(request)
            progress_callback(30, "Assets validated")
            
            # Step 3: Prepare audio
            await self._prepare_audio(request)
            progress_callback(40, "Audio prepared")
            
            # Step 4: Run Q-AVIOGEN core
            progress_callback(50, "Starting video generation")
            video_file = await self._run_qaviogen(config_file, progress_callback)
            
            # Step 5: Post-processing
            progress_callback(90, "Post-processing")
            final_video = await self._post_process_video(video_file, request)
            
            # Step 6: Move to output directory
            output_path = self.output_dir / f"{self.job_id}.mp4"
            shutil.move(final_video, output_path)
            
            progress_callback(100, "Video generation completed")
            
            # Cleanup temporary files
            await self._cleanup_temp_files()
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Video generation failed for job {self.job_id}: {e}")
            await self._cleanup_temp_files()
            raise
    
    async def _create_config_file(self, request: VideoGenerationRequest) -> str:
        """Create Q-AVIOGEN configuration file from request"""
        config_data = {
            "scene_name": request.project_name,
            "instructor_name": "API_Generated",
            "instructor_config": {
                "avatar": {
                    "model_path": request.avatar.model_path,
                    "face_texture": request.avatar.face_texture,
                    "animation_style": request.avatar.animation_style,
                    "enable_lip_sync": request.avatar.enable_lip_sync,
                    "gesture_intensity": request.avatar.gesture_intensity
                },
                "voice": {
                    "voice_file": request.voice.voice_file,
                    "voice_id": request.voice.voice_id,
                    "speed": request.voice.speed,
                    "pitch": request.voice.pitch,
                    "volume": request.voice.volume
                }
            },
            "scene_config": {
                "background_hdri": request.scene.background_hdri,
                "lighting_setup": request.scene.lighting_setup,
                "environment_intensity": request.scene.environment_intensity,
                "props": request.scene.props
            },
            "camera_config": {
                "position": request.camera.position,
                "rotation": request.camera.rotation,
                "focal_length": request.camera.focal_length,
                "tracking_target": request.camera.tracking_target
            },
            "render_settings": {
                "resolution_x": request.render.resolution_x,
                "resolution_y": request.render.resolution_y,
                "fps": request.render.fps,
                "quality": request.render.quality,
                "samples": request.render.samples,
                "enable_denoising": request.render.enable_denoising
            },
            "output_settings": {
                "format": request.output_format,
                "quality": request.output_quality,
                "output_dir": str(self.job_temp_dir)
            },
            "procedure_steps": [
                {
                    "step_id": "main_narration",
                    "content": request.procedure_text,
                    "duration": None,  # Will be calculated from audio
                    "actions": ["narrate", "gesture"]
                }
            ]
        }
        
        # Add metadata if provided
        if request.metadata:
            config_data["metadata"] = request.metadata
        
        # Save configuration file
        config_file = self.job_temp_dir / "scene_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created config file: {config_file}")
        return str(config_file)
    
    async def _validate_assets(self, request: VideoGenerationRequest):
        """Validate that all required assets exist"""
        assets_to_check = []
        
        # Avatar model
        if request.avatar.model_path:
            assets_to_check.append(request.avatar.model_path)
        
        # Face texture
        if request.avatar.face_texture:
            assets_to_check.append(request.avatar.face_texture)
        
        # Voice file
        if request.voice.voice_file:
            assets_to_check.append(request.voice.voice_file)
        
        # HDRI background
        if request.scene.background_hdri:
            assets_to_check.append(request.scene.background_hdri)
        
        # Check all assets
        for asset_path in assets_to_check:
            await validate_file_path(asset_path)
        
        logger.info(f"Validated {len(assets_to_check)} assets")
    
    async def _prepare_audio(self, request: VideoGenerationRequest) -> Optional[str]:
        """Prepare audio for the video generation"""
        if not request.voice.voice_file:
            # If no voice file, we'll need to generate TTS
            if request.voice.voice_id:
                return await self._generate_tts_audio(request)
            else:
                logger.warning("No voice file or voice ID provided")
                return None
        
        # Copy voice file to temp directory
        voice_file = Path(request.voice.voice_file)
        if not voice_file.exists():
            raise FileNotFoundError(f"Voice file not found: {voice_file}")
        
        temp_audio = self.job_temp_dir / f"audio_{voice_file.suffix}"
        shutil.copy2(voice_file, temp_audio)
        
        logger.info(f"Prepared audio file: {temp_audio}")
        return str(temp_audio)
    
    async def _generate_tts_audio(self, request: VideoGenerationRequest) -> str:
        """Generate TTS audio from text"""
        # This would integrate with your TTS system
        # For now, we'll create a placeholder
        
        tts_script = self.qaviogen_root / "tts" / "generate_audio.py"
        output_audio = self.job_temp_dir / "generated_audio.wav"
        
        cmd = [
            "python", str(tts_script),
            "--text", request.procedure_text,
            "--voice_id", request.voice.voice_id or "default",
            "--speed", str(request.voice.speed),
            "--pitch", str(request.voice.pitch),
            "--output", str(output_audio)
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.qaviogen_root
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "TTS generation failed"
            raise RuntimeError(f"TTS generation failed: {error_msg}")
        
        logger.info(f"Generated TTS audio: {output_audio}")
        return str(output_audio)
    
    async def _run_qaviogen(
        self, 
        config_file: str, 
        progress_callback: Callable[[int, str], None]
    ) -> str:
        """Run the Q-AVIOGEN core system"""
        
        cmd = [
            "python", str(self.main_script),
            "--config", config_file,
            "--output-dir", str(self.job_temp_dir),
            "--batch-mode"
        ]
        
        logger.info(f"Running Q-AVIOGEN: {' '.join(cmd)}")
        
        # Start the process
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.qaviogen_root
        )
        
        # Monitor progress
        progress = 50
        while process.returncode is None:
            await asyncio.sleep(2)
            progress = min(85, progress + 2)
            progress_callback(progress, "Rendering video...")
            
            try:
                # Check if process is still running
                await asyncio.wait_for(process.wait(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
        
        # Get final output
        _, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Q-AVIOGEN execution failed"
            raise RuntimeError(f"Q-AVIOGEN execution failed: {error_msg}")
        
        # Find the output video file
        output_files = list(self.job_temp_dir.glob("*.mp4"))
        if not output_files:
            raise RuntimeError("No output video file found")
        
        video_file = output_files[0]
        logger.info(f"Q-AVIOGEN completed: {video_file}")
        
        return str(video_file)
    
    async def _post_process_video(self, video_file: str, request: VideoGenerationRequest) -> str:
        """Post-process the generated video"""
        # For now, just return the original file
        # In the future, this could include:
        # - Video compression optimization
        # - Adding watermarks
        # - Format conversion
        # - Quality adjustments
        
        logger.info(f"Post-processing video: {video_file}")
        
        # If we need to convert format or apply post-processing
        if request.output_format != "mp4" or request.output_quality != "high":
            return await self._convert_video(video_file, request)
        
        return video_file
    
    async def _convert_video(self, input_file: str, request: VideoGenerationRequest) -> str:
        """Convert video to requested format and quality"""
        output_file = self.job_temp_dir / f"final.{request.output_format}"
        
        # FFmpeg conversion command
        cmd = [
            "ffmpeg", "-i", input_file,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", self._get_crf_for_quality(request.output_quality),
            "-c:a", "aac",
            "-b:a", "128k",
            "-y", str(output_file)
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError("Video conversion failed")
        
        logger.info(f"Converted video: {output_file}")
        return str(output_file)
    
    def _get_crf_for_quality(self, quality: str) -> str:
        """Get CRF value for video quality"""
        quality_map = {
            "low": "28",
            "medium": "23",
            "high": "18",
            "ultra": "15"
        }
        return quality_map.get(quality, "23")
    
    async def _cleanup_temp_files(self):
        """Clean up temporary files for this job"""
        try:
            if self.job_temp_dir.exists():
                shutil.rmtree(self.job_temp_dir)
                logger.info(f"Cleaned up temp directory: {self.job_temp_dir}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp files: {e}")


class BatchVideoGenerationRunner:
    """Handles batch video generation for multiple jobs"""
    
    def __init__(self, temp_dir: str, output_dir: str, max_concurrent: int = 2):
        """Initialize batch runner
        
        Args:
            temp_dir: Temporary directory for processing
            output_dir: Output directory for final videos
            max_concurrent: Maximum concurrent jobs
        """
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_batch(
        self,
        batch_id: str,
        requests: list[VideoGenerationRequest],
        progress_callback: Callable[[str, int, str], None]
    ) -> list[str]:
        """Process a batch of video generation requests
        
        Args:
            batch_id: Unique batch identifier
            requests: List of video generation requests
            progress_callback: Function to update progress (job_id, progress, message)
            
        Returns:
            List of output file paths
        """
        tasks = []
        
        for i, request in enumerate(requests):
            job_id = f"{batch_id}_{i:03d}"
            
            async def process_single(req=request, jid=job_id):
                async with self.semaphore:
                    runner = VideoGenerationRunner(jid, self.temp_dir, self.output_dir)
                    
                    def update_progress(progress: int, message: str):
                        progress_callback(jid, progress, message)
                    
                    return await runner.generate_video(req, update_progress)
            
            tasks.append(process_single())
        
        # Process all jobs concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results
        output_files = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch job {i} failed: {result}")
                output_files.append(None)
            else:
                output_files.append(result)
        
        return output_files
