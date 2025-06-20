"""
Verificación rápida de sintaxis
"""
import sys
import os

def check_imports():
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        print("Verificando importaciones...")
        
        # Check parser imports
        from parser.md_parser import MarkdownParser
        print("✅ md_parser")
        
        from parser.scene_builder import SceneBuilder  
        print("✅ scene_builder")
        
        from tts.narration import NarrationGenerator
        print("✅ narration")
        
        from blender.simulated_renderer import get_renderer_class
        print("✅ simulated_renderer")
        
        renderer_class = get_renderer_class()
        print(f"✅ Renderer class: {renderer_class.__name__}")
        
        print("🎉 Todas las importaciones exitosas")
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
