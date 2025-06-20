"""
Configuration settings for Q-AVIOGEN FastAPI Service

This module manages all configuration settings for the API service,
including environment variables and default values.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = Field("Q-AVIOGEN API", description="Application name")
    app_version: str = Field("1.0.0", description="Application version")
    debug: bool = Field(False, description="Debug mode")
    
    # Server Configuration
    host: str = Field("0.0.0.0", description="Server host")
    port: int = Field(8000, description="Server port")
    workers: int = Field(1, description="Number of worker processes")
    
    # Security Configuration
    enable_auth: bool = Field(False, description="Enable API authentication")
    api_token: Optional[str] = Field(None, description="API authentication token")
    allowed_hosts: List[str] = Field(["*"], description="Allowed hosts")
    cors_origins: List[str] = Field(["*"], description="CORS allowed origins")
    
    # Directories
    temp_dir: str = Field("./temp", description="Temporary files directory")
    output_dir: str = Field("./output", description="Output files directory")
    assets_dir: str = Field("./assets", description="Assets directory")
    logs_dir: str = Field("./logs", description="Logs directory")
    
    # Processing Configuration
    max_concurrent_jobs: int = Field(2, description="Maximum concurrent jobs")
    job_timeout_seconds: int = Field(3600, description="Job timeout in seconds")
    cleanup_interval: int = Field(3600, description="Cleanup interval in seconds")
    
    # File Limits
    max_file_size_mb: int = Field(100, description="Maximum upload file size in MB")
    max_video_duration_minutes: int = Field(30, description="Maximum video duration")
    
    # Logging Configuration
    log_level: str = Field("INFO", description="Logging level")
    log_file: str = Field("qaviogen_api.log", description="Log file name")
    log_rotation_mb: int = Field(100, description="Log rotation size in MB")
    
    # External Tools
    blender_executable: str = Field("blender", description="Blender executable path")
    ffmpeg_executable: str = Field("ffmpeg", description="FFmpeg executable path")
    python_executable: str = Field("python", description="Python executable path")
    
    # Performance Settings
    render_priority: str = Field("normal", description="Render process priority")
    memory_limit_gb: Optional[int] = Field(None, description="Memory limit in GB")
    
    # Feature Flags
    enable_docs: bool = Field(True, description="Enable API documentation")
    enable_metrics: bool = Field(True, description="Enable metrics collection")
    enable_batch_processing: bool = Field(True, description="Enable batch processing")
    enable_websockets: bool = Field(False, description="Enable WebSocket support")
    
    # Q-AVIOGEN Specific
    qaviogen_root: str = Field("./", description="Q-AVIOGEN root directory")
    default_avatar_model: str = Field(
        "./project/assets/avatars/amedeo/avatar_model.blend",
        description="Default avatar model path"
    )
    default_voice_file: str = Field(
        "./project/assets/audio/amedeo_voice_48k.wav",
        description="Default voice file path"
    )
    
    # Database Configuration (for future use)
    database_url: Optional[str] = Field(None, description="Database connection URL")
    redis_url: Optional[str] = Field(None, description="Redis connection URL")
    
    # Monitoring Configuration
    metrics_port: int = Field(9090, description="Metrics server port")
    health_check_interval: int = Field(30, description="Health check interval in seconds")
    
    # Azure Configuration (for cloud deployment)
    azure_storage_account: Optional[str] = Field(None, description="Azure storage account")
    azure_container_name: Optional[str] = Field(None, description="Azure container name")
    azure_key_vault_url: Optional[str] = Field(None, description="Azure Key Vault URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable prefix
        env_prefix = "QAVIOGEN_"
        
        # Field aliases for environment variables
        fields = {
            'api_token': {'env': ['QAVIOGEN_API_TOKEN', 'API_TOKEN']},
            'database_url': {'env': ['QAVIOGEN_DATABASE_URL', 'DATABASE_URL']},
            'redis_url': {'env': ['QAVIOGEN_REDIS_URL', 'REDIS_URL']},
            'azure_storage_account': {'env': ['AZURE_STORAGE_ACCOUNT']},
            'azure_key_vault_url': {'env': ['AZURE_KEY_VAULT_URL']},
        }


# Environment-specific settings
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    enable_docs: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    max_concurrent_jobs: int = 1


class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    log_level: str = "WARNING"
    enable_docs: bool = False
    enable_auth: bool = True
    cors_origins: List[str] = []  # Restrict in production
    max_concurrent_jobs: int = 4
    
    # Security hardening
    allowed_hosts: List[str] = []  # Must be set explicitly
    
    # Performance optimization
    workers: int = 4
    job_timeout_seconds: int = 1800  # 30 minutes


class TestingSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    temp_dir: str = "./test_temp"
    output_dir: str = "./test_output"
    max_concurrent_jobs: int = 1
    job_timeout_seconds: int = 300  # 5 minutes
    cleanup_interval: int = 60  # 1 minute


def get_settings() -> Settings:
    """Get settings based on environment
    
    Returns:
        Settings instance for current environment
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()


def validate_settings() -> bool:
    """Validate current settings
    
    Returns:
        True if settings are valid
    """
    errors = []
    
    # Check required directories
    required_dirs = [
        settings.temp_dir,
        settings.output_dir,
        settings.logs_dir
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create directory {directory}: {e}")
    
    # Check Q-AVIOGEN root
    qaviogen_main = os.path.join(settings.qaviogen_root, "main.py")
    if not os.path.exists(qaviogen_main):
        errors.append(f"Q-AVIOGEN main.py not found at {qaviogen_main}")
    
    # Check authentication settings in production
    if not settings.debug and settings.enable_auth and not settings.api_token:
        errors.append("API token must be set when authentication is enabled in production")
    
    # Check CORS settings in production
    if not settings.debug and "*" in settings.cors_origins:
        errors.append("CORS origins should not include '*' in production")
    
    # Check resource limits
    if settings.max_concurrent_jobs > 10:
        errors.append("Maximum concurrent jobs should not exceed 10")
    
    if settings.job_timeout_seconds > 7200:  # 2 hours
        errors.append("Job timeout should not exceed 2 hours")
    
    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True


# Configuration examples for different deployment scenarios
DOCKER_ENV_EXAMPLE = """
# Docker environment variables example
QAVIOGEN_DEBUG=false
QAVIOGEN_LOG_LEVEL=INFO
QAVIOGEN_HOST=0.0.0.0
QAVIOGEN_PORT=8000
QAVIOGEN_ENABLE_AUTH=true
QAVIOGEN_API_TOKEN=your-secure-api-token-here
QAVIOGEN_TEMP_DIR=/app/temp
QAVIOGEN_OUTPUT_DIR=/app/output
QAVIOGEN_MAX_CONCURRENT_JOBS=2
QAVIOGEN_CORS_ORIGINS=["https://your-domain.com"]
"""

KUBERNETES_ENV_EXAMPLE = """
# Kubernetes deployment environment variables
ENVIRONMENT=production
QAVIOGEN_DEBUG=false
QAVIOGEN_LOG_LEVEL=WARNING
QAVIOGEN_ENABLE_AUTH=true
QAVIOGEN_API_TOKEN_FILE=/etc/secrets/api-token
QAVIOGEN_ALLOWED_HOSTS=["qaviogen-api.your-domain.com"]
QAVIOGEN_CORS_ORIGINS=["https://your-frontend.com"]
QAVIOGEN_MAX_CONCURRENT_JOBS=4
QAVIOGEN_WORKERS=4
QAVIOGEN_REDIS_URL=redis://redis-service:6379
QAVIOGEN_DATABASE_URL=postgresql://user:pass@postgres-service:5432/qaviogen
"""

AZURE_ENV_EXAMPLE = """
# Azure deployment environment variables
ENVIRONMENT=production
QAVIOGEN_DEBUG=false
QAVIOGEN_ENABLE_AUTH=true
AZURE_STORAGE_ACCOUNT=your-storage-account
AZURE_CONTAINER_NAME=qaviogen-files
AZURE_KEY_VAULT_URL=https://your-keyvault.vault.azure.net/
QAVIOGEN_TEMP_DIR=/tmp/qaviogen
QAVIOGEN_OUTPUT_DIR=/app/output
QAVIOGEN_CORS_ORIGINS=["https://your-app.azurewebsites.net"]
"""
