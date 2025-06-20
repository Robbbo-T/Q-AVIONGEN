#!/usr/bin/env python3
"""
Q-AVIOGEN Scene Validator CLI v2.1
===================================

Validador de línea de comandos para configuraciones de escena Q-AVIOGEN.
Soporta todas las características v2.1: avatar personalizado, voz grabada,
timeline markers, capas, postproceso y validación aerospace-grade.

Uso:
    python validate_scene.py scene.json
    python validate_scene.py --schema schema.json scene.json
    python validate_scene.py --report scene.json
    python validate_scene.py --fix scene.json

Author: Q-AVIOGEN Team
Date: 2025-06-20
Version: 2.1.0
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.types_v2_1 import (
        SceneConfig, 
        SceneValidator,
        export_schema_info,
        __version__,
        QAVIOGEN_SCHEMA_VERSION,
        FEATURES_V2_1
    )
except ImportError as e:
    logger.error(f"Error importing Q-AVIOGEN modules: {e}")
    logger.error("Make sure you're running this from the Q-AVIOGEN root directory")
    sys.exit(1)


class SceneCLIValidator:
    """Validador CLI para escenas Q-AVIOGEN"""
    
    def __init__(self):
        self.version = __version__
        self.schema_version = QAVIOGEN_SCHEMA_VERSION
    
    def validate_file(self, file_path: str, detailed: bool = False) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Validar archivo de escena
        
        Args:
            file_path: Ruta al archivo JSON de escena
            detailed: Si generar información detallada
            
        Returns:
            Tuple de (is_valid, errors, stats)
        """
        try:
            # Verificar que el archivo existe
            if not Path(file_path).exists():
                return False, [f"File not found: {file_path}"], {}
            
            # Cargar y validar
            scene = SceneConfig.load_from_file(file_path)
            is_valid, errors = SceneValidator.validate_scene(scene)
            
            # Generar estadísticas
            stats = self._generate_stats(scene) if detailed else {}
            
            return is_valid, errors, stats
            
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"], {}
        except Exception as e:
            return False, [f"Validation error: {e}"], {}
    
    def _generate_stats(self, scene: SceneConfig) -> Dict[str, Any]:
        """Generar estadísticas de la escena"""
        return {
            "name": scene.name,
            "version": scene.version,
            "objects_count": len(scene.objects),
            "animations_count": len(scene.animations),
            "timeline_markers_count": len(scene.timeline_markers),
            "layers_count": len(scene.layers),
            "narration_segments_count": len(scene.narration.segments),
            "features": {
                "avatar_enabled": scene.narration.avatar_config.enabled,
                "custom_voice": scene.narration.voice_config.use_custom_voice,
                "camera_animated": scene.camera.animated,
                "hdri_environment": scene.environment.type.value == "hdri",
                "postprocessing_bloom": scene.render_settings.post_processing.bloom,
                "postprocessing_dof": scene.render_settings.post_processing.depth_of_field,
                "has_timeline_markers": len(scene.timeline_markers) > 0,
                "has_layers": len(scene.layers) > 0,
                "certification_level": scene.metadata.certification_level,
                "compliance_standards": scene.metadata.compliance_standards
            },
            "render_settings": {
                "resolution": f"{scene.render_settings.resolution_x}x{scene.render_settings.resolution_y}",
                "fps": scene.render_settings.fps,
                "samples": scene.render_settings.samples,
                "codec": scene.render_settings.codec.value,
                "output_format": scene.render_settings.output_format
            }
        }
    
    def generate_report(self, file_path: str) -> str:
        """Generar reporte detallado de validación"""
        try:
            scene = SceneConfig.load_from_file(file_path)
            return SceneValidator.generate_validation_report(scene)
        except Exception as e:
            return f"Error generating report: {e}"
    
    def fix_common_issues(self, file_path: str, output_path: str = None) -> Tuple[bool, List[str]]:
        """
        Intentar corregir problemas comunes en la configuración
        
        Args:
            file_path: Archivo de entrada
            output_path: Archivo de salida (None = sobrescribir)
            
        Returns:
            Tuple de (success, fixes_applied)
        """
        try:
            scene = SceneConfig.load_from_file(file_path)
            fixes_applied = []
            
            # Fix 1: Asegurar nombre de escena
            if not scene.name or not scene.name.strip():
                scene.name = Path(file_path).stem
                fixes_applied.append("Set scene name from filename")
            
            # Fix 2: Asegurar versión
            if not scene.version or scene.version != "2.1.0":
                scene.version = "2.1.0"
                fixes_applied.append("Updated version to 2.1.0")
            
            # Fix 3: Validar y corregir rangos de postproceso
            pp = scene.render_settings.post_processing
            if pp.gamma <= 0:
                pp.gamma = 1.0
                fixes_applied.append("Fixed gamma value")
            
            if not 0 <= pp.vignette_intensity <= 1:
                pp.vignette_intensity = max(0, min(1, pp.vignette_intensity))
                fixes_applied.append("Fixed vignette intensity range")
            
            # Fix 4: Corregir configuración de avatar si está habilitado pero mal configurado
            if scene.narration.avatar_config.enabled:
                if not 0.1 <= scene.narration.avatar_config.scale <= 10.0:
                    scene.narration.avatar_config.scale = 1.0
                    fixes_applied.append("Fixed avatar scale")
                
                if not 0.0 <= scene.narration.avatar_config.transparency <= 1.0:
                    scene.narration.avatar_config.transparency = 0.9
                    fixes_applied.append("Fixed avatar transparency")
            
            # Fix 5: Asegurar que los frames de renderizado sean válidos
            if scene.render_settings.frame_start > scene.render_settings.frame_end:
                scene.render_settings.frame_end = scene.render_settings.frame_start + 249
                fixes_applied.append("Fixed frame range")
            
            # Fix 6: Corregir resolución si es inválida
            if scene.render_settings.resolution_x <= 0:
                scene.render_settings.resolution_x = 1920
                fixes_applied.append("Fixed resolution X")
            
            if scene.render_settings.resolution_y <= 0:
                scene.render_settings.resolution_y = 1080
                fixes_applied.append("Fixed resolution Y")
            
            # Guardar archivo corregido
            output_file = output_path or file_path
            scene.save_to_file(output_file)
            
            return True, fixes_applied
            
        except Exception as e:
            return False, [f"Error fixing file: {e}"]
    
    def validate_against_schema(self, file_path: str, schema_path: str) -> Tuple[bool, List[str]]:
        """
        Validar archivo contra esquema JSON
        
        Args:
            file_path: Archivo de escena
            schema_path: Archivo de esquema JSON
            
        Returns:
            Tuple de (is_valid, errors)
        """
        try:
            import jsonschema
            
            # Cargar esquema
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Cargar datos de escena
            with open(file_path, 'r', encoding='utf-8') as f:
                scene_data = json.load(f)
            
            # Validar
            validator = jsonschema.Draft7Validator(schema)
            errors = list(validator.iter_errors(scene_data))
            
            if errors:
                error_messages = [f"{error.json_path}: {error.message}" for error in errors]
                return False, error_messages
            else:
                return True, []
                
        except ImportError:
            return False, ["jsonschema package not installed. Install with: pip install jsonschema"]
        except Exception as e:
            return False, [f"Schema validation error: {e}"]


def print_banner():
    """Imprimir banner del validador"""
    print("=" * 60)
    print("🚀 Q-AVIOGEN Scene Validator CLI v2.1")
    print("=" * 60)
    print(f"Schema Version: {QAVIOGEN_SCHEMA_VERSION}")
    print(f"Core Version: {__version__}")
    print(f"Features: {len(FEATURES_V2_1)} advanced capabilities")
    print("=" * 60)
    print()


def print_features():
    """Imprimir características soportadas"""
    print("🔧 Supported Features v2.1:")
    print("-" * 30)
    for key, description in FEATURES_V2_1.items():
        print(f"  ✅ {description}")
    print()


def print_validation_result(is_valid: bool, errors: List[str], stats: Dict[str, Any] = None):
    """Imprimir resultado de validación"""
    if is_valid:
        print("✅ VALIDATION PASSED")
        print("The scene configuration is valid and ready for rendering.")
    else:
        print("❌ VALIDATION FAILED")
        print(f"Found {len(errors)} error(s):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    if stats:
        print("\n📊 Scene Statistics:")
        print(f"  Name: {stats['name']}")
        print(f"  Objects: {stats['objects_count']}")
        print(f"  Animations: {stats['animations_count']}")
        print(f"  Timeline Markers: {stats['timeline_markers_count']}")
        print(f"  Layers: {stats['layers_count']}")
        print(f"  Resolution: {stats['render_settings']['resolution']}")
        print(f"  FPS: {stats['render_settings']['fps']}")
        print(f"  Codec: {stats['render_settings']['codec']}")
        
        features = stats['features']
        print("\n🎯 Active Features:")
        if features['avatar_enabled']:
            print("  ✅ Avatar enabled")
            if features['custom_voice']:
                print("  ✅ Custom voice")
        if features['camera_animated']:
            print("  ✅ Camera animation")
        if features['hdri_environment']:
            print("  ✅ HDRI environment")
        if features['postprocessing_bloom']:
            print("  ✅ Bloom postprocessing")
        if features['postprocessing_dof']:
            print("  ✅ Depth of field")
        if features['has_timeline_markers']:
            print("  ✅ Timeline markers")
        if features['has_layers']:
            print("  ✅ Layer composition")
        
        print(f"\n🔒 Certification Level: {features['certification_level'].upper()}")
        if features['compliance_standards']:
            print(f"📋 Compliance: {', '.join(features['compliance_standards'])}")


def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        description="Q-AVIOGEN Scene Validator CLI v2.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_scene.py scene.json
  python validate_scene.py --detailed scene.json
  python validate_scene.py --report scene.json
  python validate_scene.py --fix scene.json
  python validate_scene.py --schema schema.json scene.json
  python validate_scene.py --features
        """
    )
    
    parser.add_argument('file', nargs='?', help='Scene JSON file to validate')
    parser.add_argument('--detailed', '-d', action='store_true', 
                       help='Show detailed statistics')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate detailed validation report')
    parser.add_argument('--fix', '-f', action='store_true',
                       help='Attempt to fix common issues')
    parser.add_argument('--output', '-o', help='Output file for fixed scene')
    parser.add_argument('--schema', '-s', help='JSON schema file for validation')
    parser.add_argument('--features', action='store_true',
                       help='Show supported features')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress banner and extra output')
    parser.add_argument('--version', '-v', action='version', 
                       version=f'Q-AVIOGEN Validator v{__version__}')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    # Mostrar características si se solicita
    if args.features:
        print_features()
        return 0
    
    # Verificar que se proporcionó un archivo
    if not args.file:
        parser.print_help()
        return 1
    
    # Crear validador
    validator = SceneCLIValidator()
    
    try:
        if args.fix:
            # Modo de corrección
            if not args.quiet:
                print(f"🔧 Attempting to fix: {args.file}")
            
            success, fixes = validator.fix_common_issues(args.file, args.output)
            
            if success:
                print("✅ Fixes applied successfully:")
                for fix in fixes:
                    print(f"  • {fix}")
                
                if args.output:
                    print(f"💾 Fixed scene saved to: {args.output}")
                else:
                    print(f"💾 Scene updated: {args.file}")
                
                # Validar después de la corrección
                output_file = args.output or args.file
                is_valid, errors, _ = validator.validate_file(output_file)
                if is_valid:
                    print("✅ Scene is now valid!")
                else:
                    print("⚠️  Some issues remain:")
                    for error in errors:
                        print(f"  • {error}")
            else:
                print("❌ Failed to fix issues:")
                for fix in fixes:
                    print(f"  • {fix}")
                return 1
        
        elif args.report:
            # Modo de reporte
            if not args.quiet:
                print(f"📋 Generating report for: {args.file}")
            
            report = validator.generate_report(args.file)
            print(report)
        
        elif args.schema:
            # Validación contra esquema
            if not args.quiet:
                print(f"🔍 Validating against schema: {args.schema}")
            
            is_valid, errors = validator.validate_against_schema(args.file, args.schema)
            
            if is_valid:
                print("✅ SCHEMA VALIDATION PASSED")
            else:
                print("❌ SCHEMA VALIDATION FAILED")
                for error in errors:
                    print(f"  • {error}")
                return 1
        
        else:
            # Validación estándar
            if not args.quiet:
                print(f"🔍 Validating: {args.file}")
            
            is_valid, errors, stats = validator.validate_file(args.file, args.detailed)
            
            if not args.quiet:
                print()
            
            print_validation_result(is_valid, errors, stats)
            
            if not is_valid:
                return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
