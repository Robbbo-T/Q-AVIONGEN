#!/usr/bin/env python3
"""
Q-AVIOGEN Setup and Installation Script
Script de instalación y configuración para Q-AVIOGEN
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

class QAviagenSetup:
    """Setup and installation manager for Q-AVIOGEN"""
    
    def __init__(self):
        self.python_version = sys.version_info
        self.platform = platform.system()
        self.project_root = Path(__file__).parent
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        if self.python_version < (3, 8):
            console.print("❌ Python 3.8+ requerido. Versión actual:", 
                         f"{self.python_version.major}.{self.python_version.minor}")
            return False
        
        console.print(f"✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        return True
    
    def create_virtual_environment(self) -> bool:
        """Create Python virtual environment"""
        venv_path = self.project_root / "venv"
        
        if venv_path.exists():
            console.print("📦 Virtual environment ya existe")
            return True
        
        try:
            console.print("📦 Creando virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], 
                          check=True, capture_output=True)
            console.print("✅ Virtual environment creado")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Error creando virtual environment: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            console.print("❌ requirements.txt no encontrado")
            return False
        
        try:
            console.print("📥 Instalando dependencias de Python...")
            
            # Detect virtual environment
            venv_path = self.project_root / "venv"
            if venv_path.exists():
                if self.platform == "Windows":
                    pip_cmd = str(venv_path / "Scripts" / "pip.exe")
                else:
                    pip_cmd = str(venv_path / "bin" / "pip")
            else:
                pip_cmd = "pip"
            
            # Install requirements
            subprocess.run([pip_cmd, "install", "-r", str(requirements_file)], 
                          check=True)
            console.print("✅ Dependencias instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Error instalando dependencias: {e}")
            return False
    
    def check_blender_installation(self) -> bool:
        """Check if Blender is installed and accessible"""
        try:
            result = subprocess.run(["blender", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                console.print(f"✅ Blender detectado: {version_line}")
                return True
            else:
                console.print("❌ Blender no encontrado en PATH")
                return False
        except FileNotFoundError:
            console.print("❌ Blender no está instalado o no está en PATH")
            return False
    
    def create_directory_structure(self) -> bool:
        """Create necessary directory structure"""
        directories = [
            "assets/models",
            "assets/textures", 
            "assets/audio",
            "output/videos",
            "output/frames",
            "output/audio",
            "output/audio_cache",
            "temp",
            "cache"
        ]
        
        console.print("📁 Creando estructura de directorios...")
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        console.print("✅ Estructura de directorios creada")
        return True
    
    def create_example_files(self) -> bool:
        """Create example configuration and template files"""
        examples = {
            "assets/models/README.md": """# 3D Models Directory

Coloque aquí los modelos 3D:

- `bwb_q100.glb` - Modelo principal de la aeronave BWB-Q100
- `towbar.glb` - Modelo del towbar/barra de remolque
- `nose_gear.glb` - Tren de aterrizaje delantero
- `mechanic.glb` - Modelo del mecánico/persona
- `tools.glb` - Herramientas comunes

## Formatos soportados
- .glb (recomendado)
- .gltf
- .fbx
- .obj
- .blend

## Fuentes de modelos
- GAIA-QAO Asset Library
- Blender Asset Browser
- Sketchfab (con licencia)
- Modelos propios
""",
            "assets/textures/README.md": """# Textures Directory

Directorio para texturas y materiales:

- Texturas PBR (albedo, normal, roughness, metallic)
- Mapas de entorno (HDRI)
- Texturas de overlays
- Logotipos y marcas

## Formatos soportados
- .png (recomendado)
- .jpg/.jpeg
- .hdr (para HDRI)
- .exr
""",
            "config_template.ini": """# Q-AVIOGEN Configuration Template
# Copie este archivo a config_local.ini y modifique según necesidades

[general]
debug = false
log_level = INFO

[rendering]
resolution = 1080p
fps = 30
format = mp4
quality = high

[tts]
engine = pyttsx3
language = es-ES

[blender]
render_engine = CYCLES
device = GPU

# AWS Polly (opcional)
[aws]
# region = us-east-1
# access_key_id = YOUR_ACCESS_KEY
# secret_access_key = YOUR_SECRET_KEY

# ElevenLabs (opcional)
[elevenlabs]
# api_key = YOUR_ELEVENLABS_API_KEY
"""
        }
        
        console.print("📄 Creando archivos de ejemplo...")
        
        for file_path, content in examples.items():
            full_path = self.project_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        console.print("✅ Archivos de ejemplo creados")
        return True
    
    def run_tests(self) -> bool:
        """Run basic tests to verify installation"""
        console.print("🧪 Ejecutando tests básicos...")
        
        try:
            # Test imports
            sys.path.insert(0, str(self.project_root))
            
            from parser.md_parser import MarkdownParser
            from parser.yaml_parser import YAMLParser
            from parser.scene_builder import SceneBuilder
            
            # Basic functionality tests
            md_parser = MarkdownParser()
            yaml_parser = YAMLParser()
            scene_builder = SceneBuilder()
            
            console.print("✅ Importaciones correctas")
            console.print("✅ Tests básicos pasados")
            return True
            
        except Exception as e:
            console.print(f"❌ Error en tests: {e}")
            return False
    
    def setup_environment_script(self) -> bool:
        """Create environment activation scripts"""
        if self.platform == "Windows":
            script_content = f"""@echo off
echo Activando entorno Q-AVIOGEN...
call "{self.project_root}\\venv\\Scripts\\activate.bat"
echo.
echo ✅ Entorno activado. Comandos disponibles:
echo   python main.py --help
echo   python batch_render.py --help
echo.
"""
            script_path = self.project_root / "activate_env.bat"
        else:
            script_content = f"""#!/bin/bash
echo "Activando entorno Q-AVIOGEN..."
source "{self.project_root}/venv/bin/activate"
echo
echo "✅ Entorno activado. Comandos disponibles:"
echo "  python main.py --help"
echo "  python batch_render.py --help"
echo
"""
            script_path = self.project_root / "activate_env.sh"
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        if self.platform != "Windows":
            os.chmod(script_path, 0o755)
        
        console.print(f"✅ Script de activación creado: {script_path.name}")
        return True
    
    def show_completion_message(self):
        """Show setup completion message with next steps"""
        console.print("\n🎉 [bold green]¡Instalación de Q-AVIOGEN completada![/bold green]")
        console.print("=" * 60)
        
        console.print("\n📋 [bold cyan]Próximos pasos:[/bold cyan]")
        
        if self.platform == "Windows":
            console.print("1. Activar entorno: [yellow]activate_env.bat[/yellow]")
        else:
            console.print("1. Activar entorno: [yellow]source activate_env.sh[/yellow]")
        
        console.print("2. Probar instalación: [yellow]python main.py --help[/yellow]")
        console.print("3. Procesar ejemplo: [yellow]python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md[/yellow]")
        console.print("4. Procesamiento por lotes: [yellow]python batch_render.py --input-dir input/[/yellow]")
        
        console.print("\n📖 [bold cyan]Recursos:[/bold cyan]")
        console.print("• Documentación: README.md")
        console.print("• Ejemplos: input/markdown/ y input/yaml/")
        console.print("• Configuración: config_template.ini")
        console.print("• Tests: python -m pytest tests/")
        
        console.print("\n🛠️ [bold cyan]Instalaciones adicionales recomendadas:[/bold cyan]")
        if not self.check_blender_installation():
            console.print("• Blender 3.0+: https://www.blender.org/download/")
        console.print("• Git LFS para assets grandes: git lfs install")
        
        console.print("\n🆘 [bold cyan]Soporte:[/bold cyan]")
        console.print("• Issues: GitHub Issues")
        console.print("• Documentación: docs/")
        console.print("• Email: soporte@q-aviogen.com")

def main():
    """Main setup function"""
    console.print("🚀 [bold blue]Q-AVIOGEN Setup Wizard[/bold blue]")
    console.print("Configurando Q-AVIOGEN - Generador de vídeos técnicos aeroespaciales")
    console.print("=" * 70)
    
    setup = QAviagenSetup()
    
    # Setup steps
    steps = [
        ("Verificando versión de Python", setup.check_python_version),
        ("Creando virtual environment", setup.create_virtual_environment),
        ("Instalando dependencias", setup.install_dependencies),
        ("Creando estructura de directorios", setup.create_directory_structure),
        ("Creando archivos de ejemplo", setup.create_example_files),
        ("Configurando scripts de entorno", setup.setup_environment_script),
        ("Ejecutando tests básicos", setup.run_tests),
    ]
    
    failed_steps = []
    
    for step_name, step_function in track(steps, description="Configurando..."):
        console.print(f"\n📋 {step_name}")
        try:
            if not step_function():
                failed_steps.append(step_name)
        except Exception as e:
            console.print(f"❌ Error en {step_name}: {e}")
            failed_steps.append(step_name)
    
    # Check Blender (non-critical)
    console.print(f"\n📋 Verificando instalación de Blender")
    setup.check_blender_installation()
    
    # Show results
    if failed_steps:
        console.print(f"\n⚠️ [bold yellow]Setup completado con errores:[/bold yellow]")
        for step in failed_steps:
            console.print(f"  • {step}")
        console.print("\nRevise los errores antes de continuar.")
        return 1
    else:
        setup.show_completion_message()
        return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n⚠️ Setup interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n❌ Error inesperado en setup: {e}")
        sys.exit(1)
