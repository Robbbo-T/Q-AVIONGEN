"""
Tests de validación de esquema Q-AVIOGEN v2.1
==============================================

Suite completa de tests para validar el esquema de tipos v2.1 con todos
los nuevos features: avatar personalizado, voz grabada, timeline markers,
capas, postproceso y validación aerospace-grade.

Author: Q-AVIOGEN Team
Date: 2025-06-20
Version: 2.1.0
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.types_v2_1 import (
    SceneConfig, 
    CameraConfig, 
    ObjectConfig, 
    EnvironmentConfig,
    RenderSettings,
    TimelineMarker,
    SceneLayer,
    EnhancedNarrationConfig,
    VoiceConfig,
    AvatarConfig,
    NarrationSegment,
    PostProcessingSettings,
    SceneMetadata,
    SceneValidator,
    Vector3D,
    RGBAColor,
    AssetType,
    VideoCodec,
    RenderPass,
    EnvironmentType,
    AvatarType,
    VoiceGender,
    AvatarEmotionState
)


class TestBasicTypes(unittest.TestCase):
    """Tests para tipos básicos"""
    
    def test_vector3d_valid(self):
        """Test Vector3D válido"""
        vec = Vector3D(1.0, 2.0, 3.0)
        errors = vec.validate()
        self.assertEqual(len(errors), 0)
        
        # Test conversión a diccionario
        data = vec.to_dict()
        self.assertEqual(data, {"x": 1.0, "y": 2.0, "z": 3.0})
    
    def test_vector3d_invalid(self):
        """Test Vector3D inválido"""
        # Esto no debería generar errores en tiempo de ejecución ya que Python es dinámico
        # pero podemos testear con tipos incorrectos
        pass
    
    def test_rgba_color_valid(self):
        """Test RGBAColor válido"""
        color = RGBAColor(0.5, 0.7, 0.9, 1.0)
        errors = color.validate()
        self.assertEqual(len(errors), 0)
    
    def test_rgba_color_invalid(self):
        """Test RGBAColor inválido"""
        color = RGBAColor(1.5, -0.1, 0.5, 2.0)  # Valores fuera de rango
        errors = color.validate()
        self.assertGreater(len(errors), 0)


class TestTimelineMarkers(unittest.TestCase):
    """Tests para marcadores de timeline"""
    
    def test_timeline_marker_valid(self):
        """Test marcador de timeline válido"""
        marker = TimelineMarker(
            label="Inspección inicial",
            frame=50,
            color=RGBAColor(1.0, 0.0, 0.0, 1.0),
            description="Inicio del procedimiento de inspección",
            event_type="voice"
        )
        errors = marker.validate()
        self.assertEqual(len(errors), 0)
    
    def test_timeline_marker_invalid(self):
        """Test marcador de timeline inválido"""
        # Etiqueta vacía
        marker = TimelineMarker(label="", frame=10)
        errors = marker.validate()
        self.assertIn("Timeline marker label cannot be empty", errors)
        
        # Frame negativo
        marker = TimelineMarker(label="Test", frame=-5)
        errors = marker.validate()
        self.assertIn("Timeline marker frame must be non-negative", errors)


class TestVoiceAndAvatar(unittest.TestCase):
    """Tests para configuración de voz y avatar"""
    
    def test_voice_config_valid(self):
        """Test configuración de voz válida"""
        voice = VoiceConfig(
            use_custom_voice=False,
            tts_engine="azure",
            voice_name="es-ES-AlvaroNeural",
            voice_gender=VoiceGender.MALE,
            speed=1.0,
            volume=0.8,
            language="es-ES"
        )
        errors = voice.validate()
        self.assertEqual(len(errors), 0)
    
    def test_voice_config_custom_voice_missing_path(self):
        """Test configuración de voz custom sin ruta"""
        voice = VoiceConfig(
            use_custom_voice=True,
            custom_voice_path=None
        )
        errors = voice.validate()
        self.assertIn("Custom voice path required when use_custom_voice is True", errors)
    
    def test_voice_config_invalid_speed(self):
        """Test configuración de voz con velocidad inválida"""
        voice = VoiceConfig(speed=3.0)  # Fuera del rango 0.5-2.0
        errors = voice.validate()
        self.assertIn("Voice speed must be between 0.5 and 2.0", errors)
    
    def test_avatar_config_valid(self):
        """Test configuración de avatar válida"""
        avatar = AvatarConfig(
            enabled=True,
            avatar_type=AvatarType.TECHNICAL_INSTRUCTOR,
            avatar_name="Amedeo",
            scale=1.0,
            position=Vector3D(0, 0, 0),
            default_emotion=AvatarEmotionState.FRIENDLY,
            auto_gestures=True,
            screen_position="bottom_right",
            screen_size_percent=25.0,
            transparency=0.9
        )
        errors = avatar.validate()
        self.assertEqual(len(errors), 0)
    
    def test_avatar_config_invalid_scale(self):
        """Test configuración de avatar con escala inválida"""
        avatar = AvatarConfig(scale=15.0)  # Fuera del rango 0.1-10.0
        errors = avatar.validate()
        self.assertIn("Avatar scale must be between 0.1 and 10.0", errors)
    
    def test_narration_segment_valid(self):
        """Test segmento de narración válido"""
        segment = NarrationSegment(
            text="Ahora procederemos a inspeccionar el motor",
            start_time=0.0,
            duration=5.0,
            emotion=AvatarEmotionState.EXPLAINING,
            gestures=["point", "explain"],
            emphasis_words=["inspeccionar", "motor"]
        )
        errors = segment.validate()
        self.assertEqual(len(errors), 0)
    
    def test_narration_segment_invalid(self):
        """Test segmento de narración inválido"""
        # Texto vacío
        segment = NarrationSegment(text="", start_time=0.0, duration=5.0)
        errors = segment.validate()
        self.assertIn("Narration text cannot be empty", errors)
        
        # Duración negativa
        segment = NarrationSegment(text="Test", start_time=0.0, duration=-1.0)
        errors = segment.validate()
        self.assertIn("Duration must be positive", errors)


class TestPostProcessing(unittest.TestCase):
    """Tests para configuración de postprocesamiento"""
    
    def test_postprocessing_valid(self):
        """Test configuración de postprocesamiento válida"""
        pp = PostProcessingSettings(
            exposure=0.5,
            gamma=1.2,
            bloom=True,
            bloom_threshold=1.0,
            bloom_intensity=0.5,
            depth_of_field=True,
            dof_aperture=2.8,
            film_grain=True,
            grain_intensity=0.3
        )
        errors = pp.validate()
        self.assertEqual(len(errors), 0)
    
    def test_postprocessing_invalid_gamma(self):
        """Test configuración de postprocesamiento con gamma inválido"""
        pp = PostProcessingSettings(gamma=-0.5)  # Gamma debe ser positivo
        errors = pp.validate()
        self.assertIn("Gamma must be positive", errors)
    
    def test_postprocessing_invalid_vignette(self):
        """Test configuración de postprocesamiento con vignette inválido"""
        pp = PostProcessingSettings(vignette_intensity=1.5)  # Fuera del rango 0-1
        errors = pp.validate()
        self.assertIn("Vignette intensity must be between 0 and 1", errors)


class TestObjectsAndAssets(unittest.TestCase):
    """Tests para configuración de objetos y assets"""
    
    def test_object_config_basic(self):
        """Test configuración básica de objeto"""
        obj = ObjectConfig(
            name="TestCube",
            type="mesh",
            position=Vector3D(0, 0, 0),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1)
        )
        errors = obj.validate()
        self.assertEqual(len(errors), 0)
    
    def test_object_config_blend_file(self):
        """Test configuración de objeto con archivo .blend"""
        obj = ObjectConfig(
            name="EngineComponent",
            mesh_path="assets/engine.blend",
            asset_type=AssetType.BLEND,
            blend_object_name="TurbofanEngine"
        )
        # Como el archivo no existe, debería haber un error
        errors = obj.validate()
        self.assertIn("Mesh file not found", " ".join(errors))
    
    def test_object_config_blend_missing_object_name(self):
        """Test configuración de objeto .blend sin nombre de objeto"""
        obj = ObjectConfig(
            name="TestEngine",
            asset_type=AssetType.BLEND
        )
        errors = obj.validate()
        self.assertIn("For .blend files, either blend_object_name or blend_collection_name must be specified", errors)
    
    def test_object_config_empty_name(self):
        """Test configuración de objeto con nombre vacío"""
        obj = ObjectConfig(name="")
        errors = obj.validate()
        self.assertIn("Object name cannot be empty", errors)


class TestRenderSettings(unittest.TestCase):
    """Tests para configuración de renderizado"""
    
    def test_render_settings_valid(self):
        """Test configuración de renderizado válida"""
        render = RenderSettings(
            resolution_x=1920,
            resolution_y=1080,
            frame_start=1,
            frame_end=250,
            fps=24,
            samples=128,
            codec=VideoCodec.H264,
            quality="high",
            use_denoising=True
        )
        errors = render.validate()
        self.assertEqual(len(errors), 0)
    
    def test_render_settings_invalid_resolution(self):
        """Test configuración de renderizado con resolución inválida"""
        render = RenderSettings(resolution_x=0, resolution_y=-100)
        errors = render.validate()
        self.assertIn("Resolution must be positive", errors)
    
    def test_render_settings_invalid_frames(self):
        """Test configuración de renderizado con frames inválidos"""
        render = RenderSettings(frame_start=100, frame_end=50)
        errors = render.validate()
        self.assertIn("Frame start must be <= frame end", errors)


class TestSceneLayers(unittest.TestCase):
    """Tests para capas de escena"""
    
    def test_scene_layer_valid(self):
        """Test capa de escena válida"""
        layer = SceneLayer(
            name="MainObjects",
            include_objects=["Engine", "Tool"],
            render_pass=RenderPass.COMBINED,
            enabled=True,
            opacity=1.0
        )
        errors = layer.validate()
        self.assertEqual(len(errors), 0)
    
    def test_scene_layer_empty_name(self):
        """Test capa de escena con nombre vacío"""
        layer = SceneLayer(name="")
        errors = layer.validate()
        self.assertIn("Layer name cannot be empty", errors)
    
    def test_scene_layer_invalid_opacity(self):
        """Test capa de escena con opacidad inválida"""
        layer = SceneLayer(name="Test", opacity=1.5)
        errors = layer.validate()
        self.assertIn("Layer opacity must be between 0.0 and 1.0", errors)


class TestMetadata(unittest.TestCase):
    """Tests para metadata de seguridad"""
    
    def test_metadata_valid(self):
        """Test metadata válido"""
        metadata = SceneMetadata(
            author="Amedeo",
            version="1.0",
            certification_level="testing",
            compliance_standards=["AS9100", "ISO-9001"],
            approved_by="Quality Team"
        )
        errors = metadata.validate()
        self.assertEqual(len(errors), 0)
    
    def test_metadata_empty_author(self):
        """Test metadata con autor vacío"""
        metadata = SceneMetadata(author="")
        errors = metadata.validate()
        self.assertIn("Author cannot be empty", errors)
    
    def test_metadata_invalid_certification(self):
        """Test metadata con nivel de certificación inválido"""
        metadata = SceneMetadata(certification_level="invalid_level")
        errors = metadata.validate()
        self.assertIn("Invalid certification level", errors)


class TestFullSceneConfigs(unittest.TestCase):
    """Tests para configuraciones completas de escena"""
    
    def test_scene_config_basic_valid(self):
        """Test configuración básica de escena válida"""
        scene = SceneConfig.test_basic()
        is_valid, errors = SceneValidator.validate_scene(scene)
        self.assertTrue(is_valid, f"Scene validation failed: {errors}")
    
    def test_scene_config_advanced_valid(self):
        """Test configuración avanzada de escena válida (con archivos que no existen)"""
        scene = SceneConfig.test_advanced()
        is_valid, errors = SceneValidator.validate_scene(scene)
        # Esta debería fallar porque los archivos no existen
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_scene_config_aerospace_inspection(self):
        """Test configuración específica para inspección aeroespacial"""
        scene = SceneConfig.test_aerospace_inspection()
        is_valid, errors = SceneValidator.validate_scene(scene)
        # Esta también debería fallar por archivos faltantes
        self.assertFalse(is_valid)
    
    def test_scene_config_empty_name(self):
        """Test configuración de escena con nombre vacío"""
        scene = SceneConfig(name="")
        is_valid, errors = SceneValidator.validate_scene(scene)
        self.assertFalse(is_valid)
        self.assertIn("Scene name cannot be empty", errors)
    
    def test_personal_instructor_config(self):
        """Test configuración de instructor personalizado"""
        # Crear archivos temporales para testing
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as voice_file:
            voice_path = voice_file.name
        
        with tempfile.NamedTemporaryFile(suffix=".blend", delete=False) as avatar_file:
            avatar_path = avatar_file.name
        
        try:
            narration = EnhancedNarrationConfig.create_personal_instructor(
                custom_voice_path=voice_path,
                avatar_model_path=avatar_path,
                instructor_name="Amedeo"
            )
            errors = narration.validate()
            self.assertEqual(len(errors), 0)
            
            # Verificar configuración específica
            self.assertTrue(narration.voice_config.use_custom_voice)
            self.assertEqual(narration.voice_config.custom_voice_path, voice_path)
            self.assertEqual(narration.avatar_config.avatar_name, "Amedeo")
            self.assertEqual(narration.avatar_config.avatar_type, AvatarType.TECHNICAL_INSTRUCTOR)
        
        finally:
            # Limpiar archivos temporales
            os.unlink(voice_path)
            os.unlink(avatar_path)


class TestJSONSerialization(unittest.TestCase):
    """Tests para serialización JSON"""
    
    def test_scene_to_json(self):
        """Test conversión de escena a JSON"""
        scene = SceneConfig.test_basic()
        json_str = scene.to_json()
        
        # Verificar que es JSON válido
        data = json.loads(json_str)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "TestBasicScene")
    
    def test_scene_save_load_file(self):
        """Test guardar y cargar escena desde archivo"""
        scene = SceneConfig.test_basic()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix=".json", delete=False) as f:
            temp_path = f.name
        
        try:
            # Guardar
            scene.save_to_file(temp_path)
            
            # Verificar que el archivo existe y tiene contenido válido
            self.assertTrue(os.path.exists(temp_path))
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.assertEqual(data["name"], "TestBasicScene")
        
        finally:
            os.unlink(temp_path)
    
    def test_validation_report_generation(self):
        """Test generación de reporte de validación"""
        scene = SceneConfig.test_basic()
        report = SceneValidator.generate_validation_report(scene)
        
        self.assertIn("Q-AVIOGEN Scene Validation Report", report)
        self.assertIn("TestBasicScene", report)
        self.assertIn("✅ VALID", report)


class TestFixtureIntegration(unittest.TestCase):
    """Tests para integración de fixtures de test"""
    
    def test_all_fixtures_validate(self):
        """Test que todos los fixtures de test sean válidos internamente"""
        fixtures = [
            SceneConfig.test_basic(),
            # Nota: test_advanced y test_aerospace_inspection fallarán por archivos faltantes
        ]
        
        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                # Al menos la estructura interna debería ser válida
                self.assertIsNotNone(fixture.name)
                self.assertIsNotNone(fixture.camera)
                self.assertIsNotNone(fixture.environment)
                self.assertIsNotNone(fixture.render_settings)
    
    def test_fixtures_have_required_features(self):
        """Test que los fixtures tengan las características v2.1"""
        advanced_scene = SceneConfig.test_advanced()
        
        # Verificar características v2.1
        self.assertGreater(len(advanced_scene.timeline_markers), 0)
        self.assertGreater(len(advanced_scene.layers), 0)
        self.assertTrue(advanced_scene.narration.avatar_config.enabled)
        self.assertTrue(advanced_scene.camera.animated)


class TestValidationUtils(unittest.TestCase):
    """Tests para utilidades de validación"""
    
    def test_validator_with_valid_scene(self):
        """Test validador con escena válida"""
        scene = SceneConfig.test_basic()
        is_valid, errors = SceneValidator.validate_scene(scene)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validator_with_invalid_scene(self):
        """Test validador con escena inválida"""
        scene = SceneConfig(name="")  # Nombre vacío
        is_valid, errors = SceneValidator.validate_scene(scene)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_json_file_validation_nonexistent(self):
        """Test validación de archivo JSON inexistente"""
        is_valid, errors = SceneValidator.validate_json_file("nonexistent.json")
        self.assertFalse(is_valid)
        self.assertIn("Error loading file", " ".join(errors))


if __name__ == '__main__':
    print("Q-AVIOGEN Core Types v2.1 - Test Suite")
    print("=" * 50)
    print("Ejecutando tests de validación del esquema...")
    print()
    
    # Configurar test runner con más detalle
    unittest.main(verbosity=2, buffer=True)
