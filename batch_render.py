#!/usr/bin/env python3
"""
Batch Renderer for Q-AVIOGEN
Renderiza múltiples procedimientos en lote
"""

import os
import sys
import argparse
import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import main as render_single
from parser.md_parser import MarkdownParser
from parser.yaml_parser import YAMLParser

console = Console()

class BatchRenderer:
    """Batch renderer for multiple procedures"""
    
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers
        self.results = []
        
    def discover_files(self, input_dir: str, file_types: list = None) -> list:
        """Discover input files in directory"""
        if file_types is None:
            file_types = ['*.md', '*.yaml', '*.yml']
        
        input_path = Path(input_dir)
        found_files = []
        
        for pattern in file_types:
            found_files.extend(input_path.rglob(pattern))
        
        return sorted(found_files)
    
    def validate_file(self, file_path: Path) -> tuple:
        """Validate if file can be processed"""
        try:
            if file_path.suffix.lower() == '.md':
                parser = MarkdownParser()
                data = parser.parse_file(str(file_path))
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                parser = YAMLParser()
                data = parser.parse_file(str(file_path))
            else:
                return False, "Tipo de archivo no soportado"
            
            # Check if has required fields
            if not data.get('steps'):
                return False, "Sin pasos definidos"
            
            return True, "OK"
            
        except Exception as e:
            return False, str(e)
    
    def process_file(self, file_path: Path, output_dir: str, **kwargs) -> dict:
        """Process a single file"""
        result = {
            'file': str(file_path),
            'status': 'processing',
            'output': '',
            'error': '',
            'duration': 0
        }
        
        try:
            import time
            start_time = time.time()
            
            # Build command arguments
            args = [
                '--output', output_dir,
                '--format', kwargs.get('format', 'mp4'),
                '--tts-engine', kwargs.get('tts_engine', 'pyttsx3'),
                '--resolution', kwargs.get('resolution', '1080p')
            ]
            
            if file_path.suffix.lower() == '.md':
                args.extend(['--input', str(file_path)])
            else:
                args.extend(['--yaml', str(file_path)])
            
            if kwargs.get('verbose'):
                args.append('--verbose')
            
            # Simulate rendering (replace with actual call to main)
            # In real implementation, you would call the main function
            # result['output'] = render_single_with_args(args)
            
            # For now, simulate processing
            import time
            time.sleep(2)  # Simulate processing time
            
            result['status'] = 'completed'
            result['output'] = f"{output_dir}/{file_path.stem}.mp4"
            result['duration'] = time.time() - start_time
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def render_batch(self, input_dir: str, output_dir: str, **kwargs) -> list:
        """Render multiple files in batch"""
        # Discover files
        files = self.discover_files(input_dir)
        
        if not files:
            console.print(f"❌ No se encontraron archivos en: {input_dir}")
            return []
        
        console.print(f"📁 Encontrados {len(files)} archivos para procesar")
        
        # Validate files
        valid_files = []
        for file_path in files:
            is_valid, message = self.validate_file(file_path)
            if is_valid:
                valid_files.append(file_path)
            else:
                console.print(f"⚠️ Archivo inválido {file_path.name}: {message}")
        
        if not valid_files:
            console.print("❌ No hay archivos válidos para procesar")
            return []
        
        console.print(f"✅ {len(valid_files)} archivos válidos para procesar")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Process files
        with Progress(console=console) as progress:
            main_task = progress.add_task(
                "🎬 Procesando archivos...", 
                total=len(valid_files)
            )
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(self.process_file, file_path, output_dir, **kwargs): file_path
                    for file_path in valid_files
                }
                
                # Process completed tasks
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    result = future.result()
                    self.results.append(result)
                    
                    progress.update(main_task, advance=1)
                    
                    # Show status
                    if result['status'] == 'completed':
                        console.print(f"✅ {file_path.name} completado")
                    else:
                        console.print(f"❌ {file_path.name} falló: {result['error']}")
        
        return self.results
    
    def generate_report(self) -> None:
        """Generate batch processing report"""
        if not self.results:
            return
        
        # Summary statistics
        total = len(self.results)
        completed = len([r for r in self.results if r['status'] == 'completed'])
        errors = len([r for r in self.results if r['status'] == 'error'])
        
        console.print("\n📊 Resumen del Procesamiento por Lotes")
        console.print("=" * 50)
        
        # Summary table
        summary_table = Table(title="Estadísticas de Procesamiento")
        summary_table.add_column("Métrica", style="cyan")
        summary_table.add_column("Valor", style="green")
        
        summary_table.add_row("Total de archivos", str(total))
        summary_table.add_row("Completados", str(completed))
        summary_table.add_row("Errores", str(errors))
        summary_table.add_row("Tasa de éxito", f"{(completed/total*100):.1f}%" if total > 0 else "0%")
        
        console.print(summary_table)
        
        # Detailed results
        if self.results:
            console.print("\n📋 Resultados Detallados")
            
            results_table = Table(title="Resultados por Archivo")
            results_table.add_column("Archivo", style="cyan")
            results_table.add_column("Estado", style="magenta")
            results_table.add_column("Duración (s)", style="yellow")
            results_table.add_column("Output/Error", style="white")
            
            for result in self.results:
                file_name = Path(result['file']).name
                status = "✅ OK" if result['status'] == 'completed' else "❌ Error"
                duration = f"{result['duration']:.1f}" if result['duration'] > 0 else "-"
                output = result['output'] if result['status'] == 'completed' else result['error']
                
                results_table.add_row(file_name, status, duration, output[:50] + "..." if len(output) > 50 else output)
            
            console.print(results_table)

def main():
    """Main batch renderer entry point"""
    parser = argparse.ArgumentParser(
        description="Q-AVIOGEN Batch Renderer - Procesa múltiples procedimientos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python batch_render.py --input-dir input/markdown/ --output-dir output/videos/
  python batch_render.py --input-dir input/ --workers 4 --format webm
  python batch_render.py --input-dir input/ --filter "*.yaml" --resolution 4k
        """
    )
    
    # Input/Output
    parser.add_argument('--input-dir', '-i', required=True,
                       help='Directorio con archivos de entrada')
    parser.add_argument('--output-dir', '-o', default='output/batch/',
                       help='Directorio de salida (default: output/batch/)')
    
    # Processing options
    parser.add_argument('--workers', '-w', type=int, default=2,
                       help='Número de trabajadores paralelos (default: 2)')
    parser.add_argument('--filter', 
                       help='Filtro de archivos (ej: "*.md", "*.yaml")')
    
    # Video options
    parser.add_argument('--format', choices=['mp4', 'webm', 'mov', 'avi'],
                       default='mp4', help='Formato de video (default: mp4)')
    parser.add_argument('--resolution', choices=['720p', '1080p', '4k'],
                       default='1080p', help='Resolución (default: 1080p)')
    parser.add_argument('--tts-engine', choices=['pyttsx3', 'polly', 'elevenlabs'],
                       default='pyttsx3', help='Motor TTS (default: pyttsx3)')
    
    # Control options
    parser.add_argument('--dry-run', action='store_true',
                       help='Simular sin procesar realmente')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Salida verbose')
    parser.add_argument('--continue-on-error', action='store_true',
                       help='Continuar procesando aunque haya errores')
    
    args = parser.parse_args()
    
    # Initialize batch renderer
    renderer = BatchRenderer(max_workers=args.workers)
    
    console.print("🚀 [bold blue]Q-AVIOGEN Batch Renderer[/bold blue]")
    console.print(f"📂 Input: {args.input_dir}")
    console.print(f"📁 Output: {args.output_dir}")
    console.print(f"👷 Workers: {args.workers}")
    
    if args.dry_run:
        console.print("🔥 [bold yellow]MODO DRY RUN[/bold yellow] - Solo simulación")
    
    try:
        # Discover files first
        file_types = [args.filter] if args.filter else None
        files = renderer.discover_files(args.input_dir, file_types)
        
        if not files:
            console.print(f"❌ No se encontraron archivos en {args.input_dir}")
            return 1
        
        console.print(f"📋 Archivos encontrados: {len(files)}")
        for f in files[:5]:  # Show first 5
            console.print(f"  • {f.name}")
        if len(files) > 5:
            console.print(f"  ... y {len(files) - 5} más")
        
        if args.dry_run:
            console.print("✅ Dry run completado - no se procesaron archivos")
            return 0
        
        # Process files
        kwargs = {
            'format': args.format,
            'resolution': args.resolution,
            'tts_engine': args.tts_engine,
            'verbose': args.verbose,
            'continue_on_error': args.continue_on_error
        }
        
        results = renderer.render_batch(args.input_dir, args.output_dir, **kwargs)
        
        # Generate report
        renderer.generate_report()
        
        # Return exit code based on results
        if not results:
            return 1
        
        errors = len([r for r in results if r['status'] == 'error'])
        if errors > 0 and not args.continue_on_error:
            return 1
        
        console.print(f"\n🎉 [bold green]Batch processing completado![/bold green]")
        return 0
        
    except KeyboardInterrupt:
        console.print("\n⚠️ Procesamiento interrumpido por el usuario")
        return 130
    except Exception as e:
        console.print(f"\n❌ [bold red]Error inesperado:[/bold red] {e}")
        if args.verbose:
            import traceback
            console.print(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
