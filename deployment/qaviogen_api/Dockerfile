# Q-AVIOGEN FastAPI Service Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Build dependencies and setup
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    QAVIOGEN_TEMP_DIR="/app/temp" \
    QAVIOGEN_OUTPUT_DIR="/app/output" \
    QAVIOGEN_LOGS_DIR="/app/logs"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    # Blender dependencies
    blender \
    # FFmpeg for video processing
    ffmpeg \
    # Audio processing libraries
    libsndfile1 \
    # Image processing libraries
    libgl1-mesa-glx \
    libglib2.0-0 \
    # System utilities
    curl \
    wget \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create application user for security
RUN groupadd -r qaviogen && useradd -r -g qaviogen qaviogen

# Create application directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/temp /app/output /app/logs /app/assets && \
    chown -R qaviogen:qaviogen /app

# Copy application code
COPY app/ ./app/
COPY *.py ./

# Copy Q-AVIOGEN core (adjust paths as needed)
# Assuming the API is deployed with access to Q-AVIOGEN core
COPY --chown=qaviogen:qaviogen core/ ./core/
COPY --chown=qaviogen:qaviogen assets/ ./assets/
COPY --chown=qaviogen:qaviogen project/ ./project/

# Create startup script
COPY <<EOF /app/start.sh
#!/bin/bash
set -e

# Validate configuration
echo "🔧 Validating Q-AVIOGEN API configuration..."
python -c "from app.config import validate_settings; exit(0 if validate_settings() else 1)"

# Check system requirements
echo "🔍 Checking system requirements..."
python -c "
import asyncio
from app.utils import check_system_requirements

async def check():
    reqs = await check_system_requirements()
    missing = [k for k, v in reqs.items() if not v]
    if missing:
        print(f'⚠️ Missing requirements: {missing}')
    else:
        print('✅ All system requirements met')

asyncio.run(check())
"

# Start the application
echo "🚀 Starting Q-AVIOGEN FastAPI Service..."
exec "\$@"
EOF

RUN chmod +x /app/start.sh && chown qaviogen:qaviogen /app/start.sh

# Switch to non-root user
USER qaviogen

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set entrypoint and default command
ENTRYPOINT ["/app/start.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# Metadata labels
LABEL maintainer="Amedeo Pelliccia <your.email@domain.com>" \
      version="1.0.0" \
      description="Q-AVIOGEN FastAPI Service - Enterprise REST API for Avatar Video Generation" \
      org.opencontainers.image.title="Q-AVIOGEN API" \
      org.opencontainers.image.description="Enterprise REST API for Q-AVIOGEN Avatar Video Generator" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Amedeo Pelliccia" \
      org.opencontainers.image.source="https://github.com/yourusername/q-aviogen" \
      org.opencontainers.image.licenses="MIT"
