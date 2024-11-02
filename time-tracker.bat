@echo off
REM Cambiar directorio a donde está el script
cd /d "%~dp0"

REM Verificar e instalar pandas y openpyxl si no están presentes
python -m pip show pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando pandas...
    python -m pip install pandas
)

python -m pip show openpyxl >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando openpyxl...
    python -m pip install openpyxl
)

REM Ejecutar el script de Python
python time_tracker.py
