#!/usr/bin/env python3
"""
Q-AVIOGEN Scene Validator CLI v2.1
==================================

Validador CLI para archivos de configuración de escenas Q-AVIOGEN.
Soporta todas las características v2.1: .blend, timeline markers, HDRI, etc.

Usage:
    python validate_scene.py <scene_file.json>
    python validate_scene.py --suite  # Validar suite de tests
    python validate_scene.py --generate-example  # Generar ejemplo
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

# Importar tipos v2.1
try:
    from core.types_v2_1 import (
        SceneConfig, SceneValidator, create_test_scene_suite,
        get_version_info, setup_logging
    )
except ImportError as e:
    print(f"❌ Error importing Q-AVIOGEN types: {e}")
    sys.exit(1)


def validate_scene_file(filepath: str) -> None:
    """Validar un archivo de escena específico"""
    print(f"🔍 Validating scene file: {filepath}")
    print("=" * 60)
    
    try:
        # Validar archivo
        is_valid, errors, warnings = SceneValidator.validate_scene_file(filepath)
        
        # Cargar escena para más detalles
        scene = SceneConfig.load_from_file(filepath)
        
        print(f"Scene: {scene.name}")
        print(f"ID: {scene.scene_id}")
        print(f"Status: {'✅ VALID' if is_valid else '❌ INVALID'}")
        print(f"Objects: {len(scene.objects)}")
        print(f"Lights: {len(scene.lights)}")
        print(f"Animations: {len(scene.animations)}")
        print(f"Timeline Markers: {len(scene.timeline_markers)}")
        print(f"Layers: {len(scene.layers)}")
        
        # Mostrar configuración de render
        print(f"\nRender Configuration:")
        print(f"  Resolution: {scene.render_config.resolution_x}x{scene.render_config.resolution_y}")
        print(f"  Codec: {scene.render_config.codec.value}")
        print(f"  Samples: {scene.render_config.samples}")
        print(f"  Duration: {scene.render_config.get_duration_seconds():.2f}s")
        
        # Mostrar entorno
        print(f"\nEnvironment:")
        print(f"  Type: {scene.environment.type.value}")
        print(f"  HDRI: {scene.environment.hdri_path or 'None'}")
        
        # Mostrar errores
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
        
        # Mostrar advertencias
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")
        
        if is_valid:
            print(f"\n✅ Scene validation PASSED")
        else:
            print(f"\n❌ Scene validation FAILED")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error validating scene: {e}")
        sys.exit(1)


def validate_test_suite() -> None:
    """Validar suite completa de tests"""
    print("🧪 Validating Q-AVIOGEN Test Suite v2.1")
    print("=" * 60)
    
    try:
        test_scenes = create_test_scene_suite()
        total_scenes = len(test_scenes)
        valid_scenes = 0
        
        for i, scene in enumerate(test_scenes, 1):
            print(f"\n[{i}/{total_scenes}] Testing: {scene.name}")
            
            is_valid, errors, warnings = SceneValidator.validate_scene(scene)
            
            if is_valid:
                print(f"  ✅ VALID - Objects: {len(scene.objects)}, "
                      f"Lights: {len(scene.lights)}, "
                      f"Markers: {len(scene.timeline_markers)}")
                valid_scenes += 1
            else:
                print(f"  ❌ INVALID - Errors: {len(errors)}")
                for error in errors[:2]:  # Mostrar solo primeros 2 errores
                    print(f"    - {error}")
            
            if warnings:
                print(f"  ⚠️  Warnings: {len(warnings)}")
        
        print(f"\n" + "=" * 60)
        print(f"SUITE RESULTS: {valid_scenes}/{total_scenes} scenes valid")
        
        if valid_scenes == total_scenes:
            print("✅ ALL TESTS PASSED")
        else:
            print("❌ SOME TESTS FAILED")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error running test suite: {e}")
        sys.exit(1)


def generate_example_scene() -> None:
    """Generar escena de ejemplo completa"""
    print("📋 Generating Q-AVIOGEN Example Scene v2.1")
    print("=" * 60)
    
    try:
        # Crear escena industrial completa
        scene = SceneConfig.test()
        scene.name = "Q-AVIOGEN_Industrial_Demo_v2.1"
        scene.description = "Escena industrial completa demostrando todas las características v2.1"
        
        # Configurar metadata aerospace
        scene.metadata.procedure_id = "IND-DEMO-001"
        scene.metadata.aircraft_type = "Boeing 737-800"
        scene.metadata.ata_chapter = "32-41-00"
        scene.metadata.compliance_level = "certified"
        scene.metadata.approved_by = "Q-AVIOGEN Certification Authority"
        
        # Configurar render profesional
        scene.render_config.resolution_x = 2560
        scene.render_config.resolution_y = 1440
        scene.render_config.samples = 256
        scene.render_config.codec = scene.render_config.codec.__class__.PRORES
        scene.render_config.quality = "HIGH"
        
        # Postprocesamiento avanzado
        scene.render_config.post_processing.bloom = True
        scene.render_config.post_processing.bloom_intensity = 0.8
        scene.render_config.post_processing.depth_of_field = True
        scene.render_config.post_processing.dof_aperture = 1.4
        scene.render_config.post_processing.motion_blur = True
        scene.render_config.post_processing.film_grain = True
        scene.render_config.post_processing.grain_intensity = 0.3
        
        # Entorno HDRI industrial
        scene.environment.hdri_path = "assets/hdri/industrial_hangar_4k.hdr"
        scene.environment.hdri_strength = 2.0
        scene.environment.hdri_rotation = 135.0
        
        # Marcadores de procedimiento
        scene.timeline_markers.clear()
        scene.add_marker("Safety Check", 1, (0.0, 1.0, 0.0, 1.0))
        scene.add_marker("Tool Preparation", 75, (0.0, 0.5, 1.0, 1.0))
        scene.add_marker("Inspection Start", 150, (1.0, 1.0, 0.0, 1.0))
        scene.add_marker("Critical Procedure", 225, (1.0, 0.5, 0.0, 1.0))
        scene.add_marker("Documentation", 300, (0.5, 0.0, 1.0, 1.0))
        scene.add_marker("Completion", 375, (1.0, 0.0, 0.0, 1.0))
        
        # Guardar ejemplo
        output_path = "examples/industrial_demo_scene_v2_1.json"
        Path("examples").mkdir(exist_ok=True)
        
        scene.save_to_file(output_path)
        
        print(f"✅ Example scene generated: {output_path}")
        print(f"📊 Configuration:")
        print(f"  - Objects: {len(scene.objects)}")
        print(f"  - Lights: {len(scene.lights)}")
        print(f"  - Timeline Markers: {len(scene.timeline_markers)}")
        print(f"  - Layers: {len(scene.layers)}")
        print(f"  - Resolution: {scene.render_config.resolution_x}x{scene.render_config.resolution_y}")
        print(f"  - Codec: {scene.render_config.codec.value}")
        print(f"  - Duration: {scene.render_config.get_duration_seconds():.1f}s")
        
        # Validar ejemplo generado
        is_valid, errors, warnings = SceneValidator.validate_scene(scene)
        print(f"  - Validation: {'✅ VALID' if is_valid else '❌ INVALID'}")
        
        if errors:
            print(f"  - Errors: {len(errors)}")
        if warnings:
            print(f"  - Warnings: {len(warnings)}")
            
    except Exception as e:
        print(f"❌ Error generating example: {e}")
        sys.exit(1)


def show_version_info() -> None:
    """Mostrar información de versión"""
    version_info = get_version_info()
    
    print("Q-AVIOGEN Scene Validator v2.1")
    print("=" * 40)
    print(f"Version: {version_info['version']}")
    print(f"Schema Version: {version_info['schema_version']}")
    print(f"Release Date: {version_info['release_date']}")
    print(f"Compatibility: {', '.join(version_info['compatibility'])}")
    
    print(f"\nFeatures v2.1 ({len(version_info['features'])}):")
    for feature, description in version_info['features'].items():
        print(f"  ✅ {feature}: {description}")


def main():
    """Función principal CLI"""
    parser = argparse.ArgumentParser(
        description="Q-AVIOGEN Scene Validator v2.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_scene.py scene.json              # Validate single scene
  python validate_scene.py --suite                 # Run test suite
  python validate_scene.py --generate-example      # Generate example scene
  python validate_scene.py --version               # Show version info
        """
    )
    
    parser.add_argument(
        'scene_file', 
        nargs='?', 
        help='Path to scene JSON file to validate'
    )
    
    parser.add_argument(
        '--suite', 
        action='store_true', 
        help='Run complete test suite validation'
    )
    
    parser.add_argument(
        '--generate-example', 
        action='store_true', 
        help='Generate example scene configuration'
    )
    
    parser.add_argument(
        '--version', 
        action='store_true', 
        help='Show version information'
    )
    
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true', 
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.verbose:
        setup_logging("DEBUG")
    else:
        setup_logging("INFO")
    
    # Ejecutar acción solicitada
    try:
        if args.version:
            show_version_info()
        elif args.suite:
            validate_test_suite()
        elif args.generate_example:
            generate_example_scene()
        elif args.scene_file:
            if not Path(args.scene_file).exists():
                print(f"❌ Scene file not found: {args.scene_file}")
                sys.exit(1)
            validate_scene_file(args.scene_file)
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
