#!/usr/bin/env python3
"""
Q-AVIOGEN System Verification Script
Comprehensive testing without relying on terminal execution
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_status(message, success=True):
    """Print status with emoji"""
    emoji = "✅" if success else "❌"
    print(f"{emoji} {message}")

def test_imports():
    """Test all critical imports"""
    print("\n🔍 Testing imports...")
    
    try:
        # Core modules
        from core.types import SceneConfig, CameraConfig, RenderConfig
        print_status("Core types imported")
        
        from core.errors import RenderingError, ConfigurationError, create_logger
        print_status("Core errors imported")
        
        # Parser modules
        from parser.md_parser import MarkdownParser
        print_status("Markdown parser imported")
        
        from parser.yaml_parser import YAMLParser
        print_status("YAML parser imported")
        
        from parser.scene_builder import SceneBuilder
        print_status("Scene builder imported")
        
        # TTS module
        from tts.narration import NarrationGenerator
        print_status("TTS narration imported")
        
        # Blender modules
        from blender.simulated_renderer import SimulatedBlenderRenderer, get_renderer_class
        print_status("Simulated renderer imported")
        
        try:
            from blender.enhanced_renderer import EnhancedBlenderRenderer
            print_status("Enhanced renderer imported")
        except ImportError as e:
            print_status(f"Enhanced renderer import failed (expected): {e}", False)
        
        return True
        
    except Exception as e:
        print_status(f"Import failed: {e}", False)
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality of core components"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test MarkdownParser
        from parser.md_parser import MarkdownParser
        parser = MarkdownParser()
        print_status("Markdown parser instantiated")
        
        # Test SceneBuilder
        from parser.scene_builder import SceneBuilder
        scene_builder = SceneBuilder()
        print_status("Scene builder instantiated")
        
        # Test NarrationGenerator
        from tts.narration import NarrationGenerator
        narration_gen = NarrationGenerator(engine="pyttsx3")
        print_status("Narration generator instantiated")
        
        # Test SimulatedRenderer
        from blender.simulated_renderer import get_renderer_class
        RendererClass = get_renderer_class()
        renderer = RendererClass()
        print_status(f"Renderer instantiated: {RendererClass.__name__}")
        
        return True
        
    except Exception as e:
        print_status(f"Functionality test failed: {e}", False)
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that required files and directories exist"""
    print("\n📁 Testing file structure...")
    
    required_dirs = [
        "input", "input/markdown", "output", "output/videos", 
        "parser", "blender", "tts", "core", "schemas", "tests"
    ]
    
    required_files = [
        "main.py", "requirements.txt", "setup.py", "README.md",
        "core/types.py", "core/errors.py", 
        "schemas/scene_config.schema.json"
    ]
    
    all_exist = True
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print_status(f"Directory exists: {dir_name}")
        else:
            print_status(f"Directory missing: {dir_name}", False)
            all_exist = False
    
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print_status(f"File exists: {file_name}")
        else:
            print_status(f"File missing: {file_name}", False)
            all_exist = False
    
    return all_exist

def test_sample_data():
    """Test if sample input data exists and can be parsed"""
    print("\n📄 Testing sample data...")
    
    try:
        sample_md = project_root / "input" / "markdown" / "00-30-10-01-TowbarAttachment.md"
        
        if sample_md.exists():
            print_status("Sample markdown file exists")
            
            # Try to parse it
            from parser.md_parser import MarkdownParser
            parser = MarkdownParser()
            
            procedure_data = parser.parse_file(str(sample_md))
            print_status(f"Sample file parsed successfully: {procedure_data.get('title', 'Unknown')}")
            print_status(f"Steps found: {len(procedure_data.get('steps', []))}")
            
            return True
        else:
            print_status("Sample markdown file not found", False)
            return False
            
    except Exception as e:
        print_status(f"Sample data test failed: {e}", False)
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    print("🚀 Q-AVIOGEN System Verification")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Sample Data", test_sample_data)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"{test_name} test crashed: {e}", False)
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        emoji = "✅" if result else "❌"
        print(f"{emoji} {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Q-AVIOGEN system is ready!")
        print("\n📝 Next steps:")
        print("  1. Run: python main.py --help")
        print("  2. Test with sample: python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md")
        print("  3. Try batch processing: python batch_render.py")
    else:
        print("⚠️  Some components need attention before the system is fully operational.")
    
    return passed == total

if __name__ == "__main__":
    main()
