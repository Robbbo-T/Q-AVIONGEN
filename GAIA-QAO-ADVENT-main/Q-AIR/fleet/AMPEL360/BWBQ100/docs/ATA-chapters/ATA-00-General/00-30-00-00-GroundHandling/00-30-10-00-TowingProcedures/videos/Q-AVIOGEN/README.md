# Q-AVIOGEN FastAPI Service

Enterprise-ready REST API for Q-AVIOGEN Avatar Video Generator. This service provides a scalable, containerized API for generating animated aeronautical documentation videos with personalized avatars and real voice narration.

![Q-AVIOGEN API](https://img.shields.io/badge/Q--AVIOGEN-API-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-teal)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

- **🚀 High Performance**: Async FastAPI with optimized request handling
- **🎭 Avatar Integration**: Support for personalized 3D avatars with lip-sync
- **🎙️ Voice Synthesis**: Real voice narration and TTS integration
- **📦 Containerized**: Docker-ready with multi-stage builds
- **🔐 Security**: Authentication, CORS, and security best practices
- **📊 Monitoring**: Health checks, metrics, and logging
- **🔄 CI/CD Ready**: GitHub Actions workflow included
- **☁️ Cloud Native**: Azure, Kubernetes, and container deployment support

## 🏗️ Architecture

```
qaviogen_api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── runner.py            # Video generation logic
│   ├── utils.py             # Utility functions
│   ├── config.py            # Configuration management
│   └── __init__.py
├── tests/
│   ├── test_api.py          # API tests
│   └── conftest.py          # Test configuration
├── .github/workflows/
│   └── ci-cd.yml            # CI/CD pipeline
├── Dockerfile               # Docker configuration
├── docker-compose.yml      # Local development setup
├── requirements.txt         # Python dependencies
├── pytest.ini              # Test configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional)
- FFmpeg
- Blender (for 3D rendering)

### Local Development

1. **Clone and Setup**
   ```bash
   cd deployment/qaviogen_api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run Development Server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Production Build**
   ```bash
   docker build -t qaviogen-api .
   docker run -p 8000:8000 qaviogen-api
   ```

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/generate` | Submit video generation job |
| `GET` | `/jobs/{job_id}` | Get job status |
| `GET` | `/jobs` | List all jobs |
| `GET` | `/download/{job_id}` | Download generated video |
| `DELETE` | `/jobs/{job_id}` | Cancel job |

### Example Usage

#### 1. Generate Video

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "ATA_32-11-00_Nosegear_Inspection",
    "procedure_text": "Welcome to the nose gear inspection procedure...",
    "avatar": {
      "model_path": "./project/assets/avatars/amedeo/avatar_model.blend",
      "animation_style": "professional",
      "enable_lip_sync": true,
      "gesture_intensity": 0.7
    },
    "voice": {
      "voice_file": "./project/assets/audio/amedeo_voice_48k.wav",
      "speed": 1.0,
      "pitch": 1.0,
      "volume": 0.8
    },
    "render": {
      "resolution_x": 1920,
      "resolution_y": 1080,
      "fps": 30,
      "quality": "high"
    }
  }'
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Video generation job has been queued"
}
```

#### 2. Check Job Status

```bash
curl "http://localhost:8000/jobs/550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "message": "Rendering video frames...",
  "created_at": 1703123456.789
}
```

#### 3. Download Video

```bash
curl -O "http://localhost:8000/download/550e8400-e29b-41d4-a716-446655440000"
```

## 🎛️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QAVIOGEN_DEBUG` | Enable debug mode | `false` |
| `QAVIOGEN_HOST` | Server host | `0.0.0.0` |
| `QAVIOGEN_PORT` | Server port | `8000` |
| `QAVIOGEN_ENABLE_AUTH` | Enable authentication | `false` |
| `QAVIOGEN_API_TOKEN` | API authentication token | `None` |
| `QAVIOGEN_MAX_CONCURRENT_JOBS` | Max concurrent jobs | `2` |
| `QAVIOGEN_TEMP_DIR` | Temporary files directory | `./temp` |
| `QAVIOGEN_OUTPUT_DIR` | Output files directory | `./output` |
| `QAVIOGEN_CORS_ORIGINS` | CORS allowed origins | `["*"]` |

### Example .env File

```env
# Application Settings
QAVIOGEN_DEBUG=false
QAVIOGEN_LOG_LEVEL=INFO
QAVIOGEN_HOST=0.0.0.0
QAVIOGEN_PORT=8000

# Security
QAVIOGEN_ENABLE_AUTH=true
QAVIOGEN_API_TOKEN=your-secure-api-token-here
QAVIOGEN_CORS_ORIGINS=["https://your-domain.com"]

# Processing
QAVIOGEN_MAX_CONCURRENT_JOBS=4
QAVIOGEN_JOB_TIMEOUT_SECONDS=3600

# Directories
QAVIOGEN_TEMP_DIR=/app/temp
QAVIOGEN_OUTPUT_DIR=/app/output

# Optional: Database
QAVIOGEN_DATABASE_URL=postgresql://user:pass@localhost:5432/qaviogen
QAVIOGEN_REDIS_URL=redis://localhost:6379/0
```

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# With coverage
pytest --cov=app --cov-report=html

# Performance tests
pytest -m performance
```

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and workflows
- **Performance Tests**: Test response times and load handling

## 🚢 Deployment

### Azure Container Apps

```bash
# Build and push image
docker build -t qaviogen-api .
docker tag qaviogen-api your-registry.azurecr.io/qaviogen-api:latest
docker push your-registry.azurecr.io/qaviogen-api:latest

# Deploy to Azure Container Apps
az containerapp create \
  --name qaviogen-api \
  --resource-group rg-qaviogen \
  --environment qaviogen-env \
  --image your-registry.azurecr.io/qaviogen-api:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qaviogen-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: qaviogen-api
  template:
    metadata:
      labels:
        app: qaviogen-api
    spec:
      containers:
      - name: qaviogen-api
        image: qaviogen-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: QAVIOGEN_DEBUG
          value: "false"
        - name: QAVIOGEN_ENABLE_AUTH
          value: "true"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

### Docker Swarm

```yaml
version: '3.8'
services:
  qaviogen-api:
    image: qaviogen-api:latest
    ports:
      - "8000:8000"
    environment:
      - QAVIOGEN_DEBUG=false
      - QAVIOGEN_ENABLE_AUTH=true
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

## 📊 Monitoring

### Health Checks

The service provides comprehensive health checks:

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed system status
curl http://localhost:8000/health?detailed=true
```

### Metrics

- **Active Jobs**: Number of currently processing jobs
- **Queue Length**: Number of queued jobs
- **System Resources**: CPU, memory, disk usage
- **Response Times**: API endpoint performance

### Logging

Structured logging with multiple levels:

```python
# Application logs
2023-12-01 10:00:00 - qaviogen_api.main - INFO - 🚀 Starting Q-AVIOGEN FastAPI Service
2023-12-01 10:00:05 - qaviogen_api.runner - INFO - 📋 Video generation job abc123 queued
2023-12-01 10:00:10 - qaviogen_api.runner - INFO - 🎬 Starting video generation for job abc123
```

## 🔧 Development

### Code Quality

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/

# Security scan
bandit -r app/
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### API Schema

The API automatically generates OpenAPI 3.0 schema available at:
- JSON: `http://localhost:8000/openapi.json`
- YAML: Download from Swagger UI

## 🐛 Troubleshooting

### Common Issues

**Issue**: Video generation fails
```bash
# Check logs
docker logs qaviogen-api

# Verify assets
ls -la ./project/assets/avatars/
ls -la ./project/assets/audio/
```

**Issue**: High memory usage
```bash
# Monitor resources
docker stats qaviogen-api

# Adjust limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 8G
```

**Issue**: Slow API responses
```bash
# Check concurrent jobs
curl http://localhost:8000/jobs

# Reduce concurrent jobs
export QAVIOGEN_MAX_CONCURRENT_JOBS=1
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
export QAVIOGEN_DEBUG=true
export QAVIOGEN_LOG_LEVEL=DEBUG
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests: `pytest tests/`
5. Run quality checks: `black . && flake8 . && mypy .`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Create a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write tests for new features
- Update documentation
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Amedeo Pelliccia**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@domain.com

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- Q-AVIOGEN core development team
- Contributors and beta testers

## 📚 Additional Resources

- [Q-AVIOGEN Documentation](../README.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Azure Container Apps](https://docs.microsoft.com/en-us/azure/container-apps/)

---

**Ready to generate amazing aviation videos with Q-AVIOGEN API! 🚀✈️**

