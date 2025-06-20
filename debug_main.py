#!/usr/bin/env python3
"""
Q-AVIOGEN Main Entry Point - Versión Debug
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def debug_main():
    """Main function with extensive error handling"""
    try:
        print("🚀 Iniciando Q-AVIOGEN en modo debug...")
        
        # Test imports
        print("📦 Importando módulos...")
        
        from parser.md_parser import MarkdownParser
        print("  ✅ MarkdownParser")
        
        from parser.scene_builder import SceneBuilder
        print("  ✅ SceneBuilder")
        
        from tts.narration import NarrationGenerator
        print("  ✅ NarrationGenerator")
        
        from blender.simulated_renderer import get_renderer_class
        print("  ✅ get_renderer_class")
        
        # Get renderer class
        RendererClass = get_renderer_class()
        print(f"  ✅ Renderer: {RendererClass.__name__}")
        
        # Initialize components
        print("\n🔧 Inicializando componentes...")
        scene_builder = SceneBuilder(debug=True)
        print("  ✅ SceneBuilder inicializado")
        
        narration_gen = NarrationGenerator(engine="pyttsx3")
        print("  ✅ NarrationGenerator inicializado")
        
        renderer = RendererClass(resolution="1080p", fps=30, output_format="mp4")
        print(f"  ✅ {RendererClass.__name__} inicializado")
        
        # Parse input
        print("\n📖 Parseando archivo de entrada...")
        input_file = "input/markdown/00-30-10-01-TowbarAttachment.md"
        
        if not os.path.exists(input_file):
            print(f"❌ Archivo no encontrado: {input_file}")
            return False
        
        parser_md = MarkdownParser()
        procedure_data = parser_md.parse_file(input_file)
        print(f"  ✅ Procedimiento: {procedure_data.get('title', 'Sin título')}")
        print(f"  📋 Pasos: {len(procedure_data.get('steps', []))}")
        
        # Build scenes
        print("\n🎬 Construyendo escenas...")
        scenes = scene_builder.build_scenes(procedure_data)
        print(f"  ✅ {len(scenes)} escenas construidas")
        
        # Check scene types
        print("\n🔍 Verificando tipos de escenas...")
        for i, scene in enumerate(scenes[:2]):  # Solo los primeros 2 para debug
            print(f"  Escena {i+1}: {type(scene).__name__}")
            print(f"    - name: {scene.name}")
            print(f"    - duration_seconds: {scene.duration_seconds}")
            print(f"    - Tiene método .get(): {hasattr(scene, 'get')}")
        
        # Generate narration
        print("\n🗣️ Generando narración...")
        audio_files = narration_gen.generate_narration(procedure_data)
        print(f"  ✅ {len(audio_files)} archivos de audio generados")
        
        # Render video
        print("\n🎥 Renderizando vídeo...")
        output_path = renderer.render_video(
            scenes=scenes,
            audio_files=audio_files,
            output_dir="output/videos/"
        )
        print(f"  ✅ Renderizado completado: {output_path}")
        
        print("\n🎉 ¡Proceso completado exitosamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        print("\nStack trace completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_main()
    print(f"\nResultado: {'ÉXITO' if success else 'FALLO'}")
