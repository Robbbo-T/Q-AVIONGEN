"""
Blender Renderer - Advanced 3D scene renderer with enterprise features
Renderizador avanzado de escenas 3D con características empresariales
"""

import bpy
import bmesh
import os
import sys
import json
import math
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from mathutils import Vector, Euler
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.types import (
    SceneConfig, RenderSettings, RenderMetadata, RenderQuality,
    CameraConfig, LightConfig, ObjectConfig, MaterialConfig,
    AnimationConfig, OverlayConfig
)
from core.errors import (
    QAvioGenLogger, AssetImportError, RenderError, SceneConfigError,
    handle_errors, get_logger
)

class BlenderRenderer:
    """Blender-based 3D scene renderer"""
    
    # Constants
    PRINCIPLED_BSDF = 'Principled BSDF'
    
    def __init__(self, resolution: str = "1080p", fps: int = 30, output_format: str = "mp4"):
        self.resolution = self._parse_resolution(resolution)
        self.fps = fps
        self.output_format = output_format
        
        # Initialize Blender scene
        self._setup_blender_scene()
        
    def _parse_resolution(self, resolution: str) -> Tuple[int, int]:
        """Parse resolution string to width, height tuple"""
        resolutions = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160)
        }
        return resolutions.get(resolution, (1920, 1080))
    
    def _setup_blender_scene(self):
        """Setup basic Blender scene configuration"""
        # Clear existing mesh objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)
        
        # Set render settings
        scene = bpy.context.scene
        scene.render.resolution_x = self.resolution[0]
        scene.render.resolution_y = self.resolution[1]
        scene.render.fps = self.fps
        
        # Set render engine to Cycles for better quality
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU' if self._gpu_available() else 'CPU'
        
        # Enable motion blur and other quality settings
        scene.render.use_motion_blur = True
        scene.cycles.samples = 128  # Balanced quality/speed
        
        print(f"🎬 Blender configurado: {self.resolution[0]}x{self.resolution[1]} @ {self.fps}fps")
    
    def _gpu_available(self) -> bool:
        """Check if GPU rendering is available"""
        try:
            preferences = bpy.context.preferences
            cycles_preferences = preferences.addons['cycles'].preferences
            return len(cycles_preferences.devices) > 0
        except Exception:
            return False
    
    def render_video(self, scenes: List[Any], audio_files: List[str], output_dir: str) -> str:
        """Render complete video from scene configurations"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate unique output filename
        output_file = output_path / f"procedure_{hash(str(scenes))}.{self.output_format}"
        
        print(f"🎥 Iniciando renderizado de {len(scenes)} escenas")
        
        frame_offset = 1
        total_frames = 0
        
        # Process each scene
        for i, scene_config in enumerate(scenes):
            print(f"📹 Renderizando escena {i+1}/{len(scenes)}: {scene_config.name}")
            
            # Load scene configuration
            self._load_scene_config(scene_config)
            
            # Calculate frame range for this scene
            scene_duration = scene_config.duration_seconds
            scene_frames = int(scene_duration * self.fps)
            end_frame = frame_offset + scene_frames - 1
            
            # Set frame range
            bpy.context.scene.frame_start = frame_offset
            bpy.context.scene.frame_end = end_frame
            
            # Setup animations for this scene
            self._setup_scene_animations(scene_config, frame_offset)
            
            # Setup audio if available
            if i < len(audio_files) and audio_files[i]:
                self._add_audio_strip(audio_files[i], frame_offset, scene_frames)
            
            frame_offset = end_frame + 1
            total_frames = end_frame
        
        # Set final frame range
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = total_frames
        
        # Render video
        self._render_animation(str(output_file))
        
        print(f"🎉 Renderizado completado: {output_file}")
        return str(output_file)
    
    def _load_scene_config(self, scene_config):
        """Load scene configuration into Blender"""
        # Clear current scene objects (keep camera and lights)
        self._clear_scene_objects()
        
        # Setup camera
        self._setup_camera(scene_config.camera)
        
        # Setup lighting
        self._setup_lighting(scene_config.lights)
        
        # Load 3D objects
        self._load_scene_objects(scene_config.objects)
        
        # Setup materials and textures
        self._setup_materials(scene_config.objects)
        
        # Setup overlays (text objects)
        self._setup_overlays(scene_config.overlays)
        
        # Set background
        self._setup_background(scene_config.background_color)
    
    def _clear_scene_objects(self):
        """Clear all mesh objects from scene"""
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.delete()
    
    def _setup_camera(self, camera_config):
        """Setup camera based on configuration"""
        # Create or get camera
        if 'Camera' not in bpy.data.objects:
            bpy.ops.object.camera_add()
            camera = bpy.context.active_object
            camera.name = 'Camera'
        else:
            camera = bpy.data.objects['Camera']
        
        # Set camera position and rotation
        position = camera_config.position
        target = camera_config.target
        fov = camera_config.fov
        
        camera.location = position
        
        # Point camera at target
        direction = Vector(target) - Vector(position)
        camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
        # Set field of view
        camera.data.angle = math.radians(fov)
        
        # Set as active camera
        bpy.context.scene.camera = camera
    
    def _setup_lighting(self, lights_config):
        """Setup lighting based on configuration"""
        # Remove existing lights
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj, do_unlink=True)
        
        # Add configured lights
        for i, light_config in enumerate(lights_config):
            light_type = light_config.type
            position = light_config.position
            energy = light_config.energy
            color = light_config.color
            
            # Create light
            bpy.ops.object.light_add(type=light_type.upper(), location=position)
            light = bpy.context.active_object
            light.name = f"Light_{i+1}"
            
            # Configure light properties
            light.data.energy = energy
            light.data.color = color[:3]  # RGB only
            
            if light_type.upper() == 'SUN':
                light.data.angle = math.radians(5)  # Sun angular diameter
    
    def _load_scene_objects(self, objects_config):
        """Load 3D objects into the scene"""
        for obj_config in objects_config:
            if not obj_config.visible:
                continue
                
            obj_name = obj_config.name
            file_path = obj_config.file_path
            position = obj_config.position
            rotation = obj_config.rotation
            scale = obj_config.scale
            
            # Try to load from file or create placeholder
            obj = self._load_or_create_object(obj_name, file_path)
            
            if obj:
                # Set transform
                obj.location = position
                obj.rotation_euler = rotation
                obj.scale = scale
    
    def _load_or_create_object(self, name: str, file_path: str) -> Optional[object]:
        """Load object from file or create placeholder"""
        if file_path and os.path.exists(file_path):
            # Try to import the file
            try:
                if file_path.endswith('.glb') or file_path.endswith('.gltf'):
                    bpy.ops.import_scene.gltf(filepath=file_path)
                elif file_path.endswith('.obj'):
                    bpy.ops.import_scene.obj(filepath=file_path)
                elif file_path.endswith('.fbx'):
                    bpy.ops.import_scene.fbx(filepath=file_path)
                
                # Get the imported object
                obj = bpy.context.active_object
                if obj:
                    obj.name = name
                    return obj
            except Exception as e:
                print(f"⚠️ Error cargando {file_path}: {e}")
        
        # Create placeholder object
        return self._create_placeholder_object(name)
    
    def _create_placeholder_object(self, name: str) -> object:
        """Create a placeholder object when asset is not available"""
        # Create different shapes based on object name
        if 'aircraft' in name.lower() or 'bwb' in name.lower():
            # Create aircraft-like shape
            bpy.ops.mesh.primitive_cube_add(size=4)
            obj = bpy.context.active_object
            obj.scale = (4, 2, 0.5)
        elif 'towbar' in name.lower():
            # Create towbar-like shape
            bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=3)
            obj = bpy.context.active_object
            obj.rotation_euler = (0, math.radians(90), 0)
        elif 'gear' in name.lower():
            # Create gear-like shape
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1)
            obj = bpy.context.active_object
        elif 'tool' in name.lower():
            # Create tool-like shape
            bpy.ops.mesh.primitive_cube_add(size=0.5)
            obj = bpy.context.active_object
            obj.scale = (0.3, 0.3, 1.5)
        else:
            # Default cube
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.active_object
        
        obj.name = name
        
        # Add basic material
        material = bpy.data.materials.new(name=f"{name}_material")
        material.use_nodes = True
        obj.data.materials.append(material)
        
        return obj
    
    def _setup_materials(self, objects_config):
        """Setup materials for objects"""
        for obj_config in objects_config:
            obj_name = obj_config.name
            material_config = obj_config.material
            
            if obj_name in bpy.data.objects:
                obj = bpy.data.objects[obj_name]
                self._apply_material(obj, material_config)
    
    def _apply_material(self, obj: object, material_config):
        """Apply material configuration to object"""
        if not obj.data.materials:
            material = bpy.data.materials.new(name=f"{obj.name}_material")
            material.use_nodes = True
            obj.data.materials.append(material)
        else:
            material = obj.data.materials[0]
        
        if material.use_nodes:
            nodes = material.node_tree.nodes
            principled = nodes.get(self.PRINCIPLED_BSDF)
            
            if principled:
                # Set material properties
                color = material_config.color
                principled.inputs['Base Color'].default_value = color
                
                metallic = material_config.metallic
                principled.inputs['Metallic'].default_value = metallic
                
                roughness = material_config.roughness
                principled.inputs['Roughness'].default_value = roughness
                
                emission = material_config.emission
                if any(emission):
                    principled.inputs['Emission'].default_value = (*emission, 1.0)
    
    def _setup_overlays(self, overlays_config):
        """Setup text overlays"""
        for i, overlay_config in enumerate(overlays_config):
            text_content = overlay_config.text
            if not text_content:
                continue
            
            # Create text object
            bpy.ops.object.text_add()
            text_obj = bpy.context.active_object
            text_obj.name = f"Overlay_{i+1}"
            
            # Set text content
            text_obj.data.body = text_content
            
            # Position text (convert screen coordinates to 3D)
            position = overlay_config.position
            # For now, position in 3D space - later can be converted to screen space
            text_obj.location = (position[0] * 10 - 5, position[1] * 10 - 5, 5)
            
            # Set text properties
            font_size = overlay_config.font_size
            text_obj.data.size = font_size / 100.0  # Blender text size scaling
            
            # Create material for text
            material = bpy.data.materials.new(name=f"text_material_{i}")
            material.use_nodes = True
            color = overlay_config.color
            
            nodes = material.node_tree.nodes
            principled = nodes.get('Principled BSDF')
            if principled:
                principled.inputs['Base Color'].default_value = color
                principled.inputs['Emission'].default_value = color
            
            text_obj.data.materials.append(material)
    
    def _setup_background(self, background_color: Tuple[float, float, float]):
        """Setup scene background"""
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        
        world.use_nodes = True
        bg_node = world.node_tree.nodes.get('Background')
        if bg_node:
            bg_node.inputs['Color'].default_value = (*background_color, 1.0)
    
    def _setup_scene_animations(self, scene_config, frame_offset: int):
        """Setup animations for the current scene"""
        animations = scene_config.animations
        
        for anim_config in animations:
            obj_name = anim_config.object_name
            if obj_name not in bpy.data.objects:
                continue
            
            obj = bpy.data.objects[obj_name]
            keyframes = anim_config.keyframes
            
            # Clear existing animation data
            obj.animation_data_clear()
            
            # Create keyframes
            for keyframe in keyframes:
                frame = keyframe.frame + frame_offset
                
                # Set current frame
                bpy.context.scene.frame_set(frame)
                
                # Apply transformations
                if keyframe.position:
                    obj.location = keyframe.position
                    obj.keyframe_insert(data_path="location")
                
                if keyframe.rotation:
                    obj.rotation_euler = keyframe.rotation
                    obj.keyframe_insert(data_path="rotation_euler")
                
                if keyframe.scale:
                    obj.scale = keyframe.scale
                    obj.keyframe_insert(data_path="scale")
                
                # Apply material properties
                material_props = keyframe.material_properties
                if material_props and obj.data.materials:
                    material = obj.data.materials[0]
                    if material.use_nodes:
                        principled = material.node_tree.nodes.get(self.PRINCIPLED_BSDF)
                        if principled and 'emission' in material_props:
                            emission = material_props['emission']
                            principled.inputs['Emission'].default_value = (*emission, 1.0)
                            principled.inputs['Emission'].keyframe_insert(index=-1)
    
    def _add_audio_strip(self, audio_file: str, frame_start: int, duration_frames: int):
        """Add audio strip to video sequence editor"""
        if not os.path.exists(audio_file):
            print(f"⚠️ Archivo de audio no encontrado: {audio_file}")
            return
        
        # Switch to Video Sequence Editor
        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
        
        seq_editor = bpy.context.scene.sequence_editor
        
        # Add audio strip
        try:
            audio_strip = seq_editor.sequences.new_sound(
                name=f"audio_{frame_start}",
                filepath=audio_file,
                channel=1,
                frame_start=frame_start
            )
            print(f"🎵 Audio añadido: {audio_file} (frame {frame_start})")
        except Exception as e:
            print(f"⚠️ Error añadiendo audio: {e}")
    
    def _render_animation(self, output_path: str):
        """Render the complete animation"""
        # Set output settings
        scene = bpy.context.scene
        scene.render.filepath = output_path.replace(f'.{self.output_format}', '')
        
        if self.output_format == 'mp4':
            scene.render.image_settings.file_format = 'FFMPEG'
            scene.render.ffmpeg.format = 'MPEG4'
            scene.render.ffmpeg.codec = 'H264'
        elif self.output_format == 'webm':
            scene.render.image_settings.file_format = 'FFMPEG'
            scene.render.ffmpeg.format = 'WEBM'
            scene.render.ffmpeg.codec = 'WEBM'
        
        # Render animation
        print(f"🎬 Iniciando renderizado final...")
        bpy.ops.render.render(animation=True)
        print(f"✅ Renderizado completado")

# Import math for mathematical operations
import math

# Test function when run directly
def test_renderer():
    """Test the Blender renderer with sample data"""
    # This would only work if run inside Blender
    try:
        renderer = BlenderRenderer()
        print("✅ BlenderRenderer inicializado correctamente")
        
        # Test basic scene setup
        sample_scene = {
            'name': 'test_scene',
            'duration_seconds': 5.0,
            'camera': {
                'position': (0, -5, 3),
                'target': (0, 0, 0),
                'fov': 45.0
            },
            'lights': [
                {
                    'type': 'sun',
                    'position': (5, 5, 10),
                    'energy': 3.0,
                    'color': (1.0, 1.0, 1.0)
                }
            ],
            'objects': [
                {
                    'name': 'test_cube',
                    'position': (0, 0, 0),
                    'scale': (1, 1, 1),
                    'visible': True
                }
            ]
        }
        
        renderer._load_scene_config(sample_scene)
        print("✅ Configuración de escena cargada")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")

if __name__ == "__main__":
    # Only run test if we're inside Blender
    if "bpy" in sys.modules:
        test_renderer()
    else:
        print("ℹ️ Este módulo debe ejecutarse desde Blender para testing completo")
        print("✅ Módulo BlenderRenderer importado correctamente")
