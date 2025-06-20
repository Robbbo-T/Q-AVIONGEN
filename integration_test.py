#!/usr/bin/env python3
"""
Q-AVIOGEN End-to-End Integration Test Suite
Complete testing of the video generation pipeline
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import Q-AVIOGEN modules
from core.types import SceneConfig, CameraConfig, RenderConfig, MaterialConfig
from core.errors import create_logger, ConfigurationError, RenderingError
from parser.md_parser import MarkdownParser
from parser.yaml_parser import YAMLParser  
from parser.scene_builder import SceneBuilder
from tts.narration import NarrationGenerator
from blender.simulated_renderer import get_renderer_class

class QAviogenIntegrationTest:
    """Comprehensive integration test suite for Q-AVIOGEN"""
    
    def __init__(self):
        self.logger = create_logger(__name__)
        self.test_results = []
        self.temp_dir = None
        
        # Setup test environment
        self.setup_test_environment()
    
    def setup_test_environment(self):
        """Setup temporary test environment"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="q_aviogen_test_"))
        self.logger.info(f"Test environment created: {self.temp_dir}")
        
        # Create output directories
        (self.temp_dir / "output" / "videos").mkdir(parents=True, exist_ok=True)
        (self.temp_dir / "output" / "frames").mkdir(parents=True, exist_ok=True)
        (self.temp_dir / "output" / "audio").mkdir(parents=True, exist_ok=True)
    
    def cleanup_test_environment(self):
        """Cleanup test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.logger.info("Test environment cleaned up")
    
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        self.logger.info(f"{status} {test_name}: {details}")
    
    def test_core_types_validation(self) -> bool:
        """Test core types and validation"""
        try:
            # Test SceneConfig creation and validation
            scene_config = SceneConfig(
                scene_id="test_scene",
                objects=["aircraft", "hangar"],
                lighting="daylight",
                environment="hangar"
            )
            
            # Test serialization
            config_dict = scene_config.to_dict()
            assert "scene_id" in config_dict
            
            # Test from_dict
            restored_config = SceneConfig.from_dict(config_dict)
            assert restored_config.scene_id == scene_config.scene_id
            
            self.log_test_result("Core Types Validation", True, "All type operations successful")
            return True
            
        except Exception as e:
            self.log_test_result("Core Types Validation", False, f"Error: {e}")
            return False
    
    def test_markdown_parsing(self) -> bool:
        """Test markdown parsing functionality"""
        try:
            # Use existing sample file
            sample_file = project_root / "input" / "markdown" / "00-30-10-01-TowbarAttachment.md"
            
            if not sample_file.exists():
                self.log_test_result("Markdown Parsing", False, "Sample file not found")
                return False
            
            parser = MarkdownParser()
            procedure_data = parser.parse_file(str(sample_file))
            
            # Validate parsed data
            required_keys = ["title", "steps", "metadata"]
            for key in required_keys:
                if key not in procedure_data:
                    self.log_test_result("Markdown Parsing", False, f"Missing key: {key}")
                    return False
            
            steps_count = len(procedure_data.get("steps", []))
            self.log_test_result("Markdown Parsing", True, f"Parsed {steps_count} steps from {procedure_data['title']}")
            return True
            
        except Exception as e:
            self.log_test_result("Markdown Parsing", False, f"Error: {e}")
            return False
    
    def test_scene_building(self) -> bool:
        """Test scene building functionality"""
        try:
            # Create sample procedure data
            sample_procedure = {
                "title": "Test Procedure",
                "steps": [
                    {
                        "step_number": 1,
                        "action": "Attach towbar to aircraft",
                        "description": "Connect the towbar to the nose gear attachment point",
                        "components": ["towbar", "aircraft", "nose_gear"],
                        "duration": 30
                    },
                    {
                        "step_number": 2,
                        "action": "Verify connection",
                        "description": "Check that the towbar is securely attached",
                        "components": ["towbar", "attachment_point"],
                        "duration": 15
                    }
                ],
                "metadata": {
                    "aircraft_type": "commercial",
                    "procedure_type": "ground_operations"
                }
            }
            
            scene_builder = SceneBuilder()
            scenes = scene_builder.build_scenes(sample_procedure)
            
            # Validate scenes
            if not scenes:
                self.log_test_result("Scene Building", False, "No scenes generated")
                return False
            
            # Check scene structure
            for i, scene in enumerate(scenes):
                if not isinstance(scene, dict):
                    self.log_test_result("Scene Building", False, f"Scene {i} is not a dict")
                    return False
                
                required_scene_keys = ["scene_id", "objects", "camera_config"]
                for key in required_scene_keys:
                    if key not in scene:
                        self.log_test_result("Scene Building", False, f"Scene {i} missing key: {key}")
                        return False
            
            self.log_test_result("Scene Building", True, f"Generated {len(scenes)} scenes successfully")
            return True
            
        except Exception as e:
            self.log_test_result("Scene Building", False, f"Error: {e}")
            return False
    
    def test_tts_generation(self) -> bool:
        """Test TTS narration generation"""
        try:
            # Create sample procedure for TTS
            sample_procedure = {
                "title": "TTS Test Procedure",
                "steps": [
                    {
                        "step_number": 1,
                        "action": "Test narration",
                        "description": "This is a test narration for the TTS system",
                        "duration": 10
                    }
                ]
            }
            
            narration_gen = NarrationGenerator(
                engine="pyttsx3",
                output_dir=str(self.temp_dir / "output" / "audio")
            )
            
            audio_files = narration_gen.generate_narration(sample_procedure)
            
            if not audio_files:
                self.log_test_result("TTS Generation", False, "No audio files generated")
                return False
            
            # Check if files exist
            for audio_file in audio_files:
                if not Path(audio_file).exists():
                    self.log_test_result("TTS Generation", False, f"Audio file not found: {audio_file}")
                    return False
            
            self.log_test_result("TTS Generation", True, f"Generated {len(audio_files)} audio files")
            return True
            
        except Exception as e:
            self.log_test_result("TTS Generation", False, f"Error: {e}")
            return False
    
    def test_rendering_pipeline(self) -> bool:
        """Test the rendering pipeline"""
        try:
            # Get renderer class
            renderer_class = get_renderer_class()
            renderer = renderer_class(output_dir=str(self.temp_dir / "output"))
            
            # Create test scene
            test_scene = {
                "scene_id": "test_render_scene",
                "objects": ["aircraft", "towbar"],
                "camera_config": {
                    "position": [0, -10, 5],
                    "target": [0, 0, 0],
                    "fov": 45
                },
                "lighting": "daylight",
                "animation": {
                    "type": "highlight",
                    "target": "towbar",
                    "duration": 3.0
                }
            }
            
            # Render scene
            output_path = renderer.render_scene(test_scene)
            
            if not output_path:
                self.log_test_result("Rendering Pipeline", False, "No output path returned")
                return False
            
            # Check if output exists (for simulated renderer, this will be a placeholder)
            if not Path(output_path).exists():
                self.log_test_result("Rendering Pipeline", False, f"Output file not found: {output_path}")
                return False
            
            self.log_test_result("Rendering Pipeline", True, f"Rendered scene to: {output_path}")
            return True
            
        except Exception as e:
            self.log_test_result("Rendering Pipeline", False, f"Error: {e}")
            return False
    
    def test_end_to_end_workflow(self) -> bool:
        """Test complete end-to-end workflow"""
        try:
            # 1. Parse markdown
            sample_file = project_root / "input" / "markdown" / "00-30-10-01-TowbarAttachment.md"
            if not sample_file.exists():
                self.log_test_result("End-to-End Workflow", False, "Sample markdown file not found")
                return False
            
            parser = MarkdownParser()
            procedure_data = parser.parse_file(str(sample_file))
            
            # 2. Build scenes
            scene_builder = SceneBuilder()
            scenes = scene_builder.build_scenes(procedure_data)
            
            # 3. Generate narration
            narration_gen = NarrationGenerator(
                engine="pyttsx3",
                output_dir=str(self.temp_dir / "output" / "audio")
            )
            audio_files = narration_gen.generate_narration(procedure_data)
            
            # 4. Render scenes
            renderer_class = get_renderer_class()
            renderer = renderer_class(output_dir=str(self.temp_dir / "output"))
            
            rendered_files = []
            for scene in scenes[:2]:  # Limit to first 2 scenes for testing
                try:
                    output_path = renderer.render_scene(scene)
                    if output_path:
                        rendered_files.append(output_path)
                except Exception as render_error:
                    self.logger.warning(f"Scene rendering failed: {render_error}")
            
            # Validate complete workflow
            workflow_success = (
                len(procedure_data.get("steps", [])) > 0 and
                len(scenes) > 0 and
                len(audio_files) > 0 and
                len(rendered_files) > 0
            )
            
            if workflow_success:
                details = f"Processed {len(procedure_data['steps'])} steps, {len(scenes)} scenes, {len(audio_files)} audio files, {len(rendered_files)} rendered files"
                self.log_test_result("End-to-End Workflow", True, details)
                return True
            else:
                self.log_test_result("End-to-End Workflow", False, "Workflow incomplete")
                return False
            
        except Exception as e:
            self.log_test_result("End-to-End Workflow", False, f"Error: {e}")
            return False
    
    def test_configuration_validation(self) -> bool:
        """Test configuration file validation"""
        try:
            # Test scene config schema validation
            schema_file = project_root / "schemas" / "scene_config.schema.json"
            if not schema_file.exists():
                self.log_test_result("Configuration Validation", False, "Schema file not found")
                return False
            
            # Load and validate schema
            with open(schema_file, 'r') as f:
                schema = json.load(f)
            
            # Test valid configuration
            valid_config = {
                "scene_id": "test_config",
                "objects": ["aircraft"],
                "camera_config": {
                    "position": [0, -10, 5],
                    "target": [0, 0, 0],
                    "fov": 45
                },
                "lighting": "daylight"
            }
            
            # Basic validation (would require jsonschema library for full validation)
            required_props = schema.get("required", [])
            for prop in required_props:
                if prop not in valid_config:
                    self.log_test_result("Configuration Validation", False, f"Missing required property: {prop}")
                    return False
            
            self.log_test_result("Configuration Validation", True, "Configuration validation successful")
            return True
            
        except Exception as e:
            self.log_test_result("Configuration Validation", False, f"Error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        self.logger.info("🚀 Starting Q-AVIOGEN Integration Test Suite")
        
        tests = [
            ("Core Types Validation", self.test_core_types_validation),
            ("Markdown Parsing", self.test_markdown_parsing),
            ("Scene Building", self.test_scene_building),
            ("TTS Generation", self.test_tts_generation),
            ("Rendering Pipeline", self.test_rendering_pipeline),
            ("Configuration Validation", self.test_configuration_validation),
            ("End-to-End Workflow", self.test_end_to_end_workflow),
        ]
        
        for test_name, test_func in tests:
            self.logger.info(f"Running test: {test_name}")
            try:
                test_func()
            except Exception as e:
                self.log_test_result(test_name, False, f"Test crashed: {e}")
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"🎯 Test Summary: {passed_tests}/{total_tests} tests passed ({summary['success_rate']:.1f}%)")
        
        return summary
    
    def generate_test_report(self, output_file: str = None) -> str:
        """Generate detailed test report"""
        if output_file is None:
            output_file = str(project_root / "test_report.json")
        
        summary = self.run_all_tests()
        
        # Save detailed report
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Generate markdown report
        md_report = self.generate_markdown_report(summary)
        md_file = output_file.replace('.json', '.md')
        
        with open(md_file, 'w') as f:
            f.write(md_report)
        
        self.logger.info(f"📊 Test report saved: {output_file}")
        self.logger.info(f"📄 Markdown report saved: {md_file}")
        
        return output_file
    
    def generate_markdown_report(self, summary: Dict[str, Any]) -> str:
        """Generate markdown test report"""
        report_lines = [
            "# Q-AVIOGEN Integration Test Report",
            "",
            f"**Generated:** {summary['timestamp']}",
            f"**Total Tests:** {summary['total_tests']}",
            f"**Passed:** {summary['passed_tests']}",
            f"**Failed:** {summary['failed_tests']}",
            f"**Success Rate:** {summary['success_rate']:.1f}%",
            "",
            "## Test Results",
            ""
        ]
        
        for result in summary['results']:
            status_emoji = "✅" if result['success'] else "❌"
            status_text = "PASS" if result['success'] else "FAIL"
            
            report_lines.extend([
                f"### {status_emoji} {result['test']} - {status_text}",
                "",
                f"**Details:** {result['details']}",
                f"**Timestamp:** {result['timestamp']}",
                ""
            ])
        
        # Add recommendations
        if summary['success_rate'] == 100:
            report_lines.extend([
                "## 🎉 All Tests Passed!",
                "",
                "The Q-AVIOGEN system is ready for production use. Key achievements:",
                "",
                "- ✅ Core architecture is stable",
                "- ✅ All parsing pipelines work correctly", 
                "- ✅ TTS generation is functional",
                "- ✅ Rendering pipeline is operational",
                "- ✅ End-to-end workflow is validated",
                "",
                "### Next Steps:",
                "1. Deploy to staging environment",
                "2. Run performance benchmarks",
                "3. Test with real aerospace procedures",
                "4. Integrate with CI/CD pipeline"
            ])
        else:
            report_lines.extend([
                "## ⚠️ Some Tests Failed",
                "",
                "The system requires attention before production deployment.",
                "",
                "### Immediate Actions Required:",
                "1. Review failed test details above",
                "2. Fix identified issues",
                "3. Re-run integration tests",
                "4. Consider additional testing scenarios"
            ])
        
        return "\n".join(report_lines)


def main():
    """Main test execution"""
    print("🔬 Q-AVIOGEN Integration Test Suite")
    print("=" * 50)
    
    test_suite = QAviogenIntegrationTest()
    
    try:
        # Run tests and generate report
        report_file = test_suite.generate_test_report()
        
        print(f"\n📊 Complete test report available at: {report_file}")
        print("📄 Markdown report also generated (.md file)")
        
        # Print summary to console
        with open(report_file, 'r') as f:
            summary = json.load(f)
        
        print(f"\n🎯 Final Results: {summary['passed_tests']}/{summary['total_tests']} tests passed")
        
        if summary['success_rate'] == 100:
            print("🎉 Q-AVIOGEN is ready for deployment!")
        else:
            print("⚠️  Some issues need attention before deployment.")
            
    finally:
        test_suite.cleanup_test_environment()


if __name__ == "__main__":
    main()
