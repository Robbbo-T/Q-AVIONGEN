"""
Enhanced Q-AVIOGEN Types with Quantum Integration
Supports seamless integration with Quantum Diagnostic Systems (QDS)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import numpy as np
from datetime import datetime

# Existing types (enhanced)
from .types_v2_1 import *

class QuantumMeasurementType(Enum):
    """Types of quantum measurements supported"""
    MAGNETIC_FIELD = "magnetic_field"
    STRAIN = "strain"
    VIBRATION = "vibration"
    TEMPERATURE = "temperature"
    ELECTROMAGNETIC = "electromagnetic"
    PRESSURE = "pressure"

class VideoGenerationPriority(Enum):
    """Video generation priority levels"""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class QuantumProcessingMode(Enum):
    """Quantum processing modes"""
    CLASSICAL = "classical"
    QUANTUM_ENHANCED = "quantum_enhanced"
    HYBRID = "hybrid"
    FULL_QUANTUM = "full_quantum"

@dataclass
class QuantumState:
    """Quantum state information from sensors"""
    coherence_time: float  # microseconds
    fidelity: float       # 0.0 to 1.0
    snr: float           # Signal-to-noise ratio
    decoherence_rate: float  # 1/seconds
    measurement_basis: str   # e.g., "Z", "X", "Y"
    entanglement_measure: Optional[float] = None
    
@dataclass
class QuantumSensorData:
    """Quantum sensor measurement data"""
    sensor_id: str
    timestamp: datetime
    measurement_type: QuantumMeasurementType
    quantum_state: QuantumState
    raw_measurement: np.ndarray
    processed_value: float
    confidence: float  # 0.0 to 1.0
    calibration_ref: str
    environmental_conditions: Dict[str, float] = field(default_factory=dict)
    
@dataclass
class QuantumEnhancement:
    """Quantum enhancement parameters for rendering"""
    optimization_algorithm: str  # "QAOA", "VQE", "QASMBO"
    optimization_parameters: Dict[str, Any] = field(default_factory=dict)
    quantum_lighting: Optional[Dict] = None
    quantum_materials: Optional[Dict] = None
    noise_reduction: float = 0.0
    coherence_boost: float = 1.0
    
@dataclass
class EnhancedSceneDefinition(SceneDefinition):
    """Extended scene definition with quantum features"""
    quantum_enhancement: Optional[QuantumEnhancement] = None
    sensor_overlays: List[Dict] = field(default_factory=list)
    real_time_data_sources: List[str] = field(default_factory=list)
    quantum_processing_mode: QuantumProcessingMode = QuantumProcessingMode.CLASSICAL
    
@dataclass
class QuantumVideoRequest:
    """Video generation request with quantum integration"""
    input_source: Union[str, Dict]  # File path or data structure
    output_config: OutputConfiguration
    quantum_context: Optional[Dict] = None
    priority: VideoGenerationPriority = VideoGenerationPriority.NORMAL
    quantum_sensors: List[str] = field(default_factory=list)
    real_time_integration: bool = False
    emergency_mode: bool = False
    predictive_maintenance: bool = False
    
    # Enhanced metadata
    aircraft_id: Optional[str] = None
    flight_phase: Optional[str] = None
    maintenance_context: Optional[Dict] = None
    
@dataclass
class QuantumVideoJob:
    """Video generation job with quantum tracking"""
    job_id: str
    request: QuantumVideoRequest
    status: str  # "QUEUED", "PROCESSING", "COMPLETED", "FAILED"
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Quantum-specific tracking
    quantum_processing_time: Optional[float] = None
    optimization_iterations: Optional[int] = None
    quantum_enhancement_score: Optional[float] = None
    
    # Output information
    output_files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_info: Optional[str] = None
    
@dataclass
class DiagnosticTrigger:
    """Trigger conditions for automated diagnostic video generation"""
    trigger_type: str  # "anomaly", "threshold", "pattern", "manual"
    sensor_data: QuantumSensorData
    threshold_values: Dict[str, float] = field(default_factory=dict)
    pattern_match: Optional[str] = None
    severity_level: int = 1  # 1-5 scale
    
@dataclass
class PredictiveMaintenanceAlert:
    """Predictive maintenance alert with video generation"""
    alert_id: str
    component_id: str
    predicted_failure_time: datetime
    confidence: float
    maintenance_procedure: str
    quantum_signatures: List[QuantumSensorData] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    
@dataclass
class QuantumOptimizationResult:
    """Results from quantum optimization algorithms"""
    algorithm_used: str
    optimization_time: float
    iterations: int
    convergence_achieved: bool
    final_energy: float
    parameter_improvements: Dict[str, float] = field(default_factory=dict)
    quantum_advantage: Optional[float] = None  # Speedup over classical
    
@dataclass
class RealTimeQuantumStream:
    """Real-time quantum data stream configuration"""
    stream_id: str
    sensor_ids: List[str]
    sampling_rate: float  # Hz
    data_format: str
    compression: Optional[str] = None
    encryption: bool = True
    
    # Stream processing
    buffer_size: int = 1000
    processing_pipeline: List[str] = field(default_factory=list)
    anomaly_detection: bool = True
    
@dataclass
class QuantumVisualizationConfig:
    """Configuration for quantum-enhanced visualizations"""
    show_sensor_positions: bool = True
    show_field_lines: bool = False
    show_quantum_states: bool = False
    color_by_confidence: bool = True
    transparency_by_coherence: bool = True
    
    # Animation parameters
    animate_quantum_evolution: bool = False
    animation_speed: float = 1.0
    show_decoherence: bool = False
    
@dataclass
class QuantumSystemHealth:
    """Overall quantum system health status"""
    overall_status: str  # "HEALTHY", "DEGRADED", "CRITICAL", "OFFLINE"
    active_sensors: int
    total_sensors: int
    average_coherence: float
    average_confidence: float
    
    # Performance metrics
    data_processing_rate: float  # samples/second
    quantum_algorithm_efficiency: float
    error_rate: float
    
    # Alerts and warnings
    active_alerts: List[str] = field(default_factory=list)
    pending_maintenance: List[str] = field(default_factory=list)

# Quantum-enhanced error types
class QuantumIntegrationError(Exception):
    """Base exception for quantum integration errors"""
    pass

class QuantumSensorError(QuantumIntegrationError):
    """Quantum sensor specific errors"""
    def __init__(self, sensor_id: str, message: str):
        self.sensor_id = sensor_id
        super().__init__(f"Sensor {sensor_id}: {message}")

class QuantumOptimizationError(QuantumIntegrationError):
    """Quantum optimization specific errors"""
    def __init__(self, algorithm: str, message: str):
        self.algorithm = algorithm
        super().__init__(f"Optimization {algorithm}: {message}")

class QuantumStreamError(QuantumIntegrationError):
    """Real-time quantum stream errors"""
    def __init__(self, stream_id: str, message: str):
        self.stream_id = stream_id
        super().__init__(f"Stream {stream_id}: {message}")

# Utility functions for quantum data handling
def validate_quantum_state(quantum_state: QuantumState) -> bool:
    """Validate quantum state parameters"""
    if quantum_state.coherence_time <= 0:
        return False
    if not 0 <= quantum_state.fidelity <= 1:
        return False
    if quantum_state.snr < 0:
        return False
    return True

def calculate_quantum_confidence(sensor_data: QuantumSensorData) -> float:
    """Calculate overall confidence from quantum measurements"""
    quantum_confidence = (
        sensor_data.quantum_state.fidelity * 0.4 +
        min(sensor_data.quantum_state.snr / 10.0, 1.0) * 0.3 +
        min(sensor_data.quantum_state.coherence_time / 1e-6, 1.0) * 0.3
    )
    return min(quantum_confidence, 1.0)

def merge_quantum_contexts(contexts: List[Dict]) -> Dict:
    """Merge multiple quantum contexts into unified context"""
    merged = {
        'sensors': [],
        'measurements': [],
        'optimization_params': {},
        'environmental_conditions': {}
    }
    
    for context in contexts:
        if 'sensors' in context:
            merged['sensors'].extend(context['sensors'])
        if 'measurements' in context:
            merged['measurements'].extend(context['measurements'])
        if 'optimization_params' in context:
            merged['optimization_params'].update(context['optimization_params'])
        if 'environmental_conditions' in context:
            merged['environmental_conditions'].update(context['environmental_conditions'])
    
    return merged
