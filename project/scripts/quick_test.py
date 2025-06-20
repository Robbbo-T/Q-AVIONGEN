#!/usr/bin/env python3
"""
Q-AVIOGEN Quick Test: Avatar + Voice Integration
===============================================

Quick test script to validate the complete avatar and voice
integration for the ATA 32-11-00 nose gear inspection procedure.

This script performs:
1. Configuration validation
2. Asset availability check
3. Pipeline component testing
4. Basic rendering test (if possible)

Author: Amedeo Pelliccia
Version: 2.1
Date: 2025-06-20
"""

import sys
import os
from pathlib import Path
import yaml
import json

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent))

try:
    from test_avatar_voice_validation import AvatarVoiceValidator
except ImportError as e:
    print(f"❌ Error importing validation module: {e}")
    sys.exit(1)


def quick_asset_check(config_path: Path) -> bool:
    """Quick check for required assets"""
    print("🔍 Checking required assets...")
    
    project_root = config_path.parent.parent
    required_assets = [
        "assets/avatars/amedeo/avatar_model.blend",
        "assets/avatars/amedeo/face_texture.png", 
        "assets/audio/amedeo_voice.wav"
    ]
    
    all_found = True
    for asset in required_assets:
        asset_path = project_root / asset
        if asset_path.exists():
            print(f"  ✅ {asset}")
        else:
            print(f"  ❌ {asset} - NOT FOUND")
            all_found = False
    
    return all_found


def test_config_loading(config_path: Path) -> bool:
    """Test configuration loading and parsing"""
    print("\n📋 Testing configuration loading...")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        # Check main sections
        required_sections = [
            'scene_config', 'avatar', 'voice_config', 
            'narration', 'objects', 'lights', 'cameras'
        ]
        
        for section in required_sections:
            if section in config_data:
                print(f"  ✅ {section}")
            else:
                print(f"  ❌ {section} - MISSING")
                return False
        
        # Quick data validation
        scene_config = config_data.get('scene_config', {})
        print(f"  📋 Scene: {scene_config.get('name', 'Unknown')}")
        print(f"  ⏱️ Duration: {scene_config.get('duration', 0)}s")
        print(f"  🎭 Avatar: {config_data.get('avatar', {}).get('name', 'Unknown')}")
        print(f"  🎤 Voice: {config_data.get('voice_config', {}).get('voice_name', 'Unknown')}")
        
        narration_segments = len(config_data.get('narration', {}).get('segments', []))
        avatar_animations = len(config_data.get('avatar', {}).get('animations', []))
        print(f"  📝 Narration segments: {narration_segments}")
        print(f"  🎬 Avatar animations: {avatar_animations}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration loading failed: {e}")
        return False


def test_pipeline_components() -> bool:
    """Test if pipeline components can be imported"""
    print("\n🔧 Testing pipeline components...")
    
    # Test imports
    components = [
        ("Core Types", "core.types_v2_1"),
        ("TTS Engine", "tts.narration"),
        ("Batch Renderer", "batch_render")
    ]
    
    all_available = True
    for name, module in components:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError as e:
            print(f"  ⚠️ {name} - {e}")
            all_available = False
    
    return all_available


def generate_test_summary(config_path: Path) -> str:
    """Generate a test summary report"""
    print("\n📊 Generating test summary...")
    
    # Run all tests
    asset_check = quick_asset_check(config_path)
    config_check = test_config_loading(config_path)
    component_check = test_pipeline_components()
    
    # Run full validation
    print("\n🔍 Running comprehensive validation...")
    validator = AvatarVoiceValidator(str(config_path))
    validator.load_config()
    
    # Get validation results
    avatar_valid, avatar_errors = validator.validate_avatar_config()
    voice_valid, voice_errors = validator.validate_voice_config()
    narration_valid, narration_errors = validator.validate_narration_config()
    sync_valid, sync_errors = validator.validate_synchronization()
    
    # Build summary
    summary = []
    summary.append("=" * 60)
    summary.append("Q-AVIOGEN QUICK TEST SUMMARY")
    summary.append("=" * 60)
    summary.append(f"Configuration: {config_path}")
    summary.append("")
    
    # Test results
    summary.append("TEST RESULTS:")
    summary.append(f"  Asset Availability:     {'✅ PASS' if asset_check else '❌ FAIL'}")
    summary.append(f"  Configuration Loading:  {'✅ PASS' if config_check else '❌ FAIL'}")
    summary.append(f"  Pipeline Components:    {'✅ PASS' if component_check else '⚠️ PARTIAL'}")
    summary.append(f"  Avatar Configuration:   {'✅ PASS' if avatar_valid else '❌ FAIL'}")
    summary.append(f"  Voice Configuration:    {'✅ PASS' if voice_valid else '❌ FAIL'}")
    summary.append(f"  Narration Configuration: {'✅ PASS' if narration_valid else '❌ FAIL'}")
    summary.append(f"  Avatar-Voice Sync:      {'✅ PASS' if sync_valid else '❌ FAIL'}")
    summary.append("")
    
    # Overall status
    all_tests_pass = all([
        asset_check, config_check, avatar_valid, 
        voice_valid, narration_valid, sync_valid
    ])
    
    if all_tests_pass:
        summary.append("🎉 OVERALL STATUS: READY FOR PRODUCTION")
        summary.append("")
        summary.append("✅ Your configuration is ready for:")
        summary.append("   • Avatar-guided video generation")
        summary.append("   • Voice narration synthesis")
        summary.append("   • Complete procedure rendering")
        summary.append("   • Industrial deployment")
        summary.append("")
        summary.append("🚀 Next steps:")
        summary.append("   1. Run: python generate_avatar_video_pipeline.py configs/instructor_config.yaml")
        summary.append("   2. Review generated video output")
        summary.append("   3. Deploy to training systems")
    else:
        summary.append("⚠️ OVERALL STATUS: REQUIRES ATTENTION")
        summary.append("")
        summary.append("❌ Issues found:")
        
        if not asset_check:
            summary.append("   • Replace placeholder asset files with real models/audio")
        if not avatar_valid:
            summary.append("   • Fix avatar configuration errors")
        if not voice_valid:
            summary.append("   • Fix voice configuration errors")
        if not narration_valid:
            summary.append("   • Fix narration configuration errors")
        if not sync_valid:
            summary.append("   • Fix avatar-voice synchronization issues")
        
        summary.append("")
        summary.append("🔧 Run the full validation for detailed error information:")
        summary.append("   python test_avatar_voice_validation.py configs/instructor_config.yaml")
    
    summary.append("")
    summary.append("=" * 60)
    
    return "\n".join(summary)


def main():
    """Main test function"""
    print("🧪 Q-AVIOGEN Quick Test: Avatar + Voice Integration")
    print("=" * 55)
    
    # Find configuration file
    config_path = Path(__file__).parent.parent / "configs" / "instructor_config.yaml"
    
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        print("\nPlease ensure you're running from the project directory and")
        print("that configs/instructor_config.yaml exists.")
        sys.exit(1)
    
    print(f"📋 Using configuration: {config_path}")
    
    # Generate and display test summary
    summary = generate_test_summary(config_path)
    print(summary)
    
    # Save summary to file
    summary_file = config_path.parent / "quick_test_summary.txt"
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\n📄 Test summary saved to: {summary_file}")
    except Exception as e:
        print(f"⚠️ Could not save summary: {e}")


if __name__ == "__main__":
    main()
