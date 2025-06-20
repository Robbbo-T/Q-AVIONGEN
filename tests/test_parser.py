"""
Tests for Q-AVIOGEN components
Pruebas unitarias para los componentes de Q-AVIOGEN
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser.md_parser import MarkdownParser
from parser.yaml_parser import YAMLParser
from parser.scene_builder import SceneBuilder
from tts.narration import NarrationGenerator

class TestMarkdownParser:
    """Test cases for Markdown parser"""
    
    def setup_method(self):
        """Setup test environment"""
        self.parser = MarkdownParser()
        self.sample_md_content = """
# 00-30-10-01 Test Procedure

## Overview
This is a test procedure for BWB-Q100 aircraft.

## Steps

### Step 1: Test Step
- Perform test action
- Apply torque of 50Nm
- Maintain clearance of 5cm

### Step 2: Verification
- Check connections
- ⚠️ Safety warning test
"""
    
    def test_parser_initialization(self):
        """Test parser initializes correctly"""
        assert self.parser is not None
        assert hasattr(self.parser, 'md')
    
    def test_parse_content(self):
        """Test parsing markdown content"""
        result = self.parser.parse_content(self.sample_md_content, "test_procedure")
        
        assert result['id'] == '00-30-10-01'
        assert result['title'] == '00-30-10-01 Test Procedure'
        assert len(result['steps']) == 2
        assert result['aircraft_model'] == 'BWB-Q100'
    
    def test_extract_steps(self):
        """Test step extraction"""
        result = self.parser.parse_content(self.sample_md_content, "test")
        steps = result['steps']
        
        assert len(steps) == 2
        assert steps[0]['id'] == 'step_01'
        assert steps[0]['title'] == 'Test Step'
        assert 'Torque: 50 NM' in steps[0]['overlay_text']
    
    def test_ata_code_extraction(self):
        """Test ATA code extraction"""
        ata_code = self.parser._extract_ata_code("00-30-10-01 Test")
        assert ata_code == "00-30-10-01"
        
        no_ata = self.parser._extract_ata_code("No ATA code here")
        assert no_ata is None

class TestYAMLParser:
    """Test cases for YAML parser"""
    
    def setup_method(self):
        """Setup test environment"""
        self.parser = YAMLParser()
        self.sample_yaml_data = {
            'version': '1.0',
            'procedure': {
                'id': 'test-001',
                'title': 'Test Procedure',
                'aircraft': 'BWB-Q100'
            },
            'steps': [
                {
                    'id': 'step_01',
                    'description': 'Test step 1',
                    'duration': 5.0,
                    'camera': 'front_view'
                },
                {
                    'id': 'step_02',
                    'description': 'Test step 2',
                    'duration': 8.0,
                    'overlay': 'Test overlay'
                }
            ]
        }
    
    def test_parser_initialization(self):
        """Test parser initializes correctly"""
        assert self.parser is not None
        assert self.parser.supported_versions == ['1.0', '1.1']
    
    def test_parse_yaml_data(self):
        """Test parsing YAML data"""
        result = self.parser.parse_yaml_data(self.sample_yaml_data, "test")
        
        assert result['id'] == 'test-001'
        assert result['title'] == 'Test Procedure'
        assert len(result['steps']) == 2
        assert result['metadata']['total_steps'] == 2
    
    def test_yaml_validation(self):
        """Test YAML validation"""
        # Valid YAML should pass
        self.parser._validate_yaml_structure(self.sample_yaml_data)
        
        # Invalid YAML should fail
        invalid_yaml = {'procedure': {}}  # Missing steps
        with pytest.raises(ValueError):
            self.parser._validate_yaml_structure(invalid_yaml)
    
    def test_step_conversion(self):
        """Test step conversion to standard format"""
        steps = self.parser._convert_steps(self.sample_yaml_data['steps'])
        
        assert len(steps) == 2
        assert steps[0]['id'] == 'step_01'
        assert steps[0]['duration'] == 5.0
        assert steps[0]['camera_angle'] == 'front_view'
        assert steps[1]['overlay_text'] == 'Test overlay'

class TestSceneBuilder:
    """Test cases for Scene Builder"""
    
    def setup_method(self):
        """Setup test environment"""
        self.builder = SceneBuilder(debug=True)
        self.sample_procedure = {
            'id': 'test-procedure',
            'title': 'Test Procedure',
            'aircraft_model': 'BWB-Q100',
            'steps': [
                {
                    'id': 'step_01',
                    'title': 'Test Step',
                    'description': 'Test towbar attachment',
                    'duration': 5.0,
                    'camera_angle': 'overview',
                    'overlay_text': 'Test overlay'
                }
            ]
        }
    
    def test_builder_initialization(self):
        """Test builder initializes correctly"""
        assert self.builder is not None
        assert self.builder.debug is True
        assert len(self.builder.camera_presets) > 0
        assert len(self.builder.object_library) > 0
    
    def test_camera_presets(self):
        """Test camera preset configurations"""
        presets = self.builder.camera_presets
        
        assert 'default' in presets
        assert 'overview' in presets
        assert 'close_up' in presets
        
        default_cam = presets['default']
        assert len(default_cam.position) == 3
        assert default_cam.fov > 0
    
    def test_object_library(self):
        """Test object library"""
        objects = self.builder.object_library
        
        assert 'aircraft_bwb' in objects
        assert 'towbar' in objects
        assert 'nose_gear' in objects
        
        aircraft = objects['aircraft_bwb']
        assert aircraft.name == 'BWB_Aircraft'
        assert aircraft.visible is True
    
    def test_build_scenes(self):
        """Test scene building from procedure data"""
        scenes = self.builder.build_scenes(self.sample_procedure)
        
        assert len(scenes) == 1
        scene = scenes[0]
        
        assert scene.name == 'scene_step_01'
        assert scene.duration_seconds == 5.0
        assert len(scene.lights) > 0
        assert len(scene.overlays) == 1
        assert scene.overlays[0].text == 'Test overlay'
    
    def test_scene_objects_detection(self):
        """Test automatic object detection"""
        step_with_towbar = {
            'title': 'Attach towbar to nose gear',
            'description': 'Use mechanic and tools'
        }
        
        objects = self.builder._get_scene_objects(step_with_towbar, self.sample_procedure)
        object_names = [obj.name for obj in objects]
        
        assert 'BWB_Aircraft' in object_names
        assert 'Towbar' in object_names
        assert 'NoseGear' in object_names
        assert 'Mechanic' in object_names
        assert 'Tools' in object_names

class TestNarrationGenerator:
    """Test cases for Narration Generator"""
    
    def setup_method(self):
        """Setup test environment"""
        # Use offline engine for testing
        self.narration_gen = NarrationGenerator(engine="pyttsx3")
        self.sample_procedure = {
            'id': 'test-procedure',
            'title': 'Test Procedure',
            'steps': [
                {
                    'id': 'test_step_01',
                    'narration': 'This is a test narration for step one.'
                },
                {
                    'id': 'test_step_02',
                    'description': 'This is a test description for step two.'
                }
            ]
        }
    
    def test_generator_initialization(self):
        """Test generator initializes correctly"""
        assert self.narration_gen is not None
        assert self.narration_gen.engine_name == "pyttsx3"
    
    def test_cache_key_generation(self):
        """Test cache key generation"""
        key1 = self.narration_gen._get_cache_key("test text")
        key2 = self.narration_gen._get_cache_key("test text")
        key3 = self.narration_gen._get_cache_key("different text")
        
        assert key1 == key2  # Same text should generate same key
        assert key1 != key3  # Different text should generate different key
        assert len(key1) == 32  # MD5 hash length
    
    def test_engine_test(self):
        """Test engine functionality (may skip if pyttsx3 not available)"""
        try:
            result = self.narration_gen.test_engine()
            # If pyttsx3 is available, should return True or False
            assert isinstance(result, bool)
        except Exception:
            # If pyttsx3 not available, that's okay for CI
            pytest.skip("pyttsx3 not available for testing")

# Integration tests
class TestIntegration:
    """Integration tests for the complete pipeline"""
    
    def test_md_to_scenes_pipeline(self):
        """Test complete pipeline from Markdown to scenes"""
        # Parse markdown
        md_parser = MarkdownParser()
        sample_md = """
# 00-30-10-01 Integration Test

## Overview
Integration test for BWB-Q100.

## Steps

### Step 1: Test
- Test action with towbar
"""
        procedure_data = md_parser.parse_content(sample_md, "integration_test")
        
        # Build scenes
        scene_builder = SceneBuilder()
        scenes = scene_builder.build_scenes(procedure_data)
        
        # Verify pipeline
        assert len(scenes) == 1
        assert scenes[0].duration_seconds > 0
        assert len(scenes[0].objects) > 0
    
    def test_yaml_to_scenes_pipeline(self):
        """Test complete pipeline from YAML to scenes"""
        # Parse YAML
        yaml_parser = YAMLParser()
        sample_yaml = {
            'version': '1.0',
            'procedure': {
                'id': 'integration-test',
                'title': 'Integration Test',
                'aircraft': 'BWB-Q100'
            },
            'steps': [
                {
                    'id': 'step_01',
                    'description': 'Test step with towbar and nose gear',
                    'duration': 3.0,
                    'camera': 'overview'
                }
            ]
        }
        procedure_data = yaml_parser.parse_yaml_data(sample_yaml, "integration_test")
        
        # Build scenes
        scene_builder = SceneBuilder()
        scenes = scene_builder.build_scenes(procedure_data)
        
        # Verify pipeline
        assert len(scenes) == 1
        assert scenes[0].name == 'scene_step_01'

# Utility functions for testing
def create_test_files():
    """Create test files for file-based tests"""
    test_dir = Path("test_output")
    test_dir.mkdir(exist_ok=True)
    
    # Create test markdown file
    test_md = test_dir / "test.md"
    with open(test_md, 'w', encoding='utf-8') as f:
        f.write("""
# 00-30-10-01 Test Procedure

## Overview
Test procedure for file parsing.

## Steps

### Step 1: Test
- Test action
""")
    
    return test_dir

def cleanup_test_files():
    """Clean up test files"""
    import shutil
    test_dir = Path("test_output")
    if test_dir.exists():
        shutil.rmtree(test_dir)

# Test configuration
if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
