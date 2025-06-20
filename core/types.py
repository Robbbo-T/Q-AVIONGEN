"""
Q-AVIOGEN Core Types - Enhanced formal type definitions for rendering pipeline
Definiciones formales de tipos para toda la aplicación.
Uso de dataclasses y enums para garantizar robustez y mantenibilidad.
Version: 2.0 - Enterprise Grade
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Any, Tuple
from enum import Enum, auto
import json
from pathlib import Path
from datetime import datetime

class RenderMode(Enum):
    """Modos de renderizado disponibles."""
    FULL = "full"
    PREVIEW = "preview"
    WIREFRAME = "wireframe"
    MATERIAL_PREVIEW = "material_preview"


class AnimationType(Enum):
    """Tipos de animación soportados."""
    KEYFRAME = "keyframe"
    PROCEDURAL = "procedural"
    PHYSICS = "physics"
    CAMERA_PATH = "camera_path"
    HIGHLIGHT = "highlight"
    MOVE = "move"
    ROTATE = "rotate"
    SCALE = "scale"
    SEQUENCE = "sequence"


class MaterialType(Enum):
    """Tipos de material soportados."""
    PBR = "pbr"
    PRINCIPLED = "principled"
    EMISSION = "emission"
    GLASS = "glass"
    METAL = "metal"
    FABRIC = "fabric"


class LightType(Enum):
    """Tipos de luz soportados."""
    SUN = "SUN"
    POINT = "POINT"
    SPOT = "SPOT"
    AREA = "AREA"
    HDRI = "hdri"


class OutputFormat(Enum):
    """Formatos de salida soportados."""
    PNG = "PNG"
    JPEG = "JPEG"
    EXR = "EXR"
    TIFF = "TIFF"
    MP4 = "MP4"
    AVI = "AVI"


class LogLevel(Enum):
    """Niveles de logging."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class CameraType(Enum):
    """Camera types for different viewing perspectives"""
    DEFAULT = "default"
    OVERVIEW = "overview"
    FRONT_VIEW = "front_view"
    SIDE_VIEW = "side_view"
    CLOSE_UP = "close_up"
    TOP_DOWN = "top_down"
    CUSTOM = "custom"


class RenderQuality(Enum):
    """Render quality presets"""
    PREVIEW = "preview"      # Low quality, fast render
    STANDARD = "standard"    # Balanced quality/speed
    HIGH = "high"           # High quality, slower render
    PRODUCTION = "production" # Highest quality


@dataclass
class Vector3D:
    """Vector 3D para posiciones, rotaciones y escalas."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convierte a tupla para compatibilidad con Blender."""
        return (self.x, self.y, self.z)
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Vector3D':
        """Crea desde diccionario."""
        return cls(
            x=data.get('x', 0.0),
            y=data.get('y', 0.0),
            z=data.get('z', 0.0)
        )
    
    @classmethod
    def from_tuple(cls, data: Tuple[float, float, float]) -> 'Vector3D':
        """Crea desde tupla."""
        return cls(x=data[0], y=data[1], z=data[2])


@dataclass
class RGBAColor:
    """Color RGBA."""
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Convierte a tupla para compatibilidad con Blender."""
        return (self.r, self.g, self.b, self.a)
    
    @classmethod
    def from_hex(cls, hex_color: str) -> 'RGBAColor':
        """Crea color desde hex (#RRGGBB o #RRGGBBAA)."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            hex_color += 'FF'
        
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        a = int(hex_color[6:8], 16) / 255.0
        
        return cls(r=r, g=g, b=b, a=a)
    
    @classmethod
    def from_tuple(cls, data: Union[Tuple[float, float, float], Tuple[float, float, float, float]]) -> 'RGBAColor':
        """Crea desde tupla."""
        if len(data) == 3:
            return cls(r=data[0], g=data[1], b=data[2], a=1.0)
        else:
            return cls(r=data[0], g=data[1], b=data[2], a=data[3])

@dataclass
class MaterialConfig:
    """Configuración de material mejorada."""
    name: str
    type: MaterialType = MaterialType.PRINCIPLED
    base_color: RGBAColor = field(default_factory=RGBAColor)
    metallic: float = 0.0
    roughness: float = 0.5
    emission_strength: float = 0.0
    transmission: float = 0.0
    ior: float = 1.45
    normal_map: Optional[str] = None
    roughness_map: Optional[str] = None
    metallic_map: Optional[str] = None
    texture_path: Optional[str] = None
    normal_map_path: Optional[str] = None
    emission_color: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    alpha: float = 1.0
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "type": self.type.value,
            "base_color": self.base_color.to_tuple(),
            "metallic": self.metallic,
            "roughness": self.roughness,
            "emission_strength": self.emission_strength,
            "transmission": self.transmission,
            "ior": self.ior,
            "normal_map": self.normal_map,
            "roughness_map": self.roughness_map,
            "metallic_map": self.metallic_map,
            "texture_path": self.texture_path,
            "normal_map_path": self.normal_map_path,
            "emission_color": self.emission_color,
            "alpha": self.alpha,
            "custom_properties": self.custom_properties
        }

@dataclass
class CameraConfig:
    """Configuración de cámara mejorada."""
    name: str = "MainCamera"
    position: Vector3D = field(default_factory=lambda: Vector3D(0, -10, 5))
    rotation: Vector3D = field(default_factory=lambda: Vector3D(60, 0, 0))
    target: Vector3D = field(default_factory=Vector3D)
    lens: float = 50.0
    fov: float = 50.0
    type: CameraType = CameraType.DEFAULT
    clip_start: float = 0.1
    clip_end: float = 1000.0
    depth_of_field: bool = False
    focus_distance: float = 10.0
    f_stop: float = 2.8
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "target": self.target.to_tuple(),
            "lens": self.lens,
            "fov": self.fov,
            "type": self.type.value,
            "clip_start": self.clip_start,
            "clip_end": self.clip_end,
            "depth_of_field": self.depth_of_field,
            "focus_distance": self.focus_distance,
            "f_stop": self.f_stop
        }


@dataclass
class LightConfig:
    """Configuración de luz mejorada."""
    name: str
    type: LightType = LightType.SUN
    position: Vector3D = field(default_factory=Vector3D)
    rotation: Vector3D = field(default_factory=Vector3D)
    energy: float = 5.0
    color: RGBAColor = field(default_factory=RGBAColor)
    size: float = 1.0
    angle: float = 0.785398  # 45 grados en radianes
    blend: float = 0.15  # For spot lights
    hdri_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "type": self.type.value,
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "energy": self.energy,
            "color": self.color.to_tuple(),
            "size": self.size,
            "angle": self.angle,
            "blend": self.blend,
            "hdri_path": self.hdri_path
        }


@dataclass
class AnimationKeyframe:
    """Keyframe de animación."""
    frame: int
    position: Optional[Vector3D] = None
    rotation: Optional[Vector3D] = None
    scale: Optional[Vector3D] = None
    custom_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnimationConfig:
    """Configuración de animación mejorada."""
    name: str
    type: AnimationType = AnimationType.KEYFRAME
    target_object: str
    keyframes: List[AnimationKeyframe] = field(default_factory=list)
    duration_frames: int = 250
    interpolation: str = "BEZIER"
    loop: bool = False
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "type": self.type.value,
            "target_object": self.target_object,
            "keyframes": [
                {
                    "frame": kf.frame,
                    "position": kf.position.to_tuple() if kf.position else None,
                    "rotation": kf.rotation.to_tuple() if kf.rotation else None,
                    "scale": kf.scale.to_tuple() if kf.scale else None,
                    "custom_properties": kf.custom_properties
                }
                for kf in self.keyframes
            ],
            "duration_frames": self.duration_frames,
            "interpolation": self.interpolation,
            "loop": self.loop,
            "custom_properties": self.custom_properties
        }


@dataclass
class ObjectConfig:
    """Configuración de objeto 3D mejorada."""
    name: str
    type: str = "mesh"  # mesh, light, camera, empty
    mesh_path: Optional[str] = None
    position: Vector3D = field(default_factory=Vector3D)
    rotation: Vector3D = field(default_factory=Vector3D)
    scale: Vector3D = field(default_factory=lambda: Vector3D(1, 1, 1))
    material: Optional[str] = None
    visible: bool = True
    cast_shadow: bool = True
    receive_shadow: bool = True
    animations: List[str] = field(default_factory=list)
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "type": self.type,
            "mesh_path": self.mesh_path,
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "scale": self.scale.to_tuple(),
            "material": self.material,
            "visible": self.visible,
            "cast_shadow": self.cast_shadow,
            "receive_shadow": self.receive_shadow,
            "animations": self.animations,
            "custom_properties": self.custom_properties
        }


@dataclass
class OverlayTextConfig:
    """Configuración de texto overlay."""
    text: str
    position: Tuple[float, float] = (0.1, 0.9)  # Posición normalizada (0-1)
    font_size: int = 24
    color: RGBAColor = field(default_factory=RGBAColor)
    font_family: str = "Arial"
    background: bool = False
    background_color: RGBAColor = field(default_factory=lambda: RGBAColor(0, 0, 0, 0.5))
    duration_frames: Optional[int] = None
    fade_in: int = 0
    fade_out: int = 0


@dataclass
class OverlayConfig:
    """Configuración de overlays."""
    texts: List[OverlayTextConfig] = field(default_factory=list)
    watermark: Optional[str] = None
    logo: Optional[str] = None
    custom_overlays: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class RenderSettings:
    """Configuración de renderizado mejorada."""
    resolution_x: int = 1920
    resolution_y: int = 1080
    samples: int = 128
    output_format: OutputFormat = OutputFormat.PNG
    output_path: str = "output/"
    file_format: str = "PNG"
    color_mode: str = "RGBA"
    compression: int = 15
    quality: int = 90
    frame_start: int = 1
    frame_end: int = 250
    frame_step: int = 1
    use_denoising: bool = True
    motion_blur: bool = False
    transparent: bool = False
    render_quality: RenderQuality = RenderQuality.STANDARD
    
    def get_samples(self) -> int:
        """Get sample count based on quality preset"""
        if self.samples is not None:
            return self.samples
        
        quality_samples = {
            RenderQuality.PREVIEW: 32,
            RenderQuality.STANDARD: 128,
            RenderQuality.HIGH: 512,
            RenderQuality.PRODUCTION: 2048
        }
        return quality_samples[self.render_quality]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "resolution_x": self.resolution_x,
            "resolution_y": self.resolution_y,
            "samples": self.samples,
            "output_format": self.output_format.value,
            "output_path": self.output_path,
            "file_format": self.file_format,
            "color_mode": self.color_mode,
            "compression": self.compression,
            "quality": self.quality,
            "frame_start": self.frame_start,
            "frame_end": self.frame_end,
            "frame_step": self.frame_step,
            "use_denoising": self.use_denoising,
            "motion_blur": self.motion_blur,
            "transparent": self.transparent,
            "render_quality": self.render_quality.value
        }

@dataclass
class SceneConfig:
    """Configuración completa de escena mejorada."""
    name: str
    description: str = ""
    duration_seconds: float = 10.0
    camera: CameraConfig = field(default_factory=CameraConfig)
    objects: List[ObjectConfig] = field(default_factory=list)
    lights: List[LightConfig] = field(default_factory=list)
    materials: List[MaterialConfig] = field(default_factory=list)
    animations: List[AnimationConfig] = field(default_factory=list)
    overlays: OverlayConfig = field(default_factory=OverlayConfig)
    render_settings: RenderSettings = field(default_factory=RenderSettings)
    environment: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    audio_file: Optional[str] = None
    background_color: Tuple[float, float, float] = (0.2, 0.2, 0.2)
    
    def __post_init__(self):
        """Validate scene configuration after initialization"""
        if self.duration_seconds <= 0:
            raise ValueError(f"Scene duration must be positive, got {self.duration_seconds}")
        
        if not self.name or not self.name.strip():
            raise ValueError("Scene name cannot be empty")
        
        # Ensure we have at least basic lighting
        if not self.lights:
            self.lights = self._get_default_lighting()
    
    def _get_default_lighting(self) -> List[LightConfig]:
        """Get default lighting setup"""
        return [
            LightConfig(
                name="KeyLight",
                type=LightType.SUN,
                position=Vector3D(5, 5, 10),
                energy=5.0
            ),
            LightConfig(
                name="FillLight",
                type=LightType.AREA,
                position=Vector3D(-3, 2, 4),
                energy=2.0
            )
        ]
    
    def get_frame_count(self, fps: int = 24) -> int:
        """Calculate total frame count for this scene"""
        return int(self.duration_seconds * fps)
    
    def validate(self) -> List[str]:
        """Validate scene configuration and return list of issues"""
        issues = []
        
        # Check object references in animations
        object_names = {obj.name for obj in self.objects}
        for anim in self.animations:
            if anim.target_object not in object_names:
                issues.append(f"Animation targets unknown object: {anim.target_object}")
        
        # Check material references in objects
        material_names = {mat.name for mat in self.materials}
        for obj in self.objects:
            if obj.material and obj.material not in material_names:
                issues.append(f"Object '{obj.name}' references unknown material: {obj.material}")
        
        # Check audio file exists if specified
        if self.audio_file:
            from pathlib import Path
            if not Path(self.audio_file).exists():
                issues.append(f"Audio file not found: {self.audio_file}")
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para serialización."""
        def _convert_value(value):
            if hasattr(value, '__dict__'):
                if hasattr(value, 'to_dict'):
                    return value.to_dict()
                else:
                    return {k: _convert_value(v) for k, v in value.__dict__.items()}
            elif isinstance(value, list):
                return [_convert_value(item) for item in value]
            elif isinstance(value, dict):
                return {k: _convert_value(v) for k, v in value.items()}
            elif isinstance(value, Enum):
                return value.value
            else:
                return value
        
        return _convert_value(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convierte a JSON."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """Guarda configuración a archivo JSON."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneConfig':
        """Crea configuración desde diccionario."""
        # Implementación simplificada - en producción sería más robusta
        camera_data = data.get('camera', {})
        camera = CameraConfig(
            name=camera_data.get('name', 'MainCamera'),
            position=Vector3D.from_tuple(camera_data.get('position', (0, -10, 5))),
            rotation=Vector3D.from_tuple(camera_data.get('rotation', (60, 0, 0))),
            target=Vector3D.from_tuple(camera_data.get('target', (0, 0, 0))),
            fov=camera_data.get('fov', 50.0),
            lens=camera_data.get('lens', 50.0),
            type=CameraType(camera_data.get('type', 'default')),
            clip_start=camera_data.get('clip_start', 0.1),
            clip_end=camera_data.get('clip_end', 1000.0),
            depth_of_field=camera_data.get('depth_of_field', False),
            focus_distance=camera_data.get('focus_distance', 10.0),
            f_stop=camera_data.get('f_stop', 2.8)
        )
        
        render_data = data.get('render_settings', {})
        render_settings = RenderSettings(
            resolution_x=render_data.get('resolution_x', 1920),
            resolution_y=render_data.get('resolution_y', 1080),
            samples=render_data.get('samples', 128),
            output_format=OutputFormat(render_data.get('output_format', 'PNG')),
            output_path=render_data.get('output_path', 'output/'),
            render_quality=RenderQuality(render_data.get('render_quality', 'standard'))
        )
        
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            duration_seconds=data.get('duration_seconds', 10.0),
            camera=camera,
            render_settings=render_settings,
            audio_file=data.get('audio_file'),
            background_color=tuple(data.get('background_color', (0.2, 0.2, 0.2))),
            environment=data.get('environment', {}),
            metadata=data.get('metadata', {})
        )
    
    @classmethod
    def from_json_file(cls, file_path: Union[str, Path]) -> 'SceneConfig':
        """Carga configuración desde archivo JSON."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class RenderResult:
    """Resultado de renderizado mejorado."""
    success: bool
    output_files: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    render_time: float = 0.0
    memory_usage: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    scene_config: Optional[SceneConfig] = None
    render_settings: Optional[RenderSettings] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            'success': self.success,
            'output_files': self.output_files,
            'error_message': self.error_message,
            'render_time': self.render_time,
            'memory_usage': self.memory_usage,
            'metadata': self.metadata,
            'warnings': self.warnings,
            'scene_config': self.scene_config.to_dict() if self.scene_config else None,
            'render_settings': self.render_settings.to_dict() if self.render_settings else None
        }


@dataclass
class ValidationResult:
    """Resultado de validación mejorado."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    schema_version: str = "2.0"
    validation_time: float = 0.0
    
    def add_error(self, message: str) -> None:
        """Añade error de validación."""
        self.valid = False
        self.errors.append(message)
    
    def add_warning(self, message: str) -> None:
        """Añade warning de validación."""
        self.warnings.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            'valid': self.valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'schema_version': self.schema_version,
            'validation_time': self.validation_time
        }


@dataclass
class RenderMetadata:
    """Metadata sobre un renderizado completado mejorado."""
    output_file: str
    scene_config: SceneConfig
    render_settings: RenderSettings
    start_time: datetime
    end_time: datetime
    total_frames: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    system_info: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def render_duration(self) -> float:
        """Get render duration in seconds"""
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def frames_per_second_rendered(self) -> float:
        """Get average frames rendered per second"""
        if self.render_duration > 0:
            return self.total_frames / self.render_duration
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "output_file": self.output_file,
            "scene_config": self.scene_config.to_dict(),
            "render_settings": self.render_settings.to_dict(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "render_duration_seconds": self.render_duration,
            "total_frames": self.total_frames,
            "frames_per_second_rendered": self.frames_per_second_rendered,
            "errors": self.errors,
            "warnings": self.warnings,
            "system_info": self.system_info
        }
    
    def save_to_file(self, filepath: str):
        """Save metadata to JSON file"""
        from pathlib import Path
        Path(filepath).write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding='utf-8'
        )


# Aliases para compatibilidad hacia atrás
Scene = SceneConfig
Camera = CameraConfig
Object3D = ObjectConfig
Material = MaterialConfig
Light = LightConfig
Animation = AnimationConfig

# Funciones de validación de esquema
def validate_scene_config_dict(config_dict: Dict[str, Any]) -> List[str]:
    """Validate a scene configuration dictionary"""
    errors = []
    
    required_fields = ["name"]
    for field in required_fields:
        if field not in config_dict:
            errors.append(f"Missing required field: {field}")
    
    if "duration_seconds" in config_dict:
        if not isinstance(config_dict["duration_seconds"], (int, float)) or config_dict["duration_seconds"] <= 0:
            errors.append("duration_seconds must be a positive number")
    
    return errors
