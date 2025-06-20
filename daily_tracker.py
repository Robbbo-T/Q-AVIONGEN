#!/usr/bin/env python3
"""
Q-AVIOGEN Daily Progress Tracker
Inicio automático para seguimiento del plan de 30 días
Fecha inicio: 20 Junio 2025 (próximo día hábil: 23 Junio)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Rich para UI bonita
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TaskID
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.align import Align
except ImportError:
    print("Instalando rich para UI...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TaskID
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.align import Align

console = Console()

class QAviogenTracker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / "tracker_config.json"
        self.start_date = datetime(2025, 6, 23)  # Lunes 23 junio
        self.daily_hours = 4.5
        
        # Plan de 30 días detallado
        self.phases = [
            {
                "name": "🏗️ Infraestructura Mínima",
                "days": 4,
                "tasks": [
                    "Docker container + Dockerfile",
                    "API REST básico con FastAPI",
                    "Stripe/PayPal setup + facturación",
                    "Deploy en Azure/AWS básico"
                ],
                "deliverable": "MVP desplegable en cloud",
                "revenue_impact": 0
            },
            {
                "name": "📚 Documentación Marketplace",
                "days": 3,
                "tasks": [
                    "Azure Marketplace docs completas",
                    "AWS Marketplace assets",
                    "Configuración fiscal y legal (IVA, facturas)",
                    "Landing page básico"
                ],
                "deliverable": "Assets + setup legal listos",
                "revenue_impact": 0
            },
            {
                "name": "🎭 Avatar y Voz Final",
                "days": 4,
                "tasks": [
                    "Avatar profesional + animaciones",
                    "Voz ElevenLabs optimizada",
                    "Sistema de branding consistente",
                    "Templates de video mejorados"
                ],
                "deliverable": "Calidad broadcast lista",
                "revenue_impact": 500
            },
            {
                "name": "🎬 Generación de Demos",
                "days": 4,
                "tasks": [
                    "Demo completo procedimiento ATA",
                    "Video comercial 2 minutos",
                    "Screenshots para marketing",
                    "Case study documentado"
                ],
                "deliverable": "Material de ventas profesional",
                "revenue_impact": 1500  # Más realista para demos
            },
            {
                "name": "☁️ Azure Marketplace",
                "days": 5,
                "tasks": [
                    "Registro Azure Partner Center",
                    "Submission completa de aplicación",
                    "Proceso de validación",
                    "Configuración de billing",
                    "Go-live en Azure Marketplace"
                ],
                "deliverable": "Listado activo en Azure",
                "revenue_impact": 5000  # Azure es el más lucrativo
            },
            {
                "name": "🔶 AWS Marketplace", 
                "days": 3,
                "tasks": [
                    "AWS Partner registration",
                    "AMI/Container preparation",
                    "Listing submission"
                ],
                "deliverable": "Listado activo en AWS",
                "revenue_impact": 3000  # AWS también premium
            },
            {
                "name": "🔵 GCP Marketplace",
                "days": 3,
                "tasks": [
                    "Google Cloud Partner setup",
                    "Application submission",
                    "Technical validation"
                ],
                "deliverable": "Listado activo en GCP",
                "revenue_impact": 2000  # GCP menor penetración aeroespacial
            },
            {
                "name": "🌐 Landing Público + CRM",
                "days": 4,
                "tasks": [
                    "Website público profesional",
                    "CRM básico (HubSpot/Pipedrive)",
                    "Analytics y tracking",
                    "Lead capture optimizado"
                ],
                "deliverable": "Funnel de ventas activo",
                "revenue_impact": 2500  # CRM aumenta conversiones
            },
            {
                "name": "📊 Demo Comercial",
                "days": 2,
                "tasks": [
                    "PDF comercial profesional",
                    "PowerPoint para presentaciones"
                ],
                "deliverable": "Sales deck completo",
                "revenue_impact": 1000
            },
            {
                "name": "🚀 Test Final",
                "days": 2,
                "tasks": [
                    "Test completo end-to-end",
                    "Launch checklist validation"
                ],
                "deliverable": "Sistema 100% funcional",
                "revenue_impact": 5000
            }
        ]
        
        self.load_config()
    
    def load_config(self):
        """Cargar configuración y progreso"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self.create_initial_config()
            self.save_config()
    
    def save_config(self):
        """Guardar configuración y progreso"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False, default=str)
    
    def create_initial_config(self):
        """Crear configuración inicial del plan"""
        config = {
            "project_name": "Q-AVIOGEN",
            "start_date": self.start_date.isoformat(),
            "daily_hours": self.daily_hours,
            "total_days": 30,
            "current_day": 0,
            "total_revenue": 0,
            "schedule": [],
            "completed_tasks": [],
            "notes": {}
        }
        
        # Generar schedule día por día
        current_date = self.start_date
        task_index = 0
        day_in_phase = 0
        
        for day in range(30):
            current_phase = self.phases[task_index]
            
            schedule_item = {
                "day": day + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "weekday": current_date.strftime("%A"),
                "phase": current_phase["name"],
                "task": current_phase["tasks"][min(day_in_phase, len(current_phase["tasks"]) - 1)],
                "hours": self.daily_hours,
                "completed": False,
                "revenue_target": current_phase["revenue_impact"] / current_phase["days"],
                "deliverable": current_phase["deliverable"] if day_in_phase == current_phase["days"] - 1 else None
            }
            
            config["schedule"].append(schedule_item)
            
            current_date += timedelta(days=1)
            day_in_phase += 1
            
            if day_in_phase >= current_phase["days"] and task_index < len(self.phases) - 1:
                task_index += 1
                day_in_phase = 0
        
        return config
    
    def get_today_task(self):
        """Obtener la tarea de hoy"""
        today = datetime.now().date()
        
        for item in self.config["schedule"]:
            item_date = datetime.fromisoformat(item["date"]).date()
            if item_date == today:
                return item
        
        return None
    
    def display_daily_dashboard(self):
        """Mostrar dashboard principal del día"""
        today_task = self.get_today_task()
        
        if not today_task:
            console.print("🏁 [bold green]¡Plan de 30 días completado![/bold green]")
            return
        
        # Header
        layout = Layout()
        
        # Crear tabla de progreso general
        progress_table = Table(title="📊 Q-AVIOGEN - Progreso General")
        progress_table.add_column("Métrica", style="cyan")
        progress_table.add_column("Valor", style="green")
        
        completed_days = sum(1 for item in self.config["schedule"] if item["completed"])
        total_revenue = sum(item.get("revenue_target", 0) for item in self.config["schedule"] if item["completed"])
        
        progress_table.add_row("Días completados", f"{completed_days}/30")
        progress_table.add_row("Progreso", f"{completed_days/30*100:.1f}%")
        progress_table.add_row("Revenue generado", f"${total_revenue:,.0f}")
        progress_table.add_row("Horas invertidas", f"{completed_days * self.daily_hours:.1f}h")
        
        # Tarea de hoy
        today_panel = Panel(
            f"""
[bold blue]📅 {today_task['date']} - {today_task['weekday']}[/bold blue]
[bold yellow]🎯 Fase:[/bold yellow] {today_task['phase']}

[bold green]📋 Tarea de hoy ({today_task['hours']}h):[/bold green]
{today_task['task']}

[bold cyan]💰 Revenue target:[/bold cyan] ${today_task['revenue_target']:.0f}
[bold magenta]🎁 Deliverable:[/bold magenta] {today_task.get('deliverable', 'Progreso en fase')}
            """,
            title=f"🚀 DÍA {today_task['day']}/30",
            border_style="blue"
        )
        
        console.print(progress_table)
        console.print()
        console.print(today_panel)
        
        return today_task
    
    def mark_day_completed(self, day_item, notes=""):
        """Marcar día como completado"""
        for item in self.config["schedule"]:
            if item["day"] == day_item["day"]:
                item["completed"] = True
                if notes:
                    self.config["notes"][str(day_item["day"])] = notes
                break
        
        self.config["total_revenue"] += day_item.get("revenue_target", 0)
        self.save_config()
        
        console.print(f"✅ [bold green]Día {day_item['day']} marcado como completado![/bold green]")
        
        if day_item.get("deliverable"):
            console.print(f"🎁 [bold yellow]Deliverable alcanzado: {day_item['deliverable']}[/bold yellow]")
    
    def show_weekly_forecast(self):
        """Mostrar forecast semanal"""
        console.print("\n📈 [bold blue]Forecast Semanal de Revenue[/bold blue]")
        
        weeks = [
            {"name": "Semana 1 (Jun 23-29)", "days": list(range(1, 8)), "target": 0},
            {"name": "Semana 2 (Jun 30-Jul 6)", "days": list(range(8, 15)), "target": 0},
            {"name": "Semana 3 (Jul 7-13)", "days": list(range(15, 22)), "target": 1500},
            {"name": "Semana 4 (Jul 14-20)", "days": list(range(22, 29)), "target": 5000},
            {"name": "Semana 5 (Jul 21-22)", "days": list(range(29, 31)), "target": 8500}
        ]
        
        forecast_table = Table()
        forecast_table.add_column("Semana", style="cyan")
        forecast_table.add_column("Revenue Target", style="green")
        forecast_table.add_column("Estado", style="yellow")
        
        for week in weeks:
            completed_in_week = sum(1 for day in week["days"] 
                                  if day <= len(self.config["schedule"]) and 
                                  self.config["schedule"][day-1]["completed"])
            
            status = f"{completed_in_week}/{len(week['days'])} días"
            forecast_table.add_row(week["name"], f"${week['target']:,}", status)
        
        console.print(forecast_table)
    
    def show_phase_status(self):
        """Mostrar estado de todas las fases"""
        console.print("\n🏗️ [bold blue]Estado de Fases[/bold blue]")
        
        phase_table = Table()
        phase_table.add_column("Fase", style="cyan")
        phase_table.add_column("Progreso", style="green")
        phase_table.add_column("Revenue", style="yellow")
        phase_table.add_column("Deliverable", style="magenta")
        
        current_day = 1
        for phase in self.phases:
            completed_days = 0
            for day in range(current_day, current_day + phase["days"]):
                if day <= len(self.config["schedule"]) and self.config["schedule"][day-1]["completed"]:
                    completed_days += 1
            
            progress = f"{completed_days}/{phase['days']}"
            revenue = f"${phase['revenue_impact']:,}"
            
            phase_table.add_row(
                phase["name"], 
                progress, 
                revenue, 
                phase["deliverable"]
            )
            
            current_day += phase["days"]
        
        console.print(phase_table)
    
    def run_daily_check(self):
        """Ejecutar check diario completo"""
        console.clear()
        
        # Banner principal
        banner = Text("Q-AVIOGEN DAILY TRACKER", style="bold blue")
        console.print(Panel(Align.center(banner), border_style="blue"))
        
        # Dashboard principal
        today_task = self.display_daily_dashboard()
        
        if not today_task:
            return
        
        console.print()
        
        # Preguntar si la tarea está completada
        if not today_task["completed"]:
            completed = Confirm.ask(f"¿Has completado la tarea de hoy ({today_task['hours']}h)?")
            
            if completed:
                notes = Prompt.ask("Notas del día (opcional)", default="")
                self.mark_day_completed(today_task, notes)
                console.print()
        else:
            console.print("✅ [bold green]Tarea de hoy ya completada[/bold green]")
            console.print()
        
        # Mostrar forecasts
        self.show_weekly_forecast()
        console.print()
        self.show_phase_status()
        
        # Mensaje motivacional
        completed_days = sum(1 for item in self.config["schedule"] if item["completed"])
        remaining_days = 30 - completed_days
        
        if remaining_days > 0:
            console.print(f"\n🎯 [bold yellow]{remaining_days} días restantes para $15K en revenue![/bold yellow]")
            console.print("💪 [bold green]¡$15K el primer mes sería un resultado excelente![/bold green]")
            console.print("🚀 [bold cyan]Sector aeroespacial + herramienta única = oportunidad dorada[/bold cyan]")
        else:
            console.print("\n🏆 [bold green]¡FELICITACIONES! Plan de 30 días completado exitosamente.[/bold green]")
            console.print("🚀 [bold blue]Q-AVIOGEN debería estar generando $15K/mes![/bold blue]")
            console.print("💰 [bold yellow]¡Nada mal para el primer mes de un negocio![/bold yellow]")

def main():
    """Función principal"""
    try:
        tracker = QAviogenTracker()
        tracker.run_daily_check()
        
        # Mantener ventana abierta
        console.print("\n[dim]Presiona Enter para cerrar...[/dim]")
        input()
        
    except KeyboardInterrupt:
        console.print("\n👋 [yellow]¡Hasta mañana![/yellow]")
    except Exception as e:
        console.print(f"\n❌ [red]Error: {e}[/red]")
        console.print("[dim]Presiona Enter para cerrar...[/dim]")
        input()

if __name__ == "__main__":
    main()
