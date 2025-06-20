#!/usr/bin/env python3
"""
Q-AVIOGEN Avatar & Voice Validation Test
========================================

Test script to validate avatar and voice configuration for the
ATA 32-11-00 Nose Landing Gear inspection procedure.

Author: Amedeo Pelliccia
Version: 2.1
Date: 2025-06-20
"""

import sys
import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add parent directory to path to import Q-AVIOGEN modules
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from core.types_v2_1 import (
        SceneConfig, AvatarConfig, VoiceConfig, 
        EnhancedNarrationConfig, SceneValidator,
        ValidationResult, setup_logging
    )
except ImportError as e:
    print(f"❌ Error importing Q-AVIOGEN types: {e}")
    sys.exit(1)

import logging

# Setup logging
logger = setup_logging()


class AvatarVoiceValidator:
    """Validator for avatar and voice configurations"""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config_data = None
        self.validation_results = []
        
    def load_config(self) -> bool:
        """Load and parse the YAML configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
            logger.info(f"✅ Configuration loaded: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
            return False
    
    def validate_avatar_config(self) -> Tuple[bool, List[str]]:
        """Validate avatar configuration section"""
        errors = []
        
        if 'avatar' not in self.config_data:
            errors.append("Missing 'avatar' section in configuration")
            return False, errors
            
        avatar_config = self.config_data['avatar']
        
        # Required fields
        required_fields = ['name', 'model_path', 'position', 'animations']
        for field in required_fields:
            if field not in avatar_config:
                errors.append(f"Missing required avatar field: {field}")
        
        # Validate model path
        if 'model_path' in avatar_config:
            model_path = Path(self.config_path.parent.parent) / avatar_config['model_path']
            if not model_path.exists():
                errors.append(f"Avatar model file not found: {model_path}")
            else:
                logger.info(f"✅ Avatar model path validated: {model_path}")
        
        # Validate texture path
        if 'texture_path' in avatar_config:
            texture_path = Path(self.config_path.parent.parent) / avatar_config['texture_path']
            if not texture_path.exists():
                errors.append(f"Avatar texture file not found: {texture_path}")
            else:
                logger.info(f"✅ Avatar texture path validated: {texture_path}")
        
        # Validate animations
        if 'animations' in avatar_config:
            animations = avatar_config['animations']
            if not isinstance(animations, list):
                errors.append("Avatar animations must be a list")
            else:
                total_duration = 0
                for i, anim in enumerate(animations):
                    if 'name' not in anim:
                        errors.append(f"Animation {i} missing 'name' field")
                    if 'start_time' not in anim:
                        errors.append(f"Animation {i} missing 'start_time' field")
                    if 'duration' not in anim:
                        errors.append(f"Animation {i} missing 'duration' field")
                    if 'action' not in anim:
                        errors.append(f"Animation {i} missing 'action' field")
                    
                    if 'duration' in anim:
                        total_duration += anim['duration']
                
                logger.info(f"✅ Avatar animations total duration: {total_duration}s")
        
        return len(errors) == 0, errors
    
    def validate_voice_config(self) -> Tuple[bool, List[str]]:
        """Validate voice configuration section"""
        errors = []
        
        if 'voice_config' not in self.config_data:
            errors.append("Missing 'voice_config' section in configuration")
            return False, errors
            
        voice_config = self.config_data['voice_config']
        
        # Required fields
        required_fields = ['provider', 'voice_name', 'language']
        for field in required_fields:
            if field not in voice_config:
                errors.append(f"Missing required voice field: {field}")
        
        # Validate audio file if specified
        if 'audio_file' in voice_config:
            audio_path = Path(self.config_path.parent.parent) / voice_config['audio_file']
            if not audio_path.exists():
                errors.append(f"Voice audio file not found: {audio_path}")
            else:
                logger.info(f"✅ Voice audio file validated: {audio_path}")
        
        # Validate provider
        valid_providers = ['azure_cognitive_services', 'elevenlabs', 'local_tts', 'google_tts']
        if 'provider' in voice_config:
            if voice_config['provider'] not in valid_providers:
                errors.append(f"Invalid voice provider: {voice_config['provider']}")
        
        # Validate language code
        valid_languages = ['es-ES', 'en-US', 'en-GB', 'fr-FR', 'de-DE', 'it-IT']
        if 'language' in voice_config:
            if voice_config['language'] not in valid_languages:
                errors.append(f"Unsupported language code: {voice_config['language']}")
        
        return len(errors) == 0, errors
    
    def validate_narration_config(self) -> Tuple[bool, List[str]]:
        """Validate narration configuration section"""
        errors = []
        
        if 'narration' not in self.config_data:
            errors.append("Missing 'narration' section in configuration")
            return False, errors
            
        narration_config = self.config_data['narration']
        
        # Validate segments
        if 'segments' not in narration_config:
            errors.append("Missing 'segments' in narration configuration")
            return False, errors
        
        segments = narration_config['segments']
        total_duration = 0
        
        for i, segment in enumerate(segments):
            # Required fields for each segment
            required_fields = ['text', 'start_time', 'duration', 'emotion']
            for field in required_fields:
                if field not in segment:
                    errors.append(f"Segment {i} missing '{field}' field")
            
            # Validate timing
            if 'start_time' in segment and 'duration' in segment:
                if segment['start_time'] < 0:
                    errors.append(f"Segment {i} has negative start_time")
                if segment['duration'] <= 0:
                    errors.append(f"Segment {i} has invalid duration")
                
                end_time = segment['start_time'] + segment['duration']
                total_duration = max(total_duration, end_time)
            
            # Validate emotion
            valid_emotions = ['explaining', 'focused', 'warning', 'serious', 'neutral', 'friendly']
            if 'emotion' in segment:
                if segment['emotion'] not in valid_emotions:
                    errors.append(f"Segment {i} has invalid emotion: {segment['emotion']}")
            
            # Validate text content
            if 'text' in segment:
                if len(segment['text'].strip()) == 0:
                    errors.append(f"Segment {i} has empty text content")
        
        logger.info(f"✅ Narration total duration: {total_duration}s")
        
        # Check if total duration matches scene duration
        if 'scene_config' in self.config_data:
            scene_duration = self.config_data['scene_config'].get('duration', 0)
            if abs(total_duration - scene_duration) > 1.0:  # Allow 1 second tolerance
                errors.append(f"Narration duration ({total_duration}s) doesn't match scene duration ({scene_duration}s)")
        
        return len(errors) == 0, errors
    
    def validate_synchronization(self) -> Tuple[bool, List[str]]:
        """Validate avatar animation and narration synchronization"""
        errors = []
        
        avatar_animations = self.config_data.get('avatar', {}).get('animations', [])
        narration_segments = self.config_data.get('narration', {}).get('segments', [])
        
        if len(avatar_animations) != len(narration_segments):
            errors.append(f"Animation count ({len(avatar_animations)}) doesn't match narration segments ({len(narration_segments)})")
            return False, errors
        
        # Check timing synchronization
        for i, (anim, narr) in enumerate(zip(avatar_animations, narration_segments)):
            anim_start = anim.get('start_time', 0)
            narr_start = narr.get('start_time', 0)
            
            if abs(anim_start - narr_start) > 0.5:  # Allow 0.5 second tolerance
                errors.append(f"Step {i+1}: Animation and narration start times don't sync ({anim_start}s vs {narr_start}s)")
            
            anim_duration = anim.get('duration', 0)
            narr_duration = narr.get('duration', 0)
            
            if abs(anim_duration - narr_duration) > 1.0:  # Allow 1 second tolerance
                errors.append(f"Step {i+1}: Animation and narration durations don't sync ({anim_duration}s vs {narr_duration}s)")
        
        if len(errors) == 0:
            logger.info("✅ Avatar animations and narration are properly synchronized")
        
        return len(errors) == 0, errors
    
    def validate_timeline_markers(self) -> Tuple[bool, List[str]]:
        """Validate timeline markers alignment"""
        errors = []
        
        if 'timeline_markers' not in self.config_data:
            errors.append("Missing 'timeline_markers' section")
            return False, errors
        
        markers = self.config_data['timeline_markers']
        narration_segments = self.config_data.get('narration', {}).get('segments', [])
        
        # Check if key markers exist
        marker_times = {marker['name']: marker['time'] for marker in markers}
        
        expected_markers = [
            'procedure_start', 'aircraft_position_check', 'area_clearance_check',
            'strut_inspection_start', 'tire_inspection', 'steering_check',
            'q_sensor_verification', 'completion_documentation', 'procedure_complete'
        ]
        
        for expected in expected_markers:
            if expected not in marker_times:
                errors.append(f"Missing expected timeline marker: {expected}")
        
        # Validate marker timing against narration
        for i, segment in enumerate(narration_segments):
            segment_start = segment.get('start_time', 0)
            closest_marker = None
            min_diff = float('inf')
            
            for marker_name, marker_time in marker_times.items():
                diff = abs(marker_time - segment_start)
                if diff < min_diff:
                    min_diff = diff
                    closest_marker = marker_name
            
            if min_diff > 2.0:  # Allow 2 second tolerance
                logger.warning(f"⚠️ Segment {i+1} not well aligned with timeline markers (closest: {closest_marker}, diff: {min_diff}s)")
        
        return len(errors) == 0, errors
    
    def generate_validation_report(self) -> str:
        """Generate a comprehensive validation report"""
        report = []
        report.append("=" * 60)
        report.append("Q-AVIOGEN AVATAR & VOICE VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"Configuration: {self.config_path}")
        report.append(f"Timestamp: {self._get_timestamp()}")
        report.append("")
        
        # Run all validations
        validations = [
            ("Avatar Configuration", self.validate_avatar_config),
            ("Voice Configuration", self.validate_voice_config),
            ("Narration Configuration", self.validate_narration_config),
            ("Synchronization", self.validate_synchronization),
            ("Timeline Markers", self.validate_timeline_markers)
        ]
        
        all_valid = True
        total_errors = 0
        
        for section_name, validation_func in validations:
            report.append(f"## {section_name}")
            report.append("-" * 40)
            
            try:
                is_valid, errors = validation_func()
                if is_valid:
                    report.append("✅ PASSED")
                else:
                    report.append("❌ FAILED")
                    all_valid = False
                    for error in errors:
                        report.append(f"   • {error}")
                        total_errors += 1
            except Exception as e:
                report.append(f"❌ ERROR: {e}")
                all_valid = False
                total_errors += 1
            
            report.append("")
        
        # Summary
        report.append("=" * 60)
        report.append("SUMMARY")
        report.append("=" * 60)
        report.append(f"Overall Status: {'✅ VALID' if all_valid else '❌ INVALID'}")
        report.append(f"Total Errors: {total_errors}")
        
        if all_valid:
            report.append("")
            report.append("🎉 Configuration is ready for avatar-guided procedure rendering!")
            report.append("   You can proceed with video generation.")
        else:
            report.append("")
            report.append("⚠️ Please fix the errors above before proceeding with rendering.")
        
        return "\n".join(report)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Main validation function"""
    if len(sys.argv) != 2:
        print("Usage: python test_avatar_voice_validation.py <config_file.yaml>")
        print("Example: python test_avatar_voice_validation.py configs/instructor_config.yaml")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    print("🚀 Q-AVIOGEN Avatar & Voice Validation")
    print("=" * 50)
    
    # Initialize validator
    validator = AvatarVoiceValidator(config_file)
    
    # Load configuration
    if not validator.load_config():
        print("❌ Failed to load configuration file")
        sys.exit(1)
    
    # Generate and print validation report
    report = validator.generate_validation_report()
    print(report)
    
    # Save report to file
    report_path = Path(config_file).parent / "validation_report.txt"
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Validation report saved to: {report_path}")
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")


if __name__ == "__main__":
    main()
