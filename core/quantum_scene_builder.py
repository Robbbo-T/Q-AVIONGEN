"""
Quantum-Enhanced Scene Builder for Q-AVIOGEN
Integrates quantum sensor data into 3D scene generation
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import colorsys
import math

# Import base scene builder
from parser.scene_builder import SceneBuilder
from core.types_v2_1 import SceneDefinition
from core.quantum_types import (
    EnhancedSceneDefinition, QuantumEnhancement, QuantumSensorData,
    QuantumProcessingMode, QuantumVisualizationConfig
)
from core.quantum_processor import QuantumDataProcessor

class QuantumSceneBuilder(SceneBuilder):
    """Enhanced scene builder with quantum sensor integration"""
    
    def __init__(self):
        super().__init__()
        self.quantum_processor = QuantumDataProcessor()
        self.logger = logging.getLogger(__name__)
        
        # Quantum visualization settings
        self.visualization_config = QuantumVisualizationConfig()
        
        # Sensor visualization parameters
        self.sensor_visualization = {
            'magnetic_field': {
                'color_map': 'plasma',
                'scale_factor': 1e6,  # Convert Tesla to microTesla for visualization
                'glyph_type': 'arrow',
                'size_range': (0.1, 2.0)
            },
            'strain': {
                'color_map': 'viridis',
                'scale_factor': 1e6,  # Convert to microstrain
                'glyph_type': 'tensor_ellipsoid',
                'size_range': (0.1, 1.5)
            },
            'vibration': {
                'color_map': 'hot',
                'scale_factor': 1.0,  # g-force already readable
                'glyph_type': 'sphere',
                'size_range': (0.05, 1.0)
            },
            'electromagnetic': {
                'color_map': 'cool',
                'scale_factor': 1.0,  # dB scale
                'glyph_type': 'wireframe_sphere',
                'size_range': (0.2, 3.0)
            }
        }
    
    def build_quantum_enhanced_scene(self, 
                                   procedure_data: dict, 
                                   quantum_context: dict) -> EnhancedSceneDefinition:
        """Build scene with quantum sensor data integration"""
        
        self.logger.info("Building quantum-enhanced scene")
        
        # Build base scene from procedure
        base_scene = self.build_scene(procedure_data)
        
        # Extract quantum sensor data
        sensor_data = self._extract_sensor_data(quantum_context)
        
        # Quantum optimization of scene parameters
        optimization_result = self._optimize_scene_with_quantum_data(
            base_scene, sensor_data
        )
        
        # Generate quantum enhancement parameters
        quantum_enhancement = self._create_quantum_enhancement(
            sensor_data, optimization_result
        )
        
        # Create sensor visualization overlays
        sensor_overlays = self._generate_sensor_overlays(sensor_data)
        
        # Apply quantum-enhanced lighting
        enhanced_lighting = self._apply_quantum_lighting(sensor_data)
        quantum_enhancement.quantum_lighting = enhanced_lighting
        
        # Apply quantum-enhanced materials
        enhanced_materials = self._apply_quantum_materials(sensor_data)
        quantum_enhancement.quantum_materials = enhanced_materials
        
        # Determine real-time data sources
        real_time_sources = [sensor['sensor_id'] for sensor in sensor_data]
        
        return EnhancedSceneDefinition(
            # Base scene properties
            **base_scene.__dict__,
            
            # Quantum enhancements
            quantum_enhancement=quantum_enhancement,
            sensor_overlays=sensor_overlays,
            real_time_data_sources=real_time_sources,
            quantum_processing_mode=QuantumProcessingMode.QUANTUM_ENHANCED
        )
    
    def _extract_sensor_data(self, quantum_context: dict) -> List[Dict]:
        """Extract and process quantum sensor data from context"""
        
        sensor_data = []
        
        # Process sensor measurements from context
        sensors_info = quantum_context.get('sensor_data', {})
        
        for sensor_id, sensor_info in sensors_info.items():
            # Create sensor data structure
            sensor_record = {
                'sensor_id': sensor_id,
                'measurement_type': sensor_info.get('measurement_type', 'unknown'),
                'processed_value': sensor_info.get('processed_value', 0.0),
                'confidence': sensor_info.get('confidence', 0.0),
                'quantum_state': sensor_info.get('quantum_state', {}),
                'location': self._get_sensor_location(sensor_id, quantum_context),
                'visualization_params': self._get_sensor_visualization_params(
                    sensor_info.get('measurement_type', 'unknown')
                )
            }
            
            sensor_data.append(sensor_record)
        
        self.logger.info(f"Extracted data from {len(sensor_data)} quantum sensors")
        return sensor_data
    
    def _get_sensor_location(self, sensor_id: str, quantum_context: dict) -> Dict:
        """Get 3D location of sensor for visualization"""
        
        # Try to get from configuration
        sensors_config = quantum_context.get('sensors', [])
        
        for sensor in sensors_config:
            if sensor.get('id') == sensor_id:
                location = sensor.get('location', {})
                coordinates = location.get('coordinates', {})
                
                return {
                    'x': coordinates.get('x', 0.0),
                    'y': coordinates.get('y', 0.0),
                    'z': coordinates.get('z', 0.0),
                    'section': location.get('aircraft_section', 'unknown')
                }
        
        # Default location if not found
        return {'x': 0.0, 'y': 0.0, 'z': 0.0, 'section': 'unknown'}
    
    def _get_sensor_visualization_params(self, measurement_type: str) -> Dict:
        """Get visualization parameters for sensor type"""
        
        return self.sensor_visualization.get(
            measurement_type, 
            self.sensor_visualization['magnetic_field']  # Default
        )
    
    def _optimize_scene_with_quantum_data(self, base_scene: SceneDefinition, 
                                        sensor_data: List[Dict]) -> Dict:
        """Optimize scene parameters using quantum sensor data"""
        
        # Extract scene parameters for optimization
        scene_params = {
            'lighting_intensity': getattr(base_scene, 'lighting_intensity', 1.0),
            'material_roughness': getattr(base_scene, 'material_roughness', 0.5),
            'camera_position': getattr(base_scene, 'camera_position', [0, 0, 5]),
            'render_quality': getattr(base_scene, 'render_quality', 0.8),
            'animation_speed': getattr(base_scene, 'animation_speed', 1.0)
        }
        
        # Create quantum state summary for optimization
        quantum_state = self._create_quantum_state_summary(sensor_data)
        
        # Use quantum processor for optimization
        optimization_result = self.quantum_processor.optimize_rendering_parameters(
            scene_params, quantum_state
        )
        
        self.logger.info(f"Quantum optimization completed: {optimization_result.algorithm_used}")
        
        return optimization_result.parameter_improvements
    
    def _create_quantum_state_summary(self, sensor_data: List[Dict]) -> Dict:
        """Create summary of quantum state for optimization"""
        
        if not sensor_data:
            return {'system_health': {'avg_confidence': 0.5, 'avg_coherence': 1e-6}}
        
        # Calculate average metrics
        total_confidence = sum(s.get('confidence', 0.0) for s in sensor_data)
        avg_confidence = total_confidence / len(sensor_data)
        
        # Extract coherence times
        coherence_times = []
        for sensor in sensor_data:
            quantum_state = sensor.get('quantum_state', {})
            coherence_time = quantum_state.get('coherence_time', 1e-6)
            coherence_times.append(coherence_time)
        
        avg_coherence = np.mean(coherence_times) if coherence_times else 1e-6
        
        return {
            'system_health': {
                'avg_confidence': avg_confidence,
                'avg_coherence': avg_coherence,
                'active_sensors': len(sensor_data)
            },
            'sensor_data': {
                'confidence': avg_confidence,
                'field_strength': np.mean([s.get('processed_value', 0.0) for s in sensor_data])
            }
        }
    
    def _create_quantum_enhancement(self, sensor_data: List[Dict], 
                                  optimization_result: Dict) -> QuantumEnhancement:
        """Create quantum enhancement parameters"""
        
        # Determine optimization algorithm based on availability and performance
        algorithm = "QAOA" if optimization_result.get('quantum_advantage') else "classical_annealing"
        
        # Extract optimization parameters
        optimization_params = {
            'convergence_threshold': 1e-6,
            'max_iterations': 200,
            'noise_mitigation': True,
            'error_correction': False  # Not needed for NISQ algorithms
        }
        
        # Calculate noise reduction based on sensor confidence
        avg_confidence = np.mean([s.get('confidence', 0.0) for s in sensor_data])
        noise_reduction = 1.0 - avg_confidence
        
        # Calculate coherence boost
        coherence_times = []
        for sensor in sensor_data:
            quantum_state = sensor.get('quantum_state', {})
            coherence_times.append(quantum_state.get('coherence_time', 1e-6))
        
        avg_coherence = np.mean(coherence_times) if coherence_times else 1e-6
        coherence_boost = min(avg_coherence / 1e-6, 2.0)  # Cap at 2x boost
        
        return QuantumEnhancement(
            optimization_algorithm=algorithm,
            optimization_parameters=optimization_params,
            noise_reduction=noise_reduction,
            coherence_boost=coherence_boost
        )
    
    def _generate_sensor_overlays(self, sensor_data: List[Dict]) -> List[Dict]:
        """Generate 3D visualization overlays for quantum sensors"""
        
        overlays = []
        
        for sensor in sensor_data:
            location = sensor.get('location', {})
            measurement_type = sensor.get('measurement_type', 'unknown')
            processed_value = sensor.get('processed_value', 0.0)
            confidence = sensor.get('confidence', 0.0)
            viz_params = sensor.get('visualization_params', {})
            
            # Create sensor visualization overlay
            overlay = {
                'type': 'quantum_sensor',
                'sensor_id': sensor.get('sensor_id', 'unknown'),
                'position': [
                    location.get('x', 0.0),
                    location.get('y', 0.0),
                    location.get('z', 0.0)
                ],
                'measurement_type': measurement_type,
                'value': processed_value,
                'confidence': confidence,
                'visualization': self._create_sensor_visualization(
                    measurement_type, processed_value, confidence, viz_params
                )
            }
            
            overlays.append(overlay)
        
        self.logger.info(f"Generated {len(overlays)} sensor overlays")
        return overlays
    
    def _create_sensor_visualization(self, measurement_type: str, value: float, 
                                   confidence: float, viz_params: Dict) -> Dict:
        """Create visualization parameters for a specific sensor"""
        
        # Get visualization parameters
        color_map = viz_params.get('color_map', 'plasma')
        scale_factor = viz_params.get('scale_factor', 1.0)
        glyph_type = viz_params.get('glyph_type', 'sphere')
        size_range = viz_params.get('size_range', (0.1, 1.0))
        
        # Scale value for visualization
        scaled_value = abs(value) * scale_factor
        
        # Calculate size based on value magnitude
        size = self._map_value_to_size(scaled_value, size_range)
        
        # Calculate color based on value and confidence
        color = self._calculate_sensor_color(scaled_value, confidence, color_map)
        
        # Calculate transparency based on confidence
        alpha = 0.3 + 0.7 * confidence  # Range from 0.3 to 1.0
        
        return {
            'glyph_type': glyph_type,
            'size': size,
            'color': color,
            'alpha': alpha,
            'wireframe': confidence < 0.7,  # Show wireframe for low confidence
            'animation': {
                'pulse': measurement_type == 'vibration',
                'rotate': measurement_type == 'electromagnetic',
                'oscillate': measurement_type == 'magnetic_field'
            }
        }
    
    def _map_value_to_size(self, value: float, size_range: Tuple[float, float]) -> float:
        """Map sensor value to visualization size"""
        
        min_size, max_size = size_range
        
        # Log scale for large dynamic ranges
        if value > 0:
            log_value = math.log10(value + 1)
            normalized = min(log_value / 3.0, 1.0)  # Assume 3 orders of magnitude
        else:
            normalized = 0.0
        
        return min_size + normalized * (max_size - min_size)
    
    def _calculate_sensor_color(self, value: float, confidence: float, 
                              color_map: str) -> List[float]:
        """Calculate color for sensor visualization"""
        
        # Color maps
        color_maps = {
            'plasma': [(0.05, 0.03, 0.53), (0.9, 0.2, 0.3), (0.98, 0.98, 0.05)],
            'viridis': [(0.26, 0.0, 0.33), (0.13, 0.57, 0.55), (0.99, 0.91, 0.14)],
            'hot': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 1.0, 1.0)],
            'cool': [(0.0, 1.0, 1.0), (0.5, 0.5, 1.0), (1.0, 0.0, 1.0)]
        }
        
        # Get color map
        cmap = color_maps.get(color_map, color_maps['plasma'])
        
        # Normalize value for color mapping
        if value > 0:
            normalized_value = min(math.log10(value + 1) / 3.0, 1.0)
        else:
            normalized_value = 0.0
        
        # Interpolate color
        if len(cmap) == 3:
            # Three-color interpolation
            if normalized_value < 0.5:
                t = normalized_value * 2
                color = self._interpolate_color(cmap[0], cmap[1], t)
            else:
                t = (normalized_value - 0.5) * 2
                color = self._interpolate_color(cmap[1], cmap[2], t)
        else:
            # Multi-color interpolation
            segment = normalized_value * (len(cmap) - 1)
            idx = int(segment)
            t = segment - idx
            
            if idx >= len(cmap) - 1:
                color = cmap[-1]
            else:
                color = self._interpolate_color(cmap[idx], cmap[idx + 1], t)
        
        # Modulate with confidence
        confidence_factor = 0.5 + 0.5 * confidence
        color = [c * confidence_factor for c in color]
        
        return color
    
    def _interpolate_color(self, color1: Tuple[float, float, float], 
                          color2: Tuple[float, float, float], t: float) -> List[float]:
        """Interpolate between two colors"""
        
        return [
            color1[0] + t * (color2[0] - color1[0]),
            color1[1] + t * (color2[1] - color1[1]),
            color1[2] + t * (color2[2] - color1[2])
        ]
    
    def _apply_quantum_lighting(self, sensor_data: List[Dict]) -> Dict:
        """Apply quantum-enhanced lighting based on sensor data"""
        
        if not sensor_data:
            return {'type': 'standard'}
        
        # Calculate average field strengths for different measurement types
        field_strengths = {}
        for sensor in sensor_data:
            mtype = sensor.get('measurement_type', 'unknown')
            value = abs(sensor.get('processed_value', 0.0))
            
            if mtype not in field_strengths:
                field_strengths[mtype] = []
            field_strengths[mtype].append(value)
        
        # Average field strengths
        avg_fields = {k: np.mean(v) for k, v in field_strengths.items()}
        
        # Quantum-enhanced lighting parameters
        lighting = {
            'type': 'quantum_enhanced',
            'ambient_intensity': 0.3 + 0.2 * avg_fields.get('electromagnetic', 0.0),
            'directional_lights': []
        }
        
        # Add lights based on magnetic field measurements
        mag_strength = avg_fields.get('magnetic_field', 0.0)
        if mag_strength > 0:
            # Magnetic field influences lighting color temperature
            color_temp = 5500 + mag_strength * 1000  # Kelvin
            color_temp = min(max(color_temp, 3000), 8000)  # Clamp to reasonable range
            
            # Convert color temperature to RGB
            rgb = self._color_temperature_to_rgb(color_temp)
            
            lighting['directional_lights'].append({
                'direction': [0.5, -0.7, -0.5],
                'intensity': 0.8 + 0.2 * min(mag_strength, 1.0),
                'color': rgb,
                'cast_shadows': True
            })
        
        # Add fill light based on strain measurements
        strain_level = avg_fields.get('strain', 0.0)
        if strain_level > 0:
            lighting['directional_lights'].append({
                'direction': [-0.3, -0.5, 0.8],
                'intensity': 0.4 + 0.3 * min(strain_level, 1.0),
                'color': [1.0, 0.9, 0.8],  # Warm fill
                'cast_shadows': False
            })
        
        # Add rim lighting based on vibration
        vib_level = avg_fields.get('vibration', 0.0)
        if vib_level > 0:
            lighting['rim_light'] = {
                'intensity': 0.2 + 0.3 * min(vib_level, 1.0),
                'color': [0.8, 0.9, 1.0],  # Cool rim
                'falloff': 2.0
            }
        
        self.logger.info("Applied quantum-enhanced lighting")
        return lighting
    
    def _color_temperature_to_rgb(self, temp_k: float) -> List[float]:
        """Convert color temperature in Kelvin to RGB"""
        
        # Simplified black-body radiation approximation
        temp = temp_k / 100.0
        
        if temp <= 66:
            red = 1.0
        else:
            red = temp - 60
            red = 329.698727446 * (red ** -0.1332047592)
            red = min(max(red / 255.0, 0.0), 1.0)
        
        if temp <= 66:
            green = temp
            green = 99.4708025861 * math.log(green) - 161.1195681661
        else:
            green = temp - 60
            green = 288.1221695283 * (green ** -0.0755148492)
        green = min(max(green / 255.0, 0.0), 1.0)
        
        if temp >= 66:
            blue = 1.0
        elif temp <= 19:
            blue = 0.0
        else:
            blue = temp - 10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307
            blue = min(max(blue / 255.0, 0.0), 1.0)
        
        return [red, green, blue]
    
    def _apply_quantum_materials(self, sensor_data: List[Dict]) -> Dict:
        """Apply quantum-enhanced materials based on sensor data"""
        
        if not sensor_data:
            return {'type': 'standard'}
        
        # Calculate material properties based on quantum measurements
        avg_confidence = np.mean([s.get('confidence', 0.0) for s in sensor_data])
        
        # Extract coherence information
        coherence_times = []
        for sensor in sensor_data:
            quantum_state = sensor.get('quantum_state', {})
            coherence_times.append(quantum_state.get('coherence_time', 1e-6))
        
        avg_coherence = np.mean(coherence_times) if coherence_times else 1e-6
        
        # Quantum-enhanced material properties
        materials = {
            'type': 'quantum_enhanced',
            'base_material': {
                'roughness': 0.3 + 0.4 * (1.0 - avg_confidence),  # Lower confidence = rougher
                'metallic': 0.1 + 0.6 * avg_confidence,  # Higher confidence = more metallic
                'specular': 0.8 * avg_confidence,
                'emission': 0.05 * min(avg_coherence / 1e-6, 2.0)  # Subtle glow from coherence
            },
            'sensor_materials': []
        }
        
        # Create specialized materials for each sensor type
        for sensor in sensor_data:
            mtype = sensor.get('measurement_type', 'unknown')
            confidence = sensor.get('confidence', 0.0)
            
            if mtype == 'magnetic_field':
                material = {
                    'type': 'magnetic_field_material',
                    'base_color': [0.2, 0.6, 1.0],  # Blue
                    'roughness': 0.1,
                    'metallic': 0.8,
                    'emission_strength': 0.3 * confidence,
                    'animated': True
                }
            elif mtype == 'strain':
                material = {
                    'type': 'strain_material',
                    'base_color': [1.0, 0.4, 0.2],  # Orange
                    'roughness': 0.4 + 0.4 * (1.0 - confidence),
                    'metallic': 0.2,
                    'displacement_strength': 0.1 * confidence
                }
            elif mtype == 'vibration':
                material = {
                    'type': 'vibration_material',
                    'base_color': [0.8, 0.2, 0.8],  # Magenta
                    'roughness': 0.3,
                    'metallic': 0.5,
                    'animation': {
                        'type': 'oscillate',
                        'frequency': 5.0 * confidence,
                        'amplitude': 0.02
                    }
                }
            else:
                material = {
                    'type': 'generic_sensor_material',
                    'base_color': [0.5, 0.5, 0.5],
                    'roughness': 0.5,
                    'metallic': 0.3
                }
            
            materials['sensor_materials'].append(material)
        
        self.logger.info("Applied quantum-enhanced materials")
        return materials
    
    def update_scene_with_real_time_data(self, scene: EnhancedSceneDefinition, 
                                       real_time_data: Dict) -> EnhancedSceneDefinition:
        """Update scene with real-time quantum sensor data"""
        
        # Update sensor overlays with new data
        updated_overlays = []
        
        for overlay in scene.sensor_overlays:
            sensor_id = overlay.get('sensor_id')
            
            if sensor_id in real_time_data:
                # Update with new sensor data
                new_data = real_time_data[sensor_id]
                
                overlay = overlay.copy()
                overlay['value'] = new_data.get('processed_value', overlay['value'])
                overlay['confidence'] = new_data.get('confidence', overlay['confidence'])
                
                # Update visualization based on new data
                measurement_type = overlay.get('measurement_type', 'unknown')
                viz_params = overlay.get('visualization', {}).get('viz_params', {})
                
                overlay['visualization'] = self._create_sensor_visualization(
                    measurement_type,
                    overlay['value'],
                    overlay['confidence'],
                    viz_params
                )
            
            updated_overlays.append(overlay)
        
        # Create updated scene
        updated_scene = EnhancedSceneDefinition(
            **scene.__dict__
        )
        updated_scene.sensor_overlays = updated_overlays
        
        return updated_scene
