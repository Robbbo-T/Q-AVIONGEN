@echo off
REM Q-AVIOGEN Daily Startup Script
REM Se ejecuta automáticamente al iniciar Windows
REM Configurado para el plan de 30 días (23 Jun - 22 Jul 2025)

title Q-AVIOGEN Daily Tracker

echo.
echo ========================================
echo   Q-AVIOGEN DAILY TRACKER
echo   Plan de 30 días - Comercialización
echo ========================================
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\Users\amate\OneDrive\Structured\Q-AVIONGEN"

REM Verificar que Python está disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Instalando Python...
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar que rich está instalado
python -c "import rich" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando dependencias...
    pip install rich
)

REM Ejecutar el tracker diario
echo 🚀 Iniciando Q-AVIOGEN Daily Tracker...
echo.
python daily_tracker.py

REM Mantener ventana abierta si hay error
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error al ejecutar el tracker
    pause
)

exit /b 0
