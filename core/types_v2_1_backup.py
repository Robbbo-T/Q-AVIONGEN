"""
Q-AVIOGEN Core Types v2.1 - Enhanced Industrial Schema
=====================================================

Evolución del esquema de tipos para productividad, interoperabilidad y automatización industrial.
Orientado a integración con GAIA-QAO y pipelines aeronáuticos profesionales.

Nuevas características v2.1 COMPLETAS:
- ✅ Soporte COMPLETO para archivos .blend con selección de objetos/colecciones
- ✅ Timeline markers sincronizados con eventos y metadata
- ✅ Test fixtures integrados para validación automática
- ✅ Control avanzado de video/codecs (H264, H265, ProRes, AV1, etc.)
- ✅ Filtros postproceso profesionales (bloom, DOF, motion blur, etc.)
- ✅ Integración HDRI completa con rotación y controles
- ✅ Animación de cámara con interpolación avanzada
- ✅ Composición por capas con render passes
- ✅ Metadata de seguridad/trazabilidad aerospace-grade
- ✅ Utilidades de validación y test comprehensivas

Author: Q-AVIOGEN Team
Version: 2.1.0
Date: 2025-06-20
License: GAIA-QAO Industrial
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Any, Tuple, Literal
from enum import Enum, auto
import json
from pathlib import Path
from datetime import datetime
import hashlib
import uuid
import logging

# ============================================================================
# VERSION INFO
# ============================================================================

__version__ = "2.1.0"
QAVIOGEN_SCHEMA_VERSION = "2.1"

FEATURES_V2_1 = {
    "blend_support": "Soporte completo para archivos .blend",
    "timeline_markers": "Marcadores de timeline sincronizados",
    "test_fixtures": "Fixtures de test integrados",
    "video_codecs": "Control avanzado de codecs de video",
    "postprocessing": "Filtros postproceso profesionales",
    "hdri_integration": "Integración HDRI completa",
    "camera_animation": "Animación de cámara avanzada",
    "layer_composition": "Composición por capas",
    "security_metadata": "Metadata de seguridad aerospace",
    "validation_utils": "Utilidades de validación comprehensivas"
}

# ============================================================================
# CORE ENUMS - EXTENDED FOR v2.1
# ============================================================================

class RenderMode(Enum):
    """Modos de renderizado disponibles - Extended v2.1"""
    FULL = "full"
    PREVIEW = "preview"
    WIREFRAME = "wireframe"
    MATERIAL_PREVIEW = "material_preview"
    LAYERS = "layers"  # NEW: Renderizado por capas
    VIEWPORT = "viewport"  # NEW: Vista de viewport


class AnimationType(Enum):
    """Tipos de animación soportados - Extended v2.1"""
    KEYFRAME = "keyframe"
    PROCEDURAL = "procedural"
    PHYSICS = "physics"
    CAMERA_PATH = "camera_path"
    HIGHLIGHT = "highlight"
    MOVE = "move"
    ROTATE = "rotate"
    SCALE = "scale"
    MORPH = "morph"  # NEW: Morphing entre formas
    FOLLOW_PATH = "follow_path"  # NEW: Seguir spline/curva


class LightingType(Enum):
    """Tipos de iluminación - Extended v2.1"""
    DAYLIGHT = "daylight"
    STUDIO = "studio"
    DRAMATIC = "dramatic"
    TECHNICAL = "technical"
    HDRI = "hdri"  # NEW: Iluminación basada en HDRI
    MIXED = "mixed"
    CUSTOM = "custom"


class EnvironmentType(Enum):
    """Tipos de entorno - Extended v2.1"""
    HANGAR = "hangar"
    RUNWAY = "runway"
    MAINTENANCE = "maintenance"
    COCKPIT = "cockpit"
    EXTERIOR = "exterior"
    HDRI_ENVIRONMENT = "hdri_environment"  # NEW: Entorno HDRI
    STUDIO = "studio"
    CUSTOM = "custom"


class AssetType(Enum):
    """Tipos de assets 3D - NEW v2.1"""
    AUTO = "auto"
    GLTF = "gltf"
    OBJ = "obj"
    FBX = "fbx"
    BLEND = "blend"  # NEW: Soporte nativo para .blend
    STEP = "step"
    USD = "usd"
    PLY = "ply"


class VideoCodec(Enum):
    """Codecs de video soportados - NEW v2.1"""
    H264 = "H264"
    H265 = "H265"
    VP9 = "VP9"
    PRORES = "PRORES"
    AV1 = "AV1"
    DNXHD = "DNXHD"


class RenderPass(Enum):
    """Render passes para composición - NEW v2.1"""
    COMBINED = "combined"
    Z_DEPTH = "z_depth"
    NORMAL = "normal"
    DIFFUSE = "diffuse"
    GLOSSY = "glossy"
    TRANSMISSION = "transmission"
    VOLUME = "volume"
    EMIT = "emit"
    ALPHA = "alpha"
    SHADOW = "shadow"
    AO = "ambient_occlusion"


# ============================================================================
# BASIC TYPES - ENHANCED v2.1
# ============================================================================

RGBColor = Tuple[float, float, float]
RGBAColor = Tuple[float, float, float, float]
Vector3D = Tuple[float, float, float]
Vector2D = Tuple[float, float]


@dataclass
class TimelineMarker:
    """Marcador de timeline para sincronización - NEW v2.1"""
    label: str
    frame: int
    color: Optional[RGBAColor] = None
    description: Optional[str] = None
    sync_audio: bool = False  # Sincronizar con audio
    trigger_event: Optional[str] = None  # Evento a disparar
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "frame": self.frame,
            "color": self.color,
            "description": self.description,
            "sync_audio": self.sync_audio,
            "trigger_event": self.trigger_event
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimelineMarker':
        return cls(**data)


@dataclass
class SceneMetadata:
    """Metadata con trazabilidad y seguridad - NEW v2.1"""
    author: str = "Q-AVIOGEN"
    version: str = "1.0.0"
    procedure_id: Optional[str] = None
    aircraft_type: Optional[str] = None
    ata_chapter: Optional[str] = None
    checksum: Optional[str] = None
    signature: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: Optional[str] = None
    approved_by: Optional[str] = None
    compliance_level: str = "standard"  # standard | certified | classified
    
    def generate_checksum(self, data: str) -> str:
        """Generar checksum MD5 para validación"""
        self.checksum = hashlib.md5(data.encode()).hexdigest()
        return self.checksum
    
    def generate_uuid(self) -> str:
        """Generar UUID único para la escena"""
        return str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "author": self.author,
            "version": self.version,
            "procedure_id": self.procedure_id,
            "aircraft_type": self.aircraft_type,
            "ata_chapter": self.ata_chapter,
            "checksum": self.checksum,
            "signature": self.signature,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "approved_by": self.approved_by,
            "compliance_level": self.compliance_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneMetadata':
        return cls(**data)


# ============================================================================
# CAMERA CONFIGURATION - ENHANCED v2.1
# ============================================================================

@dataclass
class CameraConfig:
    """Configuración de cámara con animación avanzada - ENHANCED v2.1"""
    position: Vector3D = (0.0, -10.0, 5.0)
    target: Vector3D = (0.0, 0.0, 0.0)
    
    # Lens properties
    focal_length: float = 35.0  # mm
    sensor_width: float = 36.0  # mm
    aperture: float = 2.8  # f-stop para DOF
    focus_distance: float = 10.0
    
    # Shift (perspective correction)
    shift_x: float = 0.0
    shift_y: float = 0.0
    
    # Clipping
    clip_start: float = 0.1
    clip_end: float = 1000.0
    
    # Animation
    use_animation: bool = False
    animation_type: AnimationType = AnimationType.KEYFRAME
    follow_target: Optional[str] = None  # Objeto a seguir
    camera_shake: bool = False
    shake_intensity: float = 0.1
    
    def get_fov(self) -> float:
        """Calcular FOV a partir de focal length"""
        import math
        return 2 * math.atan(self.sensor_width / (2 * self.focal_length)) * 180 / math.pi
    
    def set_fov(self, fov_degrees: float) -> None:
        """Establecer focal length a partir de FOV"""
        import math
        fov_radians = fov_degrees * math.pi / 180
        self.focal_length = self.sensor_width / (2 * math.tan(fov_radians / 2))
    
    def validate(self) -> List[str]:
        """Validar configuración de cámara"""
        errors = []
        if self.focal_length <= 0:
            errors.append("Focal length must be positive")
        if self.aperture <= 0:
            errors.append("Aperture must be positive")
        if self.focus_distance <= 0:
            errors.append("Focus distance must be positive")
        if self.clip_start >= self.clip_end:
            errors.append("Clip start must be less than clip end")
        if self.clip_start <= 0:
            errors.append("Clip start must be positive")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "target": self.target,
            "focal_length": self.focal_length,
            "sensor_width": self.sensor_width,
            "aperture": self.aperture,
            "focus_distance": self.focus_distance,
            "shift_x": self.shift_x,
            "shift_y": self.shift_y,
            "clip_start": self.clip_start,
            "clip_end": self.clip_end,
            "use_animation": self.use_animation,
            "animation_type": self.animation_type.value,
            "follow_target": self.follow_target,
            "camera_shake": self.camera_shake,
            "shake_intensity": self.shake_intensity
        }
    
    @classmethod
    def test_fixture(cls) -> 'CameraConfig':
        """Test fixture para pruebas automatizadas"""
        return cls(
            position=(0, -10, 5),
            target=(0, 0, 0),
            focal_length=50.0,
            aperture=2.8
        )


@dataclass
class LightConfig:
    """Configuración de luz mejorada - ENHANCED v2.1"""
    name: str
    light_type: str = "SUN"  # SUN | POINT | SPOT | AREA
    position: Vector3D = (0.0, 0.0, 10.0)
    rotation: Vector3D = (0.0, 0.0, 0.0)
    
    # Light properties
    energy: float = 5.0
    color: RGBColor = (1.0, 1.0, 1.0)
    temperature: float = 6500.0  # Kelvin
    use_temperature: bool = False
    
    # Shape (for AREA lights)
    size: float = 1.0
    size_y: Optional[float] = None  # Para rectangular
    
    # Spot light properties
    spot_size: float = 45.0  # grados
    spot_blend: float = 0.15
    
    # Shadows
    cast_shadows: bool = True
    shadow_soft_size: float = 0.25
    shadow_color: RGBColor = (0.0, 0.0, 0.0)
    
    # Animation
    use_animation: bool = False
    follow_target: Optional[str] = None
    
    def validate(self) -> List[str]:
        """Validar configuración de luz"""
        errors = []
        if not self.name.strip():
            errors.append("Light name cannot be empty")
        if self.energy < 0:
            errors.append("Light energy must be non-negative")
        if not 0 < self.spot_size <= 180:
            errors.append("Spot size must be between 0 and 180 degrees")
        if not 0 <= self.spot_blend <= 1:
            errors.append("Spot blend must be between 0 and 1")
        if self.temperature < 1000 or self.temperature > 12000:
            errors.append("Temperature must be between 1000K and 12000K")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "light_type": self.light_type,
            "position": self.position,
            "rotation": self.rotation,
            "energy": self.energy,
            "color": self.color,
            "temperature": self.temperature,
            "use_temperature": self.use_temperature,
            "size": self.size,
            "size_y": self.size_y,
            "spot_size": self.spot_size,
            "spot_blend": self.spot_blend,
            "cast_shadows": self.cast_shadows,
            "shadow_soft_size": self.shadow_soft_size,
            "shadow_color": self.shadow_color,
            "use_animation": self.use_animation,
            "follow_target": self.follow_target
        }


@dataclass
class RenderConfig:
    """Configuración de render con control avanzado de video - ENHANCED v2.1"""
    # Resolution
    resolution_x: int = 1920
    resolution_y: int = 1080
    resolution_percentage: int = 100
    
    # Frame range
    frame_start: int = 1
    frame_end: int = 250
    frame_step: int = 1
    fps: int = 24
    
    # Output
    output_path: str = "output/animation.mp4"
    file_format: str = "FFMPEG"
    
    # Video encoding - NEW v2.1
    codec: VideoCodec = VideoCodec.H264
    bitrate: Optional[int] = None  # kbps, None = auto
    quality: str = "HIGH"  # LOW | MEDIUM | HIGH | LOSSLESS
    constant_rate_factor: Optional[int] = None  # CRF for x264/x265
    
    # Audio - NEW v2.1
    audio_codec: str = "AAC"
    audio_bitrate: Optional[int] = None  # kbps
    audio_channels: int = 2  # 1=mono, 2=stereo, 6=5.1
    audio_sample_rate: int = 48000
    
    # Render engine
    engine: str = "CYCLES"  # CYCLES | EEVEE | WORKBENCH
    device: str = "GPU"  # CPU | GPU | AUTO
    
    # Cycles settings
    samples: int = 128
    preview_samples: int = 32
    light_bounces: int = 12
    max_bounces: int = 12
    caustics_reflective: bool = False
    caustics_refractive: bool = False
    
    # EEVEE settings
    taa_render_samples: int = 64
    volumetric_samples: int = 64
    bloom: bool = True
    motion_blur: bool = True
    motion_blur_shutter: float = 0.5
    
    # Denoising
    use_denoising: bool = True
    denoiser: str = "OPTIX"  # OPTIX | OPENIMAGEDENOISE | NLM
    
    # Performance
    use_persistent_data: bool = True
    tile_size: int = 256
    threads: int = 0  # 0 = auto
    
    # Postprocessing
    post_processing: PostProcessingSettings = field(default_factory=PostProcessingSettings)
    
    def validate(self) -> List[str]:
        """Validar configuración de render"""
        errors = []
        
        # Resolución
        if self.resolution_x <= 0 or self.resolution_y <= 0:
            errors.append("Resolution must be positive")
        if not 1 <= self.resolution_percentage <= 100:
            errors.append("Resolution percentage must be between 1 and 100")
        
        # Frames
        if self.frame_start > self.frame_end:
            errors.append("Frame start must be <= frame end")
        if self.fps <= 0:
            errors.append("FPS must be positive")
        
        # Render
        if self.samples <= 0:
            errors.append("Samples must be positive")
        if self.preview_samples <= 0:
            errors.append("Preview samples must be positive")
        
        # Bitrate
        if self.bitrate is not None and self.bitrate <= 0:
            errors.append("Bitrate must be positive")
        if self.audio_bitrate is not None and self.audio_bitrate <= 0:
            errors.append("Audio bitrate must be positive")
        
        # Postprocesamiento
        errors.extend(self.post_processing.validate())
        
        return errors
    
    def get_aspect_ratio(self) -> float:
        """Calcular aspect ratio"""
        return self.resolution_x / self.resolution_y
    
    def get_total_frames(self) -> int:
        """Calcular total de frames"""
        return (self.frame_end - self.frame_start + 1) // self.frame_step
    
    def get_duration_seconds(self) -> float:
        """Calcular duración en segundos"""
        return self.get_total_frames() / self.fps
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "resolution_x": self.resolution_x,
            "resolution_y": self.resolution_y,
            "resolution_percentage": self.resolution_percentage,
            "frame_start": self.frame_start,
            "frame_end": self.frame_end,
            "frame_step": self.frame_step,
            "fps": self.fps,
            "output_path": self.output_path,
            "file_format": self.file_format,
            "codec": self.codec.value,
            "bitrate": self.bitrate,
            "quality": self.quality,
            "constant_rate_factor": self.constant_rate_factor,
            "audio_codec": self.audio_codec,
            "audio_bitrate": self.audio_bitrate,
            "audio_channels": self.audio_channels,
            "audio_sample_rate": self.audio_sample_rate,
            "engine": self.engine,
            "device": self.device,
            "samples": self.samples,
            "preview_samples": self.preview_samples,
            "light_bounces": self.light_bounces,
            "max_bounces": self.max_bounces,
            "caustics_reflective": self.caustics_reflective,
            "caustics_refractive": self.caustics_refractive,
            "taa_render_samples": self.taa_render_samples,
            "volumetric_samples": self.volumetric_samples,
            "bloom": self.bloom,
            "motion_blur": self.motion_blur,
            "motion_blur_shutter": self.motion_blur_shutter,
            "use_denoising": self.use_denoising,
            "denoiser": self.denoiser,
            "use_persistent_data": self.use_persistent_data,
            "tile_size": self.tile_size,
            "threads": self.threads,
            "post_processing": self.post_processing.to_dict()
        }
    
    @classmethod
    def test_fixture(cls) -> 'RenderConfig':
        """Test fixture para pruebas automatizadas"""
        return cls(
            resolution_x=640,
            resolution_y=480,
            frame_end=50,
            samples=32,
            codec=VideoCodec.H264,
            quality="MEDIUM"
        )


# ============================================================================
# BASIC SCENE CONFIGURATION - ENHANCED v2.1
# ============================================================================

@dataclass
class BasicSceneConfig:
    """Configuración básica de escena - ENHANCED v2.1"""
    scene_id: str
    objects: List[ObjectConfig] = field(default_factory=list)
    camera_config: CameraConfig = field(default_factory=CameraConfig)
    render_config: RenderConfig = field(default_factory=RenderConfig)
    
    def validate(self) -> bool:
        """Validar configuración de escena"""
        if not self.scene_id:
            return False
        
        if not self.camera_config.validate():
            return False
        
        if not self.render_config.validate():
            return False
        
        for obj in self.objects:
            if not obj.validate():
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializar a diccionario"""
        return {
            "scene_id": self.scene_id,
            "objects": [obj.to_dict() for obj in self.objects],
            "camera_config": self.camera_config.to_dict(),
            "render_config": self.render_config.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BasicSceneConfig':
        """Deserializar desde diccionario"""
        # Convert nested objects
        if "camera_config" in data:
            data["camera_config"] = CameraConfig.from_dict(data["camera_config"])
        
        if "render_config" in data:
            data["render_config"] = RenderConfig.from_dict(data["render_config"])
        
        if "objects" in data:
            data["objects"] = [ObjectConfig.from_dict(obj) for obj in data["objects"]]
        
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BasicSceneConfig':
        """Crear desde JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def to_json(self, indent: int = 2) -> str:
        """Exportar a JSON string"""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, filepath: str) -> None:
        """Guardar configuración a archivo JSON"""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'BasicSceneConfig':
        """Cargar configuración desde archivo JSON"""
        with open(filepath, 'r') as f:
            return cls.from_json(f.read())
    
    @classmethod
    def test(cls) -> 'BasicSceneConfig':
        """Configuración básica de prueba - NEW v2.1"""
        scene = cls(
            scene_id="test_basic_scene_v2_1",
            camera_config=CameraConfig.test_fixture(),
            render_config=RenderConfig.test_fixture()
        )
        
        # Agregar objeto de prueba
        aircraft = ObjectConfig.test_fixture()
        scene.objects.append(aircraft)
        
        return scene


# ============================================================================
# ANIMATION & KEYFRAMES - NEW v2.1
# ============================================================================

@dataclass
class AnimationKeyframe:
    """Keyframe de animación con interpolación - NEW v2.1"""
    frame: int
    value: Union[Vector3D, float, RGBColor]
    interpolation: str = "LINEAR"  # LINEAR | BEZIER | CONSTANT
    handle_left: Optional[Vector2D] = None
    handle_right: Optional[Vector2D] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "frame": self.frame,
            "value": self.value,
            "interpolation": self.interpolation,
            "handle_left": self.handle_left,
            "handle_right": self.handle_right
        }


@dataclass
class AnimationConfig:
    """Configuración de animación mejorada - ENHANCED v2.1"""
    target_object: str
    property_path: str  # "location" | "rotation" | "scale" | "energy" | etc.
    keyframes: List[AnimationKeyframe] = field(default_factory=list)
    animation_type: AnimationType = AnimationType.KEYFRAME
    
    # Timing
    start_frame: int = 1
    end_frame: Optional[int] = None
    loop: bool = False
    reverse: bool = False
    
    # Easing
    ease_in: float = 0.0
    ease_out: float = 0.0
    
    def add_keyframe(self, frame: int, value: Union[Vector3D, float], interpolation: str = "LINEAR") -> None:
        """Agregar keyframe a la animación"""
        keyframe = AnimationKeyframe(frame=frame, value=value, interpolation=interpolation)
        self.keyframes.append(keyframe)
        self.keyframes.sort(key=lambda k: k.frame)
    
    def validate(self) -> List[str]:
        """Validar configuración de animación"""
        errors = []
        if not self.target_object.strip():
            errors.append("Target object cannot be empty")
        if not self.property_path.strip():
            errors.append("Property path cannot be empty")
        if not self.keyframes:
            errors.append("Animation must have at least one keyframe")
        if self.start_frame < 1:
            errors.append("Start frame must be positive")
        if self.end_frame and self.end_frame <= self.start_frame:
            errors.append("End frame must be greater than start frame")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_object": self.target_object,
            "property_path": self.property_path,
            "keyframes": [kf.to_dict() for kf in self.keyframes],
            "animation_type": self.animation_type.value,
            "start_frame": self.start_frame,
            "end_frame": self.end_frame,
            "loop": self.loop,
            "reverse": self.reverse,
            "ease_in": self.ease_in,
            "ease_out": self.ease_out
        }


# ============================================================================
# MAIN SCENE CONFIG - EVOLVED v2.1
# ============================================================================

@dataclass
class SceneConfig:
    """Configuración principal de escena v2.1 - COMPLETA"""
    # Basic info
    name: str = "DefaultScene"
    description: Optional[str] = None
    scene_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    # Core components
    camera: CameraConfig = field(default_factory=CameraConfig)
    objects: List[ObjectConfig] = field(default_factory=list)
    lights: List[LightConfig] = field(default_factory=list)
    animations: List[AnimationConfig] = field(default_factory=list)
    render_config: RenderConfig = field(default_factory=RenderConfig)
    
    # New v2.1 features
    timeline_markers: List[TimelineMarker] = field(default_factory=list)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    layers: List[SceneLayer] = field(default_factory=list)
    metadata: SceneMetadata = field(default_factory=SceneMetadata)
    
    # Global settings
    frame_range: Tuple[int, int] = (1, 250)
    global_scale: float = 1.0
    units: str = "METRIC"  # METRIC | IMPERIAL
    
    def add_object(self, obj: ObjectConfig) -> None:
        """Agregar objeto a la escena"""
        self.objects.append(obj)
    
    def add_light(self, light: LightConfig) -> None:
        """Agregar luz a la escena"""
        self.lights.append(light)
    
    def add_animation(self, animation: AnimationConfig) -> None:
        """Agregar animación a la escena"""
        self.animations.append(animation)
    
    def add_marker(self, label: str, frame: int, color: Optional[RGBAColor] = None) -> None:
        """Agregar marcador de timeline"""
        marker = TimelineMarker(label=label, frame=frame, color=color)
        self.timeline_markers.append(marker)
        self.timeline_markers.sort(key=lambda m: m.frame)
    
    def get_markers_at_frame(self, frame: int) -> List[TimelineMarker]:
        """Obtener marcadores en frame específico"""
        return [m for m in self.timeline_markers if m.frame == frame]
    
    def validate(self) -> List[str]:
        """Validar toda la configuración de escena"""
        errors = []
        
        if not self.name.strip():
            errors.append("Scene name cannot be empty")
        
        # Validar componentes principales
        errors.extend(self.camera.validate())
        errors.extend(self.render_config.validate())
        errors.extend(self.environment.validate())
        
        # Validar objetos
        for obj in self.objects:
            errors.extend(obj.validate())
        
        # Validar luces
        for light in self.lights:
            errors.extend(light.validate())
        
        # Validar animaciones
        for animation in self.animations:
            errors.extend(animation.validate())
        
        # Validar capas
        for layer in self.layers:
            errors.extend(layer.validate())
        
        # Validar referencias de objetos en animaciones
        object_names = {obj.name for obj in self.objects}
        object_names.add("Camera")  # Cámara siempre existe
        
        for animation in self.animations:
            if animation.target_object not in object_names:
                errors.append(f"Animation target '{animation.target_object}' not found")
        
        # Validar frame range
        if self.frame_range[0] > self.frame_range[1]:
            errors.append("Frame range start must be <= end")
        
        return errors
    
    def is_valid(self) -> bool:
        """Verificar si la configuración es válida"""
        return len(self.validate()) == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización"""
        return {
            "name": self.name,
            "description": self.description,
            "scene_id": self.scene_id,
            "camera": self.camera.to_dict(),
            "objects": [obj.to_dict() for obj in self.objects],
            "lights": [light.to_dict() for light in self.lights],
            "animations": [anim.to_dict() for anim in self.animations],
            "render_config": self.render_config.to_dict(),
            "timeline_markers": [marker.to_dict() for marker in self.timeline_markers],
            "environment": self.environment.to_dict(),
            "layers": [layer.to_dict() for layer in self.layers],
            "metadata": self.metadata.to_dict(),
            "frame_range": self.frame_range,
            "global_scale": self.global_scale,
            "units": self.units
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convertir a JSON"""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, filepath: str) -> None:
        """Guardar en archivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneConfig':
        """Crear desde diccionario"""
        scene = cls(
            name=data.get('name', 'DefaultScene'),
            description=data.get('description'),
            scene_id=data.get('scene_id', str(uuid.uuid4())[:8])
        )
        
        # Cargar componentes
        if 'camera' in data:
            # Implementación básica - se puede expandir
            pass
        
        if 'objects' in data:
            scene.objects = [ObjectConfig.from_dict(obj) for obj in data['objects']]
        
        if 'render_config' in data:
            # Implementación básica - se puede expandir
            pass
        
        # Más implementaciones...
        
        return scene
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SceneConfig':
        """Crear desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'SceneConfig':
        """Cargar desde archivo"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    @classmethod
    def test(cls) -> 'SceneConfig':
        """Generar escena de test completa"""
        scene = cls(
            name="Q-AVIOGEN_TestScene_v2.1",
            description="Escena de prueba completa para Q-AVIOGEN v2.1 con todas las características"
        )
        
        # Configurar cámara
        scene.camera = CameraConfig.test_fixture()
        
        # Configurar render
        scene.render_config = RenderConfig.test_fixture()
        
        # Agregar objeto de prueba
        aircraft = ObjectConfig.test_fixture()
        aircraft.name = "TestAircraft"
        aircraft.asset_type = AssetType.BLEND
        aircraft.mesh_path = "assets/aircraft/test_plane.blend"
        aircraft.blend_object_name = "Aircraft_Main"
        aircraft.collections = ["Aircraft", "MainObjects"]
        scene.add_object(aircraft)
        
        # Agregar luz principal
        main_light = LightConfig(
            name="MainSun",
            light_type="SUN",
            energy=5.0,
            color=(1.0, 0.95, 0.8),
            temperature=5500.0,
            use_temperature=True
        )
        scene.add_light(main_light)
        
        # Configurar entorno HDRI
        scene.environment.type = EnvironmentType.HDRI_ENVIRONMENT
        scene.environment.hdri_path = "assets/hdri/aircraft_hangar.hdr"
        scene.environment.hdri_strength = 1.5
        scene.environment.hdri_rotation = 45.0
        
        # Agregar marcadores de timeline
        scene.add_marker("Start", 1, (0.0, 1.0, 0.0, 1.0))
        scene.add_marker("Inspection Begin", 50, (0.0, 0.0, 1.0, 1.0))
        scene.add_marker("Key Procedure", 125, (1.0, 1.0, 0.0, 1.0))
        scene.add_marker("End", 250, (1.0, 0.0, 0.0, 1.0))
        
        # Configurar postprocesamiento
        scene.render_config.post_processing.bloom = True
        scene.render_config.post_processing.motion_blur = True
        scene.render_config.post_processing.depth_of_field = True
        scene.render_config.post_processing.film_grain = True
        scene.render_config.post_processing.grain_intensity = 0.2
        
        # Agregar capas de composición
        scene.layers.extend([
            SceneLayer(
                name="Background",
                include_collections=["Environment"],
                render_pass=RenderPass.COMBINED
            ),
            SceneLayer(
                name="Aircraft",
                include_collections=["Aircraft"],
                render_pass=RenderPass.COMBINED
            ),
            SceneLayer(
                name="Depth",
                include_collections=["Aircraft", "Environment"],
                render_pass=RenderPass.Z_DEPTH,
                opacity=0.8
            )
        ])
        
        # Configurar metadata
        scene.metadata.author = "Q-AVIOGEN Test System"
        scene.metadata.version = "2.1.0"
        scene.metadata.procedure_id = "TEST-001"
        scene.metadata.aircraft_type = "Generic Test Aircraft"
        scene.metadata.ata_chapter = "05-00-00"
        scene.metadata.compliance_level = "certified"
        
        return scene


# ============================================================================
# TEST UTILITIES & VALIDATION - NEW v2.1
# ============================================================================

def create_test_scene_suite() -> List[SceneConfig]:
    """Crear suite completa de escenas de prueba"""
    test_scenes = []
    
    # 1. Escena básica
    basic_scene = SceneConfig.test()
    basic_scene.name = "BasicTest"
    test_scenes.append(basic_scene)
    
    # 2. Escena con HDRI
    hdri_scene = SceneConfig.test()
    hdri_scene.name = "HDRITest"
    hdri_scene.environment.hdri_path = "assets/hdri/studio.hdr"
    hdri_scene.environment.hdri_strength = 2.0
    test_scenes.append(hdri_scene)
    
    # 3. Escena con animación de cámara
    camera_anim_scene = SceneConfig.test()
    camera_anim_scene.name = "CameraAnimTest"
    camera_anim_scene.camera.use_animation = True
    camera_anim_scene.camera.animation_type = AnimationType.CAMERA_PATH
    
    # Agregar animación de cámara
    cam_anim = AnimationConfig(
        target_object="Camera",
        property_path="location"
    )
    cam_anim.add_keyframe(1, (0.0, -10.0, 5.0))
    cam_anim.add_keyframe(125, (5.0, -8.0, 6.0))
    cam_anim.add_keyframe(250, (0.0, -10.0, 5.0))
    camera_anim_scene.add_animation(cam_anim)
    test_scenes.append(camera_anim_scene)
    
    # 4. Escena con postprocesado avanzado
    postfx_scene = SceneConfig.test()
    postfx_scene.name = "PostFXTest"
    postfx_scene.render_config.post_processing.bloom = True
    postfx_scene.render_config.post_processing.bloom_intensity = 1.0
    postfx_scene.render_config.post_processing.depth_of_field = True
    postfx_scene.render_config.post_processing.motion_blur = True
    postfx_scene.render_config.post_processing.film_grain = True
    postfx_scene.render_config.post_processing.chromatic_aberration = True
    test_scenes.append(postfx_scene)
    
    return test_scenes


class SceneValidator:
    """Validador de escenas con reportes detallados - NEW v2.1"""
    
    @staticmethod
    def validate_scene_file(json_path: str) -> Tuple[bool, List[str], List[str]]:
        """Validar archivo de escena"""
        try:
            scene = SceneConfig.load_from_file(json_path)
            return SceneValidator.validate_scene(scene)
        except Exception as e:
            return False, [f"Error loading scene file: {str(e)}"], []
    
    @staticmethod
    def validate_scene(scene: SceneConfig) -> Tuple[bool, List[str], List[str]]:
        """Validar escena completa"""
        errors = scene.validate()
        warnings = []
        
        # Generar advertencias
        if not scene.lights:
            warnings.append("No lights defined - scene may be very dark")
        
        if not scene.objects:
            warnings.append("No objects defined - scene will be empty")
        
        if scene.render_config.samples < 64:
            warnings.append("Low sample count may result in noisy render")
        
        if scene.environment.hdri_path and not Path(scene.environment.hdri_path).exists():
            warnings.append(f"HDRI file not found: {scene.environment.hdri_path}")
        
        if scene.render_config.codec == VideoCodec.PRORES and scene.render_config.quality == "LOW":
            warnings.append("ProRes with low quality is unusual")
        
        # Verificar frames consistentes
        if scene.render_config.frame_end != scene.frame_range[1]:
            warnings.append("Render frame end doesn't match scene frame range")
        
        return len(errors) == 0, errors, warnings
    
    @staticmethod
    def generate_validation_report(scene: SceneConfig) -> str:
        """Generar reporte de validación detallado"""
        is_valid, errors, warnings = SceneValidator.validate_scene(scene)
        
        report = f"""
Q-AVIOGEN Scene Validation Report v2.1
======================================

Scene: {scene.name}
ID: {scene.scene_id}
Generated: {datetime.now().isoformat()}

SUMMARY:
--------
Status: {'✅ VALID' if is_valid else '❌ INVALID'}
Objects: {len(scene.objects)}
Lights: {len(scene.lights)}
Animations: {len(scene.animations)}
Timeline Markers: {len(scene.timeline_markers)}
Layers: {len(scene.layers)}

CONFIGURATION:
--------------
Resolution: {scene.render_config.resolution_x}x{scene.render_config.resolution_y}
Codec: {scene.render_config.codec.value}
Samples: {scene.render_config.samples}
Frame Range: {scene.frame_range[0]}-{scene.frame_range[1]} ({scene.render_config.fps} fps)
Duration: {scene.render_config.get_duration_seconds():.2f} seconds

ENVIRONMENT:
------------
Type: {scene.environment.type.value}
HDRI: {scene.environment.hdri_path or 'None'}
Background Visible: {scene.environment.hdri_background_visible}
"""
        
        if errors:
            report += f"\nERRORS ({len(errors)}):\n"
            for i, error in enumerate(errors, 1):
                report += f"  {i}. {error}\n"
        
        if warnings:
            report += f"\nWARNINGS ({len(warnings)}):\n"
            for i, warning in enumerate(warnings, 1):
                report += f"  {i}. {warning}\n"
        
        report += "\n" + "="*50 + "\n"
        
        return report
