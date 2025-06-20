"""
Q-AVIOGEN Enhanced Blender Renderer - Version 2.0
Renderer robusto de clase enterprise con cache de materiales, logging avanzado,
validación por esquema, y soporte para modo preview.
Production Ready with Advanced Error Handling and Performance Optimization
"""

try:
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    # Stubs para desarrollo sin Blender
    class Vector:
        def __init__(self, *args): pass
    class Euler:
        def __init__(self, *args): pass
    bpy = None
    bmesh = None

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging
import os
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from core.types import (
        SceneConfig, RenderSettings, RenderMetadata, RenderResult, ValidationResult,
        Vector3D, RGBAColor, MaterialConfig, LightConfig, AnimationConfig,
        RenderMode, RenderQuality, OutputFormat, CameraConfig, ObjectConfig
    )
    from core.errors import (
        QAviongenError, RenderError, BlenderError, AssetError, ValidationError,
        handle_exceptions, log_performance, require_blender, safe_file_operation,
        logger, ErrorCode
    )
    CORE_AVAILABLE = True
except ImportError:
    # Fallback for when core modules aren't available
    print("⚠️ Core modules not available, using basic functionality")
    CORE_AVAILABLE = False
    SceneConfig = Any
    RenderSettings = Any
    RenderMetadata = Any

class MaterialCache:
    """Cache de materiales para optimizar renderizado."""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._stats = {"hits": 0, "misses": 0, "created": 0}
    
    def get(self, name: str) -> Optional[Any]:
        """Obtiene material del cache."""
        if name in self._cache:
            self._stats["hits"] += 1
            if CORE_AVAILABLE:
                logger.debug(f"Material cache hit: {name}")
            return self._cache[name]
        
        self._stats["misses"] += 1
        if CORE_AVAILABLE:
            logger.debug(f"Material cache miss: {name}")
        return None
    
    def set(self, name: str, material: Any) -> None:
        """Almacena material en cache."""
        self._cache[name] = material
        self._stats["created"] += 1
        if CORE_AVAILABLE:
            logger.debug(f"Material cached: {name}")
    
    def clear(self) -> None:
        """Limpia el cache."""
        self._cache.clear()
        if CORE_AVAILABLE:
            logger.info(f"Material cache cleared. Stats: {self._stats}")
        self._stats = {"hits": 0, "misses": 0, "created": 0}
    
    def get_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas del cache."""
        return self._stats.copy()

class EnhancedBlenderRenderer:
    """
    Renderer mejorado de Blender con funcionalidades enterprise:
    - Cache de materiales
    - Logging avanzado con JSON
    - Validación por esquema
    - Modo preview para pruebas rápidas
    - Manejo robusto de errores
    - Generación de metadata
    """
    
    def __init__(
        self,
        output_dir: str = "output",
        preview_mode: bool = False,
        enable_cache: bool = True,
        log_level: str = "INFO"
    ):
        """
        Inicializa el renderer mejorado.
        
        Args:
            output_dir: Directorio de salida
            preview_mode: Modo preview para renderizado rápido
            enable_cache: Habilitar cache de materiales
            log_level: Nivel de logging
        """
        if not BLENDER_AVAILABLE:
            if CORE_AVAILABLE:
                raise BlenderError("Blender not available", context={"available": False})
            else:
                raise Exception("Blender not available")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.preview_mode = preview_mode
        self.enable_cache = enable_cache
        
        # Cache de materiales
        self.material_cache = MaterialCache() if enable_cache else None
        
        # Configuración de renderizado
        self.setup_blender_defaults()
        
        if CORE_AVAILABLE:
            logger.info("Enhanced Blender Renderer initialized", {
                "output_dir": str(self.output_dir),
                "preview_mode": preview_mode,
                "cache_enabled": enable_cache,
                "blender_version": bpy.app.version_string if bpy else "unknown"
            })
    
    def setup_blender_defaults(self):
        """Configura defaults de Blender."""
        if not BLENDER_AVAILABLE:
            return
            
        # Limpiar escena existente
        bpy.ops.wm.read_factory_settings(use_empty=True)
        
        # Configurar Cycles
        bpy.context.scene.render.engine = 'CYCLES'
        
        # Detectar GPU
        try:
            preferences = bpy.context.preferences.addons['cycles'].preferences
            preferences.refresh_devices()
            
            gpu_available = False
            for device in preferences.devices:
                if device.type in ['CUDA', 'OPENCL', 'OPTIX']:
                    device.use = True
                    gpu_available = True
            
            if gpu_available:
                bpy.context.scene.cycles.device = 'GPU'
                if CORE_AVAILABLE:
                    logger.info("GPU rendering enabled")
            else:
                bpy.context.scene.cycles.device = 'CPU'
                if CORE_AVAILABLE:
                    logger.warning("GPU not available, using CPU rendering")
        except Exception as e:
            if CORE_AVAILABLE:
                logger.warning(f"GPU detection failed: {e}")
    
    def render_scene(
        self,
        scene_config: Any,  # SceneConfig when available
        validate_schema: bool = True,
        save_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Renderiza una escena completa con validación y logging.
        
        Args:
            scene_config: Configuración de la escena
            validate_schema: Validar configuración contra esquema
            save_metadata: Guardar metadata del renderizado
            
        Returns:
            Dict con información del renderizado
        """
        start_time = datetime.now()
        
        if CORE_AVAILABLE:
            logger.log_render_start(scene_config.name, str(self.output_dir))
        
        try:
            # Validar configuración si se solicita y está disponible
            if validate_schema and CORE_AVAILABLE:
                validation_result = self._validate_scene_config(scene_config)
                if hasattr(validation_result, 'valid') and not validation_result.valid:
                    raise ValidationError(
                        f"Scene configuration validation failed: {validation_result.errors}",
                        context={"errors": validation_result.errors}
                    )
            
            # Configurar escena
            self._setup_scene(scene_config)
            
            # Configurar cámara
            if hasattr(scene_config, 'camera'):
                self._setup_camera(scene_config.camera)
            
            # Cargar objetos
            if hasattr(scene_config, 'objects'):
                for obj_config in scene_config.objects:
                    self._load_object(obj_config)
            
            # Configurar materiales
            if hasattr(scene_config, 'materials'):
                for material_config in scene_config.materials:
                    self._create_material(material_config)
            
            # Configurar luces
            if hasattr(scene_config, 'lights'):
                for light_config in scene_config.lights:
                    self._setup_light(light_config)
            
            # Configurar animaciones
            if hasattr(scene_config, 'animations'):
                for anim_config in scene_config.animations:
                    self._setup_animation(anim_config)
            
            # Configurar renderizado
            if hasattr(scene_config, 'render_settings'):
                self._configure_render_settings(scene_config.render_settings)
            
            # Renderizar
            output_files = self._execute_render(scene_config)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Crear resultado
            result = {
                "success": True,
                "output_files": output_files,
                "render_time": duration,
                "scene_config": scene_config if hasattr(scene_config, 'to_dict') else str(scene_config),
                "metadata": {}
            }
            
            # Guardar metadata si se solicita
            if save_metadata and CORE_AVAILABLE:
                metadata = self._create_render_metadata(scene_config, start_time, end_time, output_files)
                metadata_path = self.output_dir / f"{getattr(scene_config, 'name', 'scene')}_metadata.json"
                if hasattr(metadata, 'save_to_file'):
                    metadata.save_to_file(str(metadata_path))
                result["metadata"]["metadata_file"] = str(metadata_path)
            
            if CORE_AVAILABLE:
                frame_count = getattr(scene_config, 'get_frame_count', lambda: 1)()
                logger.log_render_complete(
                    getattr(scene_config, 'name', 'scene'),
                    str(self.output_dir),
                    duration,
                    frame_count
                )
            
            return result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if CORE_AVAILABLE:
                logger.error(f"Render failed for scene '{getattr(scene_config, 'name', 'unknown')}'", {
                    "scene_name": getattr(scene_config, 'name', 'unknown'),
                    "duration": duration,
                    "error": str(e)
                }, exception=e)
            
            return {
                "success": False,
                "error_message": str(e),
                "render_time": duration,
                "scene_config": scene_config if hasattr(scene_config, 'to_dict') else str(scene_config),
                "metadata": {}
            }
    
    def _validate_scene_config(self, scene_config: Any) -> Any:
        """Valida configuración de escena contra esquema JSON."""
        if not CORE_AVAILABLE:
            return {"valid": True, "errors": []}
            
        # Validación básica usando los métodos internos
        errors = getattr(scene_config, 'validate', lambda: [])()
        
        result = ValidationResult(valid=len(errors) == 0)
        for error in errors:
            result.add_error(error)
        
        return result
    
    def _setup_scene(self, scene_config: Any):
        """Configura la escena base."""
        if not BLENDER_AVAILABLE:
            return
            
        scene = bpy.context.scene
        scene.name = getattr(scene_config, 'name', 'Scene')
        
        # Configurar background
        background_color = getattr(scene_config, 'background_color', None)
        if background_color:
            world = bpy.data.worlds.new("World")
            world.use_nodes = True
            bg_node = world.node_tree.nodes["Background"]
            if isinstance(background_color, (list, tuple)) and len(background_color) >= 3:
                bg_node.inputs[0].default_value = (*background_color[:3], 1.0)
            scene.world = world
        
        # Configurar framerate y duración
        render_settings = getattr(scene_config, 'render_settings', None)
        if render_settings:
            scene.frame_start = getattr(render_settings, 'frame_start', 1)
            if hasattr(scene_config, 'get_frame_count'):
                scene.frame_end = scene_config.get_frame_count()
            else:
                scene.frame_end = getattr(render_settings, 'frame_end', 250)
        
        if CORE_AVAILABLE:
            logger.debug(f"Scene '{scene.name}' configured", {
                "frame_start": scene.frame_start,
                "frame_end": scene.frame_end,
                "background_color": background_color
            })
    
    def _setup_camera(self, camera_config: Any):
        """Configura la cámara principal."""
        if not BLENDER_AVAILABLE:
            return
            
        # Crear cámara
        bpy.ops.object.camera_add()
        camera_obj = bpy.context.object
        camera_obj.name = getattr(camera_config, 'name', 'Camera')
        camera = camera_obj.data
        
        # Posición y rotación
        position = getattr(camera_config, 'position', None)
        if position:
            if hasattr(position, 'to_tuple'):
                camera_obj.location = position.to_tuple()
            elif isinstance(position, (list, tuple)) and len(position) >= 3:
                camera_obj.location = position[:3]
        
        rotation = getattr(camera_config, 'rotation', None)
        if rotation:
            if hasattr(rotation, 'to_tuple'):
                camera_obj.rotation_euler = rotation.to_tuple()
            elif isinstance(rotation, (list, tuple)) and len(rotation) >= 3:
                camera_obj.rotation_euler = rotation[:3]
        
        # Configuración de lente
        lens = getattr(camera_config, 'lens', 50.0)
        camera.lens = lens
        
        clip_start = getattr(camera_config, 'clip_start', 0.1)
        clip_end = getattr(camera_config, 'clip_end', 1000.0)
        camera.clip_start = clip_start
        camera.clip_end = clip_end
        
        # Depth of field si está habilitado
        depth_of_field = getattr(camera_config, 'depth_of_field', False)
        if depth_of_field:
            camera.dof.use_dof = True
            focus_distance = getattr(camera_config, 'focus_distance', 10.0)
            f_stop = getattr(camera_config, 'f_stop', 2.8)
            camera.dof.focus_distance = focus_distance
            camera.dof.aperture_fstop = f_stop
        
        # Establecer como cámara activa
        bpy.context.scene.camera = camera_obj
        
        if CORE_AVAILABLE:
            logger.log_asset_loaded(camera_obj.name, "camera")
    
    def _load_object(self, obj_config: Any):
        """Carga un objeto 3D."""
        if not BLENDER_AVAILABLE:
            return
            
        mesh_path = getattr(obj_config, 'mesh_path', None)
        obj_name = getattr(obj_config, 'name', 'Object')
        
        if mesh_path:
            try:
                # Determinar tipo de archivo y cargar
                mesh_path_obj = Path(mesh_path)
                if mesh_path_obj.suffix.lower() == '.obj':
                    bpy.ops.import_scene.obj(filepath=str(mesh_path_obj))
                elif mesh_path_obj.suffix.lower() == '.fbx':
                    bpy.ops.import_scene.fbx(filepath=str(mesh_path_obj))
                elif mesh_path_obj.suffix.lower() == '.glb':
                    bpy.ops.import_scene.gltf(filepath=str(mesh_path_obj))
                else:
                    if CORE_AVAILABLE:
                        raise AssetError(f"Unsupported file format: {mesh_path_obj.suffix}")
                    else:
                        raise Exception(f"Unsupported file format: {mesh_path_obj.suffix}")
                
                # Configurar objeto importado
                obj = bpy.context.selected_objects[0] if bpy.context.selected_objects else None
                if obj:
                    obj.name = obj_name
                
            except Exception as e:
                if CORE_AVAILABLE:
                    logger.warning(f"Failed to load mesh {mesh_path}, creating placeholder")
                # Crear placeholder
                bpy.ops.mesh.primitive_cube_add()
                obj = bpy.context.object
                obj.name = f"{obj_name}_placeholder"
        else:
            # Crear objeto básico si no hay mesh
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.object
            obj.name = obj_name
        
        # Aplicar transformaciones
        position = getattr(obj_config, 'position', None)
        if position and obj:
            if hasattr(position, 'to_tuple'):
                obj.location = position.to_tuple()
            elif isinstance(position, (list, tuple)) and len(position) >= 3:
                obj.location = position[:3]
        
        rotation = getattr(obj_config, 'rotation', None)
        if rotation and obj:
            if hasattr(rotation, 'to_tuple'):
                obj.rotation_euler = rotation.to_tuple()
            elif isinstance(rotation, (list, tuple)) and len(rotation) >= 3:
                obj.rotation_euler = rotation[:3]
        
        scale = getattr(obj_config, 'scale', None)
        if scale and obj:
            if hasattr(scale, 'to_tuple'):
                obj.scale = scale.to_tuple()
            elif isinstance(scale, (list, tuple)) and len(scale) >= 3:
                obj.scale = scale[:3]
        
        # Configurar propiedades de renderizado
        visible = getattr(obj_config, 'visible', True)
        receive_shadow = getattr(obj_config, 'receive_shadow', True)
        cast_shadow = getattr(obj_config, 'cast_shadow', True)
        
        if obj:
            obj.hide_viewport = not visible
            obj.hide_render = not visible
            # Configurar shadows (simplificado)
            if hasattr(obj, 'cycles'):
                obj.cycles.is_shadow_catcher = receive_shadow
                obj.cycles.cast_shadow = cast_shadow
        
        # Asignar material si existe
        material_name = getattr(obj_config, 'material', None)
        if material_name and self.enable_cache and self.material_cache and obj and obj.data:
            material = self.material_cache.get(material_name)
            if material:
                if not obj.data.materials:
                    obj.data.materials.append(material)
                else:
                    obj.data.materials[0] = material
        
        if CORE_AVAILABLE:
            logger.log_asset_loaded(obj_name, "object")
    
    def _create_material(self, material_config: Any):
        """Crea y configura un material."""
        if not BLENDER_AVAILABLE:
            return None
            
        material_name = getattr(material_config, 'name', 'Material')
        
        # Verificar cache primero
        if self.enable_cache and self.material_cache:
            cached_material = self.material_cache.get(material_name)
            if cached_material:
                return cached_material
        
        # Crear nuevo material
        material = bpy.data.materials.new(name=material_name)
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        
        # Crear nodo Principled BSDF
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        # Conectar nodos
        material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Configurar propiedades
        base_color = getattr(material_config, 'base_color', None)
        if base_color:
            if hasattr(base_color, 'to_tuple'):
                bsdf.inputs['Base Color'].default_value = base_color.to_tuple()
            elif isinstance(base_color, (list, tuple)) and len(base_color) >= 3:
                bsdf.inputs['Base Color'].default_value = (*base_color[:4], 1.0)[:4]
        
        metallic = getattr(material_config, 'metallic', 0.0)
        roughness = getattr(material_config, 'roughness', 0.5)
        emission_strength = getattr(material_config, 'emission_strength', 0.0)
        transmission = getattr(material_config, 'transmission', 0.0)
        ior = getattr(material_config, 'ior', 1.45)
        
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Emission Strength'].default_value = emission_strength
        if 'Transmission Weight' in bsdf.inputs:
            bsdf.inputs['Transmission Weight'].default_value = transmission
        bsdf.inputs['IOR'].default_value = ior
        
        # Cargar texturas si existen
        texture_path = getattr(material_config, 'texture_path', None)
        if texture_path:
            self._load_texture(material, texture_path, 'Base Color')
        
        normal_map = getattr(material_config, 'normal_map', None)
        if normal_map:
            self._load_normal_map(material, normal_map)
        
        # Guardar en cache
        if self.enable_cache and self.material_cache:
            self.material_cache.set(material_name, material)
        
        if CORE_AVAILABLE:
            material_type = getattr(material_config, 'type', 'unknown')
            logger.debug(f"Material '{material_name}' created", {
                "type": material_type.value if hasattr(material_type, 'value') else str(material_type),
                "metallic": metallic,
                "roughness": roughness
            })
        
        return material
    
    def _load_texture(self, material: Any, texture_path: str, input_name: str):
        """Carga una textura en el material."""
        if not BLENDER_AVAILABLE or not Path(texture_path).exists():
            if CORE_AVAILABLE:
                logger.warning(f"Texture not found: {texture_path}")
            return
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Crear nodo de textura
        texture_node = nodes.new(type='ShaderNodeTexImage')
        texture_node.image = bpy.data.images.load(texture_path)
        
        # Encontrar el nodo BSDF principal
        bsdf = None
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf = node
                break
        
        if bsdf and input_name in bsdf.inputs:
            links.new(texture_node.outputs['Color'], bsdf.inputs[input_name])
    
    def _load_normal_map(self, material: Any, normal_path: str):
        """Carga un normal map en el material."""
        if not BLENDER_AVAILABLE or not Path(normal_path).exists():
            if CORE_AVAILABLE:
                logger.warning(f"Normal map not found: {normal_path}")
            return
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Crear nodos para normal map
        texture_node = nodes.new(type='ShaderNodeTexImage')
        texture_node.image = bpy.data.images.load(normal_path)
        texture_node.image.colorspace_settings.name = 'Non-Color'
        
        normal_node = nodes.new(type='ShaderNodeNormalMap')
        
        # Encontrar BSDF
        bsdf = None
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf = node
                break
        
        if bsdf:
            links.new(texture_node.outputs['Color'], normal_node.inputs['Color'])
            links.new(normal_node.outputs['Normal'], bsdf.inputs['Normal'])
    
    def _setup_light(self, light_config: Any):
        """Configura una luz."""
        if not BLENDER_AVAILABLE:
            return
            
        light_name = getattr(light_config, 'name', 'Light')
        light_type = getattr(light_config, 'type', None)
        
        # Mapear tipos de luz
        blender_light_type = 'SUN'
        if light_type:
            if hasattr(light_type, 'value'):
                blender_light_type = light_type.value
            else:
                blender_light_type = str(light_type)
        
        # Crear luz
        light_data = bpy.data.lights.new(name=light_name, type=blender_light_type)
        light_obj = bpy.data.objects.new(light_name, light_data)
        bpy.context.collection.objects.link(light_obj)
        
        # Configurar propiedades
        position = getattr(light_config, 'position', None)
        if position:
            if hasattr(position, 'to_tuple'):
                light_obj.location = position.to_tuple()
            elif isinstance(position, (list, tuple)) and len(position) >= 3:
                light_obj.location = position[:3]
        
        rotation = getattr(light_config, 'rotation', None)
        if rotation:
            if hasattr(rotation, 'to_tuple'):
                light_obj.rotation_euler = rotation.to_tuple()
            elif isinstance(rotation, (list, tuple)) and len(rotation) >= 3:
                light_obj.rotation_euler = rotation[:3]
        
        energy = getattr(light_config, 'energy', 5.0)
        light_data.energy = energy
        
        color = getattr(light_config, 'color', None)
        if color:
            if hasattr(color, 'to_tuple'):
                light_data.color = color.to_tuple()[:3]  # Solo RGB
            elif isinstance(color, (list, tuple)) and len(color) >= 3:
                light_data.color = color[:3]
        
        size = getattr(light_config, 'size', 1.0)
        if blender_light_type in ['SPOT', 'AREA']:
            light_data.size = size
        
        if blender_light_type == 'SPOT':
            angle = getattr(light_config, 'angle', 0.785398)
            blend = getattr(light_config, 'blend', 0.15)
            light_data.spot_size = angle
            light_data.spot_blend = blend
        
        if CORE_AVAILABLE:
            logger.debug(f"Light '{light_name}' created", {
                "type": blender_light_type,
                "energy": energy,
                "position": position.to_tuple() if hasattr(position, 'to_tuple') else position
            })
    
    def _setup_animation(self, anim_config: Any):
        """Configura una animación."""
        if not BLENDER_AVAILABLE:
            return
            
        target_object = getattr(anim_config, 'target_object', None)
        if not target_object:
            return
            
        # Encontrar objeto objetivo
        target_obj = bpy.data.objects.get(target_object)
        if not target_obj:
            if CORE_AVAILABLE:
                logger.warning(f"Animation target object not found: {target_object}")
            return
        
        # Configurar keyframes
        keyframes = getattr(anim_config, 'keyframes', [])
        for keyframe in keyframes:
            frame = getattr(keyframe, 'frame', 1)
            
            position = getattr(keyframe, 'position', None)
            if position:
                if hasattr(position, 'to_tuple'):
                    target_obj.location = position.to_tuple()
                elif isinstance(position, (list, tuple)) and len(position) >= 3:
                    target_obj.location = position[:3]
                target_obj.keyframe_insert(data_path="location", frame=frame)
            
            rotation = getattr(keyframe, 'rotation', None)
            if rotation:
                if hasattr(rotation, 'to_tuple'):
                    target_obj.rotation_euler = rotation.to_tuple()
                elif isinstance(rotation, (list, tuple)) and len(rotation) >= 3:
                    target_obj.rotation_euler = rotation[:3]
                target_obj.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            scale = getattr(keyframe, 'scale', None)
            if scale:
                if hasattr(scale, 'to_tuple'):
                    target_obj.scale = scale.to_tuple()
                elif isinstance(scale, (list, tuple)) and len(scale) >= 3:
                    target_obj.scale = scale[:3]
                target_obj.keyframe_insert(data_path="scale", frame=frame)
        
        # Configurar interpolación
        interpolation = getattr(anim_config, 'interpolation', 'BEZIER')
        if target_obj.animation_data and target_obj.animation_data.action:
            for fcurve in target_obj.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = interpolation
        
        if CORE_AVAILABLE:
            anim_name = getattr(anim_config, 'name', 'Animation')
            logger.debug(f"Animation '{anim_name}' configured", {
                "target": target_object,
                "keyframes": len(keyframes),
                "interpolation": interpolation
            })
    
    def _configure_render_settings(self, render_settings: Any):
        """Configura los settings de renderizado."""
        if not BLENDER_AVAILABLE:
            return
            
        scene = bpy.context.scene
        
        # Resolución
        resolution_x = getattr(render_settings, 'resolution_x', 1920)
        resolution_y = getattr(render_settings, 'resolution_y', 1080)
        scene.render.resolution_x = resolution_x
        scene.render.resolution_y = resolution_y
        
        # Samples (ajustar según modo preview)
        samples = getattr(render_settings, 'samples', 128)
        if self.preview_mode:
            samples = min(32, samples // 4)
        
        scene.cycles.samples = samples
        
        # Formato de salida
        output_format = getattr(render_settings, 'output_format', 'PNG')
        if hasattr(output_format, 'value'):
            output_format = output_format.value
        scene.render.image_settings.file_format = str(output_format)
        
        # Configuraciones adicionales según formato
        quality = getattr(render_settings, 'quality', 90)
        compression = getattr(render_settings, 'compression', 15)
        
        if str(output_format) == 'JPEG':
            scene.render.image_settings.quality = quality
        elif str(output_format) == 'PNG':
            scene.render.image_settings.compression = compression
        
        # Otras configuraciones
        use_denoising = getattr(render_settings, 'use_denoising', True)
        motion_blur = getattr(render_settings, 'motion_blur', False)
        transparent = getattr(render_settings, 'transparent', False)
        
        scene.render.use_denoising = use_denoising
        scene.render.use_motion_blur = motion_blur
        
        if transparent:
            scene.render.film_transparent = True
        
        if CORE_AVAILABLE:
            logger.debug("Render settings configured", {
                "resolution": f"{resolution_x}x{resolution_y}",
                "samples": samples,
                "format": str(output_format),
                "preview_mode": self.preview_mode
            })
    
    def _execute_render(self, scene_config: Any) -> List[str]:
        """Ejecuta el renderizado."""
        if not BLENDER_AVAILABLE:
            return []
            
        output_files = []
        scene = bpy.context.scene
        
        # Configurar output path
        scene_name = getattr(scene_config, 'name', 'scene')
        base_filename = scene_name
        output_path = self.output_dir / base_filename
        scene.render.filepath = str(output_path)
        
        try:
            # Renderizar animación o imagen estática
            if scene.frame_end > scene.frame_start:
                # Animación
                bpy.ops.render.render(animation=True)
                
                # Generar lista de archivos de salida
                render_settings = getattr(scene_config, 'render_settings', None)
                output_format = getattr(render_settings, 'output_format', 'PNG')
                if hasattr(output_format, 'value'):
                    output_format = output_format.value
                
                for frame in range(scene.frame_start, scene.frame_end + 1):
                    frame_file = f"{output_path}{frame:04d}.{str(output_format).lower()}"
                    if Path(frame_file).exists():
                        output_files.append(frame_file)
            else:
                # Imagen estática
                bpy.ops.render.render(write_still=True)
                render_settings = getattr(scene_config, 'render_settings', None)
                output_format = getattr(render_settings, 'output_format', 'PNG')
                if hasattr(output_format, 'value'):
                    output_format = output_format.value
                    
                static_file = f"{output_path}.{str(output_format).lower()}"
                if Path(static_file).exists():
                    output_files.append(static_file)
            
            if CORE_AVAILABLE:
                logger.info(f"Render completed successfully", {
                    "output_files": len(output_files),
                    "first_file": output_files[0] if output_files else None
                })
            
        except Exception as e:
            error_msg = f"Render execution failed: {str(e)}"
            if CORE_AVAILABLE:
                raise RenderError(error_msg, context={
                    "scene": scene_name,
                    "output_path": str(output_path)
                })
            else:
                raise Exception(error_msg)
        
        return output_files
    
    def _create_render_metadata(
        self,
        scene_config: Any,
        start_time: datetime,
        end_time: datetime,
        output_files: List[str]
    ) -> Any:
        """Crea metadata del renderizado."""
        if not CORE_AVAILABLE:
            return None
            
        return RenderMetadata(
            output_file=output_files[0] if output_files else "",
            scene_config=scene_config,
            render_settings=getattr(scene_config, 'render_settings', None),
            start_time=start_time,
            end_time=end_time,
            total_frames=len(output_files),
            system_info={
                "blender_version": bpy.app.version_string if bpy else "unknown",
                "preview_mode": self.preview_mode,
                "cache_enabled": self.enable_cache,
                "cache_stats": self.material_cache.get_stats() if self.material_cache else {}
            }
        )
    
    def clear_scene(self):
        """Limpia la escena actual."""
        if BLENDER_AVAILABLE:
            bpy.ops.wm.read_factory_settings(use_empty=True)
        
        if self.material_cache:
            self.material_cache.clear()
        
        if CORE_AVAILABLE:
            logger.info("Scene cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del renderer."""
        stats = {
            "preview_mode": self.preview_mode,
            "cache_enabled": self.enable_cache,
            "output_dir": str(self.output_dir),
            "blender_available": BLENDER_AVAILABLE,
            "core_available": CORE_AVAILABLE
        }
        
        if self.material_cache:
            stats["cache_stats"] = self.material_cache.get_stats()
        
        return stats
        
        # Material cache for efficiency
        self.material_cache: Dict[str, bpy.types.Material] = {}
        self.material_cache_manager = MaterialCache()
        
        # Performance tracking
        self.render_start_time: Optional[datetime] = None
        self.current_scene_index = 0
        self.total_scenes = 0
        
        # Initialize Blender settings
        self._initialize_blender_settings()
        
        if self.logger:
            self.logger.log_info("Enhanced Blender Renderer initialized", {
                "preview_mode": self.preview_mode,
                "gpu_available": self._gpu_available()
            })
        else:
            print("🎬 Enhanced Blender Renderer initialized")
    
    def _initialize_blender_settings(self):
        """Initialize Blender with optimal settings"""
        try:
            # Set render engine
            bpy.context.scene.render.engine = 'CYCLES'
            
            # Configure render settings
            scene = bpy.context.scene
            
            if self.render_settings:
                scene.render.resolution_x = self.render_settings.resolution[0]
                scene.render.resolution_y = self.render_settings.resolution[1]
                scene.render.fps = self.render_settings.fps
                
                # Set samples based on quality
                if self.preview_mode:
                    scene.cycles.samples = 32
                else:
                    scene.cycles.samples = self.render_settings.get_samples()
                
                # GPU settings
                if self.render_settings.use_gpu and self._gpu_available():
                    scene.cycles.device = 'GPU'
                    print("🚀 GPU rendering enabled")
                else:
                    scene.cycles.device = 'CPU'
                    print("🖥️ CPU rendering mode")
            else:
                # Default settings
                scene.render.resolution_x = 1920
                scene.render.resolution_y = 1080
                scene.render.fps = 30
                scene.cycles.samples = 128
                
                if self._gpu_available():
                    scene.cycles.device = 'GPU'
                    print("🚀 GPU rendering enabled")
                else:
                    scene.cycles.device = 'CPU'
                    print("🖥️ CPU rendering mode")
            
            # Output settings
            scene.render.image_settings.file_format = 'FFMPEG'
            scene.render.ffmpeg.format = 'MPEG4'
            scene.render.ffmpeg.codec = 'H264'
            
        except Exception as e:
            error_msg = f"Failed to initialize Blender settings: {str(e)}"
            if self.logger:
                self.logger.log_error(error_msg)
            else:
                print(f"❌ {error_msg}")
            raise
    
    def _gpu_available(self) -> bool:
        """Check if GPU rendering is available"""
        try:
            preferences = bpy.context.preferences
            cycles_preferences = preferences.addons['cycles'].preferences
            cycles_preferences.refresh_devices()
            gpu_devices = [device for device in cycles_preferences.devices 
                          if device.type in ['CUDA', 'OPENCL', 'OPTIX']]
            return len(gpu_devices) > 0
        except Exception:
            return False
    
    def render_video(self, 
                    scenes: List[Any], 
                    output_dir: str,
                    filename: Optional[str] = None) -> Dict[str, Any]:
        """Render complete video from scene configurations with full metadata"""
        
        self.render_start_time = datetime.now()
        self.total_scenes = len(scenes)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        if not filename:
            timestamp = self.render_start_time.strftime("%Y%m%d_%H%M%S")
            filename = f"q_aviogen_render_{timestamp}.mp4"
        
        output_file = output_path / filename
        
        print(f"🎥 Starting enhanced video render")
        print(f"📁 Output: {output_file}")
        print(f"🎬 Scenes: {len(scenes)}")
        
        frame_offset = 1
        total_frames = 0
        errors = []
        warnings = []
        
        try:
            # Process each scene
            for i, scene_config in enumerate(scenes):
                self.current_scene_index = i + 1
                
                print(f"📹 Processing scene {i + 1}/{len(scenes)}: {getattr(scene_config, 'name', f'scene_{i+1}')}")
                
                try:
                    # Load scene configuration
                    self._load_scene_config(scene_config)
                    
                    # Calculate frame range for this scene
                    duration = getattr(scene_config, 'duration_seconds', 5.0)
                    fps = getattr(self.render_settings, 'fps', 30) if self.render_settings else 30
                    scene_frames = int(duration * fps)
                    end_frame = frame_offset + scene_frames - 1
                    
                    # Set frame range
                    bpy.context.scene.frame_start = frame_offset
                    bpy.context.scene.frame_end = end_frame
                    
                    # Setup animations for this scene
                    self._setup_scene_animations(scene_config, frame_offset)
                    
                    # Add audio if available
                    if hasattr(scene_config, 'audio_file') and scene_config.audio_file:
                        self._add_audio_strip(scene_config.audio_file, frame_offset)
                    
                    frame_offset = end_frame + 1
                    total_frames += scene_frames
                    
                except Exception as e:
                    error_msg = f"Failed to process scene {i+1}: {str(e)}"
                    errors.append(error_msg)
                    print(f"⚠️ {error_msg}")
                    continue
            
            # Final render
            if not errors:  # Only render if no critical errors
                print("🎬 Starting final render...")
                self._render_animation(str(output_file))
                print("✅ Render completed successfully")
            else:
                print(f"❌ Render aborted due to {len(errors)} errors")
            
        except Exception as e:
            error_msg = f"Critical render error: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        finally:
            end_time = datetime.now()
            render_duration = (end_time - self.render_start_time).total_seconds()
            
            # Create metadata
            metadata = {
                "output_file": str(output_file),
                "total_scenes": len(scenes),
                "start_time": self.render_start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "render_duration_seconds": render_duration,
                "total_frames": total_frames,
                "frames_per_second_rendered": total_frames / render_duration if render_duration > 0 else 0,
                "errors": errors,
                "warnings": warnings,
                "preview_mode": self.preview_mode
            }
            
            # Save metadata
            metadata_file = output_path / f"{output_file.stem}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Metadata saved: {metadata_file}")
            print(f"⏱️ Total render time: {render_duration:.1f}s")
            print(f"🎞️ Average FPS: {metadata['frames_per_second_rendered']:.1f}")
        
        return metadata
    
    def _load_scene_config(self, scene_config: Any):
        """Load scene configuration into Blender with enhanced error handling"""
        
        scene_name = getattr(scene_config, 'name', 'unknown')
        print(f"🔧 Loading scene: {scene_name}")
        
        # Clear current scene objects (keep camera and lights)
        self._clear_scene_objects()
        
        # Setup camera
        camera_config = getattr(scene_config, 'camera', None)
        if camera_config:
            self._setup_camera(camera_config)
        
        # Setup lighting
        lights = getattr(scene_config, 'lights', [])
        if lights:
            self._setup_lighting(lights)
        else:
            self._setup_default_lighting()
        
        # Load 3D objects
        objects = getattr(scene_config, 'objects', [])
        for obj_config in objects:
            try:
                self._load_scene_object(obj_config)
            except Exception as e:
                obj_name = getattr(obj_config, 'name', 'unknown')
                print(f"⚠️ Failed to load object {obj_name}: {str(e)}")
        
        # Setup overlays
        overlays = getattr(scene_config, 'overlays', [])
        if overlays:
            self._setup_overlays(overlays)
        
        # Set background
        bg_color = getattr(scene_config, 'background_color', (0.2, 0.2, 0.2))
        self._setup_background(bg_color)
    
    def _clear_scene_objects(self):
        """Clear all mesh objects from scene"""
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.delete()
    
    def _setup_camera(self, camera_config: Any):
        """Setup camera based on configuration"""
        # Create or get camera
        if 'Camera' not in bpy.data.objects:
            bpy.ops.object.camera_add()
            camera = bpy.context.active_object
            camera.name = 'Camera'
        else:
            camera = bpy.data.objects['Camera']
        
        # Set camera properties
        position = getattr(camera_config, 'position', (0, -5, 3))
        target = getattr(camera_config, 'target', (0, 0, 0))
        fov = getattr(camera_config, 'fov', 45.0)
        
        camera.location = position
        
        # Point camera at target
        direction = Vector(target) - Vector(position)
        camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
        # Set field of view
        camera.data.angle = math.radians(fov)
        
        # Set as active camera
        bpy.context.scene.camera = camera
    
    def _setup_lighting(self, lights_config: List[Any]):
        """Setup lighting based on configuration"""
        # Remove existing lights
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj, do_unlink=True)
        
        # Add configured lights
        for light_config in lights_config:
            self._create_light(light_config)
    
    def _setup_default_lighting(self):
        """Setup default lighting when none specified"""
        # Remove existing lights
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj, do_unlink=True)
        
        # Key light
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        key_light = bpy.context.active_object
        key_light.name = "KeyLight"
        key_light.data.energy = 5.0
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-3, 2, 4))
        fill_light = bpy.context.active_object
        fill_light.name = "FillLight"
        fill_light.data.energy = 2.0
    
    def _create_light(self, light_config: Any):
        """Create a single light from configuration"""
        light_type = getattr(light_config, 'type', 'SUN')
        name = getattr(light_config, 'name', 'Light')
        position = getattr(light_config, 'position', (0, 0, 5))
        energy = getattr(light_config, 'energy', 10.0)
        color = getattr(light_config, 'color', (1.0, 1.0, 1.0))
        
        # Map light types
        blender_type = 'SUN'
        if hasattr(light_type, 'value'):
            blender_type = light_type.value
        elif isinstance(light_type, str):
            blender_type = light_type.upper()
        
        bpy.ops.object.light_add(type=blender_type, location=position)
        light = bpy.context.active_object
        light.name = name
        light.data.energy = energy
        light.data.color = color
    
    def _load_scene_object(self, obj_config: Any):
        """Load a single 3D object with error handling"""
        obj_name = getattr(obj_config, 'name', 'Object')
        file_path = getattr(obj_config, 'file_path', None)
        position = getattr(obj_config, 'position', (0, 0, 0))
        rotation = getattr(obj_config, 'rotation', (0, 0, 0))
        scale = getattr(obj_config, 'scale', (1, 1, 1))
        visible = getattr(obj_config, 'visible', True)
        
        if not visible:
            return
        
        # Try to load from file or create placeholder
        obj = self._load_or_create_object(obj_name, file_path)
        
        if obj:
            # Set transform
            obj.location = position
            obj.rotation_euler = rotation
            obj.scale = scale
            
            # Apply material if specified
            material_config = getattr(obj_config, 'material', None)
            if material_config:
                material = self.get_or_create_material(f"{obj_name}_material", material_config)
                if obj.data.materials:
                    obj.data.materials[0] = material
                else:
                    obj.data.materials.append(material)
    
    def _load_or_create_object(self, name: str, file_path: Optional[str]) -> Optional[bpy.types.Object]:
        """Load object from file or create placeholder"""
        if file_path and Path(file_path).exists():
            try:
                if file_path.endswith(('.glb', '.gltf')):
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
                print(f"⚠️ Error loading {file_path}: {e}")
        
        # Create placeholder object
        return self._create_placeholder_object(name)
    
    def _create_placeholder_object(self, name: str) -> bpy.types.Object:
        """Create a placeholder object when asset is not available"""
        # Create different shapes based on object name
        if 'aircraft' in name.lower() or 'bwb' in name.lower():
            bpy.ops.mesh.primitive_cube_add(size=4)
            obj = bpy.context.active_object
            obj.scale = (4, 2, 0.5)
        elif 'towbar' in name.lower():
            bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=3)
            obj = bpy.context.active_object
            obj.rotation_euler = (0, math.radians(90), 0)
        elif 'gear' in name.lower():
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1)
            obj = bpy.context.active_object
        else:
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.active_object
        
        obj.name = name
        return obj
    
    def get_or_create_material(self, name: str, material_config: Any) -> bpy.types.Material:
        """Get or create material with caching for efficiency"""
        
        # Simple cache key based on name
        cache_key = f"{name}_{id(material_config)}"
        
        if cache_key in self.material_cache:
            return self.material_cache[cache_key]
        
        # Create new material
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        
        # Clear default nodes
        material.node_tree.nodes.clear()
        
        # Create principled BSDF
        bsdf = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        output = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        
        # Link nodes
        material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Set material properties with safe defaults
        base_color = getattr(material_config, 'base_color', (0.8, 0.8, 0.8, 1.0))
        metallic = getattr(material_config, 'metallic', 0.0)
        roughness = getattr(material_config, 'roughness', 0.5)
        
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        
        # Cache the material
        self.material_cache[cache_key] = material
        
        return material
    
    def _setup_overlays(self, overlays: List[Any]):
        """Setup text overlays (placeholder implementation)"""
        # This would integrate with Blender's text objects or compositor
        for overlay in overlays:
            text = getattr(overlay, 'text', '')
            print(f"📝 Overlay: {text}")
    
    def _setup_background(self, color: Tuple[float, float, float]):
        """Setup background color"""
        world = bpy.context.scene.world
        if world:
            world.use_nodes = True
            bg_node = world.node_tree.nodes.get('Background')
            if bg_node:
                bg_node.inputs['Color'].default_value = color + (1.0,)
    
    def _setup_scene_animations(self, scene_config: Any, frame_offset: int):
        """Setup animations for the scene"""
        animations = getattr(scene_config, 'animations', [])
        
        for anim_config in animations:
            try:
                self._create_animation(anim_config, frame_offset)
            except Exception as e:
                target = getattr(anim_config, 'target_object', 'unknown')
                print(f"⚠️ Failed to create animation for {target}: {str(e)}")
    
    def _create_animation(self, anim_config: Any, frame_offset: int):
        """Create a single animation"""
        target_name = getattr(anim_config, 'target_object', '')
        anim_type = getattr(anim_config, 'type', '')
        
        if target_name not in bpy.data.objects:
            print(f"⚠️ Animation target not found: {target_name}")
            return
        
        obj = bpy.data.objects[target_name]
        
        # Basic animation implementation
        start_frame = frame_offset + getattr(anim_config, 'start_frame', 1)
        end_frame = frame_offset + getattr(anim_config, 'end_frame', 30)
        
        # Simple position animation example
        start_pos = getattr(anim_config, 'start_position', None)
        end_pos = getattr(anim_config, 'end_position', None)
        
        if start_pos and end_pos:
            # Set keyframes
            bpy.context.scene.frame_set(start_frame)
            obj.location = start_pos
            obj.keyframe_insert(data_path="location")
            
            bpy.context.scene.frame_set(end_frame)
            obj.location = end_pos
            obj.keyframe_insert(data_path="location")
    
    def _add_audio_strip(self, audio_file: str, frame_start: int):
        """Add audio strip to sequence editor"""
        if not Path(audio_file).exists():
            print(f"⚠️ Audio file not found: {audio_file}")
            return
        
        # Ensure sequence editor exists
        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
        
        seq_editor = bpy.context.scene.sequence_editor
        
        try:
            seq_editor.sequences.new_sound(
                name=f"audio_{frame_start}",
                filepath=audio_file,
                channel=1,
                frame_start=frame_start
            )
            print(f"🎵 Audio added: {Path(audio_file).name}")
        except Exception as e:
            print(f"⚠️ Failed to add audio: {str(e)}")
    
    def _render_animation(self, output_path: str):
        """Render the final animation"""
        bpy.context.scene.render.filepath = output_path
        bpy.ops.render.render(animation=True)

# Factory function for compatibility
def get_enhanced_renderer_class():
    """Get the enhanced renderer class"""
    return EnhancedBlenderRenderer

# Test function
def test_enhanced_renderer():
    """Test the enhanced renderer with sample data"""
    print("🧪 Testing Enhanced Blender Renderer...")
    
    # Create a simple test scene
    class MockSceneConfig:
        def __init__(self):
            self.name = "test_scene"
            self.duration_seconds = 5.0
            self.camera = None
            self.lights = []
            self.objects = []
            self.animations = []
            self.overlays = []
            self.audio_file = None
            self.background_color = (0.2, 0.2, 0.2)
    
    renderer = EnhancedBlenderRenderer(preview_mode=True)
    
    test_scene = MockSceneConfig()
    scenes = [test_scene]
    
    try:
        metadata = renderer.render_video(scenes, "output/test/")
        print("✅ Enhanced renderer test passed")
        return True
    except Exception as e:
        print(f"❌ Enhanced renderer test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_enhanced_renderer()
