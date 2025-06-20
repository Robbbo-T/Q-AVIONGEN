#!/usr/bin/env python3
"""
Scene Configuration Generator for Q-AVIOGEN
Generador de configuraciones de escena para Q-AVIOGEN
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

def create_towbar_attachment_procedure() -> Dict[str, Any]:
    """Create a complete towbar attachment procedure configuration"""
    
    procedure = {
        "metadata": {
            "title": "Towbar Attachment Procedure",
            "procedure_id": "00-30-10-01",
            "aircraft_type": "BWB Q-100", 
            "created_by": "Q-AVIOGEN Generator",
            "version": "1.0"
        },
        "render_settings": {
            "quality": "high",
            "resolution": [1920, 1080],
            "fps": 30,
            "use_gpu": True
        },
        "scenes": [
            {
                "name": "step_01_positioning",
                "duration_seconds": 8.0,
                "camera": {
                    "position": [0, -6, 4],
                    "target": [0, 0, 0],
                    "fov": 50,
                    "type": "overview"
                },
                "lights": [
                    {
                        "name": "KeyLight", 
                        "type": "SUN",
                        "position": [5, 5, 10],
                        "energy": 5.0,
                        "color": [1.0, 1.0, 1.0]
                    },
                    {
                        "name": "FillLight",
                        "type": "AREA", 
                        "position": [-3, 2, 4],
                        "energy": 2.0,
                        "color": [0.9, 0.9, 1.0]
                    }
                ],
                "objects": [
                    {
                        "name": "BWB_Aircraft",
                        "file_path": "assets/models/bwb_q100.glb",
                        "position": [0, 0, 0],
                        "rotation": [0, 0, 0],
                        "scale": [1, 1, 1],
                        "visible": True,
                        "material": {
                            "base_color": [0.7, 0.7, 0.8, 1.0],
                            "metallic": 0.1,
                            "roughness": 0.3,
                            "emission_strength": 0.0
                        }
                    },
                    {
                        "name": "Towbar",
                        "file_path": "assets/models/towbar.glb",
                        "position": [0, -5, 0],
                        "rotation": [0, 0, 0],
                        "scale": [1, 1, 1],
                        "visible": True,
                        "material": {
                            "base_color": [0.8, 0.6, 0.2, 1.0],
                            "metallic": 0.7,
                            "roughness": 0.2
                        }
                    },
                    {
                        "name": "Ground_Plane",
                        "position": [0, 0, -0.1],
                        "scale": [20, 20, 0.1],
                        "material": {
                            "base_color": [0.3, 0.3, 0.3, 1.0],
                            "roughness": 0.8
                        }
                    }
                ],
                "animations": [
                    {
                        "type": "move",
                        "target_object": "Towbar",
                        "start_frame": 30,
                        "end_frame": 180,
                        "start_position": [0, -5, 0],
                        "end_position": [0, -2, 0],
                        "easing": "BEZIER"
                    }
                ],
                "overlays": [
                    {
                        "text": "Step 1: Position towbar near aircraft nose gear",
                        "position": [0.5, 0.9],
                        "font_size": 28,
                        "duration": 8.0,
                        "fade_in": 0.5,
                        "fade_out": 0.5
                    }
                ],
                "audio_file": "audio/step_01_positioning.wav",
                "background_color": [0.15, 0.15, 0.2]
            },
            {
                "name": "step_02_alignment",
                "duration_seconds": 6.0,
                "camera": {
                    "position": [2, -3, 2],
                    "target": [0, -1.5, 0],
                    "fov": 60,
                    "type": "close_up"
                },
                "lights": [
                    {
                        "name": "KeyLight",
                        "type": "SUN", 
                        "position": [5, 5, 10],
                        "energy": 5.0,
                        "color": [1.0, 1.0, 1.0]
                    },
                    {
                        "name": "SpotLight",
                        "type": "SPOT",
                        "position": [1, -2, 3],
                        "energy": 8.0,
                        "color": [1.0, 0.9, 0.8]
                    }
                ],
                "objects": [
                    {
                        "name": "BWB_Aircraft",
                        "file_path": "assets/models/bwb_q100.glb",
                        "position": [0, 0, 0],
                        "visible": True,
                        "material": {
                            "base_color": [0.7, 0.7, 0.8, 1.0],
                            "metallic": 0.1,
                            "roughness": 0.3
                        }
                    },
                    {
                        "name": "Towbar",
                        "file_path": "assets/models/towbar.glb", 
                        "position": [0, -2, 0],
                        "visible": True,
                        "material": {
                            "base_color": [0.8, 0.6, 0.2, 1.0],
                            "metallic": 0.7,
                            "roughness": 0.2
                        }
                    },
                    {
                        "name": "Connection_Pin",
                        "position": [0, -1.8, 0.2],
                        "scale": [0.1, 0.1, 0.5],
                        "material": {
                            "base_color": [0.9, 0.9, 0.9, 1.0],
                            "metallic": 0.9,
                            "roughness": 0.1
                        }
                    }
                ],
                "animations": [
                    {
                        "type": "move",
                        "target_object": "Towbar",
                        "start_frame": 1,
                        "end_frame": 120,
                        "start_position": [0, -2, 0],
                        "end_position": [0, -1.5, 0],
                        "easing": "BEZIER"
                    },
                    {
                        "type": "highlight",
                        "target_object": "Connection_Pin",
                        "start_frame": 90,
                        "end_frame": 180,
                        "highlight_color": [1.0, 0.5, 0.0]
                    }
                ],
                "overlays": [
                    {
                        "text": "Step 2: Align towbar with nose gear connection point",
                        "position": [0.5, 0.9],
                        "font_size": 28,
                        "duration": 6.0
                    }
                ],
                "audio_file": "audio/step_02_alignment.wav",
                "background_color": [0.15, 0.15, 0.2]
            },
            {
                "name": "step_03_connection",
                "duration_seconds": 10.0,
                "camera": {
                    "position": [1, -1, 1.5],
                    "target": [0, -1.5, 0.2],
                    "fov": 70,
                    "type": "close_up"
                },
                "lights": [
                    {
                        "name": "KeyLight",
                        "type": "SUN",
                        "position": [3, 3, 8],
                        "energy": 4.0,
                        "color": [1.0, 1.0, 1.0]
                    },
                    {
                        "name": "TaskLight",
                        "type": "AREA",
                        "position": [0.5, -1, 2],
                        "energy": 6.0,
                        "color": [1.0, 1.0, 0.9]
                    }
                ],
                "objects": [
                    {
                        "name": "BWB_Aircraft",
                        "file_path": "assets/models/bwb_q100.glb",
                        "position": [0, 0, 0],
                        "visible": True,
                        "material": {
                            "base_color": [0.7, 0.7, 0.8, 1.0],
                            "metallic": 0.1,
                            "roughness": 0.3
                        }
                    },
                    {
                        "name": "Towbar",
                        "file_path": "assets/models/towbar.glb",
                        "position": [0, -1.5, 0],
                        "visible": True,
                        "material": {
                            "base_color": [0.8, 0.6, 0.2, 1.0],
                            "metallic": 0.7,
                            "roughness": 0.2
                        }
                    },
                    {
                        "name": "Connection_Pin",
                        "position": [0, -1.8, 0.2],
                        "scale": [0.1, 0.1, 0.5],
                        "material": {
                            "base_color": [0.9, 0.9, 0.9, 1.0],
                            "metallic": 0.9,
                            "roughness": 0.1
                        }
                    }
                ],
                "animations": [
                    {
                        "type": "move",
                        "target_object": "Connection_Pin",
                        "start_frame": 60,
                        "end_frame": 180,
                        "start_position": [0, -1.8, 0.2],
                        "end_position": [0, -1.5, 0.2],
                        "easing": "LINEAR"
                    },
                    {
                        "type": "highlight",
                        "target_object": "Connection_Pin",
                        "start_frame": 180,
                        "end_frame": 300,
                        "highlight_color": [0.0, 1.0, 0.0]
                    }
                ],
                "overlays": [
                    {
                        "text": "Step 3: Insert connection pin through designated holes",
                        "position": [0.5, 0.9],
                        "font_size": 28,
                        "duration": 10.0
                    },
                    {
                        "text": "Ensure pin is fully seated and secure",
                        "position": [0.5, 0.1],
                        "font_size": 20,
                        "duration": 5.0,
                        "fade_in": 5.0
                    }
                ],
                "audio_file": "audio/step_03_connection.wav",
                "background_color": [0.15, 0.15, 0.2]
            }
        ]
    }
    
    return procedure

def create_inspection_procedure() -> Dict[str, Any]:
    """Create a visual inspection procedure configuration"""
    
    procedure = {
        "metadata": {
            "title": "Visual Inspection Procedure",
            "procedure_id": "05-10-00-01",
            "aircraft_type": "Generic",
            "created_by": "Q-AVIOGEN Generator",
            "version": "1.0"
        },
        "render_settings": {
            "quality": "standard",
            "resolution": [1920, 1080],
            "fps": 24,
            "use_gpu": True
        },
        "scenes": [
            {
                "name": "overview_inspection",
                "duration_seconds": 12.0,
                "camera": {
                    "position": [0, -8, 6],
                    "target": [0, 0, 0],
                    "fov": 35,
                    "type": "overview"
                },
                "lights": [
                    {
                        "name": "SunLight",
                        "type": "SUN",
                        "position": [10, 10, 20],
                        "energy": 3.0,
                        "color": [1.0, 0.95, 0.9]
                    }
                ],
                "objects": [
                    {
                        "name": "Aircraft",
                        "position": [0, 0, 0],
                        "material": {
                            "base_color": [0.8, 0.8, 0.85, 1.0],
                            "metallic": 0.2,
                            "roughness": 0.4
                        }
                    }
                ],
                "animations": [
                    {
                        "type": "rotate",
                        "target_object": "Aircraft",
                        "start_frame": 1,
                        "end_frame": 288,
                        "start_position": [0, 0, 0],
                        "end_position": [0, 0, 6.28]  # Full rotation
                    }
                ],
                "overlays": [
                    {
                        "text": "Perform 360° visual inspection",
                        "position": [0.5, 0.9],
                        "font_size": 32,
                        "duration": 12.0
                    }
                ],
                "audio_file": "audio/overview_inspection.wav"
            }
        ]
    }
    
    return procedure

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description="Q-AVIOGEN Scene Configuration Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available procedure templates:
  towbar      - Complete towbar attachment procedure (3 scenes)
  inspection  - Visual inspection procedure (1 scene)
  custom      - Interactive custom procedure builder

Examples:
  python generate_config.py --template towbar --output procedures/towbar.json
  python generate_config.py --template inspection --output procedures/inspection.json
  python generate_config.py --custom --output procedures/custom.json
        """
    )
    
    parser.add_argument('--template', '-t',
                       choices=['towbar', 'inspection'],
                       help='Use predefined procedure template')
    
    parser.add_argument('--custom', '-c', action='store_true',
                       help='Create custom procedure interactively')
    
    parser.add_argument('--output', '-o', required=True,
                       help='Output JSON file path')
    
    parser.add_argument('--validate', action='store_true',
                       help='Validate generated configuration against schema')
    
    parser.add_argument('--pretty', action='store_true', default=True,
                       help='Pretty-print JSON output (default: True)')
    
    args = parser.parse_args()
    
    # Generate configuration based on template
    if args.template == 'towbar':
        config = create_towbar_attachment_procedure()
        print("🔧 Generated towbar attachment procedure configuration")
    
    elif args.template == 'inspection':
        config = create_inspection_procedure()
        print("🔍 Generated visual inspection procedure configuration")
    
    elif args.custom:
        config = create_custom_procedure_interactive()
        print("✨ Generated custom procedure configuration")
    
    else:
        print("❌ Please specify --template or --custom")
        return 1
    
    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write configuration file
    with open(output_path, 'w', encoding='utf-8') as f:
        if args.pretty:
            json.dump(config, f, indent=2, ensure_ascii=False)
        else:
            json.dump(config, f, ensure_ascii=False)
    
    print(f"✅ Configuration saved to: {output_path}")
    
    # Validate if requested
    if args.validate:
        try:
            # Basic validation
            scenes = config.get('scenes', [])
            if not scenes:
                print("⚠️ Warning: No scenes found in configuration")
            else:
                print(f"📋 Configuration contains {len(scenes)} scene(s)")
                
                for i, scene in enumerate(scenes):
                    scene_name = scene.get('name', f'scene_{i+1}')
                    duration = scene.get('duration_seconds', 0)
                    objects_count = len(scene.get('objects', []))
                    
                    print(f"   Scene {i+1}: {scene_name} ({duration}s, {objects_count} objects)")
            
            print("✅ Basic validation passed")
            
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return 1
    
    # Show usage instructions
    print(f"\n📖 Usage instructions:")
    print(f"   CLI render: python cli_render.py --input {output_path} --output videos/")
    print(f"   Python API: scene_configs = load_scene_configs('{output_path}')")
    
    return 0

def create_custom_procedure_interactive() -> Dict[str, Any]:
    """Create custom procedure through interactive prompts"""
    
    print("\n🎬 Creating custom procedure configuration...")
    
    # Get basic metadata
    title = input("Procedure title: ") or "Custom Procedure"
    procedure_id = input("Procedure ID: ") or "CUSTOM-001"
    aircraft_type = input("Aircraft type: ") or "Generic"
    
    # Get render settings
    quality = input("Render quality (preview/standard/high/production) [standard]: ") or "standard"
    resolution = input("Resolution (720p/1080p/4k) [1080p]: ") or "1080p"
    fps = int(input("Frame rate [30]: ") or "30")
    
    # Scene configuration
    scene_count = int(input("Number of scenes [1]: ") or "1")
    
    scenes = []
    for i in range(scene_count):
        print(f"\n--- Scene {i+1} ---")
        scene_name = input(f"Scene name: ") or f"scene_{i+1}"
        duration = float(input(f"Duration (seconds) [5.0]: ") or "5.0")
        
        # Basic scene structure
        scene = {
            "name": scene_name,
            "duration_seconds": duration,
            "camera": {
                "position": [0, -5, 3],
                "target": [0, 0, 0],
                "fov": 45,
                "type": "default"
            },
            "lights": [
                {
                    "name": "KeyLight",
                    "type": "SUN",
                    "position": [5, 5, 10],
                    "energy": 5.0,
                    "color": [1.0, 1.0, 1.0]
                }
            ],
            "objects": [],
            "animations": [],
            "overlays": [],
            "background_color": [0.2, 0.2, 0.2]
        }
        
        # Add basic object
        add_objects = input("Add objects? (y/n) [y]: ").lower() != 'n'
        if add_objects:
            obj_name = input("Object name [TestObject]: ") or "TestObject"
            scene["objects"].append({
                "name": obj_name,
                "position": [0, 0, 0],
                "visible": True
            })
        
        # Add overlay
        add_overlay = input("Add text overlay? (y/n) [y]: ").lower() != 'n'
        if add_overlay:
            overlay_text = input("Overlay text: ") or f"Scene {i+1}: {scene_name}"
            scene["overlays"].append({
                "text": overlay_text,
                "position": [0.5, 0.9],
                "font_size": 28,
                "duration": duration
            })
        
        scenes.append(scene)
    
    # Resolution mapping
    resolution_map = {
        "720p": [1280, 720],
        "1080p": [1920, 1080],
        "4k": [3840, 2160]
    }
    
    config = {
        "metadata": {
            "title": title,
            "procedure_id": procedure_id,
            "aircraft_type": aircraft_type,
            "created_by": "Q-AVIOGEN Interactive Generator",
            "version": "1.0"
        },
        "render_settings": {
            "quality": quality,
            "resolution": resolution_map.get(resolution, [1920, 1080]),
            "fps": fps,
            "use_gpu": True
        },
        "scenes": scenes
    }
    
    return config

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
