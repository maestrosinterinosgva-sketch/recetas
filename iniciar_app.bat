@echo off
chcp 65001 > nul
echo ===================================================
echo     NutriChef AI - Analizador & Comparador
echo ===================================================
echo Iniciando servidor en http://127.0.0.1:8000...
echo.

cd /d "%~dp0"
if exist "venv\Scripts\python.exe" (
    start "" cmd /c "timeout /t 2 /nobreak > nul & start http://127.0.0.1:8000"
    .\venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000
) else (
    echo [ERROR] No se encontró el entorno virtual 'venv'.
    echo Por favor asegúrate de ejecutar primero la instalación de dependencias.
    pause
)
