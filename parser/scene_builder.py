"""
Scene Builder - Converts parsed procedure data into 3D scene descriptions
Construye descripciones de escenas 3D a partir de datos de procedimientos parseados
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class CameraType(Enum):
    """Available camera angles"""
    OVERVIEW = "overview"
    FRONT_VIEW = "front_view"
    SIDE_VIEW = "side_view"
    CLOSE_UP = "close_up"
    TOP_DOWN = "top_down"
    DEFAULT = "default"

class AnimationType(Enum):
    """Available animation types"""
    HIGHLIGHT = "highlight"
    MOVE = "move"
    ROTATE = "rotate"
    SCALE = "scale"
    SEQUENCE = "sequence"
    FADE = "fade"

@dataclass
class CameraConfig:
    """Camera configuration for a scene"""
    position: Tuple[float, float, float] = (0, 0, 5)
    target: Tuple[float, float, float] = (0, 0, 0)
    fov: float = 45.0
    type: CameraType = CameraType.DEFAULT

@dataclass
class LightConfig:
    """Lighting configuration"""
    type: str = "sun"  # sun, area, point, spot
    position: Tuple[float, float, float] = (5, 5, 5)
    energy: float = 3.0
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)

@dataclass
class MaterialConfig:
    """Material configuration for objects"""
    name: str = "default"
    color: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)
    metallic: float = 0.0
    roughness: float = 0.5
    emission: Tuple[float, float, float] = (0.0, 0.0, 0.0)

@dataclass
class ObjectConfig:
    """3D Object configuration"""
    name: str
    file_path: str = ""
    position: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    scale: Tuple[float, float, float] = (1, 1, 1)
    material: MaterialConfig = field(default_factory=MaterialConfig)
    visible: bool = True

@dataclass
class OverlayConfig:
    """Text overlay configuration"""
    text: str
    position: Tuple[float, float] = (0.1, 0.9)  # Screen coordinates (0-1)
    font_size: int = 24
    color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    background_color: Optional[Tuple[float, float, float, float]] = None
    duration: float = 0.0  # 0 = entire scene duration

@dataclass
class AnimationKeyframe:
    """Animation keyframe"""
    frame: int
    position: Optional[Tuple[float, float, float]] = None
    rotation: Optional[Tuple[float, float, float]] = None
    scale: Optional[Tuple[float, float, float]] = None
    material_properties: Optional[Dict[str, Any]] = None

@dataclass
class AnimationConfig:
    """Animation configuration"""
    object_name: str
    animation_type: AnimationType
    keyframes: List[AnimationKeyframe] = field(default_factory=list)
    duration_frames: int = 60
    interpolation: str = "LINEAR"  # LINEAR, BEZIER, CONSTANT

@dataclass
class SceneConfig:
    """Complete scene configuration"""
    name: str
    duration_seconds: float
    camera: CameraConfig = field(default_factory=CameraConfig)
    lights: List[LightConfig] = field(default_factory=list)
    objects: List[ObjectConfig] = field(default_factory=list)
    animations: List[AnimationConfig] = field(default_factory=list)
    overlays: List[OverlayConfig] = field(default_factory=list)
    audio_file: str = ""
    background_color: Tuple[float, float, float] = (0.2, 0.2, 0.2)

class SceneBuilder:
    """Builds 3D scene configurations from procedure data"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.assets_path = Path("assets")
        self.camera_presets = self._init_camera_presets()
        self.object_library = self._init_object_library()
        
    def _init_camera_presets(self) -> Dict[str, CameraConfig]:
        """Initialize camera preset configurations"""
        return {
            "default": CameraConfig(
                position=(0, -5, 3),
                target=(0, 0, 0),
                fov=45.0,
                type=CameraType.DEFAULT
            ),
            "overview": CameraConfig(
                position=(0, -8, 6),
                target=(0, 0, 0),
                fov=35.0,
                type=CameraType.OVERVIEW
            ),
            "front_view": CameraConfig(
                position=(0, -3, 0),
                target=(0, 0, 0),
                fov=50.0,
                type=CameraType.FRONT_VIEW
            ),
            "side_view": CameraConfig(
                position=(5, -2, 2),
                target=(0, 0, 0),
                fov=45.0,
                type=CameraType.SIDE_VIEW
            ),
            "close_up": CameraConfig(
                position=(0, -1.5, 1),
                target=(0, 0, 0),
                fov=60.0,
                type=CameraType.CLOSE_UP
            ),
            "top_down": CameraConfig(
                position=(0, 0, 8),
                target=(0, 0, 0),
                fov=40.0,
                type=CameraType.TOP_DOWN
            )
        }
    
    def _init_object_library(self) -> Dict[str, ObjectConfig]:
        """Initialize library of common objects"""
        return {
            "aircraft_bwb": ObjectConfig(
                name="BWB_Aircraft",
                file_path="models/bwb_q100.glb",
                position=(0, 0, 0),
                scale=(1, 1, 1)
            ),
            "towbar": ObjectConfig(
                name="Towbar",
                file_path="models/towbar.glb",
                position=(0, -2, 0),
                scale=(1, 1, 1)
            ),
            "nose_gear": ObjectConfig(
                name="NoseGear",
                file_path="models/nose_gear.glb",
                position=(0, 1.5, -0.5),
                scale=(1, 1, 1)
            ),
            "mechanic": ObjectConfig(
                name="Mechanic",
                file_path="models/mechanic.glb",
                position=(2, -1, 0),
                scale=(1, 1, 1)
            ),
            "tools": ObjectConfig(
                name="Tools",
                file_path="models/tools.glb",
                position=(1, -2, 0),
                scale=(1, 1, 1)
            )
        }
    
    def build_scenes(self, procedure_data: Dict[str, Any]) -> List[SceneConfig]:
        """Build scene configurations from procedure data"""
        scenes = []
        
        if self.debug:
            print(f"🎬 Construyendo escenas para: {procedure_data.get('title', 'Sin título')}")
        
        for i, step in enumerate(procedure_data.get('steps', [])):
            scene = self._build_scene_for_step(step, i, procedure_data)
            scenes.append(scene)
            
            if self.debug:
                print(f"  📹 Escena {i+1}: {scene.name} ({scene.duration_seconds}s)")
        
        return scenes
    
    def _build_scene_for_step(self, step: Dict[str, Any], step_index: int, procedure_data: Dict[str, Any]) -> SceneConfig:
        """Build a scene configuration for a single step"""
        
        # Basic scene setup
        scene = SceneConfig(
            name=f"scene_{step.get('id', f'step_{step_index+1}')}",
            duration_seconds=step.get('duration', 5.0)
        )
        
        # Configure camera
        camera_angle = step.get('camera_angle', 'default')
        scene.camera = self._get_camera_config(camera_angle)
        
        # Add default lighting
        scene.lights = self._get_default_lighting()
        
        # Add objects based on procedure context
        scene.objects = self._get_scene_objects(step, procedure_data)
        
        # Add overlays if specified
        if step.get('overlay_text'):
            overlay = OverlayConfig(
                text=step['overlay_text'],
                duration=scene.duration_seconds
            )
            scene.overlays.append(overlay)
        
        # Add animations if specified
        if 'animation' in step:
            animations = self._build_animations(step['animation'], scene.duration_seconds)
            scene.animations.extend(animations)
        
        # Set audio file reference
        scene.audio_file = f"audio/{step.get('id', f'step_{step_index+1}')}.wav"
        
        return scene
    
    def _get_camera_config(self, camera_angle: str) -> CameraConfig:
        """Get camera configuration for specified angle"""
        return self.camera_presets.get(camera_angle, self.camera_presets['default'])
    
    def _get_default_lighting(self) -> List[LightConfig]:
        """Get default lighting setup"""
        return [
            LightConfig(
                type="sun",
                position=(5, 5, 10),
                energy=3.0,
                color=(1.0, 0.98, 0.9)  # Slightly warm white
            ),
            LightConfig(
                type="area",
                position=(-3, -3, 5),
                energy=1.5,
                color=(0.9, 0.95, 1.0)  # Slightly cool fill light
            )
        ]
    
    def _get_scene_objects(self, step: Dict[str, Any], procedure_data: Dict[str, Any]) -> List[ObjectConfig]:
        """Get objects for the scene based on step and procedure context"""
        objects = []
        
        # Always include the aircraft
        aircraft_model = procedure_data.get('aircraft_model', '').lower()
        if 'bwb' in aircraft_model or 'q100' in aircraft_model:
            objects.append(self.object_library['aircraft_bwb'])
        
        # Add objects based on step content
        step_text = f"{step.get('title', '')} {step.get('description', '')}".lower()
        
        if 'towbar' in step_text:
            objects.append(self.object_library['towbar'])
        
        if 'nose gear' in step_text or 'landing gear' in step_text:
            objects.append(self.object_library['nose_gear'])
        
        if 'mechanic' in step_text or 'person' in step_text:
            objects.append(self.object_library['mechanic'])
        
        if 'tool' in step_text or 'wrench' in step_text:
            objects.append(self.object_library['tools'])
        
        return objects
    
    def _build_animations(self, animation_data: Dict[str, Any], duration_seconds: float) -> List[AnimationConfig]:
        """Build animation configurations from animation data"""
        animations = []
        duration_frames = int(duration_seconds * 30)  # Assume 30 FPS
        
        if animation_data.get('type') == 'highlight':
            # Create highlight animation
            target = animation_data.get('target', 'default')
            animation = AnimationConfig(
                object_name=target,
                animation_type=AnimationType.HIGHLIGHT,
                duration_frames=duration_frames
            )
            
            # Create keyframes for highlight effect
            animation.keyframes = [
                AnimationKeyframe(frame=0, material_properties={'emission': (0, 0, 0)}),
                AnimationKeyframe(frame=15, material_properties={'emission': (0.5, 0.5, 0)}),
                AnimationKeyframe(frame=duration_frames, material_properties={'emission': (0, 0, 0)})
            ]
            animations.append(animation)
        
        elif animation_data.get('type') == 'move':
            # Create movement animation
            target = animation_data.get('target', 'default')
            start_pos = animation_data.get('start_position', (0, 0, 0))
            end_pos = animation_data.get('end_position', (1, 0, 0))
            
            animation = AnimationConfig(
                object_name=target,
                animation_type=AnimationType.MOVE,
                duration_frames=duration_frames
            )
            
            animation.keyframes = [
                AnimationKeyframe(frame=0, position=start_pos),
                AnimationKeyframe(frame=duration_frames, position=end_pos)
            ]
            animations.append(animation)
        
        elif animation_data.get('type') == 'sequence':
            # Handle sequence of animations
            actions = animation_data.get('actions', [])
            frame_offset = 0
            
            for action in actions:
                action_duration = int(action.get('duration', 2.0) * 30)
                target = action.get('target', 'default')
                
                animation = AnimationConfig(
                    object_name=target,
                    animation_type=AnimationType(action.get('action', 'move')),
                    duration_frames=action_duration
                )
                
                # Add keyframes based on action type
                if action.get('action') == 'rotate':
                    animation.keyframes = [
                        AnimationKeyframe(frame=frame_offset, rotation=(0, 0, 0)),
                        AnimationKeyframe(frame=frame_offset + action_duration, 
                                        rotation=action.get('rotation', (0, 0, 90)))
                    ]
                
                animations.append(animation)
                frame_offset += action_duration
        
        return animations
    
    def export_scene(self, scene: SceneConfig, output_path: str) -> None:
        """Export scene configuration to JSON file"""
        # Convert scene to dictionary for JSON serialization
        scene_dict = {
            'name': scene.name,
            'duration_seconds': scene.duration_seconds,
            'camera': {
                'position': scene.camera.position,
                'target': scene.camera.target,
                'fov': scene.camera.fov,
                'type': scene.camera.type.value
            },
            'lights': [
                {
                    'type': light.type,
                    'position': light.position,
                    'energy': light.energy,
                    'color': light.color
                }
                for light in scene.lights
            ],
            'objects': [
                {
                    'name': obj.name,
                    'file_path': obj.file_path,
                    'position': obj.position,
                    'rotation': obj.rotation,
                    'scale': obj.scale,
                    'visible': obj.visible,
                    'material': {
                        'name': obj.material.name,
                        'color': obj.material.color,
                        'metallic': obj.material.metallic,
                        'roughness': obj.material.roughness,
                        'emission': obj.material.emission
                    }
                }
                for obj in scene.objects
            ],
            'animations': [
                {
                    'object_name': anim.object_name,
                    'animation_type': anim.animation_type.value,
                    'duration_frames': anim.duration_frames,
                    'interpolation': anim.interpolation,
                    'keyframes': [
                        {
                            'frame': kf.frame,
                            'position': kf.position,
                            'rotation': kf.rotation,
                            'scale': kf.scale,
                            'material_properties': kf.material_properties
                        }
                        for kf in anim.keyframes
                    ]
                }
                for anim in scene.animations
            ],
            'overlays': [
                {
                    'text': overlay.text,
                    'position': overlay.position,
                    'font_size': overlay.font_size,
                    'color': overlay.color,
                    'background_color': overlay.background_color,
                    'duration': overlay.duration
                }
                for overlay in scene.overlays
            ],
            'audio_file': scene.audio_file,
            'background_color': scene.background_color
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scene_dict, f, indent=2, ensure_ascii=False)
        
        if self.debug:
            print(f"📁 Escena exportada a: {output_path}")

# Example usage and testing
if __name__ == "__main__":
    # Test scene builder with sample data
    sample_procedure = {
        'id': '00-30-10-01',
        'title': 'Towbar Attachment Test',
        'aircraft_model': 'BWB-Q100',
        'steps': [
            {
                'id': 'step_01',
                'title': 'Position Towbar',
                'description': 'Position the towbar near the nose gear',
                'duration': 5.0,
                'camera_angle': 'overview',
                'overlay_text': 'Clearance: 10cm minimum',
                'animation': {
                    'type': 'highlight',
                    'target': 'towbar',
                    'duration': 2.0
                }
            },
            {
                'id': 'step_02',
                'title': 'Attach Connection',
                'description': 'Secure the towbar to nose gear',
                'duration': 8.0,
                'camera_angle': 'close_up',
                'overlay_text': 'Torque: 100Nm',
                'animation': {
                    'type': 'sequence',
                    'actions': [
                        {'action': 'move', 'target': 'towbar', 'duration': 3.0},
                        {'action': 'rotate', 'target': 'connector', 'duration': 2.0}
                    ]
                }
            }
        ]
    }
    
    builder = SceneBuilder(debug=True)
    scenes = builder.build_scenes(sample_procedure)
    
    print(f"\n📋 Escenas generadas: {len(scenes)}")
    for i, scene in enumerate(scenes):
        print(f"  Escena {i+1}: {scene.name}")
        print(f"    Duración: {scene.duration_seconds}s")
        print(f"    Objetos: {len(scene.objects)}")
        print(f"    Animaciones: {len(scene.animations)}")
        print(f"    Overlays: {len(scene.overlays)}")
        
        # Export scene for testing
        output_path = f"test_scene_{i+1}.json"
        builder.export_scene(scene, output_path)
