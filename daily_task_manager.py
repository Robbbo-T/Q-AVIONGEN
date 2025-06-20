#!/usr/bin/env python3
"""
Q-AVIOGEN Daily Task Manager
Sistema de seguimiento automático del plan de 30 días
Inicio: 20 de junio 2025
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import pandas as pd

@dataclass
class DailyTask:
    date: str
    task: str
    hours: float
    completed: bool = False
    actual_hours: float = 0.0
    notes: str = ""
    priority: int = 1  # 1=Alta, 2=Media, 3=Baja

class QAviogenTaskManager:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.data_file = self.base_path / "task_progress.json"
        self.config_file = self.base_path / "config.json"
        self.start_date = datetime(2025, 6, 20).date()
        
        # Configuración de fases del proyecto
        self.phases = [
            ("Infraestructura mínima (Docker + API)", 4, ["Docker setup", "API básica", "Base de datos", "Tests iniciales"]),
            ("Documentación Marketplace + Web", 3, ["Docs Azure", "Docs AWS", "Landing page"]),
            ("Avatar y voz final", 4, ["Avatar 3D", "Sistema TTS", "Integración", "Tests de calidad"]),
            ("Generación de demos", 4, ["Videos demo", "Screenshots", "Casos de uso", "Material marketing"]),
            ("Azure listing (registro y validación)", 5, ["Registro Azure", "Documentación", "Validación", "Certificación", "Publicación"]),
            ("AWS listing", 3, ["Registro AWS", "AMI creation", "Marketplace listing"]),
            ("GCP listing", 3, ["Registro GCP", "Container images", "Marketplace listing"]),
            ("Landing pública + CRM básico", 4, ["Landing final", "CRM setup", "Analytics", "Testing"]),
            ("Demo comercial PDF + PPT", 2, ["Pitch deck", "Demo PDF"]),
            ("Test final full pipeline", 2, ["Testing completo", "Validación final"])
        ]
        
        self.daily_hours = 4.5
        self.initialize_tasks()
        
    def initialize_tasks(self):
        """Inicializa las tareas diarias basadas en las fases"""
        if self.data_file.exists():
            self.load_progress()
        else:
            self.create_initial_schedule()
            self.save_progress()
    
    def create_initial_schedule(self):
        """Crea el cronograma inicial de 30 días"""
        self.tasks = []
        current_day = self.start_date
        task_index = 0
        hours_remaining = self.phases[task_index][1] * self.daily_hours
        task_name = self.phases[task_index][0]
        subtasks = self.phases[task_index][2]
        subtask_index = 0
        
        for day in range(30):
            daily_task = f"{task_name}"
            if subtasks and subtask_index < len(subtasks):
                daily_task += f" - {subtasks[subtask_index]}"
            
            task = DailyTask(
                date=current_day.strftime("%Y-%m-%d"),
                task=daily_task,
                hours=min(self.daily_hours, hours_remaining),
                priority=1 if hours_remaining > self.daily_hours else 2
            )
            
            self.tasks.append(task)
            current_day += timedelta(days=1)
            hours_remaining -= self.daily_hours
            
            # Avanzar subtarea cada día
            if subtasks:
                subtask_index = (subtask_index + 1) % len(subtasks)
            
            # Cambiar a siguiente fase si es necesario
            if hours_remaining <= 0 and task_index + 1 < len(self.phases):
                task_index += 1
                task_name = self.phases[task_index][0]
                subtasks = self.phases[task_index][2]
                subtask_index = 0
                hours_remaining = self.phases[task_index][1] * self.daily_hours
    
    def load_progress(self):
        """Carga el progreso desde archivo JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [DailyTask(**task) for task in data['tasks']]
        except Exception as e:
            print(f"Error cargando progreso: {e}")
            self.create_initial_schedule()
    
    def save_progress(self):
        """Guarda el progreso a archivo JSON"""
        try:
            data = {
                'tasks': [asdict(task) for task in self.tasks],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando progreso: {e}")
    
    def get_today_task(self) -> Optional[DailyTask]:
        """Obtiene la tarea de hoy"""
        today = datetime.now().date().strftime("%Y-%m-%d")
        for task in self.tasks:
            if task.date == today:
                return task
        return None
    
    def get_week_tasks(self) -> List[DailyTask]:
        """Obtiene las tareas de esta semana"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        week_tasks = []
        for task in self.tasks:
            task_date = datetime.strptime(task.date, "%Y-%m-%d").date()
            if week_start <= task_date <= week_end:
                week_tasks.append(task)
        return week_tasks
    
    def mark_completed(self, date: str, actual_hours: float = None, notes: str = ""):
        """Marca una tarea como completada"""
        for task in self.tasks:
            if task.date == date:
                task.completed = True
                if actual_hours:
                    task.actual_hours = actual_hours
                if notes:
                    task.notes = notes
                break
        self.save_progress()
    
    def get_progress_stats(self) -> Dict:
        """Calcula estadísticas de progreso"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        total_planned_hours = sum(task.hours for task in self.tasks)
        total_actual_hours = sum(task.actual_hours for task in self.tasks)
        
        # Calcular progreso por fase
        phase_progress = {}
        for phase_name, _, _ in self.phases:
            phase_tasks = [task for task in self.tasks if phase_name in task.task]
            if phase_tasks:
                completed = sum(1 for task in phase_tasks if task.completed)
                total = len(phase_tasks)
                phase_progress[phase_name] = {
                    'completed': completed,
                    'total': total,
                    'percentage': (completed / total) * 100 if total > 0 else 0
                }
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_percentage': (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
            'total_planned_hours': total_planned_hours,
            'total_actual_hours': total_actual_hours,
            'efficiency': (total_planned_hours / total_actual_hours) * 100 if total_actual_hours > 0 else 100,
            'phase_progress': phase_progress
        }

class DailyTaskGUI:
    def __init__(self, task_manager: QAviogenTaskManager):
        self.task_manager = task_manager
        self.root = tk.Tk()
        self.root.title("Q-AVIOGEN - Plan Diario")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.setup_gui()
        
    def configure_styles(self):
        """Configura los estilos del GUI"""
        self.style.configure('Title.TLabel', 
                           font=('Arial', 16, 'bold'),
                           background='#1e1e1e',
                           foreground='#00d4ff')
        
        self.style.configure('Subtitle.TLabel',
                           font=('Arial', 12, 'bold'),
                           background='#1e1e1e',
                           foreground='#ffffff')
        
        self.style.configure('Task.TLabel',
                           font=('Arial', 10),
                           background='#1e1e1e',
                           foreground='#cccccc')
    
    def setup_gui(self):
        """Configura la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="Q-AVIOGEN - Plan de Desarrollo 30 Días",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Fecha actual
        today = datetime.now().strftime("%A %d de %B, %Y")
        date_label = ttk.Label(main_frame, 
                              text=f"Hoy: {today}",
                              style='Subtitle.TLabel')
        date_label.pack(pady=(0, 10))
        
        # Tarea de hoy
        self.setup_today_task(main_frame)
        
        # Progreso general
        self.setup_progress_section(main_frame)
        
        # Tareas de la semana
        self.setup_week_tasks(main_frame)
        
        # Botones de acción
        self.setup_action_buttons(main_frame)
    
    def setup_today_task(self, parent):
        """Configura la sección de tarea de hoy"""
        today_frame = ttk.LabelFrame(parent, text="Tarea de Hoy", padding=15)
        today_frame.pack(fill=tk.X, pady=(0, 20))
        
        today_task = self.task_manager.get_today_task()
        
        if today_task:
            # Mostrar tarea
            task_text = f"📋 {today_task.task}"
            if today_task.completed:
                task_text += " ✅"
            
            task_label = ttk.Label(today_frame, text=task_text, style='Task.TLabel')
            task_label.pack(anchor=tk.W, pady=(0, 5))
            
            # Horas planificadas
            hours_label = ttk.Label(today_frame, 
                                   text=f"⏰ Horas planificadas: {today_task.hours}h",
                                   style='Task.TLabel')
            hours_label.pack(anchor=tk.W, pady=(0, 5))
            
            # Frame para marcar como completado
            if not today_task.completed:
                complete_frame = ttk.Frame(today_frame)
                complete_frame.pack(fill=tk.X, pady=(10, 0))
                
                ttk.Label(complete_frame, text="Horas trabajadas:").pack(side=tk.LEFT)
                self.hours_var = tk.StringVar(value=str(today_task.hours))
                hours_entry = ttk.Entry(complete_frame, textvariable=self.hours_var, width=5)
                hours_entry.pack(side=tk.LEFT, padx=(5, 10))
                
                complete_btn = ttk.Button(complete_frame, 
                                        text="Marcar Completado",
                                        command=self.mark_today_completed)
                complete_btn.pack(side=tk.LEFT)
            else:
                status_label = ttk.Label(today_frame, 
                                       text=f"✅ Completado - {today_task.actual_hours}h trabajadas",
                                       style='Subtitle.TLabel')
                status_label.pack(anchor=tk.W, pady=(10, 0))
        else:
            no_task_label = ttk.Label(today_frame, 
                                    text="No hay tareas programadas para hoy",
                                    style='Task.TLabel')
            no_task_label.pack()
    
    def setup_progress_section(self, parent):
        """Configura la sección de progreso"""
        progress_frame = ttk.LabelFrame(parent, text="Progreso General", padding=15)
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats = self.task_manager.get_progress_stats()
        
        # Barra de progreso
        progress_label = ttk.Label(progress_frame, 
                                 text=f"Progreso: {stats['completed_tasks']}/{stats['total_tasks']} tareas ({stats['completion_percentage']:.1f}%)")
        progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        progress_bar = ttk.Progressbar(progress_frame, 
                                     length=300, 
                                     mode='determinate')
        progress_bar['value'] = stats['completion_percentage']
        progress_bar.pack(anchor=tk.W, pady=(0, 10))
        
        # Estadísticas de horas
        hours_label = ttk.Label(progress_frame,
                              text=f"Horas: {stats['total_actual_hours']:.1f}h trabajadas de {stats['total_planned_hours']:.1f}h planificadas")
        hours_label.pack(anchor=tk.W)
    
    def setup_week_tasks(self, parent):
        """Configura la sección de tareas de la semana"""
        week_frame = ttk.LabelFrame(parent, text="Tareas de Esta Semana", padding=15)
        week_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Crear Treeview para mostrar tareas
        columns = ('Fecha', 'Tarea', 'Horas', 'Estado')
        tree = ttk.Treeview(week_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(week_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Llenar con datos
        week_tasks = self.task_manager.get_week_tasks()
        for task in week_tasks:
            status = "✅ Completado" if task.completed else "⏳ Pendiente"
            tree.insert('', tk.END, values=(
                task.date,
                task.task[:50] + "..." if len(task.task) > 50 else task.task,
                f"{task.hours}h",
                status
            ))
    
    def setup_action_buttons(self, parent):
        """Configura los botones de acción"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        # Botón para ver forecast
        forecast_btn = ttk.Button(button_frame, 
                                text="Ver Forecast de Ingresos",
                                command=self.show_revenue_forecast)
        forecast_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para ver progreso detallado
        progress_btn = ttk.Button(button_frame,
                                text="Progreso Detallado",
                                command=self.show_detailed_progress)
        progress_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para cerrar
        close_btn = ttk.Button(button_frame,
                             text="Cerrar",
                             command=self.root.quit)
        close_btn.pack(side=tk.RIGHT)
    
    def mark_today_completed(self):
        """Marca la tarea de hoy como completada"""
        try:
            hours = float(self.hours_var.get())
            today = datetime.now().date().strftime("%Y-%m-%d")
            self.task_manager.mark_completed(today, hours)
            messagebox.showinfo("Éxito", "Tarea marcada como completada!")
            self.root.quit()
            self.root.destroy()
            # Reabrir ventana actualizada
            DailyTaskGUI(self.task_manager).run()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido de horas")
    
    def show_revenue_forecast(self):
        """Muestra el forecast de ingresos"""
        RevenueFrecastWindow(self.task_manager)
    
    def show_detailed_progress(self):
        """Muestra el progreso detallado"""
        DetailedProgressWindow(self.task_manager)
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

class RevenueFrecastWindow:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.window = tk.Toplevel()
        self.window.title("Forecast de Ingresos - Q-AVIOGEN")
        self.window.geometry("900x700")
        self.window.configure(bg='#1e1e1e')
        
        self.setup_forecast_gui()
    
    def setup_forecast_gui(self):
        """Configura la GUI del forecast"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = ttk.Label(main_frame, 
                         text="Forecast de Ingresos Q-AVIOGEN",
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        # Crear forecast data
        forecast_data = self.generate_revenue_forecast()
        
        # Mostrar tabla de forecast
        self.create_forecast_table(main_frame, forecast_data)
        
        # Crear gráfico
        self.create_revenue_chart(main_frame, forecast_data)
    
    def generate_revenue_forecast(self):
        """Genera el forecast de ingresos basado en el progreso"""
        stats = self.task_manager.get_progress_stats()
        
        # Milestones de ingresos basados en fases completadas
        milestones = {
            "Infraestructura mínima (Docker + API)": {
                "month": 1,
                "revenue": 5000,
                "customers": 20,
                "description": "MVP listo, primeros beta users"
            },
            "Documentación Marketplace + Web": {
                "month": 1.5,
                "revenue": 15000,
                "customers": 50,
                "description": "Landing profesional, marketing activo"
            },
            "Avatar y voz final": {
                "month": 2,
                "revenue": 35000,
                "customers": 120,
                "description": "Producto diferenciado, demos impresionantes"
            },
            "Generación de demos": {
                "month": 2.5,
                "revenue": 65000,
                "customers": 200,
                "description": "Material comercial profesional"
            },
            "Azure listing (registro y validación)": {
                "month": 3,
                "revenue": 120000,
                "customers": 350,
                "description": "Marketplace Azure activo"
            },
            "AWS listing": {
                "month": 4,
                "revenue": 200000,
                "customers": 500,
                "description": "Doble marketplace exposure"
            },
            "GCP listing": {
                "month": 5,
                "revenue": 320000,
                "customers": 750,
                "description": "Triple marketplace presence"
            },
            "Landing pública + CRM básico": {
                "month": 6,
                "revenue": 500000,
                "customers": 1000,
                "description": "Máquina de ventas optimizada"
            }
        }
        
        # Calcular progreso actual
        current_month = 0
        current_revenue = 0
        
        for phase_name, milestone in milestones.items():
            if phase_name in stats['phase_progress']:
                phase_progress = stats['phase_progress'][phase_name]['percentage']
                if phase_progress >= 100:
                    current_month = milestone['month']
                    current_revenue = milestone['revenue']
        
        # Proyección mensual
        forecast = []
        for i in range(1, 13):  # 12 meses
            base_growth = 1.3  # 30% crecimiento mensual base
            
            if i <= current_month:
                # Usar datos reales hasta el progreso actual
                month_revenue = min(current_revenue, 500000)
            else:
                # Proyección basada en crecimiento
                if current_revenue > 0:
                    month_revenue = current_revenue * (base_growth ** (i - current_month))
                else:
                    month_revenue = 5000 * (base_growth ** (i - 1))
            
            # Limitar crecimiento máximo
            month_revenue = min(month_revenue, 2000000)  # Cap en $2M mensual
            
            forecast.append({
                'month': f"Mes {i}",
                'revenue': int(month_revenue),
                'customers': int(month_revenue / 150),  # $150 ARPU promedio
                'growth': 0 if i == 1 else int(((month_revenue / forecast[i-2]['revenue']) - 1) * 100) if i > 1 else 30
            })
        
        return forecast
    
    def create_forecast_table(self, parent, forecast_data):
        """Crea la tabla de forecast"""
        table_frame = ttk.LabelFrame(parent, text="Proyección Mensual", padding=15)
        table_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Crear Treeview
        columns = ('Mes', 'Ingresos ($)', 'Clientes', 'Crecimiento (%)')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        
        # Llenar datos
        for data in forecast_data[:6]:  # Mostrar solo primeros 6 meses
            tree.insert('', tk.END, values=(
                data['month'],
                f"${data['revenue']:,}",
                data['customers'],
                f"{data['growth']}%"
            ))
        
        tree.pack(fill=tk.X)
        
        # Resumen anual
        total_revenue = sum(data['revenue'] for data in forecast_data)
        summary_label = ttk.Label(table_frame,
                                text=f"Proyección Anual Total: ${total_revenue:,}",
                                font=('Arial', 12, 'bold'))
        summary_label.pack(pady=(10, 0))
    
    def create_revenue_chart(self, parent, forecast_data):
        """Crea el gráfico de ingresos"""
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        chart_frame = ttk.LabelFrame(parent, text="Gráfico de Crecimiento", padding=15)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), facecolor='#1e1e1e')
        
        months = [data['month'] for data in forecast_data[:6]]
        revenues = [data['revenue'] for data in forecast_data[:6]]
        customers = [data['customers'] for data in forecast_data[:6]]
        
        # Gráfico de ingresos
        ax1.plot(months, revenues, marker='o', color='#00d4ff', linewidth=2, markersize=6)
        ax1.set_title('Proyección de Ingresos Mensuales', color='white', fontsize=12)
        ax1.set_ylabel('Ingresos ($)', color='white')
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#2d2d2d')
        
        # Formatear y rotar etiquetas del eje x
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico de clientes
        ax2.bar(months, customers, color='#ff6b6b', alpha=0.7)
        ax2.set_title('Proyección de Clientes', color='white', fontsize=12)
        ax2.set_ylabel('Número de Clientes', color='white')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#2d2d2d')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class DetailedProgressWindow:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.window = tk.Toplevel()
        self.window.title("Progreso Detallado - Q-AVIOGEN")
        self.window.geometry("1000x600")
        self.window.configure(bg='#1e1e1e')
        
        self.setup_progress_gui()
    
    def setup_progress_gui(self):
        """Configura la GUI de progreso detallado"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = ttk.Label(main_frame,
                         text="Progreso Detallado por Fases",
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        # Crear notebook para las pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de progreso por fases
        self.create_phase_progress_tab(notebook)
        
        # Pestaña de todas las tareas
        self.create_all_tasks_tab(notebook)
    
    def create_phase_progress_tab(self, notebook):
        """Crea la pestaña de progreso por fases"""
        phase_frame = ttk.Frame(notebook)
        notebook.add(phase_frame, text="Progreso por Fases")
        
        stats = self.task_manager.get_progress_stats()
        
        for phase_name, progress_data in stats['phase_progress'].items():
            # Frame para cada fase
            phase_container = ttk.LabelFrame(phase_frame, text=phase_name, padding=10)
            phase_container.pack(fill=tk.X, pady=(0, 10))
            
            # Información de progreso
            progress_text = f"{progress_data['completed']}/{progress_data['total']} tareas completadas ({progress_data['percentage']:.1f}%)"
            progress_label = ttk.Label(phase_container, text=progress_text)
            progress_label.pack(anchor=tk.W)
            
            # Barra de progreso
            progress_bar = ttk.Progressbar(phase_container,
                                         length=400,
                                         mode='determinate')
            progress_bar['value'] = progress_data['percentage']
            progress_bar.pack(anchor=tk.W, pady=(5, 0))
    
    def create_all_tasks_tab(self, notebook):
        """Crea la pestaña con todas las tareas"""
        tasks_frame = ttk.Frame(notebook)
        notebook.add(tasks_frame, text="Todas las Tareas")
        
        # Crear Treeview
        columns = ('Fecha', 'Tarea', 'Horas Plan.', 'Horas Real.', 'Estado', 'Notas')
        tree = ttk.Treeview(tasks_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Tarea':
                tree.column(col, width=300)
            elif col == 'Notas':
                tree.column(col, width=200)
            else:
                tree.column(col, width=100)
        
        # Scrollbar
        scrollbar_v = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_h = ttk.Scrollbar(tasks_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Empaquetar
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        tasks_frame.grid_rowconfigure(0, weight=1)
        tasks_frame.grid_columnconfigure(0, weight=1)
        
        # Llenar con todas las tareas
        for task in self.task_manager.tasks:
            status = "✅ Completado" if task.completed else "⏳ Pendiente"
            tree.insert('', tk.END, values=(
                task.date,
                task.task,
                f"{task.hours}h",
                f"{task.actual_hours}h" if task.actual_hours > 0 else "",
                status,
                task.notes[:50] + "..." if len(task.notes) > 50 else task.notes
            ))

def create_startup_script():
    """Crea el script de inicio automático"""
    startup_content = f'''@echo off
cd /d "{Path(__file__).parent}"
python "{Path(__file__)}" --startup
'''
    
    startup_path = Path(__file__).parent / "startup_qaviongen.bat"
    with open(startup_path, 'w') as f:
        f.write(startup_content)
    
    print(f"Script de inicio creado en: {startup_path}")
    print("Para activar inicio automático, copia este archivo a:")
    print("Windows: %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Q-AVIOGEN Task Manager')
    parser.add_argument('--startup', action='store_true', 
                       help='Modo de inicio automático (muestra solo tarea del día)')
    
    args = parser.parse_args()
    
    # Crear manager de tareas
    task_manager = QAviogenTaskManager()
    
    if args.startup:
        # Modo startup: mostrar solo tarea del día
        today_task = task_manager.get_today_task()
        if today_task and not today_task.completed:
            # Mostrar notificación simple
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            
            message = f"🚀 Q-AVIOGEN - Tarea de Hoy\n\n📋 {today_task.task}\n⏰ {today_task.hours} horas planificadas"
            result = messagebox.askyesno("Q-AVIOGEN Daily Task", 
                                       f"{message}\n\n¿Abrir panel completo?")
            
            if result:
                root.destroy()
                DailyTaskGUI(task_manager).run()
            else:
                root.destroy()
        else:
            print("No hay tareas pendientes para hoy o ya están completadas.")
    else:
        # Modo normal: interfaz completa
        app = DailyTaskGUI(task_manager)
        app.run()

if __name__ == "__main__":
    # Crear script de inicio al ejecutar por primera vez
    create_startup_script()
    main()
