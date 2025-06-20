@echo off
cd /d "c:\Users\amate\OneDrive\Structured\Q-AVIONGEN"
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo Ejecutando debug_main.py...
python debug_main.py
pause
