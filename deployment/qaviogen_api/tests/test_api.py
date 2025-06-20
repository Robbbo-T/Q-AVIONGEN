"""
Test suite for Q-AVIOGEN FastAPI Service

This module contains comprehensive tests for the API endpoints,
models, utilities, and business logic.
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Import the app and dependencies
from app.main import app
from app.models import VideoGenerationRequest, AvatarConfig, VoiceConfig
from app.config import Settings, TestingSettings
from app.utils import validate_request, cleanup_old_files


# Test fixtures
@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create test client"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client() -> Generator[AsyncClient, None, None]:
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as async_test_client:
        yield async_test_client


@pytest.fixture
def test_settings() -> TestingSettings:
    """Test settings configuration"""
    return TestingSettings()


@pytest.fixture
def sample_video_request() -> VideoGenerationRequest:
    """Sample video generation request for testing"""
    return VideoGenerationRequest(
        project_name="Test_Project",
        procedure_text="This is a test procedure for video generation. It contains enough text to meet the minimum requirements.",
        avatar=AvatarConfig(
            model_path="./test_assets/avatar_model.blend",
            face_texture="./test_assets/face_texture.png",
            animation_style="professional",
            enable_lip_sync=True,
            gesture_intensity=0.7
        ),
        voice=VoiceConfig(
            voice_file="./test_assets/test_voice.wav",
            speed=1.0,
            pitch=1.0,
            volume=0.8
        )
    )


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """Create temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


# Test classes
class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client: TestClient):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
        assert "active_jobs" in data


class TestVideoGenerationEndpoint:
    """Test video generation endpoints"""
    
    def test_generate_video_success(self, client: TestClient, sample_video_request: VideoGenerationRequest):
        """Test successful video generation request"""
        response = client.post(
            "/generate",
            json=sample_video_request.dict()
        )
        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "queued"
        assert "message" in data
    
    def test_generate_video_invalid_request(self, client: TestClient):
        """Test video generation with invalid request"""
        invalid_request = {
            "project_name": "",  # Invalid: empty name
            "procedure_text": "Too short",  # Invalid: too short
        }
        response = client.post("/generate", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_generate_video_missing_avatar(self, client: TestClient):
        """Test video generation with missing avatar config"""
        invalid_request = {
            "project_name": "Test Project",
            "procedure_text": "This is a valid procedure text that meets the minimum length requirements.",
            # Missing avatar config
        }
        response = client.post("/generate", json=invalid_request)
        assert response.status_code == 422


class TestJobManagementEndpoints:
    """Test job management endpoints"""
    
    def test_get_job_status_not_found(self, client: TestClient):
        """Test getting status of non-existent job"""
        response = client.get("/jobs/non-existent-job-id")
        assert response.status_code == 404
    
    def test_list_jobs_empty(self, client: TestClient):
        """Test listing jobs when none exist"""
        response = client.get("/jobs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_cancel_job_not_found(self, client: TestClient):
        """Test cancelling non-existent job"""
        response = client.delete("/jobs/non-existent-job-id")
        assert response.status_code == 404
    
    def test_download_video_not_found(self, client: TestClient):
        """Test downloading video for non-existent job"""
        response = client.get("/download/non-existent-job-id")
        assert response.status_code == 404


class TestModels:
    """Test Pydantic models"""
    
    def test_video_generation_request_validation(self):
        """Test video generation request model validation"""
        # Valid request
        valid_data = {
            "project_name": "Test Project",
            "procedure_text": "This is a valid procedure text that meets the minimum length requirements.",
            "avatar": {
                "model_path": "./test_assets/avatar_model.blend",
                "animation_style": "professional"
            },
            "voice": {
                "voice_file": "./test_assets/test_voice.wav"
            }
        }
        request = VideoGenerationRequest(**valid_data)
        assert request.project_name == "Test Project"
        assert request.avatar.model_path == "./test_assets/avatar_model.blend"
    
    def test_video_generation_request_invalid_text(self):
        """Test video generation request with invalid procedure text"""
        invalid_data = {
            "project_name": "Test Project",
            "procedure_text": "Short",  # Too short
            "avatar": {
                "model_path": "./test_assets/avatar_model.blend"
            },
            "voice": {
                "voice_file": "./test_assets/test_voice.wav"
            }
        }
        with pytest.raises(ValueError):
            VideoGenerationRequest(**invalid_data)
    
    def test_avatar_config_validation(self):
        """Test avatar configuration validation"""
        # Valid config
        valid_config = AvatarConfig(
            model_path="./test_assets/avatar_model.blend",
            animation_style="professional",
            gesture_intensity=0.7
        )
        assert valid_config.model_path == "./test_assets/avatar_model.blend"
        assert valid_config.gesture_intensity == 0.7
        
        # Invalid gesture intensity
        with pytest.raises(ValueError):
            AvatarConfig(
                model_path="./test_assets/avatar_model.blend",
                gesture_intensity=1.5  # Out of range
            )
    
    def test_voice_config_validation(self):
        """Test voice configuration validation"""
        # Valid config
        valid_config = VoiceConfig(
            voice_file="./test_assets/test_voice.wav",
            speed=1.2,
            pitch=0.9,
            volume=0.8
        )
        assert valid_config.voice_file == "./test_assets/test_voice.wav"
        assert valid_config.speed == 1.2
        
        # Invalid speed
        with pytest.raises(ValueError):
            VoiceConfig(
                voice_file="./test_assets/test_voice.wav",
                speed=3.0  # Out of range
            )


class TestUtilities:
    """Test utility functions"""
    
    @pytest.mark.asyncio
    async def test_validate_request_success(self, sample_video_request: VideoGenerationRequest):
        """Test successful request validation"""
        # Should not raise any exception
        await validate_request(sample_video_request)
    
    @pytest.mark.asyncio
    async def test_validate_request_empty_text(self):
        """Test request validation with empty procedure text"""
        from fastapi import HTTPException
        
        invalid_request = VideoGenerationRequest(
            project_name="Test Project",
            procedure_text="",  # Empty text
            avatar=AvatarConfig(model_path="./test_assets/avatar_model.blend"),
            voice=VoiceConfig(voice_file="./test_assets/test_voice.wav")
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await validate_request(invalid_request)
        assert exc_info.value.status_code == 400
    
    def test_cleanup_old_files(self, temp_directory: Path):
        """Test cleanup of old files"""
        # Create test files
        old_file = temp_directory / "old_file.txt"
        new_file = temp_directory / "new_file.txt"
        
        old_file.write_text("old content")
        new_file.write_text("new content")
        
        # Modify timestamps to simulate old file
        import time
        old_time = time.time() - 48 * 3600  # 48 hours ago
        os.utime(old_file, (old_time, old_time))
        
        # Run cleanup (24 hour threshold)
        deleted_count = cleanup_old_files(temp_directory, max_age_hours=24)
        
        # Old file should be deleted, new file should remain
        assert deleted_count == 1
        assert not old_file.exists()
        assert new_file.exists()


class TestConfiguration:
    """Test configuration management"""
    
    def test_test_settings(self):
        """Test testing environment settings"""
        settings = TestingSettings()
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.temp_dir == "./test_temp"
        assert settings.max_concurrent_jobs == 1
    
    def test_environment_variable_override(self, monkeypatch):
        """Test environment variable override"""
        monkeypatch.setenv("QAVIOGEN_MAX_CONCURRENT_JOBS", "5")
        monkeypatch.setenv("QAVIOGEN_DEBUG", "false")
        
        settings = TestingSettings()
        assert settings.max_concurrent_jobs == 5
        assert settings.debug is False


class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_video_generation_workflow(self, async_client: AsyncClient, sample_video_request: VideoGenerationRequest):
        """Test complete video generation workflow"""
        # Step 1: Submit job
        response = await async_client.post(
            "/generate",
            json=sample_video_request.dict()
        )
        assert response.status_code == 202
        job_data = response.json()
        job_id = job_data["job_id"]
        
        # Step 2: Check job status
        response = await async_client.get(f"/jobs/{job_id}")
        assert response.status_code == 200
        status_data = response.json()
        assert status_data["job_id"] == job_id
        assert status_data["status"] in ["queued", "processing"]
        
        # Step 3: List jobs
        response = await async_client.get("/jobs")
        assert response.status_code == 200
        jobs_list = response.json()
        assert len(jobs_list) >= 1
        assert any(job["job_id"] == job_id for job in jobs_list)
        
        # Step 4: Cancel job (if still running)
        response = await async_client.delete(f"/jobs/{job_id}")
        if response.status_code == 200:
            # Job was successfully cancelled
            cancel_data = response.json()
            assert "message" in cancel_data
    
    @pytest.mark.asyncio
    async def test_concurrent_job_submission(self, async_client: AsyncClient, sample_video_request: VideoGenerationRequest):
        """Test concurrent job submission"""
        # Submit multiple jobs concurrently
        tasks = []
        for i in range(3):
            request_copy = sample_video_request.copy()
            request_copy.project_name = f"Test_Project_{i}"
            
            task = async_client.post(
                "/generate",
                json=request_copy.dict()
            )
            tasks.append(task)
        
        # Wait for all submissions
        responses = await asyncio.gather(*tasks)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 202
            data = response.json()
            assert "job_id" in data
            assert data["status"] == "queued"


class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_invalid_json_request(self, client: TestClient):
        """Test handling of invalid JSON"""
        response = client.post(
            "/generate",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client: TestClient):
        """Test handling of missing required fields"""
        incomplete_request = {
            "project_name": "Test Project"
            # Missing required fields
        }
        response = client.post("/generate", json=incomplete_request)
        assert response.status_code == 422
    
    def test_invalid_data_types(self, client: TestClient):
        """Test handling of invalid data types"""
        invalid_request = {
            "project_name": "Test Project",
            "procedure_text": "Valid procedure text that meets minimum requirements.",
            "avatar": {
                "model_path": "./test_assets/avatar_model.blend",
                "gesture_intensity": "invalid_type"  # Should be float
            },
            "voice": {
                "voice_file": "./test_assets/test_voice.wav"
            }
        }
        response = client.post("/generate", json=invalid_request)
        assert response.status_code == 422


# Performance tests
class TestPerformance:
    """Performance and load tests"""
    
    @pytest.mark.asyncio
    async def test_health_endpoint_performance(self, async_client: AsyncClient):
        """Test health endpoint response time"""
        import time
        
        start_time = time.time()
        response = await async_client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.1  # Should respond within 100ms
    
    @pytest.mark.asyncio
    async def test_concurrent_health_checks(self, async_client: AsyncClient):
        """Test concurrent health check requests"""
        tasks = [async_client.get("/health") for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            assert response.status_code == 200


# Fixtures for test data
@pytest.fixture(scope="session")
def test_assets_directory():
    """Create test assets directory with sample files"""
    test_dir = Path("./test_assets")
    test_dir.mkdir(exist_ok=True)
    
    # Create dummy asset files for testing
    (test_dir / "avatar_model.blend").touch()
    (test_dir / "face_texture.png").touch()
    (test_dir / "test_voice.wav").touch()
    
    yield test_dir
    
    # Cleanup after tests
    import shutil
    if test_dir.exists():
        shutil.rmtree(test_dir)


# Test configuration
pytest_plugins = ["pytest_asyncio"]

# Custom markers
pytestmark = [
    pytest.mark.asyncio,
]

# Test discovery configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add marker for integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Add marker for performance tests
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
