"""
YAML Parser for Declarative Procedure Definitions
Parsea archivos YAML con definiciones declarativas de procedimientos
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class YAMLStep:
    """Represents a step from YAML configuration"""
    id: str
    description: str
    camera: str = "default"
    duration: float = 5.0
    narration: str = ""
    overlay: str = ""
    animation: Optional[Dict[str, Any]] = None
    safety_notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class YAMLProcedure:
    """Complete procedure from YAML"""
    id: str
    title: str
    aircraft: str = ""
    ata_code: str = ""
    overview: str = ""
    steps: List[YAMLStep] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class YAMLParser:
    """Parser for YAML-based procedure definitions"""
    
    def __init__(self):
        self.supported_versions = ['1.0', '1.1']
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a YAML file and return procedure data"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo YAML no encontrado: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")
        
        return self.parse_yaml_data(yaml_data, file_path.stem)
    
    def parse_yaml_data(self, yaml_data: Dict[str, Any], filename: str = "") -> Dict[str, Any]:
        """Parse YAML data structure and convert to standard format"""
        
        # Validate YAML structure
        self._validate_yaml_structure(yaml_data)
        
        # Extract main procedure info
        procedure_info = yaml_data.get('procedure', {})
        steps_data = yaml_data.get('steps', [])
        settings = yaml_data.get('settings', {})
        
        # Build procedure data in standard format
        procedure_data = {
            'id': procedure_info.get('id', filename),
            'title': procedure_info.get('title', 'Procedimiento sin título'),
            'overview': procedure_info.get('overview', ''),
            'aircraft_model': procedure_info.get('aircraft', ''),
            'ata_code': procedure_info.get('ata_code', procedure_info.get('id', '')),
            'steps': self._convert_steps(steps_data),
            'metadata': {
                'source_file': filename,
                'source_type': 'yaml',
                'version': yaml_data.get('version', '1.0'),
                'settings': settings,
                'total_steps': len(steps_data),
                'estimated_duration': self._calculate_total_duration(steps_data)
            }
        }
        
        return procedure_data
    
    def _validate_yaml_structure(self, yaml_data: Dict[str, Any]) -> None:
        """Validate that YAML has required structure"""
        required_keys = ['procedure', 'steps']
        
        for key in required_keys:
            if key not in yaml_data:
                raise ValueError(f"YAML debe contener la clave '{key}'")
        
        if not isinstance(yaml_data['steps'], list):
            raise ValueError("'steps' debe ser una lista")
        
        if not yaml_data['steps']:
            raise ValueError("Debe haber al menos un paso en 'steps'")
        
        # Validate version if present
        version = yaml_data.get('version', '1.0')
        if version not in self.supported_versions:
            raise ValueError(f"Versión {version} no soportada. Versiones soportadas: {self.supported_versions}")
    
    def _convert_steps(self, steps_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert YAML steps to standard step format"""
        converted_steps = []
        
        for i, step in enumerate(steps_data):
            # Ensure step has required fields
            if 'description' not in step:
                raise ValueError(f"Paso {i+1} debe tener 'description'")
            
            converted_step = {
                'id': step.get('id', f"step_{str(i+1).zfill(2)}"),
                'title': step.get('title', step['description']),
                'description': step['description'],
                'duration': float(step.get('duration', 5.0)),
                'camera_angle': step.get('camera', 'default'),
                'overlay_text': step.get('overlay', ''),
                'narration': step.get('narration', step['description']),
                'safety_notes': step.get('safety_notes', [])
            }
            
            # Handle animation data
            if 'animation' in step:
                converted_step['animation'] = step['animation']
            
            # Handle metadata
            if 'metadata' in step:
                converted_step['metadata'] = step['metadata']
            
            converted_steps.append(converted_step)
        
        return converted_steps
    
    def _calculate_total_duration(self, steps_data: List[Dict[str, Any]]) -> float:
        """Calculate total estimated duration"""
        total = 0.0
        for step in steps_data:
            total += float(step.get('duration', 5.0))
        return total
    
    def create_template(self, output_path: str, procedure_id: str = "example") -> None:
        """Create a template YAML file"""
        template = {
            'version': '1.0',
            'procedure': {
                'id': procedure_id,
                'title': 'Ejemplo de Procedimiento',
                'aircraft': 'BWB-Q100',
                'ata_code': '00-30-10-01',
                'overview': 'Este es un ejemplo de procedimiento técnico'
            },
            'settings': {
                'default_duration': 5.0,
                'default_camera': 'front_view',
                'quality': 'high',
                'resolution': '1080p'
            },
            'steps': [
                {
                    'id': 'step_01',
                    'title': 'Preparación inicial',
                    'description': 'Verificar que todos los equipos estén disponibles',
                    'camera': 'overview',
                    'duration': 3.0,
                    'narration': 'Comenzamos verificando que todos los equipos necesarios estén disponibles y en buenas condiciones.',
                    'overlay': 'Verificación de equipos',
                    'safety_notes': [
                        'Usar equipo de protección personal',
                        'Verificar que el área esté despejada'
                    ],
                    'animation': {
                        'type': 'highlight',
                        'target': 'equipment_area',
                        'duration': 2.0
                    }
                },
                {
                    'id': 'step_02',
                    'title': 'Ejecución del procedimiento',
                    'description': 'Ejecutar el procedimiento principal',
                    'camera': 'close_up',
                    'duration': 8.0,
                    'narration': 'Procedemos a ejecutar el paso principal del procedimiento con cuidado.',
                    'overlay': 'Torque: 100Nm',
                    'animation': {
                        'type': 'sequence',
                        'actions': [
                            {'action': 'move', 'target': 'tool', 'duration': 2.0},
                            {'action': 'rotate', 'target': 'connector', 'duration': 3.0}
                        ]
                    }
                },
                {
                    'id': 'step_03',
                    'title': 'Verificación final',
                    'description': 'Verificar que el procedimiento se completó correctamente',
                    'camera': 'overview',
                    'duration': 4.0,
                    'narration': 'Finalmente, verificamos que todo se haya completado correctamente.',
                    'overlay': 'Verificación completa',
                    'safety_notes': [
                        'Revisar conexiones',
                        'Documentar en el log'
                    ]
                }
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(template, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"Template YAML creado en: {output_path}")

# Example usage and testing
if __name__ == "__main__":
    # Test creating template
    parser = YAMLParser()
    
    # Create template
    template_path = "example_procedure.yaml"
    parser.create_template(template_path, "00-30-10-01")
    
    # Test parsing the template
    try:
        result = parser.parse_file(template_path)
        print("📋 Resultado del parser YAML:")
        print(f"ID: {result['id']}")
        print(f"Título: {result['title']}")
        print(f"Pasos: {len(result['steps'])}")
        print(f"Duración total: {result['metadata']['estimated_duration']}s")
        
        for step in result['steps']:
            print(f"  - {step['id']}: {step['title']} ({step['duration']}s)")
            if step['overlay_text']:
                print(f"    Overlay: {step['overlay_text']}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    # Clean up
    import os
    if os.path.exists(template_path):
        os.remove(template_path)
