#!/usr/bin/env python3
"""
Q-AVIOGEN CLI Renderer - Command line tool for standalone rendering
Herramienta CLI para renderizado independiente compatible con CI/CD
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import jsonschema

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.types import SceneConfig, RenderSettings, RenderQuality, scene_config_from_dict
    from core.errors import setup_logging, QAvioGenError, ErrorCode
    from blender.enhanced_renderer import EnhancedBlenderRenderer
    CORE_AVAILABLE = True
except ImportError:
    print("⚠️ Core modules not available, using basic functionality")
    CORE_AVAILABLE = False

def load_json_schema(schema_path: str) -> Dict[str, Any]:
    """Load JSON schema for validation"""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading schema: {e}")
        return {}

def validate_scene_config(config: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """Validate scene configuration against schema"""
    errors = []
    
    if not schema:
        return ["Schema not available for validation"]
    
    try:
        jsonschema.validate(config, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation error: {e.message}")
    except Exception as e:
        errors.append(f"Validation error: {str(e)}")
    
    return errors

def load_scene_configs(input_path: str, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Load and validate scene configurations from file"""
    
    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single scene and multiple scenes
    if isinstance(data, dict):
        if 'scenes' in data:
            scenes = data['scenes']
        else:
            scenes = [data]
    elif isinstance(data, list):
        scenes = data
    else:
        raise ValueError("Invalid input format: expected dict or list")
    
    # Validate each scene
    validated_scenes = []
    for i, scene in enumerate(scenes):
        validation_errors = validate_scene_config(scene, schema)
        if validation_errors:
            print(f"⚠️ Scene {i+1} validation errors:")
            for error in validation_errors:
                print(f"   - {error}")
        else:
            validated_scenes.append(scene)
    
    if not validated_scenes:
        raise ValueError("No valid scenes found in input file")
    
    return validated_scenes

def create_render_settings(args) -> Any:
    """Create render settings from command line arguments"""
    
    if not CORE_AVAILABLE:
        return None
    
    # Map quality string to enum
    quality_map = {
        'preview': RenderQuality.PREVIEW,
        'standard': RenderQuality.STANDARD,
        'high': RenderQuality.HIGH,
        'production': RenderQuality.PRODUCTION
    }
    
    quality = quality_map.get(args.quality, RenderQuality.STANDARD)
    
    # Parse resolution
    if 'x' in args.resolution:
        width, height = map(int, args.resolution.split('x'))
        resolution = (width, height)
    else:
        resolution_map = {
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160)
        }
        resolution = resolution_map.get(args.resolution, (1920, 1080))
    
    return RenderSettings(
        quality=quality,
        resolution=resolution,
        fps=args.fps,
        samples=args.samples,
        use_gpu=args.gpu,
        output_format=args.format,
        codec=args.codec,
        bitrate=args.bitrate
    )

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description="Q-AVIOGEN CLI Renderer - Standalone 3D video rendering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic render
  python cli_render.py --input scenes.json --output output/

  # High quality render with custom settings
  python cli_render.py --input config.json --output videos/ --quality high --resolution 4k --fps 60

  # Preview render (fast)
  python cli_render.py --input scenes.json --output preview/ --quality preview --gpu

  # CI/CD compatible
  blender --background --python cli_render.py -- --input config.json --output build/videos/ --quiet

Schema validation:
  The tool validates input against schemas/scene_config.schema.json
  
Exit codes:
  0: Success
  1: Input/output errors
  2: Validation errors  
  3: Render errors
        """
    )
    
    # Input/Output
    parser.add_argument('--input', '-i', required=True,
                       help='Input JSON file with scene configurations')
    parser.add_argument('--output', '-o', required=True,
                       help='Output directory for rendered videos')
    parser.add_argument('--filename', '-f',
                       help='Output filename (auto-generated if not specified)')
    
    # Render Quality
    parser.add_argument('--quality', '-q', 
                       choices=['preview', 'standard', 'high', 'production'],
                       default='standard',
                       help='Render quality preset (default: standard)')
    parser.add_argument('--resolution', '-r',
                       default='1080p',
                       help='Resolution: 720p, 1080p, 4k, or WIDTHxHEIGHT (default: 1080p)')
    parser.add_argument('--fps',
                       type=int, default=30,
                       help='Frames per second (default: 30)')
    parser.add_argument('--samples',
                       type=int,
                       help='Render samples (overrides quality preset)')
    
    # Hardware
    parser.add_argument('--gpu', action='store_true',
                       help='Enable GPU rendering (default: auto-detect)')
    parser.add_argument('--no-gpu', action='store_true',
                       help='Force CPU rendering')
    
    # Output format
    parser.add_argument('--format',
                       choices=['mp4', 'webm', 'mov', 'avi'],
                       default='mp4',
                       help='Output video format (default: mp4)')
    parser.add_argument('--codec',
                       default='h264',
                       help='Video codec (default: h264)')
    parser.add_argument('--bitrate',
                       default='10M',
                       help='Video bitrate (default: 10M)')
    
    # Validation and logging
    parser.add_argument('--schema',
                       default='schemas/scene_config.schema.json',
                       help='JSON schema file for validation')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate input, do not render')
    parser.add_argument('--log-level',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO',
                       help='Logging level (default: INFO)')
    parser.add_argument('--log-file',
                       help='Log file path (default: console only)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Minimal output (for CI/CD)')
    
    # Preview mode
    parser.add_argument('--preview', action='store_true',
                       help='Enable preview mode (faster, lower quality)')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = 'ERROR' if args.quiet else args.log_level
    logger = None
    
    if CORE_AVAILABLE:
        logger = setup_logging(
            log_level=log_level,
            log_file=args.log_file,
            enable_console=not args.quiet,
            enable_json=bool(args.log_file)
        )
    
    try:
        # Load and validate schema
        if not args.quiet:
            print("📋 Loading configuration schema...")
        
        schema_path = Path(args.schema)
        if schema_path.exists():
            schema = load_json_schema(str(schema_path))
        else:
            if not args.quiet:
                print(f"⚠️ Schema file not found: {schema_path}")
            schema = {}
        
        # Load scene configurations
        if not args.quiet:
            print(f"📖 Loading scene configurations from: {args.input}")
        
        scene_configs = load_scene_configs(args.input, schema)
        
        if not args.quiet:
            print(f"✅ Loaded {len(scene_configs)} valid scene(s)")
        
        # Validation-only mode
        if args.validate_only:
            if not args.quiet:
                print("✅ Validation completed successfully")
            return 0
        
        # Create render settings
        render_settings = create_render_settings(args)
        
        # Override GPU setting if specified
        if args.no_gpu and render_settings:
            render_settings.use_gpu = False
        elif args.gpu and render_settings:
            render_settings.use_gpu = True
        
        # Initialize renderer
        if not args.quiet:
            print("🎬 Initializing Blender renderer...")
        
        if CORE_AVAILABLE:
            renderer = EnhancedBlenderRenderer(
                render_settings=render_settings,
                logger=logger,
                preview_mode=args.preview
            )
        else:
            # Fallback to basic implementation
            print("❌ Enhanced renderer not available, basic functionality only")
            return 3
        
        # Convert configs to SceneConfig objects if possible
        scenes = []
        if CORE_AVAILABLE:
            for config in scene_configs:
                try:
                    scene = scene_config_from_dict(config)
                    scenes.append(scene)
                except Exception as e:
                    if logger:
                        logger.log_error(QAvioGenError(
                            f"Failed to create scene from config: {str(e)}",
                            ErrorCode.INVALID_SCENE_CONFIG
                        ))
                    else:
                        print(f"❌ Error creating scene: {e}")
                    return 2
        else:
            scenes = scene_configs
        
        # Render video
        if not args.quiet:
            print("🎥 Starting video render...")
        
        try:
            metadata = renderer.render_video(
                scenes=scenes,
                output_dir=args.output,
                filename=args.filename
            )
            
            if not args.quiet:
                print(f"✅ Render completed successfully!")
                if hasattr(metadata, 'output_file'):
                    print(f"📁 Output: {metadata.output_file}")
                elif isinstance(metadata, dict):
                    print(f"📁 Output: {metadata.get('output_file', 'Unknown')}")
            
            return 0
            
        except Exception as e:
            if logger:
                logger.log_error(QAvioGenError(
                    f"Render failed: {str(e)}",
                    ErrorCode.RENDER_FAILED
                ))
            else:
                print(f"❌ Render failed: {e}")
            return 3
    
    except FileNotFoundError as e:
        if logger:
            logger.log_error(QAvioGenError(
                str(e),
                ErrorCode.ASSET_NOT_FOUND
            ))
        else:
            print(f"❌ File not found: {e}")
        return 1
    
    except ValueError as e:
        if logger:
            logger.log_error(QAvioGenError(
                str(e),
                ErrorCode.INVALID_SCENE_CONFIG
            ))
        else:
            print(f"❌ Validation error: {e}")
        return 2
    
    except Exception as e:
        if logger:
            logger.log_error(QAvioGenError(
                f"Unexpected error: {str(e)}",
                ErrorCode.RENDER_FAILED
            ))
        else:
            print(f"❌ Unexpected error: {e}")
        return 3

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
