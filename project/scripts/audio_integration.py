#!/usr/bin/env python3
"""
Q-AVIOGEN Audio Integration Script
=================================

Script to integrate real audio files (M4A, WAV) into the Q-AVIOGEN system.
Handles format conversion, validation, and configuration updates.

Author: Amedeo Pelliccia
Version: 2.1
Date: 2025-06-20
"""

import sys
import os
import shutil
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List

def check_ffmpeg_available() -> bool:
    """Check if FFmpeg is available for audio conversion"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_m4a_to_wav(input_file: str, output_file: str, 
                      sample_rate: int = 48000, channels: int = 1) -> bool:
    """Convert M4A to WAV using FFmpeg"""
    
    if not check_ffmpeg_available():
        print("❌ FFmpeg not available for audio conversion")
        return False
    
    try:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-ar', str(sample_rate),  # Sample rate
            '-ac', str(channels),     # Channels (1=mono, 2=stereo)
            '-sample_fmt', 's24',     # 24-bit depth
            '-y',                     # Overwrite output
            output_file
        ]
        
        print(f"🔄 Converting {input_file} to {output_file}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Conversion successful: {output_file}")
            return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def copy_audio_file(source: str, destination: str) -> bool:
    """Copy audio file to destination"""
    try:
        # Create destination directory if it doesn't exist
        dest_path = Path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source, destination)
        print(f"✅ Copied: {source} → {destination}")
        return True
        
    except Exception as e:
        print(f"❌ Copy failed: {e}")
        return False

def update_config_for_real_audio(config_path: str) -> bool:
    """Update instructor configuration to use real audio files"""
    
    try:
        # Load current configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Update voice configuration to use real audio
        if 'voice_config' in config:
            config['voice_config']['use_real_audio'] = True
            config['voice_config']['audio_file'] = "assets/audio/real_samples/amedeo_voice_48k.wav"
            
            # Add timestamp of integration
            config['voice_config']['integration_date'] = "2025-06-20"
            config['voice_config']['integration_status'] = "real_audio_integrated"
        
        # Save updated configuration
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Configuration updated: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration update failed: {e}")
        return False

def validate_integration(project_root: str) -> Dict[str, Any]:
    """Validate that audio integration was successful"""
    
    validation = {
        'success': True,
        'files_found': [],
        'files_missing': [],
        'config_updated': False,
        'recommendations': []
    }
    
    # Check for required files
    required_files = [
        "assets/audio/real_samples/amedeo_voice_48k.wav",
        "configs/instructor_config.yaml"
    ]
    
    for file_path in required_files:
        full_path = Path(project_root) / file_path
        if full_path.exists():
            validation['files_found'].append(file_path)
        else:
            validation['files_missing'].append(file_path)
            validation['success'] = False
    
    # Check configuration
    config_path = Path(project_root) / "configs" / "instructor_config.yaml"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            voice_config = config.get('voice_config', {})
            if voice_config.get('use_real_audio', False):
                validation['config_updated'] = True
            
        except Exception as e:
            validation['recommendations'].append(f"Configuration validation error: {e}")
    
    return validation

def generate_integration_report(validation: Dict[str, Any]) -> str:
    """Generate integration status report"""
    
    report = []
    report.append("=" * 60)
    report.append("Q-AVIOGEN AUDIO INTEGRATION REPORT")
    report.append("=" * 60)
    report.append(f"Integration Date: 2025-06-20")
    report.append(f"Status: {'✅ SUCCESS' if validation['success'] else '❌ INCOMPLETE'}")
    report.append("")
    
    if validation['files_found']:
        report.append("✅ FILES INTEGRATED:")
        for file_path in validation['files_found']:
            report.append(f"  • {file_path}")
        report.append("")
    
    if validation['files_missing']:
        report.append("❌ FILES MISSING:")
        for file_path in validation['files_missing']:
            report.append(f"  • {file_path}")
        report.append("")
    
    report.append(f"Configuration Updated: {'✅ YES' if validation['config_updated'] else '❌ NO'}")
    report.append("")
    
    if validation['success']:
        report.append("🎉 INTEGRATION COMPLETE!")
        report.append("")
        report.append("Next Steps:")
        report.append("1. Run audio analysis: python audio_analyzer.py amedeo_voice_48k.wav")
        report.append("2. Test TTS pipeline with real voice")
        report.append("3. Generate test video with avatar")
        report.append("4. Validate audio-visual synchronization")
    else:
        report.append("⚠️ INTEGRATION INCOMPLETE")
        report.append("")
        report.append("Required Actions:")
        report.append("1. Copy real audio files to project")
        report.append("2. Run integration script again")
        report.append("3. Validate all files are in place")
    
    if validation['recommendations']:
        report.append("")
        report.append("💡 RECOMMENDATIONS:")
        for rec in validation['recommendations']:
            report.append(f"  • {rec}")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)

def main():
    """Main integration function"""
    
    print("🎵 Q-AVIOGEN Audio Integration Script")
    print("=" * 50)
    
    # Get project root (go up 2 levels from scripts directory)
    project_root = Path(__file__).parent.parent
    
    print(f"Project Root: {project_root}")
    print()
    
    # Check if real audio files are available
    print("🔍 Checking for real audio files...")
    
    # Look for files in various possible locations
    possible_locations = [
        project_root / "Grabación.m4a",
        project_root / "amedeo_voice_48k.wav",
        Path.cwd() / "Grabación.m4a",
        Path.cwd() / "amedeo_voice_48k.wav"
    ]
    
    found_files = []
    for location in possible_locations:
        if location.exists():
            found_files.append(location)
            print(f"  ✅ Found: {location}")
    
    if not found_files:
        print("  ❌ No audio files found in current directory or project root")
        print()
        print("Please copy your audio files to one of these locations:")
        print("  • Grabación.m4a")
        print("  • amedeo_voice_48k.wav")
        print()
        print("Then run this script again.")
        return
    
    # Create real_samples directory
    real_samples_dir = project_root / "assets" / "audio" / "real_samples"
    real_samples_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Created directory: {real_samples_dir}")
    
    # Process found files
    for file_path in found_files:
        filename = file_path.name
        destination = real_samples_dir / filename
        
        if filename.endswith('.m4a'):
            # Copy M4A file
            copy_audio_file(str(file_path), str(destination))
            
            # Convert to WAV if needed
            wav_filename = filename.replace('.m4a', '_48k.wav')
            wav_destination = real_samples_dir / wav_filename
            
            if not wav_destination.exists():
                success = convert_m4a_to_wav(str(destination), str(wav_destination))
                if not success:
                    print("⚠️ M4A to WAV conversion failed - you may need to install FFmpeg")
        
        elif filename.endswith('.wav'):
            # Copy WAV file directly
            copy_audio_file(str(file_path), str(destination))
    
    # Update configuration
    print("\n🔧 Updating configuration...")
    config_path = project_root / "configs" / "instructor_config.yaml"
    config_updated = update_config_for_real_audio(str(config_path))
    
    # Validate integration
    print("\n🔍 Validating integration...")
    validation = validate_integration(str(project_root))
    
    # Generate and display report
    report = generate_integration_report(validation)
    print("\n" + report)
    
    # Save report
    report_file = project_root / "audio_integration_report.txt"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {report_file}")
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")

if __name__ == "__main__":
    main()
