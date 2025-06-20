#!/usr/bin/env python3
"""
Q-AVIOGEN Audio File Analyzer
============================

Script to analyze and validate audio files for the Q-AVIOGEN voice synthesis system.
Specifically designed to validate Amedeo Pelliccia's voice samples.

Author: Amedeo Pelliccia
Version: 2.1
Date: 2025-06-20
"""

import sys
import os
import wave
from pathlib import Path
from typing import Dict, Any, Optional

def analyze_wav_file(file_path: str) -> Dict[str, Any]:
    """Analyze a WAV file and return its properties"""
    
    try:
        with wave.open(file_path, 'rb') as wav_file:
            # Get basic properties
            frames = wav_file.getnframes()
            sample_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            
            # Calculate duration
            duration = frames / float(sample_rate)
            
            # Calculate bit depth
            bit_depth = sample_width * 8
            
            return {
                'file_path': file_path,
                'format': 'WAV',
                'duration_seconds': duration,
                'sample_rate_hz': sample_rate,
                'channels': channels,
                'bit_depth': bit_depth,
                'total_frames': frames,
                'file_size_bytes': os.path.getsize(file_path),
                'is_valid': True,
                'analysis_errors': []
            }
            
    except Exception as e:
        return {
            'file_path': file_path,
            'format': 'Unknown',
            'is_valid': False,
            'analysis_errors': [str(e)]
        }

def validate_audio_requirements(audio_info: Dict[str, Any]) -> Dict[str, Any]:
    """Validate audio file against Q-AVIOGEN requirements"""
    
    validation = {
        'meets_requirements': True,
        'warnings': [],
        'errors': [],
        'recommendations': []
    }
    
    if not audio_info.get('is_valid'):
        validation['meets_requirements'] = False
        validation['errors'].append("File could not be analyzed")
        return validation
    
    # Check sample rate
    sample_rate = audio_info.get('sample_rate_hz', 0)
    if sample_rate < 44100:
        validation['errors'].append(f"Sample rate too low: {sample_rate}Hz (minimum: 44.1kHz)")
        validation['meets_requirements'] = False
    elif sample_rate != 48000:
        validation['warnings'].append(f"Sample rate is {sample_rate}Hz, preferred: 48kHz")
    
    # Check bit depth
    bit_depth = audio_info.get('bit_depth', 0)
    if bit_depth < 16:
        validation['errors'].append(f"Bit depth too low: {bit_depth}-bit (minimum: 16-bit)")
        validation['meets_requirements'] = False
    elif bit_depth == 16:
        validation['recommendations'].append("Consider using 24-bit for better quality")
    
    # Check channels
    channels = audio_info.get('channels', 0)
    if channels != 1:
        if channels == 2:
            validation['warnings'].append("Stereo audio detected, mono preferred for voice synthesis")
        else:
            validation['errors'].append(f"Unsupported channel count: {channels} (should be 1 for mono)")
    
    # Check duration
    duration = audio_info.get('duration_seconds', 0)
    if duration < 10:
        validation['warnings'].append(f"Duration is short: {duration:.1f}s (recommended: 30-60s)")
    elif duration > 120:
        validation['warnings'].append(f"Duration is long: {duration:.1f}s (recommended: 30-60s)")
    
    # Check file size
    file_size_mb = audio_info.get('file_size_bytes', 0) / (1024 * 1024)
    if file_size_mb > 50:
        validation['warnings'].append(f"Large file size: {file_size_mb:.1f}MB")
    
    return validation

def generate_audio_report(audio_info: Dict[str, Any], validation: Dict[str, Any]) -> str:
    """Generate a comprehensive audio analysis report"""
    
    report = []
    report.append("=" * 70)
    report.append("Q-AVIOGEN AUDIO ANALYSIS REPORT")
    report.append("=" * 70)
    report.append(f"File: {audio_info.get('file_path', 'Unknown')}")
    report.append(f"Analysis Date: 2025-06-20")
    report.append("")
    
    if audio_info.get('is_valid'):
        report.append("📊 AUDIO PROPERTIES:")
        report.append("-" * 40)
        report.append(f"Format:      {audio_info.get('format', 'Unknown')}")
        report.append(f"Duration:    {audio_info.get('duration_seconds', 0):.2f} seconds")
        report.append(f"Sample Rate: {audio_info.get('sample_rate_hz', 0):,} Hz")
        report.append(f"Bit Depth:   {audio_info.get('bit_depth', 0)}-bit")
        report.append(f"Channels:    {audio_info.get('channels', 0)} ({'Mono' if audio_info.get('channels') == 1 else 'Stereo' if audio_info.get('channels') == 2 else 'Multi-channel'})")
        report.append(f"File Size:   {audio_info.get('file_size_bytes', 0) / (1024*1024):.1f} MB")
        report.append("")
        
        # Validation results
        report.append("🔍 VALIDATION RESULTS:")
        report.append("-" * 40)
        
        status = "✅ PASSED" if validation['meets_requirements'] else "❌ FAILED"
        report.append(f"Overall Status: {status}")
        report.append("")
        
        if validation['errors']:
            report.append("❌ ERRORS (Must Fix):")
            for error in validation['errors']:
                report.append(f"  • {error}")
            report.append("")
        
        if validation['warnings']:
            report.append("⚠️ WARNINGS:")
            for warning in validation['warnings']:
                report.append(f"  • {warning}")
            report.append("")
        
        if validation['recommendations']:
            report.append("💡 RECOMMENDATIONS:")
            for rec in validation['recommendations']:
                report.append(f"  • {rec}")
            report.append("")
        
        # Q-AVIOGEN compatibility
        report.append("🎬 Q-AVIOGEN COMPATIBILITY:")
        report.append("-" * 40)
        
        if validation['meets_requirements']:
            report.append("✅ Compatible with Q-AVIOGEN voice synthesis")
            report.append("✅ Ready for TTS training and avatar integration")
            report.append("✅ Suitable for production use")
        else:
            report.append("❌ Requires processing before use")
            report.append("⚠️ May need format conversion or quality improvement")
        
        report.append("")
        
        # Next steps
        report.append("🚀 NEXT STEPS:")
        report.append("-" * 40)
        
        if validation['meets_requirements']:
            report.append("1. Update instructor_config.yaml audio_file path")
            report.append("2. Test with TTS synthesis pipeline")
            report.append("3. Validate avatar-voice synchronization")
            report.append("4. Generate test video with real voice")
        else:
            report.append("1. Fix errors listed above")
            report.append("2. Re-process audio file if needed")
            report.append("3. Re-run analysis after fixes")
            report.append("4. Proceed with integration once validated")
        
    else:
        report.append("❌ ANALYSIS FAILED:")
        report.append("-" * 40)
        for error in audio_info.get('analysis_errors', []):
            report.append(f"  • {error}")
        report.append("")
        report.append("Please check file format and try again.")
    
    report.append("")
    report.append("=" * 70)
    
    return "\n".join(report)

def main():
    """Main analysis function"""
    
    if len(sys.argv) < 2:
        print("Usage: python audio_analyzer.py <audio_file.wav>")
        print("Example: python audio_analyzer.py amedeo_voice_48k.wav")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        sys.exit(1)
    
    print("🎵 Q-AVIOGEN Audio File Analyzer")
    print("=" * 50)
    print(f"Analyzing: {audio_file}")
    print()
    
    # Analyze audio file
    audio_info = analyze_wav_file(audio_file)
    
    # Validate against requirements
    validation = validate_audio_requirements(audio_info)
    
    # Generate and display report
    report = generate_audio_report(audio_info, validation)
    print(report)
    
    # Save report to file
    report_file = Path(audio_file).stem + "_analysis_report.txt"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {report_file}")
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")

if __name__ == "__main__":
    main()
