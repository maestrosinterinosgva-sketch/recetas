@echo off
chcp 65001 >nul
set PATH=C:\Program Files\nodejs;C:\Users\herri\AppData\Roaming\npm;C:\Users\herri\AppData\Local\Programs\Git\cmd;%PATH%
echo ========================================================
echo   Subir NutriChef AI a GitHub
echo ========================================================
echo.
set /p REPO_URL="Pega la URL de tu repositorio de GitHub (ej: https://github.com/usuario/recetas.git): "
if "%REPO_URL%"=="" (
    echo [ERROR] No has introducido ninguna URL. Cancelando.
    pause
    exit /b
)
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main
echo Subiendo codigo a GitHub...
git push -u origin main
echo.
echo ========================================================
echo   [OK] Codigo subido a GitHub con exito!
echo ========================================================
pause
