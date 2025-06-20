#!/usr/bin/env python3
"""
Q-AVIOGEN Main Entry Point
Generador automático de vídeos técnicos para procedimientos aeroespaciales
"""

import sys
import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from parser.md_parser import MarkdownParser
from parser.yaml_parser import YAMLParser
from parser.scene_builder import SceneBuilder
from tts.narration import NarrationGenerator
from blender.render_scene import BlenderRenderer

console = Console()

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Q-AVIOGEN: Generador de vídeos técnicos aeroespaciales",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --input input/markdown/towbar.md --output output/videos/
  python main.py --yaml input/yaml/procedure.yaml --format mp4
  python main.py --input example.md --debug --verbose
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', '-i', 
                           help='Archivo Markdown de entrada (.md)')
    input_group.add_argument('--yaml', '-y', 
                           help='Archivo YAML declarativo de entrada')
    
    # Output options
    parser.add_argument('--output', '-o', 
                       default='output/videos/',
                       help='Directorio de salida (default: output/videos/)')
    parser.add_argument('--format', '-f', 
                       choices=['mp4', 'webm', 'mov', 'avi'],
                       default='mp4',
                       help='Formato de vídeo de salida (default: mp4)')
    
    # Processing options
    parser.add_argument('--tts-engine', 
                       choices=['pyttsx3', 'polly', 'elevenlabs'],
                       default='pyttsx3',
                       help='Motor de síntesis de voz (default: pyttsx3)')
    parser.add_argument('--resolution', 
                       choices=['720p', '1080p', '4k'],
                       default='1080p',
                       help='Resolución de vídeo (default: 1080p)')
    parser.add_argument('--fps', 
                       type=int, default=30,
                       help='Frames por segundo (default: 30)')
    
    # Debug options
    parser.add_argument('--debug', action='store_true',
                       help='Activar modo debug')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Salida verbose')
    parser.add_argument('--dry-run', action='store_true',
                       help='Simular ejecución sin renderizar')
    
    args = parser.parse_args()
    
    # Configure logging based on verbosity
    if args.verbose:
        console.print("🔧 [bold blue]Q-AVIOGEN v1.0.0[/bold blue] - Modo verbose activado")
    
    try:
        # Initialize components
        scene_builder = SceneBuilder(debug=args.debug)
        narration_gen = NarrationGenerator(engine=args.tts_engine)
        renderer = BlenderRenderer(
            resolution=args.resolution,
            fps=args.fps,
            output_format=args.format
        )
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Step 1: Parse input
            task1 = progress.add_task("📖 Parseando archivo de entrada...", total=None)
            
            if args.input:
                # Parse Markdown
                parser_md = MarkdownParser()
                procedure_data = parser_md.parse_file(args.input)
            elif args.yaml:
                # Parse YAML
                parser_yaml = YAMLParser()
                procedure_data = parser_yaml.parse_file(args.yaml)
            
            progress.update(task1, description="✅ Archivo parseado correctamente")
            progress.remove_task(task1)
            
            if args.verbose:
                console.print(f"📋 Procedimiento: {procedure_data.get('title', 'Sin título')}")
                console.print(f"🔢 Pasos encontrados: {len(procedure_data.get('steps', []))}")
            
            # Step 2: Build scenes
            task2 = progress.add_task("🎬 Construyendo escenas 3D...", total=None)
            scenes = scene_builder.build_scenes(procedure_data)
            progress.update(task2, description="✅ Escenas construidas")
            progress.remove_task(task2)
            
            # Step 3: Generate narration
            task3 = progress.add_task("🗣️ Generando narración...", total=None)
            audio_files = narration_gen.generate_narration(procedure_data)
            progress.update(task3, description="✅ Narración generada")
            progress.remove_task(task3)
            
            if args.dry_run:
                console.print("🔥 [bold yellow]DRY RUN:[/bold yellow] Simulación completada sin renderizar")
                console.print(f"📁 Se habría creado: {args.output}")
                return
            
            # Step 4: Render video
            task4 = progress.add_task("🎥 Renderizando vídeo...", total=None)
            output_path = renderer.render_video(
                scenes=scenes,
                audio_files=audio_files,
                output_dir=args.output
            )
            progress.update(task4, description="✅ Vídeo renderizado")
            progress.remove_task(task4)
        
        # Success message
        console.print(f"\n🎉 [bold green]¡Vídeo generado exitosamente![/bold green]")
        console.print(f"📁 Ubicación: {output_path}")
        console.print(f"📏 Resolución: {args.resolution}")
        console.print(f"🎵 Audio: {args.tts_engine}")
        
    except FileNotFoundError as e:
        console.print(f"❌ [bold red]Error:[/bold red] Archivo no encontrado: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ [bold red]Error inesperado:[/bold red] {e}")
        if args.debug:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
