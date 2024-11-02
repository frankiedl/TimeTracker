@echo off
REM Change directory to where the script is located
cd /d "%~dp0"

REM Check and install pandas and openpyxl if they are not present
python -m pip show pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pandas...
    python -m pip install pandas
)

python -m pip show openpyxl >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing openpyxl...
    python -m pip install openpyxl
)

REM Run the Python script
python time_tracker.py
