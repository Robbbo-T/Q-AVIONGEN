# Q-AIR API Documentation
## Quantum-Aerospace Intelligent Assistant REST API

**API Version:** 2.1.0  
**Last Updated:** 2025-06-21  
**Base URL:** `https://api.qair.sqa-org.org/v2`  

---

## 📋 Table of Contents
- [Authentication](#authentication)
- [Core Endpoints](#core-endpoints)
- [Propulsion Control API](#propulsion-control-api)
- [Quantum Computing API](#quantum-computing-api)
- [Lifecycle Management API](#lifecycle-management-api)
- [XAI Visualization API](#xai-visualization-api)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [SDK Examples](#sdk-examples)

---

## 🔐 Authentication

### Bearer Token Authentication
All API requests require authentication using Bearer tokens in the Authorization header.

```http
Authorization: Bearer <your-api-token>
Content-Type: application/json
```

### Obtaining API Tokens
```bash
curl -X POST https://api.qair.sqa-org.org/v2/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your-username",
    "password": "your-password",
    "scope": "qair:read qair:write qair:admin"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "qair:read qair:write"
}
```

---

## 🔧 Core Endpoints

### System Health Check
Check the overall health and status of the Q-AIR system.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-21T10:30:00Z",
  "version": "2.1.0",
  "services": {
    "propulsion-core": "healthy",
    "quantum-control": "healthy",
    "lifecycle-dashboard": "healthy",
    "xai-visualizer": "healthy"
  },
  "performance": {
    "response_time_ms": 45,
    "cpu_usage": 23.5,
    "memory_usage": 67.2
  }
}
```

### System Configuration
Retrieve current system configuration and capabilities.

```http
GET /config
```

**Response:**
```json
{
  "propulsion": {
    "h2_storage_pressure": 700,
    "ht_pem_operating_temp": 180,
    "safety_factor": 2.5
  },
  "quantum": {
    "backend": "qiskit_aer",
    "max_qubits": 32,
    "vqe_iterations": 100,
    "qaoa_layers": 3
  },
  "sustainability": {
    "target_co2_reduction": 88,
    "recyclability_target": 90
  }
}
```

---

## ⚡ Propulsion Control API

### Hydrogen Storage System

#### Get Storage Status
```http
GET /propulsion/storage/status
```

**Response:**
```json
{
  "storage_id": "h2-tank-001",
  "pressure": 695.5,
  "temperature": 22.3,
  "fill_level": 87.2,
  "safety_status": "normal",
  "last_inspection": "2025-06-20T08:00:00Z",
  "next_maintenance": "2025-07-20T08:00:00Z"
}
```

#### Update Storage Parameters
```http
PATCH /propulsion/storage/{storage_id}
Content-Type: application/json

{
  "target_pressure": 700,
  "temperature_setpoint": 20,
  "safety_mode": "enhanced"
}
```

### Fuel Cell Management

#### HT-PEM Fuel Cell Status
```http
GET /propulsion/fuelcell/status
```

**Response:**
```json
{
  "cell_id": "htpem-stack-001",
  "operating_temperature": 185.2,
  "power_output": 2.47,
  "efficiency": 0.63,
  "stack_voltage": 48.6,
  "current_density": 0.52,
  "co_tolerance": 0.035,
  "status": "optimal",
  "performance_metrics": {
    "power_density_kw_kg": 2.47,
    "thermal_efficiency": 0.63,
    "electrical_efficiency": 0.58
  }
}
```

#### Optimize Fuel Cell Performance
```http
POST /propulsion/fuelcell/optimize
Content-Type: application/json

{
  "optimization_target": "efficiency",
  "constraints": {
    "max_temperature": 200,
    "min_power_output": 2.0,
    "safety_margin": 0.2
  },
  "algorithm": "quantum_vqe"
}
```

**Response:**
```json
{
  "optimization_id": "opt-2025-06-21-001",
  "status": "completed",
  "execution_time_ms": 4850,
  "results": {
    "optimal_temperature": 188.5,
    "optimal_pressure": 1.8,
    "predicted_efficiency": 0.66,
    "improvement_percentage": 4.8
  },
  "quantum_metrics": {
    "algorithm_used": "VQE",
    "iterations": 85,
    "convergence_achieved": true
  }
}
```

### Safety Monitoring

#### Real-time Safety Status
```http
GET /propulsion/safety/status
```

**Response:**
```json
{
  "overall_status": "safe",
  "risk_level": "low",
  "active_monitors": [
    {
      "monitor_id": "pressure-sensor-001",
      "parameter": "h2_pressure",
      "current_value": 695.5,
      "threshold_warning": 720,
      "threshold_critical": 750,
      "status": "normal"
    },
    {
      "monitor_id": "temp-sensor-002",
      "parameter": "storage_temperature",
      "current_value": 22.3,
      "threshold_warning": 30,
      "threshold_critical": 35,
      "status": "normal"
    }
  ],
  "emergency_protocols": {
    "auto_shutdown_enabled": true,
    "emergency_venting": "ready",
    "fire_suppression": "armed"
  }
}
```

---

## ⚛️ Quantum Computing API

### Algorithm Execution

#### Execute VQE Algorithm
```http
POST /quantum/vqe/execute
Content-Type: application/json

{
  "problem_type": "molecular_optimization",
  "molecule": {
    "formula": "H2O2",
    "basis_set": "sto-3g"
  },
  "parameters": {
    "max_iterations": 100,
    "convergence_threshold": 1e-6,
    "optimizer": "SPSA"
  },
  "quantum_backend": "qiskit_aer"
}
```

**Response:**
```json
{
  "execution_id": "vqe-2025-06-21-001",
  "status": "completed",
  "algorithm": "VQE",
  "execution_time_ms": 12500,
  "results": {
    "ground_state_energy": -75.0129,
    "optimal_parameters": [0.785, 1.23, -0.456, 2.11],
    "iterations_to_convergence": 78,
    "final_cost": 1.2e-7
  },
  "quantum_metrics": {
    "qubits_used": 12,
    "circuit_depth": 45,
    "gate_count": 234,
    "fidelity": 0.987
  }
}
```

#### Execute QAOA Algorithm
```http
POST /quantum/qaoa/execute
Content-Type: application/json

{
  "problem_type": "route_optimization",
  "graph": {
    "nodes": 8,
    "edges": [
      {"from": 0, "to": 1, "weight": 2.5},
      {"from": 1, "to": 2, "weight": 3.1},
      {"from": 2, "to": 3, "weight": 1.8}
    ]
  },
  "parameters": {
    "layers": 3,
    "shots": 1024
  }
}
```

**Response:**
```json
{
  "execution_id": "qaoa-2025-06-21-002",
  "status": "completed",
  "algorithm": "QAOA",
  "execution_time_ms": 8750,
  "results": {
    "optimal_route": [0, 1, 3, 2, 4, 7, 6, 5],
    "total_distance": 15.7,
    "optimization_ratio": 0.92,
    "solution_probability": 0.73
  },
  "quantum_metrics": {
    "qubits_used": 8,
    "circuit_depth": 21,
    "measurement_counts": {
      "00110110": 247,
      "01101100": 198,
      "10011001": 156
    }
  }
}
```

### Quantum Sensing

#### NV-Center Magnetometry
```http
GET /quantum/sensing/magnetometry
```

**Response:**
```json
{
  "sensor_id": "nv-mag-001",
  "measurement_timestamp": "2025-06-21T10:45:32Z",
  "magnetic_field": {
    "magnitude_nt": 125.7,
    "direction": {
      "x": 45.2,
      "y": -12.8,
      "z": 87.3
    },
    "uncertainty_nt": 0.8
  },
  "sensor_performance": {
    "sensitivity_pt_sqrt_hz": 95,
    "coherence_time_ms": 2.3,
    "temperature_c": 25.1
  }
}
```

### Algorithm Status

#### List Running Algorithms
```http
GET /quantum/algorithms/status
```

**Response:**
```json
{
  "active_algorithms": [
    {
      "execution_id": "vqe-2025-06-21-003",
      "algorithm": "VQE",
      "status": "running",
      "progress": 65,
      "estimated_completion": "2025-06-21T10:55:00Z"
    }
  ],
  "queue": [
    {
      "execution_id": "qaoa-2025-06-21-004",
      "algorithm": "QAOA",
      "status": "queued",
      "priority": "high",
      "estimated_start": "2025-06-21T10:52:00Z"
    }
  ],
  "resource_usage": {
    "qubits_allocated": 20,
    "qubits_available": 32,
    "cpu_usage": 78.5,
    "memory_usage": 45.2
  }
}
```

---

## 🌱 Lifecycle Management API

### Carbon Footprint Tracking

#### Get Lifecycle Emissions
```http
GET /lifecycle/emissions/{aircraft_id}
```

**Response:**
```json
{
  "aircraft_id": "qair-001",
  "lifecycle_phase": "operation",
  "emissions": {
    "design_phase_kg_co2": 12500,
    "manufacturing_kg_co2": 85000,
    "operation_kg_co2": 0,
    "maintenance_kg_co2": 2500,
    "end_of_life_kg_co2": -5000,
    "total_lifecycle_kg_co2": 95000
  },
  "comparison": {
    "conventional_aircraft_kg_co2": 785000,
    "reduction_percentage": 87.9
  },
  "tracking_period": {
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-06-21T10:45:32Z"
  }
}
```

#### Update Material Recovery Data
```http
POST /lifecycle/materials/recovery
Content-Type: application/json

{
  "aircraft_id": "qair-001",
  "component_id": "wing-section-001",
  "material_type": "carbon_fiber",
  "recovery_method": "chemical_recycling",
  "recovered_mass_kg": 125.5,
  "recovery_efficiency": 0.89,
  "new_application": "fuselage_panel"
}
```

### Sustainability Metrics

#### Circular Economy Dashboard
```http
GET /lifecycle/sustainability/dashboard
```

**Response:**
```json
{
  "overall_metrics": {
    "co2_reduction_target": 88,
    "co2_reduction_achieved": 87.9,
    "recyclability_target": 90,
    "recyclability_achieved": 87.3,
    "sustainable_materials_percentage": 76.8
  },
  "material_flows": {
    "aluminum": {
      "used_kg": 1250,
      "recycled_kg": 1125,
      "recycling_rate": 0.90
    },
    "carbon_fiber": {
      "used_kg": 890,
      "recycled_kg": 756,
      "recycling_rate": 0.85
    },
    "titanium": {
      "used_kg": 345,
      "recycled_kg": 310,
      "recycling_rate": 0.90
    }
  },
  "compliance_status": {
    "icao_ltag": "compliant",
    "eu_green_deal": "compliant",
    "carbon_neutral_2050": "on_track"
  }
}
```

---

## 🎯 XAI Visualization API

### Explanation Generation

#### Generate System Explanation
```http
POST /xai/explain
Content-Type: application/json

{
  "component": "propulsion_optimization",
  "decision_id": "opt-2025-06-21-001",
  "explanation_type": "technical",
  "target_audience": "engineer"
}
```

**Response:**
```json
{
  "explanation_id": "exp-2025-06-21-001",
  "component": "propulsion_optimization",
  "decision": {
    "description": "Fuel cell temperature optimization",
    "input_parameters": {
      "current_temperature": 185.2,
      "target_efficiency": 0.65,
      "safety_constraints": ["max_temp_200C", "min_power_2kW"]
    },
    "output_recommendation": {
      "optimal_temperature": 188.5,
      "predicted_efficiency": 0.66,
      "confidence": 0.94
    }
  },
  "explanation": {
    "reasoning": "The VQE algorithm identified that increasing temperature to 188.5°C optimizes the proton exchange membrane conductivity while maintaining safety margins. This temperature maximizes the trade-off between ionic conductivity and thermal stability.",
    "key_factors": [
      {
        "factor": "membrane_conductivity",
        "impact": 0.78,
        "direction": "positive"
      },
      {
        "factor": "thermal_stability",
        "impact": 0.65,
        "direction": "neutral"
      },
      {
        "factor": "safety_margin",
        "impact": 0.91,
        "direction": "positive"
      }
    ],
    "visualization_data": {
      "mermaid_diagram": "flowchart TD\n    A[Temperature Input] --> B[Membrane Analysis]\n    B --> C[Efficiency Calculation]\n    C --> D[Safety Check]\n    D --> E[Optimal Temperature]",
      "performance_charts": {
        "temperature_vs_efficiency": [
          {"temp": 180, "efficiency": 0.62},
          {"temp": 185, "efficiency": 0.63},
          {"temp": 188.5, "efficiency": 0.66},
          {"temp": 195, "efficiency": 0.64},
          {"temp": 200, "efficiency": 0.62}
        ]
      }
    }
  }
}
```

### Dashboard Data

#### Real-time Dashboard Metrics
```http
GET /xai/dashboard/realtime
```

**Response:**
```json
{
  "timestamp": "2025-06-21T10:45:32Z",
  "system_overview": {
    "status": "optimal",
    "efficiency": 0.63,
    "safety_score": 0.98,
    "sustainability_index": 0.87
  },
  "key_metrics": [
    {
      "metric": "fuel_cell_efficiency",
      "value": 0.63,
      "unit": "ratio",
      "trend": "increasing",
      "target": 0.65
    },
    {
      "metric": "h2_consumption_rate",
      "value": 2.34,
      "unit": "kg/hour",
      "trend": "stable",
      "target": 2.50
    },
    {
      "metric": "co2_emissions",
      "value": 0,
      "unit": "kg/hour",
      "trend": "stable",
      "target": 0
    }
  ],
  "alerts": [],
  "recommendations": [
    {
      "id": "rec-001",
      "type": "optimization",
      "priority": "medium",
      "description": "Consider increasing fuel cell temperature by 3.3°C for 4.8% efficiency improvement",
      "estimated_benefit": "0.03 efficiency gain"
    }
  ]
}
```

### Visualization Assets

#### Generate Mermaid Diagram
```http
POST /xai/visualize/mermaid
Content-Type: application/json

{
  "diagram_type": "flowchart",
  "data_source": "propulsion_flow",
  "style": "technical",
  "include_metrics": true
}
```

**Response:**
```json
{
  "diagram_id": "mermaid-2025-06-21-001",
  "diagram_code": "flowchart TD\n    A[H₂ Storage<br/>695.5 bar] --> B[Pressure Regulator]\n    B --> C[HT-PEM Fuel Cell<br/>185.2°C]\n    C --> D[Power Output<br/>2.47 kW]\n    D --> E[Propulsion System]\n    \n    F[Safety Monitor] --> A\n    F --> B\n    F --> C\n    \n    style A fill:#e1f5fe\n    style C fill:#f3e5f5\n    style F fill:#ffebee",
  "metadata": {
    "created_at": "2025-06-21T10:45:32Z",
    "data_timestamp": "2025-06-21T10:45:30Z",
    "auto_refresh": true,
    "refresh_interval_ms": 5000
  }
}
```

---

## ❌ Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "The specified temperature exceeds safety limits",
    "details": {
      "parameter": "operating_temperature",
      "provided_value": 250,
      "max_allowed": 200,
      "safety_margin": 20
    },
    "timestamp": "2025-06-21T10:45:32Z",
    "request_id": "req-2025-06-21-001"
  },
  "suggestions": [
    "Reduce temperature to within safe operating range (160-200°C)",
    "Contact safety team if higher temperatures are required"
  ]
}
```

### Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `AUTHENTICATION_FAILED` | Invalid or expired token | 401 |
| `INSUFFICIENT_PERMISSIONS` | Missing required scope | 403 |
| `INVALID_PARAMETER` | Parameter validation failed | 400 |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist | 404 |
| `SAFETY_CONSTRAINT_VIOLATION` | Operation violates safety limits | 422 |
| `QUANTUM_BACKEND_UNAVAILABLE` | Quantum computing resources unavailable | 503 |
| `OPTIMIZATION_TIMEOUT` | Algorithm execution exceeded time limit | 408 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |

---

## 🚦 Rate Limiting

### Rate Limit Headers
All API responses include rate limiting information:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-RateLimit-Window: 3600
```

### Rate Limits by Endpoint Category

| Category | Limit | Window |
|----------|-------|--------|
| Authentication | 10 requests | 15 minutes |
| Read Operations | 1000 requests | 1 hour |
| Write Operations | 100 requests | 1 hour |
| Quantum Execution | 10 requests | 1 hour |
| Safety Critical | 50 requests | 1 hour |

---

## 🛠️ SDK Examples

### Python SDK
```python
from qair_sdk import QAIRClient

# Initialize client
client = QAIRClient(
    base_url="https://api.qair.sqa-org.org/v2",
    api_token="your-api-token"
)

# Execute quantum optimization
result = client.quantum.vqe.execute(
    problem_type="molecular_optimization",
    molecule={"formula": "H2O2", "basis_set": "sto-3g"},
    max_iterations=100
)

print(f"Ground state energy: {result.ground_state_energy}")
print(f"Optimization completed in {result.execution_time_ms}ms")

# Monitor propulsion system
status = client.propulsion.get_status()
print(f"Fuel cell efficiency: {status.fuel_cell.efficiency}")
print(f"Safety status: {status.safety.overall_status}")

# Generate explanation
explanation = client.xai.explain(
    component="propulsion_optimization",
    decision_id=result.execution_id,
    explanation_type="technical"
)

print(f"Explanation: {explanation.reasoning}")
```

### JavaScript SDK
```javascript
import { QAIRClient } from '@qair/sdk';

// Initialize client
const client = new QAIRClient({
  baseURL: 'https://api.qair.sqa-org.org/v2',
  apiToken: 'your-api-token'
});

// Execute QAOA optimization
const result = await client.quantum.qaoa.execute({
  problemType: 'route_optimization',
  graph: {
    nodes: 8,
    edges: [
      { from: 0, to: 1, weight: 2.5 },
      { from: 1, to: 2, weight: 3.1 }
    ]
  },
  parameters: { layers: 3, shots: 1024 }
});

console.log(`Optimal route: ${result.optimal_route}`);
console.log(`Total distance: ${result.total_distance}`);

// Real-time dashboard updates
const dashboard = client.xai.dashboard.subscribe();
dashboard.on('update', (metrics) => {
  console.log(`System efficiency: ${metrics.system_overview.efficiency}`);
  console.log(`Safety score: ${metrics.system_overview.safety_score}`);
});
```

### cURL Examples
```bash
# Get system health
curl -X GET https://api.qair.sqa-org.org/v2/health \
  -H "Authorization: Bearer YOUR_TOKEN"

# Execute VQE optimization
curl -X POST https://api.qair.sqa-org.org/v2/quantum/vqe/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "molecular_optimization",
    "molecule": {"formula": "H2", "basis_set": "sto-3g"},
    "parameters": {"max_iterations": 50}
  }'

# Get propulsion status
curl -X GET https://api.qair.sqa-org.org/v2/propulsion/fuelcell/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📚 Additional Resources

### OpenAPI Specification
- **Full OpenAPI 3.0 spec**: [api.qair.sqa-org.org/v2/openapi.json](https://api.qair.sqa-org.org/v2/openapi.json)
- **Interactive documentation**: [docs.qair.sqa-org.org/api](https://docs.qair.sqa-org.org/api)

### SDKs and Libraries
- **Python SDK**: [github.com/SQA-org/qair-python-sdk](https://github.com/SQA-org/qair-python-sdk)
- **JavaScript SDK**: [github.com/SQA-org/qair-js-sdk](https://github.com/SQA-org/qair-js-sdk)
- **Go SDK**: [github.com/SQA-org/qair-go-sdk](https://github.com/SQA-org/qair-go-sdk)

### Support
- **API Support**: [api-support@sqa-org.org](mailto:api-support@sqa-org.org)
- **Technical Documentation**: [docs.qair.sqa-org.org](https://docs.qair.sqa-org.org)
- **Community Forum**: [community.qair.sqa-org.org](https://community.qair.sqa-org.org)

---

**API Version:** 2.1.0  
**Last Updated:** 2025-06-21  
**Next Review:** 2025-09-21  

*This API documentation is continuously updated. For the latest changes, see our [changelog](https://docs.qair.sqa-org.org/api/changelog).*
