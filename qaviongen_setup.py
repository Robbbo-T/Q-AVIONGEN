#!/usr/bin/env python3
"""
Q-AVIOGEN Setup and Installation Script
Configura el sistema de seguimiento diario automático
"""

import os
import sys
import json
import shutil
import winreg
from pathlib import Path
import subprocess

class QAviogenSetup:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.project_name = "Q-AVIOGEN"
        
    def check_requirements(self):
        """Verifica e instala los requisitos"""
        print("🔍 Verificando requisitos...")
        
        required_packages = [
            'tkinter',
            'matplotlib',
            'pandas',
            'numpy'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'tkinter':
                    import tkinter
                elif package == 'matplotlib':
                    import matplotlib
                elif package == 'pandas':
                    import pandas
                elif package == 'numpy':
                    import numpy
                print(f"✅ {package} está instalado")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} no está instalado")
        
        if missing_packages:
            print(f"\n📦 Instalando paquetes faltantes: {', '.join(missing_packages)}")
            self.install_packages(missing_packages)
        
        print("✅ Todos los requisitos están listos")
    
    def install_packages(self, packages):
        """Instala los paquetes faltantes"""
        for package in packages:
            if package == 'tkinter':
                print("⚠️ tkinter debe instalarse manualmente con Python")
                continue
            
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error instalando {package}")
    
    def create_desktop_shortcut(self):
        """Crea acceso directo en el escritorio"""
        print("🖥️ Creando acceso directo en el escritorio...")
        
        try:
            import win32com.client
            
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / f"{self.project_name} - Daily Task Manager.lnk"
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{self.base_path / "daily_task_manager.py"}"'
            shortcut.WorkingDirectory = str(self.base_path)
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print(f"✅ Acceso directo creado: {shortcut_path}")
            
        except ImportError:
            print("⚠️ pywin32 no disponible, creando archivo .bat en su lugar...")
            self.create_batch_shortcut()
    
    def create_batch_shortcut(self):
        """Crea un archivo .bat como alternativa"""
        desktop = Path.home() / "Desktop"
        batch_path = desktop / f"{self.project_name} Daily Task Manager.bat"
        
        batch_content = f'''@echo off
title Q-AVIOGEN Daily Task Manager
cd /d "{self.base_path}"
python daily_task_manager.py
pause
'''
        
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        
        print(f"✅ Archivo batch creado: {batch_path}")
    
    def setup_startup(self):
        """Configura inicio automático con Windows"""
        print("🚀 Configurando inicio automático...")
        
        try:
            # Crear script de inicio
            startup_script = self.base_path / "startup_qaviongen.bat"
            startup_content = f'''@echo off
cd /d "{self.base_path}"
python daily_task_manager.py --startup
'''
            
            with open(startup_script, 'w') as f:
                f.write(startup_content)
            
            # Copiar a carpeta de inicio de Windows
            startup_folder = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
            startup_dest = startup_folder / "Q-AVIOGEN_Daily_Task.bat"
            
            if startup_folder.exists():
                shutil.copy2(startup_script, startup_dest)
                print(f"✅ Script de inicio configurado: {startup_dest}")
            else:
                print("⚠️ Carpeta de inicio no encontrada")
                print(f"Copia manualmente {startup_script} a la carpeta de inicio de Windows")
            
        except Exception as e:
            print(f"❌ Error configurando inicio automático: {e}")
    
    def create_calendar_file(self):
        """Crea archivo de calendario .ics para importar"""
        print("📅 Creando archivo de calendario...")
        
        from datetime import datetime, timedelta
        
        # Leer configuración
        with open(self.base_path / "config.json", 'r') as f:
            config = json.load(f)
        
        start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
        
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Q-AVIOGEN//Daily Task Manager//ES
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Q-AVIOGEN Desarrollo
X-WR-TIMEZONE:Europe/Madrid
X-WR-CALDESC:Plan de desarrollo de 30 días para Q-AVIOGEN
"""
        
        # Crear eventos para cada día
        phases = [
            ("Infraestructura mínima (Docker + API)", 4),
            ("Documentación Marketplace + Web", 3),
            ("Avatar y voz final", 4),
            ("Generación de demos", 4),
            ("Azure listing (registro y validación)", 5),
            ("AWS listing", 3),
            ("GCP listing", 3),
            ("Landing pública + CRM básico", 4),
            ("Demo comercial PDF + PPT", 2),
            ("Test final full pipeline", 2)
        ]
        
        current_day = start_date
        task_index = 0
        hours_remaining = phases[task_index][1] * config['daily_hours']
        task_name = phases[task_index][0]
        
        for day in range(30):
            # Crear evento
            event_start = current_day.replace(hour=9, minute=0)  # 9 AM
            event_end = event_start + timedelta(hours=config['daily_hours'])
            
            ics_content += f"""
BEGIN:VEVENT
UID:{current_day.strftime('%Y%m%d')}@qaviongen.com
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{event_start.strftime('%Y%m%dT%H%M%S')}
DTEND:{event_end.strftime('%Y%m%dT%H%M%S')}
SUMMARY:Q-AVIOGEN: {task_name}
DESCRIPTION:Trabajo en {task_name}\\nHoras: {min(config['daily_hours'], hours_remaining)}h\\nDía {day + 1} de 30
LOCATION:Home Office
STATUS:TENTATIVE
TRANSP:OPAQUE
END:VEVENT"""
            
            current_day += timedelta(days=1)
            hours_remaining -= config['daily_hours']
            
            if hours_remaining <= 0 and task_index + 1 < len(phases):
                task_index += 1
                task_name = phases[task_index][0]
                hours_remaining = phases[task_index][1] * config['daily_hours']
        
        ics_content += "\nEND:VCALENDAR"
        
        # Guardar archivo
        calendar_file = self.base_path / "Q-AVIOGEN_Plan_30_Dias.ics"
        with open(calendar_file, 'w', encoding='utf-8') as f:
            f.write(ics_content)
        
        print(f"✅ Archivo de calendario creado: {calendar_file}")
        print("   Puedes importarlo en Google Calendar, Outlook, etc.")
    
    def create_readme(self):
        """Crea archivo README con instrucciones"""
        print("📖 Creando documentación...")
        
        readme_content = f"""# Q-AVIOGEN Daily Task Manager

## Instalación Completada ✅

El sistema de seguimiento diario de Q-AVIOGEN ha sido configurado correctamente.

## Archivos Creados

- `daily_task_manager.py` - Aplicación principal
- `config.json` - Configuración del proyecto
- `Q-AVIOGEN_Plan_30_Dias.ics` - Calendario para importar
- `startup_qaviongen.bat` - Script de inicio automático
- `task_progress.json` - Archivo de progreso (se crea automáticamente)

## Cómo Usar

### Inicio Diario Automático
- El sistema se inicia automáticamente al encender Windows
- Muestra una notificación con la tarea del día
- Opción de abrir el panel completo

### Ejecutar Manualmente
```bash
python daily_task_manager.py
```

### Modo Solo Notificación
```bash
python daily_task_manager.py --startup
```

## Funcionalidades

### Panel Principal
- 📋 Tarea del día actual
- ⏰ Horas planificadas vs trabajadas
- ✅ Marcar tareas como completadas
- 📊 Progreso general del proyecto

### Forecast de Ingresos
- 💰 Proyección mensual de ingresos
- 📈 Gráficos de crecimiento
- 👥 Estimación de clientes
- 🎯 Milestones por fase

### Progreso Detallado
- 📋 Todas las tareas del proyecto
- 🔍 Progreso por fases
- 📝 Notas y tiempo real trabajado
- 📊 Estadísticas de eficiencia

## Configuración

Edita `config.json` para personalizar:
- Horas de trabajo diarias
- Días laborables
- Objetivos de ingresos
- Fechas de lanzamiento

## Calendario

Importa `Q-AVIOGEN_Plan_30_Dias.ics` en tu aplicación de calendario favorita:
- Google Calendar
- Microsoft Outlook
- Apple Calendar
- Cualquier app compatible con .ics

## Soporte

Para problemas o mejoras:
- Revisa los logs en la aplicación
- Verifica que todos los requisitos estén instalados
- Contacta al equipo de desarrollo

## Cronograma de 30 Días

### Fases del Proyecto:
1. **Infraestructura mínima** (4 días) - Docker + API básica
2. **Documentación Marketplace** (3 días) - Docs para Azure/AWS/GCP
3. **Avatar y voz final** (4 días) - Sistema TTS completo
4. **Generación de demos** (4 días) - Material comercial
5. **Azure listing** (5 días) - Registro y validación
6. **AWS listing** (3 días) - Marketplace AWS
7. **GCP listing** (3 días) - Marketplace GCP
8. **Landing pública + CRM** (4 días) - Web final
9. **Demo comercial** (2 días) - PDF + PPT
10. **Test final** (2 días) - Validación completa

### Objetivos de Ingresos:
- **Mes 1**: $25,000 ARR
- **Mes 3**: $100,000 ARR
- **Mes 6**: $500,000 ARR
- **Mes 12**: $2,000,000 ARR

¡Éxito en el desarrollo de Q-AVIOGEN! 🚀
"""
        
        readme_file = self.base_path / "README_Daily_Task_Manager.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ Documentación creada: {readme_file}")
    
    def run_setup(self):
        """Ejecuta la configuración completa"""
        print("🚀 Iniciando configuración de Q-AVIOGEN Daily Task Manager\n")
        
        try:
            self.check_requirements()
            print()
            
            self.create_desktop_shortcut()
            print()
            
            self.setup_startup()
            print()
            
            self.create_calendar_file()
            print()
            
            self.create_readme()
            print()
            
            print("🎉 ¡Configuración completada exitosamente!")
            print("\n📋 Próximos pasos:")
            print("1. Importa Q-AVIOGEN_Plan_30_Dias.ics en tu calendario")
            print("2. El sistema se iniciará automáticamente mañana")
            print("3. Usa el acceso directo del escritorio para abrir el panel")
            print("4. ¡Comienza a trabajar en Q-AVIOGEN!")
            
            # Preguntar si ejecutar ahora
            try:
                response = input("\n¿Quieres abrir el Task Manager ahora? (y/n): ")
                if response.lower() in ['y', 'yes', 's', 'si', 'sí']:
                    subprocess.run([sys.executable, "daily_task_manager.py"])
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
            
        except Exception as e:
            print(f"❌ Error durante la configuración: {e}")
            print("Por favor revisa los errores y ejecuta setup.py nuevamente")

if __name__ == "__main__":
    setup = QAviogenSetup()
    setup.run_setup()
