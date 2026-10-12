@echo off
chcp 65001 >nul
set PATH=C:\Program Files\nodejs;C:\Users\herri\AppData\Roaming\npm;C:\Users\herri\AppData\Local\Programs\Git\cmd;%PATH%
cd /d "%~dp0"
echo ========================================================
echo   Sincronizando NutriChef con GitHub y Render
echo ========================================================
echo.
git push origin main
echo.
echo ========================================================
echo   [OK] Codigo subido a GitHub con exito!
echo   Render se actualizara automaticamente en 1 minuto.
echo ========================================================
pause
