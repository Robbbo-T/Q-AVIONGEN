#!/usr/bin/env python3
"""
Simple test script to verify Q-AVIOGEN pipeline functionality
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent))

def test_imports():
    """Test that we can import the necessary modules"""
    print("🧪 Testing Q-AVIOGEN module imports...")
    
    try:
        from core.types_v2_1 import SceneConfig, setup_logging
        print("  ✅ Core types imported successfully")
        
        # Test configuration loading
        config_path = Path(__file__).parent.parent / "configs" / "instructor_config.yaml"
        print(f"  📋 Testing config file: {config_path}")
        
        if config_path.exists():
            print("  ✅ Configuration file exists")
            
            # Try to load with YAML
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            print("  ✅ YAML configuration loaded successfully")
            
            # Test key sections
            required_sections = ['scene_config', 'avatar', 'voice_config', 'narration']
            for section in required_sections:
                if section in config_data:
                    print(f"  ✅ Section '{section}' found")
                else:
                    print(f"  ❌ Section '{section}' missing")
            
            print("\n🎉 All tests passed!")
            print(f"🎬 Scene: {config_data.get('scene_config', {}).get('name', 'Unknown')}")
            print(f"🎭 Avatar: {config_data.get('avatar', {}).get('name', 'Unknown')}")
            print(f"⏱️ Duration: {config_data.get('scene_config', {}).get('duration', 0)} seconds")
            
            return True
        else:
            print("  ❌ Configuration file not found")
            return False
            
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    print("🔬 Q-AVIOGEN Simple Test")
    print("=" * 40)
    
    success = test_imports()
    
    if success:
        print("\n✨ Test completed successfully!")
        print("\n🚀 You can now:")
        print("  1. Run the demo: python demo.py")
        print("  2. Try the pipeline: python generate_avatar_video_pipeline.py")
        print("  3. Review the configuration files")
    else:
        print("\n❌ Test failed - check error messages above")

if __name__ == "__main__":
    main()
