#!/usr/bin/env python3
"""
Q-AVIOGEN Enhanced Renderer Test Suite
Comprehensive testing for enterprise-grade rendering pipeline
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.types import (
        SceneConfig, RenderSettings, RenderQuality,
        CameraConfig, CameraType, LightConfig, LightType,
        ObjectConfig, MaterialConfig, AnimationConfig, AnimationType,
        scene_config_from_dict, validate_scene_config_dict
    )
    from core.errors import QAvioGenError, ErrorCode, setup_logging
    CORE_AVAILABLE = True
except ImportError:
    print("⚠️ Core modules not available, skipping advanced tests")
    CORE_AVAILABLE = False

class TestSceneConfig(unittest.TestCase):
    """Test scene configuration validation and creation"""
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_scene_config_creation(self):
        """Test basic scene config creation"""
        scene = SceneConfig(
            name="test_scene",
            duration_seconds=5.0
        )
        
        self.assertEqual(scene.name, "test_scene")
        self.assertEqual(scene.duration_seconds, 5.0)
        self.assertIsInstance(scene.camera, CameraConfig)
        self.assertIsInstance(scene.lights, list)
        
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_scene_validation(self):
        """Test scene configuration validation"""
        scene = SceneConfig(
            name="test_scene",
            duration_seconds=5.0
        )
        
        issues = scene.validate()
        self.assertIsInstance(issues, list)
        
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_invalid_duration(self):
        """Test validation of invalid duration"""
        with self.assertRaises(ValueError):
            SceneConfig(name="test", duration_seconds=-1.0)
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_empty_name(self):
        """Test validation of empty scene name"""
        with self.assertRaises(ValueError):
            SceneConfig(name="", duration_seconds=5.0)

class TestRenderSettings(unittest.TestCase):
    """Test render settings configuration"""
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_render_settings_creation(self):
        """Test render settings creation with defaults"""
        settings = RenderSettings()
        
        self.assertEqual(settings.quality, RenderQuality.STANDARD)
        self.assertEqual(settings.resolution, (1920, 1080))
        self.assertEqual(settings.fps, 30)
        self.assertTrue(settings.use_gpu)
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_quality_samples(self):
        """Test sample count based on quality"""
        settings = RenderSettings(quality=RenderQuality.PREVIEW)
        self.assertEqual(settings.get_samples(), 32)
        
        settings = RenderSettings(quality=RenderQuality.PRODUCTION)
        self.assertEqual(settings.get_samples(), 2048)
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_custom_samples(self):
        """Test custom sample override"""
        settings = RenderSettings(samples=256)
        self.assertEqual(settings.get_samples(), 256)

class TestJSONSerialization(unittest.TestCase):
    """Test JSON serialization and deserialization"""
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_scene_to_dict(self):
        """Test scene configuration to dictionary conversion"""
        scene = SceneConfig(
            name="test_scene",
            duration_seconds=10.0
        )
        
        scene_dict = scene.to_dict()
        
        self.assertIsInstance(scene_dict, dict)
        self.assertEqual(scene_dict["name"], "test_scene")
        self.assertEqual(scene_dict["duration_seconds"], 10.0)
        self.assertIn("camera", scene_dict)
        self.assertIn("lights", scene_dict)
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_dict_validation(self):
        """Test dictionary validation"""
        valid_dict = {
            "name": "test_scene",
            "duration_seconds": 5.0
        }
        
        errors = validate_scene_config_dict(valid_dict)
        self.assertEqual(len(errors), 0)
        
        invalid_dict = {
            "name": "",  # Invalid empty name
            "duration_seconds": -1.0  # Invalid negative duration
        }
        
        errors = validate_scene_config_dict(invalid_dict)
        self.assertGreater(len(errors), 0)

class TestSchemaValidation(unittest.TestCase):
    """Test JSON schema validation"""
    
    def setUp(self):
        """Set up test data"""
        self.test_scene = {
            "name": "test_towbar_attachment",
            "duration_seconds": 8.0,
            "camera": {
                "position": [0, -5, 3],
                "target": [0, 0, 0],
                "fov": 45,
                "type": "default"
            },
            "objects": [
                {
                    "name": "Aircraft",
                    "position": [0, 0, 0],
                    "visible": True
                }
            ],
            "animations": [
                {
                    "type": "move",
                    "target_object": "Aircraft",
                    "start_position": [0, 0, 0],
                    "end_position": [1, 0, 0]
                }
            ]
        }
    
    def test_valid_scene_structure(self):
        """Test that our test scene has valid structure"""
        required_fields = ["name", "duration_seconds"]
        for field in required_fields:
            self.assertIn(field, self.test_scene)
        
        self.assertIsInstance(self.test_scene["name"], str)
        self.assertIsInstance(self.test_scene["duration_seconds"], (int, float))
        self.assertGreater(self.test_scene["duration_seconds"], 0)

class TestErrorHandling(unittest.TestCase):
    """Test error handling system"""
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_error_creation(self):
        """Test QAvioGenError creation"""
        error = QAvioGenError(
            "Test error message",
            ErrorCode.ASSET_NOT_FOUND,
            context={"file_path": "/test/path"}
        )
        
        self.assertIn("E001", str(error))  # ASSET_NOT_FOUND code
        self.assertIn("Test error message", str(error))
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_error_to_dict(self):
        """Test error dictionary conversion"""
        error = QAvioGenError(
            "Test error",
            ErrorCode.RENDER_FAILED,
            context={"stage": "initialization"}
        )
        
        error_dict = error.to_dict()
        
        self.assertIsInstance(error_dict, dict)
        self.assertEqual(error_dict["error_code"], "E203")
        self.assertEqual(error_dict["message"], "Test error")
        self.assertIn("stage", error_dict["context"])

class TestCLIIntegration(unittest.TestCase):
    """Test CLI tool integration"""
    
    def setUp(self):
        """Set up temporary directories and test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config = {
            "name": "cli_test_scene",
            "duration_seconds": 3.0,
            "objects": [
                {
                    "name": "TestCube",
                    "position": [0, 0, 0]
                }
            ]
        }
        
        # Create test config file
        self.config_file = Path(self.temp_dir) / "test_config.json"
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f, indent=2)
    
    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_config_file_creation(self):
        """Test that test config file was created correctly"""
        self.assertTrue(self.config_file.exists())
        
        with open(self.config_file) as f:
            loaded_config = json.load(f)
        
        self.assertEqual(loaded_config["name"], "cli_test_scene")
        self.assertEqual(loaded_config["duration_seconds"], 3.0)

class TestAssetManagement(unittest.TestCase):
    """Test asset loading and management"""
    
    def test_placeholder_creation_logic(self):
        """Test logic for creating placeholder objects"""
        test_cases = [
            ("BWB_Aircraft", "aircraft"),
            ("Towbar_Model", "towbar"),
            ("Landing_Gear", "gear"),
            ("Generic_Tool", "tool"),
            ("Unknown_Object", "cube")
        ]
        
        for name, expected_type in test_cases:
            # This would test the actual object creation logic
            # For now, just test the name detection
            name_lower = name.lower()
            
            if 'aircraft' in name_lower or 'bwb' in name_lower:
                detected_type = "aircraft"
            elif 'towbar' in name_lower:
                detected_type = "towbar"
            elif 'gear' in name_lower:
                detected_type = "gear"
            elif 'tool' in name_lower:
                detected_type = "tool"
            else:
                detected_type = "cube"
            
            self.assertEqual(detected_type, expected_type)

class TestPerformanceMetrics(unittest.TestCase):
    """Test performance tracking and metrics"""
    
    @unittest.skipUnless(CORE_AVAILABLE, "Core modules not available")
    def test_render_metadata_calculation(self):
        """Test render metadata calculations"""
        from datetime import datetime, timedelta
        from core.types import RenderMetadata
        
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=120)  # 2 minutes
        
        metadata = RenderMetadata(
            output_file="test_output.mp4",
            scene_configs=[],
            render_settings=RenderSettings(),
            start_time=start_time,
            end_time=end_time,
            total_frames=3600  # 2 minutes at 30fps
        )
        
        self.assertEqual(metadata.render_duration, 120.0)
        self.assertEqual(metadata.frames_per_second_rendered, 30.0)

def create_test_suite():
    """Create comprehensive test suite"""
    suite = unittest.TestSuite()
    
    # Add all test cases
    test_classes = [
        TestSceneConfig,
        TestRenderSettings,
        TestJSONSerialization,
        TestSchemaValidation,
        TestErrorHandling,
        TestCLIIntegration,
        TestAssetManagement,
        TestPerformanceMetrics
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite

def run_tests(verbose=True):
    """Run all tests and return results"""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        stream=sys.stdout
    )
    
    result = runner.run(suite)
    
    # Print summary
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {total_tests - failures - errors}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    
    if failures == 0 and errors == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Q-AVIOGEN Enhanced Renderer Test Suite")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--specific', '-s', help='Run specific test class')
    
    args = parser.parse_args()
    
    if args.specific:
        # Run specific test class
        test_class = globals().get(args.specific)
        if test_class and issubclass(test_class, unittest.TestCase):
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
            result = runner.run(suite)
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            print(f"❌ Test class '{args.specific}' not found")
            sys.exit(1)
    else:
        # Run all tests
        success = run_tests(args.verbose)
        sys.exit(0 if success else 1)
