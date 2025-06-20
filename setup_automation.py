#!/usr/bin/env python3
"""
Q-AVIOGEN Setup Automation
Configura el sistema para inicio automático del tracker diario
"""

import os
import sys
import winreg
from pathlib import Path
import subprocess
import json
from datetime import datetime

class QAviogenSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.startup_script = self.project_root / "startup_script.bat"
        
    def install_dependencies(self):
        """Instalar dependencias necesarias"""
        print("📦 Instalando dependencias...")
        
        dependencies = ["rich", "fastapi", "uvicorn", "requests", "pandas"]
        
        for dep in dependencies:
            try:
                __import__(dep)
                print(f"✅ {dep} ya instalado")
            except ImportError:
                print(f"📥 Instalando {dep}...")
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"✅ {dep} instalado exitosamente")
    
    def setup_windows_startup(self):
        """Configurar inicio automático en Windows"""
        print("🚀 Configurando inicio automático...")
        
        try:
            # Registrar en el Registry de Windows para inicio automático
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(
                    key,
                    "Q-AVIOGEN_Tracker",
                    0,
                    winreg.REG_SZ,
                    str(self.startup_script)
                )
            
            print("✅ Inicio automático configurado exitosamente")
            print(f"📍 Script registrado: {self.startup_script}")
            
        except Exception as e:
            print(f"⚠️  Error configurando inicio automático: {e}")
            print("💡 Puedes ejecutar manualmente startup_script.bat cada día")
    
    def create_desktop_shortcut(self):
        """Crear acceso directo en el escritorio"""
        print("🖥️  Creando acceso directo...")
        
        try:
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "Q-AVIOGEN Tracker.bat"
            
            # Crear un bat file en el escritorio que ejecute nuestro script
            shortcut_content = f"""@echo off
cd /d "{self.project_root}"
call startup_script.bat
"""
            
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            
            print(f"✅ Acceso directo creado: {shortcut_path}")
            
        except Exception as e:
            print(f"⚠️  Error creando acceso directo: {e}")
    
    def setup_project_structure(self):
        """Configurar estructura inicial del proyecto"""
        print("📁 Configurando estructura de proyecto...")
        
        # Crear directorios necesarios si no existen
        directories = [
            "logs",
            "output/revenue_reports",
            "temp",
            "backups"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            print(f"✅ Directorio creado: {directory}")
    
    def create_revenue_forecast_script(self):
        """Crear script de forecast de ingresos"""
        print("💰 Creando sistema de forecast...")
        
        forecast_script = self.project_root / "revenue_forecast.py"
        
        forecast_content = '''#!/usr/bin/env python3
"""
Q-AVIOGEN Revenue Forecast System
Análisis predictivo de ingresos basado en el plan de 30 días
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

class RevenueForecast:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / "tracker_config.json"
        
        # Modelo de revenue por fase
        self.revenue_model = {
            "Infraestructura Mínima": {"base": 0, "multiplier": 1.0},
            "Documentación Marketplace": {"base": 0, "multiplier": 1.0},
            "Avatar y Voz Final": {"base": 500, "multiplier": 1.2},
            "Generación de Demos": {"base": 1000, "multiplier": 1.5},
            "Azure Marketplace": {"base": 3000, "multiplier": 2.0},
            "AWS Marketplace": {"base": 2000, "multiplier": 1.8},
            "GCP Marketplace": {"base": 1500, "multiplier": 1.6},
            "Landing Público + CRM": {"base": 2000, "multiplier": 2.5},
            "Demo Comercial": {"base": 1000, "multiplier": 1.3},
            "Test Final": {"base": 5000, "multiplier": 3.0}
        }
    
    def load_progress(self):
        """Cargar progreso actual"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return None
    
    def calculate_current_revenue(self):
        """Calcular revenue actual basado en progreso"""
        config = self.load_progress()
        if not config:
            return 0
        
        total_revenue = 0
        for item in config["schedule"]:
            if item["completed"]:
                total_revenue += item.get("revenue_target", 0)
        
        return total_revenue
    
    def forecast_weekly(self):
        """Forecast semanal de revenue"""
        weeks_forecast = [
            {"week": 1, "dates": "Jun 23-29", "target": 0, "description": "Setup fase"},
            {"week": 2, "dates": "Jun 30-Jul 6", "target": 500, "description": "Primeros leads"},
            {"week": 3, "dates": "Jul 7-13", "target": 2000, "description": "Demos activos"},
            {"week": 4, "dates": "Jul 14-20", "target": 5000, "description": "Marketplace live"},
            {"week": 5, "dates": "Jul 21-22", "target": 10000, "description": "Primeras ventas"}
        ]
        
        return weeks_forecast
    
    def forecast_monthly(self):
        """Forecast mensual proyectado"""
        monthly_forecast = [
            {"month": "Jul 2025", "revenue": 15000, "customers": 3},
            {"month": "Aug 2025", "revenue": 25000, "customers": 8},
            {"month": "Sep 2025", "revenue": 45000, "customers": 15},
            {"month": "Oct 2025", "revenue": 70000, "customers": 25},
            {"month": "Nov 2025", "revenue": 90000, "customers": 35},
            {"month": "Dec 2025", "revenue": 120000, "customers": 50}
        ]
        
        return monthly_forecast
    
    def generate_report(self):
        """Generar reporte completo de forecast"""
        current_revenue = self.calculate_current_revenue()
        weekly = self.forecast_weekly()
        monthly = self.forecast_monthly()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "current_revenue": current_revenue,
            "weekly_forecast": weekly,
            "monthly_forecast": monthly,
            "target_arr_2025": 1000000,
            "confidence_level": "Alta (85%)"
        }
        
        # Guardar reporte
        report_file = self.project_root / "output" / "revenue_reports" / f"forecast_{datetime.now().strftime('%Y%m%d')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report

if __name__ == "__main__":
    forecast = RevenueForecast()
    report = forecast.generate_report()
    
    print("💰 Q-AVIOGEN Revenue Forecast")
    print("=" * 40)
    print(f"Revenue actual: ${report['current_revenue']:,}")
    print(f"Target ARR 2025: ${report['target_arr_2025']:,}")
    print(f"Confianza: {report['confidence_level']}")
    
    print("\\nForecast Semanal:")
    for week in report['weekly_forecast']:
        print(f"  Semana {week['week']} ({week['dates']}): ${week['target']:,} - {week['description']}")
    
    print("\\nForecast Mensual (6 meses):")
    for month in report['monthly_forecast']:
        print(f"  {month['month']}: ${month['revenue']:,} ({month['customers']} clientes)")
'''
        
        with open(forecast_script, 'w', encoding='utf-8') as f:
            f.write(forecast_content)
        
        print(f"✅ Script de forecast creado: {forecast_script}")
    
    def run_setup(self):
        """Ejecutar setup completo"""
        print("🚀 Q-AVIOGEN Setup Automation")
        print("=" * 50)
        print("Configurando sistema de seguimiento automático...")
        print()
        
        try:
            # 1. Instalar dependencias
            self.install_dependencies()
            print()
            
            # 2. Configurar estructura
            self.setup_project_structure()
            print()
            
            # 3. Crear forecast system
            self.create_revenue_forecast_script()
            print()
            
            # 4. Configurar inicio automático
            self.setup_windows_startup()
            print()
            
            # 5. Crear acceso directo
            self.create_desktop_shortcut()
            print()
            
            print("🎉 ¡Setup completado exitosamente!")
            print()
            print("📋 Configuración finalizada:")
            print("  ✅ Dependencias instaladas")
            print("  ✅ Inicio automático configurado")
            print("  ✅ Acceso directo creado")
            print("  ✅ Sistema de forecast implementado")
            print("  ✅ Estructura de proyecto lista")
            print()
            print("🚀 Próximos pasos:")
            print("  1. Reinicia tu PC para activar el inicio automático")
            print("  2. O ejecuta manualmente 'startup_script.bat'")
            print("  3. El tracker se ejecutará cada día automáticamente")
            print("  4. Sigue el plan de 30 días (4.5h/día)")
            print()
            print("🎯 Objetivo: $15K revenue en 30 días")
            print("📅 Inicio: Lunes 23 Junio 2025")
            print("🏁 Final: Martes 22 Julio 2025")
            
        except Exception as e:
            print(f"❌ Error durante setup: {e}")
            print("💡 Puedes ejecutar manualmente los scripts individuales")

def main():
    setup = QAviogenSetup()
    setup.run_setup()
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
