#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento de Q-AVIOGEN
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test import parser
    from parser.md_parser import MarkdownParser
    print("✅ MarkdownParser importado correctamente")
    
    # Test import scene builder
    from parser.scene_builder import SceneBuilder
    print("✅ SceneBuilder importado correctamente")
    
    # Test import TTS
    from tts.narration import NarrationGenerator
    print("✅ NarrationGenerator importado correctamente")
    
    # Test simulated renderer
    from blender.simulated_renderer import SimulatedBlenderRenderer
    print("✅ SimulatedBlenderRenderer importado correctamente")
    
    # Test parsing a file
    parser = MarkdownParser()
    input_file = "input/markdown/00-30-10-01-TowbarAttachment.md"
    
    if os.path.exists(input_file):
        print(f"📖 Parseando archivo: {input_file}")
        procedure_data = parser.parse_file(input_file)
        print(f"✅ Archivo parseado: {procedure_data['title']}")
        print(f"📋 Pasos encontrados: {len(procedure_data['steps'])}")
        
        # Test scene building
        print("🎬 Construyendo escenas...")
        scene_builder = SceneBuilder()
        scenes = scene_builder.build_scenes(procedure_data)
        print(f"✅ {len(scenes)} escenas construidas")
        
        # Test narration generation
        print("🗣️ Generando narración...")
        narration_gen = NarrationGenerator(engine="pyttsx3")
        audio_files = narration_gen.generate_narration(procedure_data)
        print(f"✅ {len(audio_files)} archivos de audio generados")
        
        # Test simulated rendering
        print("🎥 Iniciando renderizado simulado...")
        renderer = SimulatedBlenderRenderer()
        output_path = renderer.render_video(scenes, audio_files, "output/videos/")
        print(f"✅ Renderizado completado: {output_path}")
        
    else:
        print(f"❌ Archivo no encontrado: {input_file}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
