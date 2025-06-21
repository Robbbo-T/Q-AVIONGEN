# Q-AIR Development Setup Guide
## Quick Start for Contributors and Developers

**Setup Version:** 2.1.0  
**Last Updated:** 2025-06-21  
**Estimated Setup Time:** 30-45 minutes  

---

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Setup](#quick-setup)
- [Development Environment](#development-environment)
- [Module-Specific Setup](#module-specific-setup)
- [Testing Framework](#testing-framework)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Performance Optimization](#performance-optimization)

---

## 🎯 Prerequisites

### System Requirements
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10, macOS 10.15, Ubuntu 20.04 | Windows 11, macOS 12+, Ubuntu 22.04+ |
| **RAM** | 8 GB | 16 GB+ |
| **CPU** | 4 cores | 8 cores+ |
| **Storage** | 20 GB free | 50 GB+ SSD |
| **Network** | Broadband | High-speed for quantum backends |

### Required Software

#### 1. **Python Environment**
```bash
# Python 3.9 or higher
python --version  # Should show 3.9+

# Install Poetry for dependency management
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2. **Node.js Environment**
```bash
# Node.js 18 or higher
node --version  # Should show v18+
npm --version   # Should show 8+

# Install Yarn (optional but recommended)
npm install -g yarn
```

#### 3. **Docker Platform**
```bash
# Docker Desktop or Docker Engine
docker --version  # Should show 20.10+
docker-compose --version  # Should show 2.0+
```

#### 4. **Git and Development Tools**
```bash
# Git version control
git --version  # Should show 2.30+

# Optional: GitHub CLI
gh --version
```

---

## 🚀 Quick Setup

### 1. Repository Clone and Initial Setup
```bash
# Clone the main repository
git clone https://github.com/SQA-org/sq-aia.git Q-AIR
cd Q-AIR

# Verify project structure
ls -la
# Should show: propulsion-core/, quantum-control/, lifecycle-dashboard/, xai-visualizer/

# Copy environment template
cp .env.example .env
```

### 2. Environment Configuration
Edit the `.env` file with your configuration:

```bash
# .env file configuration
# ======================

# Development Environment
NODE_ENV=development
PYTHON_ENV=development
DEBUG=qair:*

# Database Configuration
DATABASE_URL=postgresql://qair:dev_password@localhost:5432/qair_dev
REDIS_URL=redis://localhost:6379/0

# Quantum Computing Backend
QUANTUM_BACKEND=qiskit_aer  # Options: qiskit_aer, ibm_quantum, classical_fallback
IBM_QUANTUM_TOKEN=your_ibm_quantum_token_here  # Required for IBM Quantum

# API Configuration
API_BASE_URL=http://localhost:8000
API_SECRET_KEY=your_development_secret_key_here

# Safety and Compliance
SAFETY_MODE=development  # Options: development, testing, production
ENABLE_SAFETY_OVERRIDES=true
LOG_LEVEL=debug

# Performance Monitoring
ENABLE_METRICS=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

### 3. One-Command Setup
```bash
# Run the setup script for complete environment
./scripts/setup-dev.sh

# Or use the Makefile
make setup
```

This script will:
- Install all Python dependencies
- Install all Node.js dependencies
- Set up pre-commit hooks
- Initialize the database
- Start required services

---

## 🔧 Development Environment

### Project Structure Overview
```
Q-AIR/
├── propulsion-core/          # Hydrogen-electric propulsion systems
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
├── quantum-control/          # Quantum computing algorithms
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
├── lifecycle-dashboard/      # Sustainability tracking
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── xai-visualizer/          # Explainable AI interface
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── shared/                  # Shared utilities and types
├── docs/                   # Documentation
├── scripts/                # Development scripts
├── k8s/                   # Kubernetes configurations
├── docker-compose.yml     # Local development environment
└── Makefile              # Development commands
```

### Development Workflow Setup

#### Git Configuration
```bash
# Configure Git for the project
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Install pre-commit hooks
pre-commit install

# Test pre-commit hooks
pre-commit run --all-files
```

#### IDE Configuration

##### Visual Studio Code
Install recommended extensions:
```bash
# Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension bradlc.vscode-tailwindcss
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
```

VS Code settings (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "typescript.preferences.includePackageJsonAutoImports": "auto",
  "eslint.validate": ["javascript", "typescript", "vue"],
  "files.associations": {
    "*.md": "markdown"
  }
}
```

---

## 🧩 Module-Specific Setup

### 1. Propulsion Core Module

#### Environment Setup
```bash
cd propulsion-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
poetry install

# Install additional quantum chemistry packages
pip install pyscf openfermion
```

#### Configuration
```python
# propulsion-core/config/development.py
PROPULSION_CONFIG = {
    "h2_storage": {
        "pressure_bar": 700,
        "temperature_k": 20,
        "safety_factor": 2.5,
        "simulation_mode": True
    },
    "ht_pem": {
        "operating_temp_range": (160, 220),
        "target_power_density": 3.0,
        "efficiency_target": 0.65,
        "co_tolerance": 0.04
    },
    "safety": {
        "enable_overrides": True,
        "log_all_events": True,
        "alert_threshold": "low"
    }
}
```

#### Development Server
```bash
# Start development server
python -m propulsion_core.server --dev

# Or using the Makefile
make run-propulsion-dev
```

### 2. Quantum Control Module

#### Environment Setup
```bash
cd quantum-control

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Qiskit and dependencies
poetry install

# Install additional quantum packages
pip install qiskit[visualization] qiskit-aer qiskit-optimization
```

#### Quantum Backend Configuration
```python
# quantum-control/config/development.py
QUANTUM_CONFIG = {
    "backend": "qiskit_aer",  # Local simulation
    "max_qubits": 32,
    "shots": 1024,
    "optimization_level": 1,
    
    "vqe": {
        "max_iterations": 100,
        "convergence_threshold": 1e-6,
        "optimizer": "SPSA"
    },
    
    "qaoa": {
        "layers": 3,
        "classical_optimizer": "COBYLA"
    },
    
    # IBM Quantum (requires token)
    "ibm_quantum": {
        "token": "your_token_here",
        "hub": "ibm-q",
        "group": "open",
        "project": "main"
    }
}
```

#### Development Server
```bash
# Start quantum control server
python -m quantum_control.server --dev

# Test quantum algorithms
python -m quantum_control.test_algorithms
```

### 3. Lifecycle Dashboard Module

#### Environment Setup
```bash
cd lifecycle-dashboard

# Install Python dependencies
poetry install

# Install additional sustainability packages
pip install lifecycle-assessment carbon-footprint
```

#### Database Setup
```bash
# Initialize PostgreSQL database
createdb qair_lifecycle_dev

# Run migrations
python manage.py migrate

# Load sample data
python manage.py loaddata fixtures/sample_lifecycle_data.json
```

#### Development Server
```bash
# Start lifecycle dashboard
python -m lifecycle_dashboard.server --dev

# Run background tasks
python -m lifecycle_dashboard.tasks --dev
```

### 4. XAI Visualizer Module

#### Environment Setup
```bash
cd xai-visualizer

# Install Node.js dependencies
npm install
# Or with Yarn
yarn install

# Install additional visualization packages
npm install d3 @types/d3 mermaid react-flow-renderer
```

#### Configuration
```json
// xai-visualizer/config/development.json
{
  "api": {
    "baseUrl": "http://localhost:8000",
    "timeout": 30000,
    "retries": 3
  },
  "visualization": {
    "mermaid": {
      "theme": "default",
      "maxTextSize": 90000
    },
    "d3": {
      "width": 800,
      "height": 600,
      "animation": true
    }
  },
  "features": {
    "realTimeUpdates": true,
    "quantumVisualization": true,
    "sustainabilityDashboard": true
  }
}
```

#### Development Server
```bash
# Start React development server
npm run dev

# Or with Yarn
yarn dev

# Run with specific port
npm run dev -- --port 3001
```

---

## 🧪 Testing Framework

### Test Architecture Overview
```mermaid
flowchart TD
    A[Unit Tests] --> D[Test Runner]
    B[Integration Tests] --> D
    C[E2E Tests] --> D
    
    D --> E[Coverage Report]
    D --> F[Performance Metrics]
    D --> G[Safety Validation]
    
    E --> H[Quality Gate]
    F --> H
    G --> H
    
    style A fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    style B fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style C fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style H fill:#ffebee,stroke:#d32f2f,stroke-width:2px
```

### Running Tests

#### Python Tests (PyTest)
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=propulsion_core --cov=quantum_control --cov=lifecycle_dashboard

# Run specific test categories
pytest -m "unit"           # Unit tests only
pytest -m "integration"    # Integration tests only
pytest -m "safety"         # Safety-critical tests only

# Run tests for specific module
pytest propulsion-core/tests/
pytest quantum-control/tests/

# Run with verbose output
pytest -v --tb=short
```

#### JavaScript Tests (Jest)
```bash
cd xai-visualizer

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test suites
npm test -- --testPathPattern=components
npm test -- --testPathPattern=utils

# Run in watch mode
npm run test:watch
```

#### Integration Tests
```bash
# Run full integration test suite
make test-integration

# Test specific integrations
pytest tests/integration/test_propulsion_quantum.py
pytest tests/integration/test_quantum_xai.py
pytest tests/integration/test_lifecycle_dashboard.py
```

### Test Configuration

#### PyTest Configuration (`pytest.ini`)
```ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra 
    --strict-markers 
    --strict-config 
    --cov=src 
    --cov-report=term-missing:skip-covered 
    --cov-report=html:htmlcov 
    --cov-report=xml
testpaths = tests
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    safety: Safety-critical tests
    quantum: Quantum computing tests
    slow: Slow running tests
```

#### Jest Configuration (`jest.config.js`)
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

---

## 🔍 Debugging and Troubleshooting

### Debug Configuration

#### Python Debugging
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Propulsion Core",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/propulsion-core/src/main.py",
      "args": ["--debug"],
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    },
    {
      "name": "Python: Quantum Control",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/quantum-control/src/main.py",
      "args": ["--debug"],
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

#### JavaScript Debugging
```json
// .vscode/launch.json (additional configuration)
{
  "name": "Launch Chrome",
  "type": "pwa-chrome",
  "request": "launch",
  "url": "http://localhost:3000",
  "webRoot": "${workspaceFolder}/xai-visualizer/src"
}
```

### Common Issues and Solutions

#### 1. Quantum Backend Connection Issues
```bash
# Test quantum backend connectivity
python -c "
from qiskit import IBMQ
try:
    IBMQ.load_account()
    print('IBM Quantum connection: OK')
except:
    print('IBM Quantum connection: Failed')
    print('Using local simulator instead')
"

# Fix: Update quantum backend configuration
export QUANTUM_BACKEND=qiskit_aer
```

#### 2. Database Connection Problems
```bash
# Check PostgreSQL status
pg_isready -h localhost -p 5432

# Reset database
dropdb qair_dev
createdb qair_dev
python manage.py migrate
```

#### 3. Docker Issues
```bash
# Clean Docker environment
docker-compose down -v
docker system prune -a

# Rebuild containers
docker-compose build --no-cache
docker-compose up
```

#### 4. Node.js Dependencies
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Debugging Tools

#### Logging Configuration
```python
# shared/logging_config.py
import logging
import sys

def setup_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/qair-debug.log')
        ]
    )
    
    # Quantum-specific logging
    qiskit_logger = logging.getLogger('qiskit')
    qiskit_logger.setLevel(logging.WARNING)
    
    # Safety-critical logging
    safety_logger = logging.getLogger('qair.safety')
    safety_logger.setLevel(logging.DEBUG)
```

#### Performance Profiling
```bash
# Profile Python code
python -m cProfile -o profile.stats main.py
python -c "
import pstats
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative').print_stats(20)
"

# Profile memory usage
pip install memory-profiler
python -m memory_profiler main.py
```

---

## ⚡ Performance Optimization

### Development Performance Tips

#### 1. Python Optimization
```python
# Use async/await for I/O operations
import asyncio
import aiohttp

async def fetch_quantum_results():
    async with aiohttp.ClientSession() as session:
        async with session.get('/api/quantum/status') as response:
            return await response.json()

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(params):
    # Expensive quantum computation
    pass
```

#### 2. React Performance
```typescript
// Use React.memo for expensive components
import React, { memo, useMemo, useCallback } from 'react';

const QuantumVisualization = memo(({ data }) => {
  const processedData = useMemo(() => {
    return expensiveDataProcessing(data);
  }, [data]);
  
  const handleUpdate = useCallback((newData) => {
    // Handle updates efficiently
  }, []);
  
  return <div>{/* Visualization */}</div>;
});
```

#### 3. Database Performance
```sql
-- Add indexes for frequent queries
CREATE INDEX idx_aircraft_emissions ON lifecycle_emissions(aircraft_id, timestamp);
CREATE INDEX idx_quantum_executions ON quantum_executions(status, created_at);

-- Optimize queries
EXPLAIN ANALYZE SELECT * FROM propulsion_metrics 
WHERE timestamp > NOW() - INTERVAL '1 hour';
```

### Build Optimization

#### Docker Multi-Stage Builds
```dockerfile
# Dockerfile.prod
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 📚 Additional Resources

### Development Scripts
```bash
# Available make commands
make help                    # Show all available commands
make setup                   # Complete development setup
make test                    # Run all tests
make test-integration        # Run integration tests
make lint                    # Run code linting
make format                  # Format code
make build                   # Build all modules
make docker-build            # Build Docker images
make docker-run              # Run with Docker
make clean                   # Clean build artifacts
```

### Useful Development Commands
```bash
# Monitor logs in real-time
tail -f logs/qair-*.log

# Watch for file changes
find . -name "*.py" | entr -r python main.py

# Monitor system resources
htop
docker stats

# Database queries
psql qair_dev -c "SELECT * FROM propulsion_metrics LIMIT 10;"
```

### Documentation Generation
```bash
# Generate Python documentation
sphinx-build -b html docs/ docs/_build/

# Generate API documentation
swagger-codegen generate -i api/openapi.yaml -l html2 -o docs/api/

# Generate type documentation
typedoc --out docs/types xai-visualizer/src/
```

### Support and Community
- **Development Chat**: [discord.gg/qair-dev](https://discord.gg/qair-dev)
- **Technical Documentation**: [docs.qair.sqa-org.org](https://docs.qair.sqa-org.org)
- **Issue Tracking**: [github.com/SQA-org/sq-aia/issues](https://github.com/SQA-org/sq-aia/issues)
- **Development Wiki**: [wiki.qair.sqa-org.org](https://wiki.qair.sqa-org.org)

---

**Setup Guide Version:** 2.1.0  
**Last Updated:** 2025-06-21  
**Next Review:** 2025-09-21  

*Happy coding! 🚀 For additional help, reach out to the development team at dev-support@sqa-org.org*
