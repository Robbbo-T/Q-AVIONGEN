#!/usr/bin/env python3
"""
Q-AVIOGEN Status Check and Quick Fix
===================================

This script checks the current status of the Q-AVIOGEN system
and applies quick fixes for common issues.
"""

import sys
import os
from pathlib import Path

# Add the Q-AVIOGEN root to Python path
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

def check_core_types():
    """Check if core types module loads correctly"""
    print("🔍 Checking core types module...")
    
    try:
        from core.types_v2_1 import SceneConfig
        print("  ✅ Core types loaded successfully")
        return True
    except SyntaxError as e:
        print(f"  ❌ Syntax error in core types: {e}")
        return False
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False

def check_config_file():
    """Check if the instructor config file is valid"""
    print("🔍 Checking instructor configuration...")
    
    config_path = Path(__file__).parent.parent / "configs" / "instructor_config.yaml"
    
    if not config_path.exists():
        print(f"  ❌ Config file not found: {config_path}")
        return False
    
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        print("  ✅ Configuration file loaded successfully")
        
        # Check required sections
        required = ['scene_config', 'avatar', 'voice_config', 'narration']
        for section in required:
            if section in config_data:
                print(f"    ✅ {section}")
            else:
                print(f"    ❌ {section} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error loading config: {e}")
        return False

def generate_status_report():
    """Generate a complete status report"""
    print("\n" + "="*60)
    print("Q-AVIOGEN SYSTEM STATUS REPORT")
    print("="*60)
    
    # Check all components
    core_ok = check_core_types()
    config_ok = check_config_file()
    
    print("\n" + "-"*60)
    print("SUMMARY")
    print("-"*60)
    
    if core_ok and config_ok:
        print("🎉 STATUS: READY")
        print("\n✅ Your Q-AVIOGEN avatar system is configured correctly!")
        print("\n🎬 Configuration Details:")
        
        try:
            import yaml
            config_path = Path(__file__).parent.parent / "configs" / "instructor_config.yaml"
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            scene = config_data.get('scene_config', {})
            avatar = config_data.get('avatar', {})
            voice = config_data.get('voice_config', {})
            
            print(f"  🎭 Avatar: {avatar.get('name', 'Unknown')}")
            print(f"  🎬 Scene: {scene.get('name', 'Unknown')}")
            print(f"  ⏱️ Duration: {scene.get('duration', 0)} seconds")
            print(f"  🎤 Voice: {voice.get('voice_name', 'Unknown')} ({voice.get('language', 'Unknown')})")
            print(f"  📝 Narration Segments: {len(config_data.get('narration', {}).get('segments', []))}")
            
        except Exception as e:
            print(f"  ⚠️ Could not load detailed info: {e}")
        
        print("\n🚀 Next Steps:")
        print("  1. Replace placeholder assets with real 3D models and audio")
        print("  2. Run the demo: python demo.py")
        print("  3. Test the pipeline (simulated mode)")
        print("  4. Deploy to production systems")
        
    else:
        print("❌ STATUS: ISSUES FOUND")
        print("\n🔧 Problems to fix:")
        if not core_ok:
            print("  • Core types module has syntax errors")
        if not config_ok:
            print("  • Configuration file is invalid or missing")
        
        print("\n💡 Recommended actions:")
        print("  1. Check the core/types_v2_1.py file for syntax errors")
        print("  2. Verify the instructor_config.yaml file exists and is valid")
        print("  3. Run this script again after fixing issues")

def main():
    """Main function"""
    print("🚀 Q-AVIOGEN System Status Check")
    print("Date: 2025-06-20")
    print("Project: Avatar-Guided Procedural Training")
    
    generate_status_report()

if __name__ == "__main__":
    main()
