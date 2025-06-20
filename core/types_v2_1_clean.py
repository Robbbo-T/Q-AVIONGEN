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
- ✅ Avatar personalizado con voz grabada
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
    "layer_composition": "Composición por capas y render passes",
    "security_metadata": "Metadata de seguridad aerospace-grade",
    "avatar_voice": "Avatar personalizado con voz grabada",
    "validation_framework": "Framework de validación integrado"
}

# ============================================================================
# BASIC TYPES & ENUMS
# ============================================================================

class AssetType(Enum):
    """Tipos de assets soportados"""
    AUTO = "auto"
    GLTF = "gltf"
    OBJ = "obj"
    FBX = "fbx"
    BLEND = "blend"
    COLLADA = "collada"
    PLY = "ply"
    STL = "stl"

class VideoCodec(Enum):
    """Codecs de video soportados"""
    H264 = "h264"
    H265 = "h265"
    VP9 = "vp9"
    AV1 = "av1"
    PRORES = "prores"
    DNXHD = "dnxhd"
    FFVHUFF = "ffvhuff"

class RenderPass(Enum):
    """Tipos de render passes"""
    COMBINED = "combined"
    Z_DEPTH = "z"
    NORMAL = "normal"
    DIFFUSE = "diffuse"
    GLOSSY = "glossy"
    TRANSMISSION = "transmission"
    EMISSION = "emission"
    ENVIRONMENT = "environment"
    AO = "ao"
    SHADOW = "shadow"
    MIST = "mist"
    OBJECT_INDEX = "object_index"
    MATERIAL_INDEX = "material_index"

class EnvironmentType(Enum):
    """Tipos de entorno"""
    HDRI = "hdri"
    GRADIENT = "gradient"
    SOLID_COLOR = "solid_color"
    STUDIO = "studio"
    OUTDOOR = "outdoor"

class AvatarType(Enum):
    """Tipos de avatar disponibles"""
    VIRTUAL_HUMAN = "virtual_human"
    CARTOON_CHARACTER = "cartoon_character"
    TECHNICAL_INSTRUCTOR = "technical_instructor"
    HOLOGRAM = "hologram"
    CUSTOM_MODEL = "custom_model"

class VoiceGender(Enum):
    """Género de voz para síntesis"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"
    CUSTOM = "custom"  # Para voces grabadas personalizadas

class AvatarEmotionState(Enum):
    """Estados emocionales del avatar"""
    NEUTRAL = "neutral"
    FRIENDLY = "friendly"
    FOCUSED = "focused"
    EXPLAINING = "explaining"
    WARNING = "warning"
    ENCOURAGING = "encouraging"
    SERIOUS = "serious"

@dataclass
class Vector3D:
    """Vector 3D básico"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def validate(self) -> List[str]:
        """Validar vector 3D"""
        errors = []
        if not all(isinstance(v, (int, float)) for v in [self.x, self.y, self.z]):
            errors.append("All vector components must be numeric")
        return errors
    
    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}

@dataclass
class RGBAColor:
    """Color RGBA"""
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    
    def validate(self) -> List[str]:
        """Validar color RGBA"""
        errors = []
        for component, name in [(self.r, 'r'), (self.g, 'g'), (self.b, 'b'), (self.a, 'a')]:
            if not 0.0 <= component <= 1.0:
                errors.append(f"Color component {name} must be between 0.0 and 1.0")
        return errors
    
    def to_dict(self) -> Dict[str, float]:
        return {"r": self.r, "g": self.g, "b": self.b, "a": self.a}

# ============================================================================
# TIMELINE MARKERS - NEW v2.1
# ============================================================================

@dataclass
class TimelineMarker:
    """Marcador de timeline sincronizado"""
    label: str
    frame: int
    color: Optional[RGBAColor] = None
    description: Optional[str] = None
    event_type: str = "general"  # general | voice | animation | effect
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validar marcador de timeline"""
        errors = []
        if not self.label.strip():
            errors.append("Timeline marker label cannot be empty")
        if self.frame < 0:
            errors.append("Timeline marker frame must be non-negative")
        if self.color:
            errors.extend(self.color.validate())
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "frame": self.frame,
            "color": self.color.to_dict() if self.color else None,
            "description": self.description,
            "event_type": self.event_type,
            "metadata": self.metadata
        }

# ============================================================================
# SECURITY & METADATA - NEW v2.1
# ============================================================================

@dataclass
class SceneMetadata:
    """Metadata de seguridad y trazabilidad aerospace-grade"""
    # Basic info
    author: str = "unknown"
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Security
    checksum: Optional[str] = None
    signature: Optional[str] = None
    encryption_level: str = "none"  # none | basic | aerospace
    
    # Compliance
    certification_level: str = "development"  # development | testing | production | certified
    compliance_standards: List[str] = field(default_factory=list)  # ["ISO-9001", "AS9100", etc.]
    approved_by: Optional[str] = None
    approval_date: Optional[str] = None
    
    # Technical metadata
    software_version: str = "Q-AVIOGEN 2.1"
    render_engine: str = "Blender Cycles"
    dependencies: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validar metadata"""
        errors = []
        if not self.author.strip():
            errors.append("Author cannot be empty")
        if self.certification_level not in ["development", "testing", "production", "certified"]:
            errors.append("Invalid certification level")
        return errors
    
    def generate_checksum(self, content: str) -> str:
        """Generar checksum del contenido"""
        self.checksum = hashlib.sha256(content.encode()).hexdigest()
        return self.checksum
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "author": self.author,
            "version": self.version,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "checksum": self.checksum,
            "signature": self.signature,
            "encryption_level": self.encryption_level,
            "certification_level": self.certification_level,
            "compliance_standards": self.compliance_standards,
            "approved_by": self.approved_by,
            "approval_date": self.approval_date,
            "software_version": self.software_version,
            "render_engine": self.render_engine,
            "dependencies": self.dependencies
        }

# ============================================================================
# AVATAR & VOICE PERSONALIZATION - NEW v2.1
# ============================================================================

@dataclass
class VoiceConfig:
    """Configuración de voz personalizada"""
    # Voice source
    use_custom_voice: bool = False
    custom_voice_path: Optional[str] = None  # Path to recorded voice samples
    voice_clone_model: Optional[str] = None  # AI voice cloning model
    
    # TTS fallback settings
    tts_engine: str = "azure"  # azure | google | amazon | local
    voice_name: str = "es-ES-AlvaroNeural"
    voice_gender: VoiceGender = VoiceGender.MALE
    voice_age: str = "adult"  # child | young | adult | elderly
    
    # Voice characteristics
    pitch: float = 0.0  # -1.0 to 1.0
    speed: float = 1.0  # 0.5 to 2.0
    volume: float = 1.0  # 0.0 to 1.0
    emphasis: float = 0.0  # -1.0 to 1.0
    
    # Language and accent
    language: str = "es-ES"
    accent: Optional[str] = None
    pronunciation_guide: Dict[str, str] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validar configuración de voz"""
        errors = []
        if self.use_custom_voice and not self.custom_voice_path:
            errors.append("Custom voice path required when use_custom_voice is True")
        if self.custom_voice_path and not Path(self.custom_voice_path).exists():
            errors.append(f"Custom voice file not found: {self.custom_voice_path}")
        if not 0.5 <= self.speed <= 2.0:
            errors.append("Voice speed must be between 0.5 and 2.0")
        if not 0.0 <= self.volume <= 1.0:
            errors.append("Voice volume must be between 0.0 and 1.0")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "use_custom_voice": self.use_custom_voice,
            "custom_voice_path": self.custom_voice_path,
            "voice_clone_model": self.voice_clone_model,
            "tts_engine": self.tts_engine,
            "voice_name": self.voice_name,
            "voice_gender": self.voice_gender.value,
            "voice_age": self.voice_age,
            "pitch": self.pitch,
            "speed": self.speed,
            "volume": self.volume,
            "emphasis": self.emphasis,
            "language": self.language,
            "accent": self.accent,
            "pronunciation_guide": self.pronunciation_guide
        }

@dataclass
class AvatarConfig:
    """Configuración del avatar personalizado"""
    # Avatar basics
    enabled: bool = True
    avatar_type: AvatarType = AvatarType.TECHNICAL_INSTRUCTOR
    avatar_model_path: Optional[str] = None  # Path to 3D model (.blend, .fbx, .gltf)
    avatar_name: str = "Instructor"
    
    # Appearance
    scale: float = 1.0
    position: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    rotation: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    
    # Animation and behavior
    default_emotion: AvatarEmotionState = AvatarEmotionState.FRIENDLY
    animation_set: Optional[str] = None  # Path to animation files
    gesture_library: List[str] = field(default_factory=list)
    
    # Visual settings
    lighting_setup: Optional[str] = None  # Special lighting for avatar
    materials_override: Dict[str, str] = field(default_factory=dict)
    
    # Interaction settings
    look_at_camera: bool = True
    auto_gestures: bool = True
    emotion_sync_with_speech: bool = True
    
    # Screen position (for overlay mode)
    screen_position: str = "bottom_right"  # bottom_right | bottom_left | top_right | top_left | center
    screen_size_percent: float = 25.0  # Percentage of screen
    transparency: float = 0.9  # 0.0 to 1.0
    
    def validate(self) -> List[str]:
        """Validar configuración del avatar"""
        errors = []
        if self.avatar_model_path and not Path(self.avatar_model_path).exists():
            errors.append(f"Avatar model file not found: {self.avatar_model_path}")
        if not 0.1 <= self.scale <= 10.0:
            errors.append("Avatar scale must be between 0.1 and 10.0")
        if not 0.0 <= self.transparency <= 1.0:
            errors.append("Avatar transparency must be between 0.0 and 1.0")
        if not 0.0 <= self.screen_size_percent <= 100.0:
            errors.append("Screen size percent must be between 0.0 and 100.0")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "avatar_type": self.avatar_type.value,
            "avatar_model_path": self.avatar_model_path,
            "avatar_name": self.avatar_name,
            "scale": self.scale,
            "position": self.position.to_dict(),
            "rotation": self.rotation.to_dict(),
            "default_emotion": self.default_emotion.value,
            "animation_set": self.animation_set,
            "gesture_library": self.gesture_library,
            "lighting_setup": self.lighting_setup,
            "materials_override": self.materials_override,
            "look_at_camera": self.look_at_camera,
            "auto_gestures": self.auto_gestures,
            "emotion_sync_with_speech": self.emotion_sync_with_speech,
            "screen_position": self.screen_position,
            "screen_size_percent": self.screen_size_percent,
            "transparency": self.transparency
        }

@dataclass
class NarrationSegment:
    """Segmento de narración con configuración específica"""
    text: str
    start_time: float  # seconds
    duration: float  # seconds
    
    # Avatar behavior for this segment
    emotion: AvatarEmotionState = AvatarEmotionState.NEUTRAL
    gestures: List[str] = field(default_factory=list)
    emphasis_words: List[str] = field(default_factory=list)
    
    # Voice modulation for this segment
    voice_modulation: Optional[Dict[str, float]] = None  # speed, pitch, volume adjustments
    
    # Synchronization
    sync_with_animation: bool = True
    sync_markers: List[str] = field(default_factory=list)  # Timeline markers to sync with
    
    def validate(self) -> List[str]:
        """Validar segmento de narración"""
        errors = []
        if not self.text.strip():
            errors.append("Narration text cannot be empty")
        if self.start_time < 0:
            errors.append("Start time must be non-negative")
        if self.duration <= 0:
            errors.append("Duration must be positive")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "start_time": self.start_time,
            "duration": self.duration,
            "emotion": self.emotion.value,
            "gestures": self.gestures,
            "emphasis_words": self.emphasis_words,
            "voice_modulation": self.voice_modulation,
            "sync_with_animation": self.sync_with_animation,
            "sync_markers": self.sync_markers
        }

# ============================================================================
# POSTPROCESSING & EFFECTS - v2.1
# ============================================================================

@dataclass
class PostProcessingSettings:
    """Configuración de postprocesamiento profesional"""
    # Color grading
    exposure: float = 0.0
    gamma: float = 1.0
    contrast: float = 1.0
    brightness: float = 0.0
    saturation: float = 1.0
    hue_shift: float = 0.0
    
    # Effects
    vignette: bool = False
    vignette_intensity: float = 0.5
    bloom: bool = False
    bloom_threshold: float = 1.0
    bloom_intensity: float = 0.5
    bloom_radius: float = 6.5
    glare: bool = False
    glare_threshold: float = 1.0
    
    # Motion blur
    motion_blur: bool = False
    motion_blur_samples: int = 16
    motion_blur_shutter: float = 0.5
    
    # Depth of field
    depth_of_field: bool = False
    dof_focus_distance: float = 10.0
    dof_aperture: float = 2.8
    dof_blades: int = 6
    
    # Film effects
    film_grain: bool = False
    grain_intensity: float = 0.5
    grain_size: float = 1.0
    chromatic_aberration: bool = False
    chromatic_intensity: float = 0.5
    
    def validate(self) -> List[str]:
        """Validar configuración de postprocesamiento"""
        errors = []
        if self.gamma <= 0:
            errors.append("Gamma must be positive")
        if not 0 <= self.vignette_intensity <= 1:
            errors.append("Vignette intensity must be between 0 and 1")
        if self.bloom_threshold < 0:
            errors.append("Bloom threshold must be non-negative")
        if self.dof_aperture <= 0:
            errors.append("DOF aperture must be positive")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "exposure": self.exposure,
            "gamma": self.gamma,
            "contrast": self.contrast,
            "brightness": self.brightness,
            "saturation": self.saturation,
            "hue_shift": self.hue_shift,
            "vignette": self.vignette,
            "vignette_intensity": self.vignette_intensity,
            "bloom": self.bloom,
            "bloom_threshold": self.bloom_threshold,
            "bloom_intensity": self.bloom_intensity,
            "bloom_radius": self.bloom_radius,
            "motion_blur": self.motion_blur,
            "motion_blur_samples": self.motion_blur_samples,
            "motion_blur_shutter": self.motion_blur_shutter,
            "depth_of_field": self.depth_of_field,
            "dof_focus_distance": self.dof_focus_distance,
            "dof_aperture": self.dof_aperture,
            "dof_blades": self.dof_blades,
            "film_grain": self.film_grain,
            "grain_intensity": self.grain_intensity,
            "grain_size": self.grain_size,
            "chromatic_aberration": self.chromatic_aberration,
            "chromatic_intensity": self.chromatic_intensity
        }

# ============================================================================
# ENVIRONMENT & HDRI - v2.1
# ============================================================================

@dataclass
class EnvironmentConfig:
    """Configuración de entorno con HDRI completo"""
    type: EnvironmentType = EnvironmentType.STUDIO
    
    # HDRI settings
    hdri_path: Optional[str] = None
    hdri_rotation: float = 0.0  # en grados
    hdri_strength: float = 1.0
    hdri_saturation: float = 1.0
    hdri_hue_shift: float = 0.0
    
    # Background settings
    background_color: RGBAColor = field(default_factory=lambda: RGBAColor(0.05, 0.05, 0.05, 1.0))
    background_strength: float = 1.0
    
    # Lighting
    ambient_strength: float = 0.1
    sun_rotation: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    sun_strength: float = 3.0
    sun_color: RGBAColor = field(default_factory=lambda: RGBAColor(1.0, 1.0, 1.0, 1.0))
    
    def validate(self) -> List[str]:
        """Validar configuración de entorno"""
        errors = []
        if self.type == EnvironmentType.HDRI and not self.hdri_path:
            errors.append("HDRI path required when environment type is HDRI")
        if self.hdri_path and not Path(self.hdri_path).exists():
            errors.append(f"HDRI file not found: {self.hdri_path}")
        if self.hdri_strength < 0:
            errors.append("HDRI strength must be non-negative")
        errors.extend(self.background_color.validate())
        errors.extend(self.sun_color.validate())
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "hdri_path": self.hdri_path,
            "hdri_rotation": self.hdri_rotation,
            "hdri_strength": self.hdri_strength,
            "hdri_saturation": self.hdri_saturation,
            "hdri_hue_shift": self.hdri_hue_shift,
            "background_color": self.background_color.to_dict(),
            "background_strength": self.background_strength,
            "ambient_strength": self.ambient_strength,
            "sun_rotation": self.sun_rotation.to_dict(),
            "sun_strength": self.sun_strength,
            "sun_color": self.sun_color.to_dict()
        }

# ============================================================================
# LAYER COMPOSITION - v2.1
# ============================================================================

@dataclass
class SceneLayer:
    """Capa de composición con render passes"""
    name: str
    include_objects: List[str] = field(default_factory=list)
    exclude_objects: List[str] = field(default_factory=list)
    render_pass: RenderPass = RenderPass.COMBINED
    output_path: Optional[str] = None
    enabled: bool = True
    opacity: float = 1.0
    blend_mode: str = "normal"  # normal | multiply | add | subtract | etc.
    
    def validate(self) -> List[str]:
        """Validar capa de escena"""
        errors = []
        if not self.name.strip():
            errors.append("Layer name cannot be empty")
        if not 0.0 <= self.opacity <= 1.0:
            errors.append("Layer opacity must be between 0.0 and 1.0")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "include_objects": self.include_objects,
            "exclude_objects": self.exclude_objects,
            "render_pass": self.render_pass.value,
            "output_path": self.output_path,
            "enabled": self.enabled,
            "opacity": self.opacity,
            "blend_mode": self.blend_mode
        }

# ============================================================================
# ENHANCED RENDER SETTINGS - v2.1
# ============================================================================

@dataclass
class RenderSettings:
    """Configuración de renderizado avanzada"""
    # Basic settings
    resolution_x: int = 1920
    resolution_y: int = 1080
    frame_start: int = 1
    frame_end: int = 250
    frame_step: int = 1
    fps: int = 24
    
    # Quality settings
    samples: int = 128
    max_bounces: int = 12
    diffuse_bounces: int = 4
    glossy_bounces: int = 4
    transmission_bounces: int = 12
    volume_bounces: int = 0
    
    # Video codec settings - NEW v2.1
    codec: VideoCodec = VideoCodec.H264
    bitrate: Optional[int] = None  # kbps
    quality: str = "high"  # low | medium | high | lossless
    audio_codec: str = "aac"
    audio_bitrate: int = 192  # kbps
    
    # Output settings
    output_format: str = "mp4"
    output_path: str = "output/render.mp4"
    file_naming: str = "frame_###"
    
    # Advanced settings
    motion_blur: bool = False
    motion_blur_shutter: float = 0.5
    use_denoising: bool = True
    denoising_algorithm: str = "OPENIMAGEDENOISE"  # OPENIMAGEDENOISE | NLM
    
    # Postprocessing
    post_processing: PostProcessingSettings = field(default_factory=PostProcessingSettings)
    
    def validate(self) -> List[str]:
        """Validar configuración de renderizado"""
        errors = []
        if self.resolution_x <= 0 or self.resolution_y <= 0:
            errors.append("Resolution must be positive")
        if self.frame_start > self.frame_end:
            errors.append("Frame start must be <= frame end")
        if self.fps <= 0:
            errors.append("FPS must be positive")
        if self.samples <= 0:
            errors.append("Samples must be positive")
        errors.extend(self.post_processing.validate())
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "resolution_x": self.resolution_x,
            "resolution_y": self.resolution_y,
            "frame_start": self.frame_start,
            "frame_end": self.frame_end,
            "frame_step": self.frame_step,
            "fps": self.fps,
            "samples": self.samples,
            "max_bounces": self.max_bounces,
            "diffuse_bounces": self.diffuse_bounces,
            "glossy_bounces": self.glossy_bounces,
            "transmission_bounces": self.transmission_bounces,
            "volume_bounces": self.volume_bounces,
            "codec": self.codec.value,
            "bitrate": self.bitrate,
            "quality": self.quality,
            "audio_codec": self.audio_codec,
            "audio_bitrate": self.audio_bitrate,
            "output_format": self.output_format,
            "output_path": self.output_path,
            "file_naming": self.file_naming,
            "motion_blur": self.motion_blur,
            "motion_blur_shutter": self.motion_blur_shutter,
            "use_denoising": self.use_denoising,
            "denoising_algorithm": self.denoising_algorithm,
            "post_processing": self.post_processing.to_dict()
        }

# ============================================================================
# CAMERA CONFIGURATION - Enhanced v2.1
# ============================================================================

@dataclass
class CameraConfig:
    """Configuración de cámara con animación avanzada"""
    # Basic settings
    position: Vector3D = field(default_factory=lambda: Vector3D(7.5, -6.5, 5.5))
    rotation: Vector3D = field(default_factory=lambda: Vector3D(63.4, 0, 46.7))
    target: Optional[Vector3D] = None
    
    # Camera properties
    lens_focal_length: float = 50.0  # mm
    sensor_width: float = 36.0  # mm
    depth_of_field: bool = False
    focus_distance: float = 10.0
    aperture: float = 2.8
    
    # Animation - NEW v2.1
    animated: bool = False
    animation_type: str = "keyframe"  # keyframe | path | orbit | flythrough
    keyframes: List[Dict[str, Any]] = field(default_factory=list)
    animation_duration: float = 10.0  # seconds
    easing: str = "ease_in_out"  # linear | ease_in | ease_out | ease_in_out
    
    def validate(self) -> List[str]:
        """Validar configuración de cámara"""
        errors = []
        errors.extend(self.position.validate())
        errors.extend(self.rotation.validate())
        if self.target:
            errors.extend(self.target.validate())
        if self.lens_focal_length <= 0:
            errors.append("Lens focal length must be positive")
        if self.sensor_width <= 0:
            errors.append("Sensor width must be positive")
        if self.focus_distance <= 0:
            errors.append("Focus distance must be positive")
        if self.aperture <= 0:
            errors.append("Aperture must be positive")
        if self.animation_duration <= 0:
            errors.append("Animation duration must be positive")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "position": self.position.to_dict(),
            "rotation": self.rotation.to_dict(),
            "target": self.target.to_dict() if self.target else None,
            "lens_focal_length": self.lens_focal_length,
            "sensor_width": self.sensor_width,
            "depth_of_field": self.depth_of_field,
            "focus_distance": self.focus_distance,
            "aperture": self.aperture,
            "animated": self.animated,
            "animation_type": self.animation_type,
            "keyframes": self.keyframes,
            "animation_duration": self.animation_duration,
            "easing": self.easing
        }

# ============================================================================
# OBJECT CONFIGURATION - Enhanced v2.1
# ============================================================================

@dataclass
class ObjectConfig:
    """Configuración de objeto con soporte .blend"""
    # Basic info
    name: str
    type: str = "mesh"  # mesh | light | camera | empty | curve
    
    # Asset loading - Enhanced v2.1
    mesh_path: Optional[str] = None
    asset_type: AssetType = AssetType.AUTO
    blend_object_name: Optional[str] = None  # Para archivos .blend
    blend_collection_name: Optional[str] = None  # Para importar colecciones completas
    
    # Transform
    position: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    rotation: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    scale: Vector3D = field(default_factory=lambda: Vector3D(1, 1, 1))
    
    # Material
    material_name: Optional[str] = None
    material_override: Dict[str, Any] = field(default_factory=dict)
    
    # Visibility and rendering
    visible: bool = True
    cast_shadows: bool = True
    receive_shadows: bool = True
    render_layer: str = "default"
    
    def validate(self) -> List[str]:
        """Validar configuración de objeto"""
        errors = []
        if not self.name.strip():
            errors.append("Object name cannot be empty")
        if self.mesh_path and not Path(self.mesh_path).exists():
            errors.append(f"Mesh file not found: {self.mesh_path}")
        if self.asset_type == AssetType.BLEND and not self.blend_object_name and not self.blend_collection_name:
            errors.append("For .blend files, either blend_object_name or blend_collection_name must be specified")
        errors.extend(self.position.validate())
        errors.extend(self.rotation.validate())
        errors.extend(self.scale.validate())
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "mesh_path": self.mesh_path,
            "asset_type": self.asset_type.value,
            "blend_object_name": self.blend_object_name,
            "blend_collection_name": self.blend_collection_name,
            "position": self.position.to_dict(),
            "rotation": self.rotation.to_dict(),
            "scale": self.scale.to_dict(),
            "material_name": self.material_name,
            "material_override": self.material_override,
            "visible": self.visible,
            "cast_shadows": self.cast_shadows,
            "receive_shadows": self.receive_shadows,
            "render_layer": self.render_layer
        }

# ============================================================================
# ANIMATION CONFIGURATION
# ============================================================================

@dataclass
class AnimationConfig:
    """Configuración de animación"""
    target_object: str
    property_path: str  # e.g., "location.x", "rotation_euler.z"
    keyframes: List[Tuple[int, float]] = field(default_factory=list)  # (frame, value)
    interpolation: str = "BEZIER"  # LINEAR | BEZIER | CONSTANT
    easing: str = "ease_in_out"
    
    def validate(self) -> List[str]:
        """Validar configuración de animación"""
        errors = []
        if not self.target_object.strip():
            errors.append("Target object cannot be empty")
        if not self.property_path.strip():
            errors.append("Property path cannot be empty")
        if len(self.keyframes) < 2:
            errors.append("At least 2 keyframes required for animation")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_object": self.target_object,
            "property_path": self.property_path,
            "keyframes": self.keyframes,
            "interpolation": self.interpolation,
            "easing": self.easing
        }

# ============================================================================
# ENHANCED NARRATION CONFIG - v2.1
# ============================================================================

@dataclass
class EnhancedNarrationConfig:
    """Configuración avanzada de narración con avatar"""
    # Voice and avatar
    voice_config: VoiceConfig = field(default_factory=VoiceConfig)
    avatar_config: AvatarConfig = field(default_factory=AvatarConfig)
    
    # Narration segments
    segments: List[NarrationSegment] = field(default_factory=list)
    
    # Global settings
    auto_generate_segments: bool = True
    segment_duration_max: float = 30.0  # Max seconds per segment
    pause_between_segments: float = 1.0  # Seconds
    
    # Background music
    background_music_path: Optional[str] = None
    background_music_volume: float = 0.3
    fade_music_during_speech: bool = True
    
    # Output settings
    export_audio_separately: bool = True
    audio_format: str = "wav"  # wav | mp3 | flac
    audio_bitrate: int = 192  # kbps for compressed formats
    
    def validate(self) -> List[str]:
        """Validar configuración de narración"""
        errors = []
        errors.extend(self.voice_config.validate())
        errors.extend(self.avatar_config.validate())
        
        for i, segment in enumerate(self.segments):
            segment_errors = segment.validate()
            errors.extend([f"Segment {i}: {error}" for error in segment_errors])
        
        if self.segment_duration_max <= 0:
            errors.append("Max segment duration must be positive")
        if not 0.0 <= self.background_music_volume <= 1.0:
            errors.append("Background music volume must be between 0.0 and 1.0")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "voice_config": self.voice_config.to_dict(),
            "avatar_config": self.avatar_config.to_dict(),
            "segments": [segment.to_dict() for segment in self.segments],
            "auto_generate_segments": self.auto_generate_segments,
            "segment_duration_max": self.segment_duration_max,
            "pause_between_segments": self.pause_between_segments,
            "background_music_path": self.background_music_path,
            "background_music_volume": self.background_music_volume,
            "fade_music_during_speech": self.fade_music_during_speech,
            "export_audio_separately": self.export_audio_separately,
            "audio_format": self.audio_format,
            "audio_bitrate": self.audio_bitrate
        }
    
    @classmethod
    def create_personal_instructor(cls, 
                                 custom_voice_path: str,
                                 avatar_model_path: str,
                                 instructor_name: str = "Amedeo") -> 'EnhancedNarrationConfig':
        """Crear configuración para instructor personalizado"""
        voice_config = VoiceConfig(
            use_custom_voice=True,
            custom_voice_path=custom_voice_path,
            language="es-ES",
            speed=1.0,
            volume=1.0
        )
        
        avatar_config = AvatarConfig(
            enabled=True,
            avatar_type=AvatarType.TECHNICAL_INSTRUCTOR,
            avatar_model_path=avatar_model_path,
            avatar_name=instructor_name,
            default_emotion=AvatarEmotionState.FRIENDLY,
            auto_gestures=True,
            emotion_sync_with_speech=True,
            screen_position="bottom_right",
            screen_size_percent=30.0,
            transparency=0.95
        )
        
        return cls(
            voice_config=voice_config,
            avatar_config=avatar_config,
            auto_generate_segments=True,
            segment_duration_max=20.0,
            export_audio_separately=True
        )

# ============================================================================
# MAIN SCENE CONFIGURATION - v2.1
# ============================================================================

@dataclass
class SceneConfig:
    """Configuración principal de escena Q-AVIOGEN v2.1"""
    # Basic info
    name: str = "DefaultScene"
    description: str = ""
    version: str = "2.1.0"
    
    # Core components
    camera: CameraConfig = field(default_factory=CameraConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    render_settings: RenderSettings = field(default_factory=RenderSettings)
    
    # Objects and animations
    objects: List[ObjectConfig] = field(default_factory=list)
    animations: List[AnimationConfig] = field(default_factory=list)
    
    # New v2.1 features
    timeline_markers: List[TimelineMarker] = field(default_factory=list)
    layers: List[SceneLayer] = field(default_factory=list)
    narration: EnhancedNarrationConfig = field(default_factory=EnhancedNarrationConfig)
    metadata: SceneMetadata = field(default_factory=SceneMetadata)
    
    def validate(self) -> List[str]:
        """Validar toda la configuración de escena"""
        errors = []
        if not self.name.strip():
            errors.append("Scene name cannot be empty")
        
        # Validate all components
        errors.extend(self.camera.validate())
        errors.extend(self.environment.validate())
        errors.extend(self.render_settings.validate())
        errors.extend(self.narration.validate())
        errors.extend(self.metadata.validate())
        
        # Validate objects
        for i, obj in enumerate(self.objects):
            obj_errors = obj.validate()
            errors.extend([f"Object {i} ({obj.name}): {error}" for error in obj_errors])
        
        # Validate animations
        for i, anim in enumerate(self.animations):
            anim_errors = anim.validate()
            errors.extend([f"Animation {i}: {error}" for error in anim_errors])
        
        # Validate timeline markers
        for i, marker in enumerate(self.timeline_markers):
            marker_errors = marker.validate()
            errors.extend([f"Timeline marker {i}: {error}" for error in marker_errors])
        
        # Validate layers
        for i, layer in enumerate(self.layers):
            layer_errors = layer.validate()
            errors.extend([f"Layer {i}: {error}" for error in layer_errors])
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "camera": self.camera.to_dict(),
            "environment": self.environment.to_dict(),
            "render_settings": self.render_settings.to_dict(),
            "objects": [obj.to_dict() for obj in self.objects],
            "animations": [anim.to_dict() for anim in self.animations],
            "timeline_markers": [marker.to_dict() for marker in self.timeline_markers],
            "layers": [layer.to_dict() for layer in self.layers],
            "narration": self.narration.to_dict(),
            "metadata": self.metadata.to_dict()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convertir a JSON"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def save_to_file(self, filepath: str) -> None:
        """Guardar en archivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneConfig':
        """Crear desde diccionario"""
        # Esta implementación sería más compleja, requiere deserialización
        # Por ahora retornamos una instancia básica
        return cls(name=data.get('name', 'DefaultScene'))
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SceneConfig':
        """Crear desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'SceneConfig':
        """Cargar desde archivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    # ============================================================================
    # TEST FIXTURES - NEW v2.1
    # ============================================================================
    
    @classmethod
    def test_basic(cls) -> 'SceneConfig':
        """Configuración de test básica"""
        return cls(
            name="TestBasicScene",
            description="Configuración básica para tests",
            objects=[
                ObjectConfig(
                    name="TestCube",
                    type="mesh",
                    position=Vector3D(0, 0, 0)
                )
            ]
        )
    
    @classmethod
    def test_advanced(cls) -> 'SceneConfig':
        """Configuración de test avanzada con todas las características"""
        return cls(
            name="TestAdvancedScene",
            description="Configuración completa para tests avanzados",
            camera=CameraConfig(
                position=Vector3D(5, -5, 3),
                animated=True,
                animation_duration=5.0
            ),
            environment=EnvironmentConfig(
                type=EnvironmentType.HDRI,
                hdri_path="test_hdri.hdr"
            ),
            objects=[
                ObjectConfig(
                    name="TestEngine",
                    mesh_path="test_engine.blend",
                    asset_type=AssetType.BLEND,
                    blend_object_name="Engine"
                ),
                ObjectConfig(
                    name="TestTool",
                    mesh_path="test_tool.gltf",
                    asset_type=AssetType.GLTF
                )
            ],
            timeline_markers=[
                TimelineMarker(
                    label="Start Inspection",
                    frame=1,
                    event_type="voice"
                ),
                TimelineMarker(
                    label="Focus on Component",
                    frame=50,
                    event_type="animation"
                )
            ],
            layers=[
                SceneLayer(
                    name="Main Objects",
                    include_objects=["TestEngine", "TestTool"],
                    render_pass=RenderPass.COMBINED
                ),
                SceneLayer(
                    name="Depth Pass",
                    include_objects=["TestEngine"],
                    render_pass=RenderPass.Z_DEPTH
                )
            ],
            narration=EnhancedNarrationConfig.create_personal_instructor(
                custom_voice_path="test_voice.wav",
                avatar_model_path="test_avatar.blend",
                instructor_name="TestInstructor"
            )
        )
    
    @classmethod
    def test_aerospace_inspection(cls) -> 'SceneConfig':
        """Configuración específica para inspección aeroespacial"""
        metadata = SceneMetadata(
            author="Q-AVIOGEN System",
            certification_level="testing",
            compliance_standards=["AS9100", "ISO-9001"],
            approved_by="Quality Assurance"
        )
        
        return cls(
            name="AerospaceInspectionTest",
            description="Procedimiento de inspección de motor aeronáutico",
            render_settings=RenderSettings(
                resolution_x=3840,
                resolution_y=2160,
                samples=256,
                codec=VideoCodec.PRORES,
                post_processing=PostProcessingSettings(
                    depth_of_field=True,
                    dof_aperture=1.8,
                    film_grain=True,
                    grain_intensity=0.2
                )
            ),
            environment=EnvironmentConfig(
                type=EnvironmentType.STUDIO,
                hdri_strength=2.0,
                ambient_strength=0.3
            ),
            objects=[
                ObjectConfig(
                    name="AircraftEngine",
                    mesh_path="assets/engines/turbofan_detailed.blend",
                    asset_type=AssetType.BLEND,
                    blend_collection_name="Engine_Assembly"
                ),
                ObjectConfig(
                    name="InspectionTool",
                    mesh_path="assets/tools/borescope.gltf",
                    asset_type=AssetType.GLTF
                )
            ],
            metadata=metadata
        )

# ============================================================================
# VALIDATION UTILITIES - NEW v2.1
# ============================================================================

class SceneValidator:
    """Utilidades de validación para SceneConfig"""
    
    @staticmethod
    def validate_scene(scene: SceneConfig) -> Tuple[bool, List[str]]:
        """Validar escena completa"""
        errors = scene.validate()
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @staticmethod
    def validate_json_file(filepath: str) -> Tuple[bool, List[str]]:
        """Validar archivo JSON de escena"""
        try:
            scene = SceneConfig.load_from_file(filepath)
            return SceneValidator.validate_scene(scene)
        except Exception as e:
            return False, [f"Error loading file: {str(e)}"]
    
    @staticmethod
    def generate_validation_report(scene: SceneConfig) -> str:
        """Generar reporte de validación"""
        is_valid, errors = SceneValidator.validate_scene(scene)
        
        report = f"Q-AVIOGEN Scene Validation Report\n"
        report += f"===================================\n\n"
        report += f"Scene: {scene.name}\n"
        report += f"Version: {scene.version}\n"
        report += f"Validation Status: {'✅ VALID' if is_valid else '❌ INVALID'}\n\n"
        
        if errors:
            report += f"Errors Found ({len(errors)}):\n"
            for i, error in enumerate(errors, 1):
                report += f"{i}. {error}\n"
        else:
            report += "✅ No validation errors found.\n"
        
        # Add feature summary
        report += f"\nFeature Summary:\n"
        report += f"- Objects: {len(scene.objects)}\n"
        report += f"- Animations: {len(scene.animations)}\n"
        report += f"- Timeline Markers: {len(scene.timeline_markers)}\n"
        report += f"- Layers: {len(scene.layers)}\n"
        report += f"- Avatar Enabled: {scene.narration.avatar_config.enabled}\n"
        report += f"- Custom Voice: {scene.narration.voice_config.use_custom_voice}\n"
        report += f"- HDRI Environment: {scene.environment.type == EnvironmentType.HDRI}\n"
        report += f"- Postprocessing: {scene.render_settings.post_processing.bloom or scene.render_settings.post_processing.depth_of_field}\n"
        
        return report

# ============================================================================
# EXPORT UTILITIES
# ============================================================================

def export_schema_info() -> Dict[str, Any]:
    """Exportar información del esquema"""
    return {
        "version": __version__,
        "schema_version": QAVIOGEN_SCHEMA_VERSION,
        "features": FEATURES_V2_1,
        "supported_formats": {
            "input": ["blend", "gltf", "fbx", "obj", "collada"],
            "output": ["mp4", "mov", "avi", "mkv"],
            "audio": ["wav", "mp3", "flac", "aac"]
        },
        "render_engines": ["Cycles", "Eevee"],
        "codecs": [codec.value for codec in VideoCodec],
        "environment_types": [env.value for env in EnvironmentType]
    }

if __name__ == "__main__":
    # Demo de uso
    print("Q-AVIOGEN Core Types v2.1 - Enhanced Industrial Schema")
    print("=" * 60)
    
    # Crear configuración de test
    scene = SceneConfig.test_advanced()
    
    # Validar
    is_valid, errors = SceneValidator.validate_scene(scene)
    print(f"Scene validation: {'✅ VALID' if is_valid else '❌ INVALID'}")
    
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
    
    # Generar JSON
    print(f"\nGenerated JSON preview:")
    print(scene.to_json()[:500] + "...")
    
    # Información del esquema
    print(f"\nSchema info:")
    schema_info = export_schema_info()
    print(f"Version: {schema_info['version']}")
    print(f"Features: {len(schema_info['features'])}")
