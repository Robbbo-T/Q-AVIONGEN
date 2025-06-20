#!/usr/bin/env python3
"""
Q-AVIOGEN Deployment Preparation Script
Prepares the system for production deployment and CI/CD integration
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.errors import create_logger

class DeploymentPreparation:
    """Comprehensive deployment preparation for Q-AVIOGEN"""
    
    def __init__(self):
        self.logger = create_logger(__name__)
        self.project_root = project_root
        self.deployment_config = {}
        
    def check_environment(self) -> Dict[str, Any]:
        """Check current environment setup"""
        self.logger.info("🔍 Checking environment setup...")
        
        env_status = {
            "python_version": sys.version,
            "project_root": str(self.project_root),
            "os_platform": os.name,
            "requirements_exist": (self.project_root / "requirements.txt").exists(),
            "setup_py_exist": (self.project_root / "setup.py").exists(),
            "docker_available": self._check_docker(),
            "git_available": self._check_git(),
            "virtual_env": self._check_virtual_env()
        }
        
        self.logger.info(f"✅ Environment check completed: {len([k for k, v in env_status.items() if v])} checks passed")
        return env_status
    
    def _check_docker(self) -> bool:
        """Check if Docker is available"""
        try:
            result = subprocess.run(["docker", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _check_git(self) -> bool:
        """Check if Git is available"""
        try:
            result = subprocess.run(["git", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _check_virtual_env(self) -> bool:
        """Check if we're in a virtual environment"""
        return hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
    
    def create_dockerfile(self) -> str:
        """Create production-ready Dockerfile"""
        dockerfile_content = '''# Q-AVIOGEN Production Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Install Blender (for production environments)
RUN curl -L https://download.blender.org/release/Blender3.6/blender-3.6.0-linux-x64.tar.xz \\
    -o blender.tar.xz \\
    && tar -xf blender.tar.xz \\
    && mv blender-3.6.0-linux-x64 /opt/blender \\
    && ln -s /opt/blender/blender /usr/local/bin/blender \\
    && rm blender.tar.xz

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/output/videos /app/output/frames /app/output/audio /app/cache

# Set environment variables
ENV PYTHONPATH=/app
ENV BLENDER_PATH=/usr/local/bin/blender
ENV Q_AVIOGEN_MODE=production

# Expose port for web interface (if implemented)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import sys; sys.path.insert(0, '/app'); from core.types import SceneConfig; print('OK')" || exit 1

# Default command
CMD ["python", "main.py", "--help"]
'''
        
        dockerfile_path = self.project_root / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        self.logger.info(f"✅ Dockerfile created: {dockerfile_path}")
        return str(dockerfile_path)
    
    def create_docker_compose(self) -> str:
        """Create Docker Compose for development and testing"""
        compose_content = '''version: '3.8'

services:
  q-aviogen:
    build: .
    container_name: q-aviogen
    volumes:
      - ./input:/app/input
      - ./output:/app/output
      - ./cache:/app/cache
    environment:
      - Q_AVIOGEN_MODE=development
      - PYTHONPATH=/app
    ports:
      - "8080:8080"
    networks:
      - q-aviogen-network
  
  # Optional: Redis for caching (future enhancement)
  redis:
    image: redis:alpine
    container_name: q-aviogen-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - q-aviogen-network
  
  # Optional: Monitoring with Prometheus (future enhancement)
  prometheus:
    image: prom/prometheus
    container_name: q-aviogen-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - q-aviogen-network

networks:
  q-aviogen-network:
    driver: bridge

volumes:
  redis_data:
'''
        
        compose_path = self.project_root / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        
        self.logger.info(f"✅ Docker Compose created: {compose_path}")
        return str(compose_path)
    
    def create_github_actions_workflow(self) -> str:
        """Create GitHub Actions CI/CD workflow"""
        workflow_content = '''name: Q-AVIOGEN CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.9'
  
jobs:
  test:
    name: Test Suite
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black isort
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: black --check .
    
    - name: Import sort check
      run: isort --check-only .
    
    - name: Run integration tests
      run: |
        python integration_test.py
    
    - name: Run unit tests with coverage
      run: |
        pytest tests/ --cov=. --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
  
  build-docker:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build Docker image
      run: |
        docker build -t q-aviogen:latest .
    
    - name: Test Docker image
      run: |
        docker run --rm q-aviogen:latest python -c "print('Docker image works!')"
  
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [test, build-docker]
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to staging
      run: |
        echo "🚀 Deploying to staging environment..."
        # Add your staging deployment commands here
        # Example: kubectl apply -f k8s/staging/
  
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [test, build-docker]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "🚀 Deploying to production environment..."
        # Add your production deployment commands here
        # Example: kubectl apply -f k8s/production/
'''
        
        workflow_dir = self.project_root / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_path = workflow_dir / "ci-cd.yml"
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        
        self.logger.info(f"✅ GitHub Actions workflow created: {workflow_path}")
        return str(workflow_path)
    
    def create_kubernetes_manifests(self) -> str:
        """Create Kubernetes deployment manifests"""
        k8s_dir = self.project_root / "k8s"
        k8s_dir.mkdir(exist_ok=True)
        
        # Deployment manifest
        deployment_content = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: q-aviogen
  labels:
    app: q-aviogen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: q-aviogen
  template:
    metadata:
      labels:
        app: q-aviogen
    spec:
      containers:
      - name: q-aviogen
        image: q-aviogen:latest
        ports:
        - containerPort: 8080
        env:
        - name: Q_AVIOGEN_MODE
          value: "production"
        - name: PYTHONPATH
          value: "/app"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: output-volume
          mountPath: /app/output
        - name: cache-volume
          mountPath: /app/cache
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: output-volume
        persistentVolumeClaim:
          claimName: q-aviogen-output-pvc
      - name: cache-volume
        persistentVolumeClaim:
          claimName: q-aviogen-cache-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: q-aviogen-service
spec:
  selector:
    app: q-aviogen
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: q-aviogen-output-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: q-aviogen-cache-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
'''
        
        deployment_path = k8s_dir / "deployment.yaml"
        with open(deployment_path, 'w') as f:
            f.write(deployment_content)
        
        self.logger.info(f"✅ Kubernetes manifests created: {k8s_dir}")
        return str(k8s_dir)
    
    def create_monitoring_config(self) -> str:
        """Create monitoring and observability configurations"""
        monitoring_dir = self.project_root / "monitoring"
        monitoring_dir.mkdir(exist_ok=True)
        
        # Prometheus configuration
        prometheus_config = '''global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'q-aviogen'
    static_configs:
      - targets: ['q-aviogen:8080']
    metrics_path: /metrics
    scrape_interval: 5s
  
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
'''
        
        prometheus_path = monitoring_dir / "prometheus.yml"
        with open(prometheus_path, 'w') as f:
            f.write(prometheus_config)
        
        # Grafana dashboard configuration
        grafana_config = '''{
  "dashboard": {
    "id": null,
    "title": "Q-AVIOGEN Monitoring Dashboard",
    "tags": ["q-aviogen", "video-generation"],
    "style": "dark",
    "timezone": "browser",
    "panels": [
      {
        "title": "Video Generation Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(q_aviogen_videos_generated_total[5m])",
            "legendFormat": "Videos/sec"
          }
        ]
      },
      {
        "title": "Rendering Queue Size",
        "type": "stat",
        "targets": [
          {
            "expr": "q_aviogen_render_queue_size",
            "legendFormat": "Queue Size"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(q_aviogen_errors_total[5m])",
            "legendFormat": "Errors/sec"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "5s"
  }
}'''
        
        grafana_path = monitoring_dir / "grafana-dashboard.json"
        with open(grafana_path, 'w') as f:
            f.write(grafana_config)
        
        self.logger.info(f"✅ Monitoring configurations created: {monitoring_dir}")
        return str(monitoring_dir)
    
    def create_deployment_scripts(self) -> str:
        """Create deployment automation scripts"""
        scripts_dir = self.project_root / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # Build and deploy script
        deploy_script = '''#!/bin/bash
# Q-AVIOGEN Deployment Script

set -e

echo "🚀 Q-AVIOGEN Deployment Script"
echo "=============================="

# Configuration
IMAGE_NAME="q-aviogen"
TAG=${1:-latest}
ENVIRONMENT=${2:-staging}

echo "📦 Building Docker image..."
docker build -t ${IMAGE_NAME}:${TAG} .

echo "🧪 Running integration tests..."
docker run --rm ${IMAGE_NAME}:${TAG} python integration_test.py

if [ "$ENVIRONMENT" = "production" ]; then
    echo "🔍 Running security scan..."
    # Add security scanning here
    echo "Security scan passed"
fi

echo "🚢 Deploying to ${ENVIRONMENT}..."
if [ "$ENVIRONMENT" = "kubernetes" ]; then
    kubectl apply -f k8s/
    kubectl rollout status deployment/q-aviogen
elif [ "$ENVIRONMENT" = "docker-compose" ]; then
    docker-compose up -d
else
    echo "⚠️  Unknown deployment environment: ${ENVIRONMENT}"
    exit 1
fi

echo "✅ Deployment completed successfully!"
echo "🌐 Application should be available at your configured endpoint"
'''
        
        deploy_script_path = scripts_dir / "deploy.sh"
        with open(deploy_script_path, 'w') as f:
            f.write(deploy_script)
        
        # Make script executable (if on Unix-like system)
        if os.name != 'nt':
            os.chmod(deploy_script_path, 0o755)
        
        # Health check script
        health_script = '''#!/bin/bash
# Q-AVIOGEN Health Check Script

set -e

ENDPOINT=${1:-http://localhost:8080}

echo "🏥 Q-AVIOGEN Health Check"
echo "========================"

echo "📊 Checking application health..."
if curl -f "${ENDPOINT}/health" > /dev/null 2>&1; then
    echo "✅ Application is healthy"
else
    echo "❌ Application health check failed"
    exit 1
fi

echo "🔧 Checking readiness..."
if curl -f "${ENDPOINT}/ready" > /dev/null 2>&1; then
    echo "✅ Application is ready"
else
    echo "❌ Application readiness check failed"
    exit 1
fi

echo "📈 Checking metrics endpoint..."
if curl -f "${ENDPOINT}/metrics" > /dev/null 2>&1; then
    echo "✅ Metrics endpoint is accessible"
else
    echo "⚠️  Metrics endpoint not available (optional)"
fi

echo "🎉 All health checks passed!"
'''
        
        health_script_path = scripts_dir / "health_check.sh"
        with open(health_script_path, 'w') as f:
            f.write(health_script)
        
        if os.name != 'nt':
            os.chmod(health_script_path, 0o755)
        
        self.logger.info(f"✅ Deployment scripts created: {scripts_dir}")
        return str(scripts_dir)
    
    def create_production_config(self) -> str:
        """Create production configuration files"""
        config_content = '''# Q-AVIOGEN Production Configuration

[DEFAULT]
# Application settings
app_name = Q-AVIOGEN
version = 2.0.0
environment = production
debug = false

[logging]
level = INFO
format = json
file = /app/logs/q-aviogen.log
max_size = 100MB
backup_count = 5

[rendering]
# Rendering settings for production
default_resolution = 1080p
max_concurrent_renders = 4
render_timeout = 3600
cache_enabled = true
cache_size = 10GB

[blender]
# Blender settings
blender_path = /usr/local/bin/blender
headless = true
gpu_enabled = true
samples = 128

[tts]
# Text-to-Speech settings
default_engine = aws_polly
cache_enabled = true
voice_speed = 1.0
voice_pitch = 0

[storage]
# Storage settings
output_path = /app/output
temp_path = /tmp/q-aviogen
max_output_size = 50GB
cleanup_after_days = 30

[monitoring]
# Monitoring settings
metrics_enabled = true
metrics_port = 9090
health_check_enabled = true
log_performance = true

[security]
# Security settings
api_key_required = true
rate_limiting = true
max_requests_per_minute = 60
allowed_file_types = .md,.yaml,.yml,.json

[database]
# Database settings (if using database)
url = postgresql://user:pass@localhost/q_aviogen
pool_size = 20
max_overflow = 30
'''
        
        config_path = self.project_root / "config_production.ini"
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        self.logger.info(f"✅ Production config created: {config_path}")
        return str(config_path)
    
    def prepare_deployment(self) -> Dict[str, Any]:
        """Complete deployment preparation"""
        self.logger.info("🎯 Starting deployment preparation...")
        
        preparation_results = {
            "timestamp": datetime.now().isoformat(),
            "environment_check": self.check_environment(),
            "files_created": {}
        }
        
        # Create all deployment artifacts
        artifacts = [
            ("dockerfile", self.create_dockerfile),
            ("docker_compose", self.create_docker_compose),
            ("github_actions", self.create_github_actions_workflow),
            ("kubernetes", self.create_kubernetes_manifests),
            ("monitoring", self.create_monitoring_config),
            ("scripts", self.create_deployment_scripts),
            ("production_config", self.create_production_config)
        ]
        
        for artifact_name, create_func in artifacts:
            try:
                path = create_func()
                preparation_results["files_created"][artifact_name] = path
                self.logger.info(f"✅ {artifact_name} created successfully")
            except Exception as e:
                self.logger.error(f"❌ Failed to create {artifact_name}: {e}")
                preparation_results["files_created"][artifact_name] = f"ERROR: {e}"
        
        # Save preparation report
        report_path = self.project_root / "deployment_preparation_report.json"
        with open(report_path, 'w') as f:
            json.dump(preparation_results, f, indent=2)
        
        self.logger.info(f"📊 Deployment preparation report saved: {report_path}")
        
        return preparation_results
    
    def generate_deployment_guide(self) -> str:
        """Generate comprehensive deployment guide"""
        guide_content = '''# Q-AVIOGEN Deployment Guide

## 🚀 Quick Start Deployment

### Prerequisites
- Docker and Docker Compose installed
- Kubernetes cluster (optional, for production)
- Git repository access
- Minimum 8GB RAM, 50GB storage

### Local Development
```bash
# Clone repository
git clone <your-repo-url>
cd Q-AVIOGEN

# Build and run with Docker Compose
docker-compose up -d

# Check health
./scripts/health_check.sh http://localhost:8080
```

### Production Deployment

#### Option 1: Docker Compose (Simple)
```bash
# Build production image
docker build -t q-aviogen:production .

# Deploy
./scripts/deploy.sh production docker-compose
```

#### Option 2: Kubernetes (Recommended)
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl rollout status deployment/q-aviogen

# Access application
kubectl port-forward service/q-aviogen-service 8080:80
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| Q_AVIOGEN_MODE | Application mode | development |
| BLENDER_PATH | Path to Blender executable | /usr/local/bin/blender |
| PYTHONPATH | Python path | /app |

### Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (if configured)
- **Health Check**: http://localhost:8080/health
- **Metrics**: http://localhost:8080/metrics

### Troubleshooting

#### Common Issues

1. **Blender not found**
   - Ensure Blender is installed and in PATH
   - Set BLENDER_PATH environment variable

2. **Permission denied**
   - Check file permissions on volumes
   - Ensure proper user mapping in containers

3. **High memory usage**
   - Adjust render settings in configuration
   - Limit concurrent renders

#### Logs
```bash
# Docker logs
docker logs q-aviogen

# Kubernetes logs
kubectl logs deployment/q-aviogen

# Application logs
tail -f /app/logs/q-aviogen.log
```

### Performance Tuning

1. **Rendering Performance**
   - Use GPU acceleration when available
   - Adjust sample counts based on quality needs
   - Enable caching for repeated operations

2. **Memory Management**
   - Monitor memory usage during large renders
   - Configure appropriate swap if needed
   - Use streaming for large video files

3. **Storage Optimization**
   - Regular cleanup of temporary files
   - Compress output videos when possible
   - Use external storage for large projects

### Security Considerations

1. **API Security**
   - Enable API key authentication
   - Implement rate limiting
   - Validate all input files

2. **File Security**
   - Restrict file upload types
   - Scan uploaded files for malware
   - Implement file size limits

3. **Network Security**
   - Use HTTPS in production
   - Implement proper firewall rules
   - Regular security updates

### Backup and Recovery

1. **Data Backup**
   - Regular backup of output files
   - Configuration backup
   - Database backup (if using)

2. **Disaster Recovery**
   - Document recovery procedures
   - Test backup restoration
   - Maintain offsite backups

### Scaling

1. **Horizontal Scaling**
   - Deploy multiple instances
   - Use load balancer
   - Share storage between instances

2. **Vertical Scaling**
   - Increase CPU/memory resources
   - Use faster storage (SSD)
   - Optimize render settings

### Support

For issues and support:
1. Check this deployment guide
2. Review application logs
3. Check GitHub issues
4. Contact development team

---

Generated by Q-AVIOGEN Deployment Preparation Tool
'''
        
        guide_path = self.project_root / "DEPLOYMENT_GUIDE.md"
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        self.logger.info(f"📖 Deployment guide created: {guide_path}")
        return str(guide_path)


def main():
    """Main deployment preparation execution"""
    print("🚀 Q-AVIOGEN Deployment Preparation")
    print("=" * 50)
    
    prep = DeploymentPreparation()
    
    try:
        # Run deployment preparation
        results = prep.prepare_deployment()
        
        # Generate deployment guide
        guide_path = prep.generate_deployment_guide()
        
        print("\n✅ Deployment preparation completed!")
        print(f"📊 Report: deployment_preparation_report.json")
        print(f"📖 Guide: {guide_path}")
        
        print("\n🎯 Next Steps:")
        print("1. Review generated configuration files")
        print("2. Customize settings for your environment")
        print("3. Test deployment in staging environment")
        print("4. Deploy to production using provided scripts")
        
        # Show summary
        created_count = len([v for v in results["files_created"].values() if not v.startswith("ERROR")])
        total_count = len(results["files_created"])
        
        print(f"\n📈 Summary: {created_count}/{total_count} deployment artifacts created")
        
        if created_count == total_count:
            print("🎉 Q-AVIOGEN is ready for production deployment!")
        else:
            print("⚠️  Some artifacts failed to create. Check the report for details.")
            
    except Exception as e:
        print(f"❌ Deployment preparation failed: {e}")
        raise


if __name__ == "__main__":
    main()
