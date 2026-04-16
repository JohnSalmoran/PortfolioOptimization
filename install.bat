@echo off
REM Script de instalación rápida para Portfolio Analyzer Pro
REM Para Windows

cls
echo.
echo ================================
echo Portfolio Analyzer Pro - Setup
echo ================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en PATH
    echo Descarga Python desde: https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Crear entorno virtual
echo [1/4] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

echo.
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado

echo.
echo [3/4] Instalando dependencias...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Hubo un error instalando las dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas

echo.
echo [4/4] Listo!
echo.
echo ================================
echo Para ejecutar la aplicación:
echo.
echo   venv\Scripts\activate
echo   streamlit run app.py
echo.
echo La aplicación se abrirá en:
echo   http://localhost:8501
echo ================================
echo.
pause
