#!/usr/bin/env python3
"""
Q-AVIOGEN Avatar Demo - Simple Validation
=========================================

Simplified demo script to show the avatar and voice configuration
for the ATA 32-11-00 nose gear inspection procedure.

Author: Amedeo Pelliccia
Date: 2025-06-20
"""

import json
import yaml
from pathlib import Path

def load_and_display_config():
    """Load and display the instructor configuration"""
    
    config_path = Path(__file__).parent.parent / "configs" / "instructor_config.yaml"
    
    print("🎬 Q-AVIOGEN Avatar Demo - Amedeo Pelliccia Instructor")
    print("=" * 60)
    print(f"Configuration: {config_path}")
    print()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Display scene information
        scene = config.get('scene_config', {})
        print(f"📋 Scene: {scene.get('name', 'Unknown')}")
        print(f"🆔 Scene ID: {scene.get('scene_id', 'Unknown')}")
        print(f"⏱️ Duration: {scene.get('duration', 0)} seconds")
        print(f"🎞️ Resolution: {scene.get('resolution', {}).get('width', 1920)}x{scene.get('resolution', {}).get('height', 1080)}")
        print()
        
        # Display avatar information
        avatar = config.get('avatar', {})
        print(f"🎭 Avatar: {avatar.get('name', 'Unknown')}")
        print(f"📍 Position: {avatar.get('position', [0, 0, 0])}")
        print(f"👔 Clothing: {avatar.get('clothing', {}).get('type', 'Unknown')}")
        print(f"🎬 Animations: {len(avatar.get('animations', []))}")
        print()
        
        # Display voice configuration
        voice = config.get('voice_config', {})
        print(f"🎤 Voice Provider: {voice.get('provider', 'Unknown')}")
        print(f"🗣️ Voice Name: {voice.get('voice_name', 'Unknown')}")
        print(f"🌍 Language: {voice.get('language', 'Unknown')}")
        print(f"🎭 Emotion Support: {voice.get('emotion_support', False)}")
        print()
        
        # Display narration segments
        narration = config.get('narration', {})
        segments = narration.get('segments', [])
        print(f"📝 Narration Segments: {len(segments)}")
        print(f"⏱️ Total Duration: {narration.get('total_duration', 0)} seconds")
        print()
        
        print("🎯 Procedure Steps:")
        for i, segment in enumerate(segments[:7], 1):  # Show first 7 steps
            text = segment.get('text', '')[:60] + "..." if len(segment.get('text', '')) > 60 else segment.get('text', '')
            emotion = segment.get('emotion', 'neutral')
            duration = segment.get('duration', 0)
            print(f"  {i}. [{emotion:>8}] ({duration:4.1f}s) {text}")
        
        print()
        
        # Display timeline markers
        markers = config.get('timeline_markers', [])
        print(f"🏁 Timeline Markers: {len(markers)}")
        for marker in markers[:5]:  # Show first 5 markers
            name = marker.get('name', 'Unknown')
            time = marker.get('time', 0)
            marker_type = marker.get('marker_type', 'unknown')
            print(f"  • {time:5.1f}s - {name} ({marker_type})")
        
        if len(markers) > 5:
            print(f"  ... and {len(markers) - 5} more markers")
        
        print()
        
        # Asset paths
        print("📁 Required Assets:")
        assets = [
            ("Avatar Model", avatar.get('model_path', 'Unknown')),
            ("Face Texture", avatar.get('texture_path', 'Unknown')),
            ("Voice Sample", voice.get('audio_file', 'Unknown'))
        ]
        
        for name, path in assets:
            asset_path = Path(__file__).parent.parent / path if path != 'Unknown' else None
            status = "✅ EXISTS" if asset_path and asset_path.exists() else "📝 PLACEHOLDER"
            print(f"  • {name:13}: {path} ({status})")
        
        print()
        
        # Output configuration
        output = config.get('output', {})
        print("🎥 Output Configuration:")
        print(f"  • Format: {output.get('format', 'mp4').upper()}")
        print(f"  • Codec: {output.get('codec', 'h264').upper()}")
        print(f"  • Quality: {output.get('quality', 'high').title()}")
        print(f"  • Filename: {output.get('filename', 'output.mp4')}")
        
        print()
        print("🎉 Configuration loaded successfully!")
        print()
        print("🚀 Next Steps:")
        print("  1. Replace placeholder assets with real 3D models and audio")
        print("  2. Run: python generate_avatar_video_pipeline.py")
        print("  3. Review generated training video")
        print("  4. Deploy to aviation training systems")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

def main():
    """Main demo function"""
    success = load_and_display_config()
    
    if success:
        print("\n✨ Demo completed successfully!")
    else:
        print("\n❌ Demo failed - check configuration file")

if __name__ == "__main__":
    main()
