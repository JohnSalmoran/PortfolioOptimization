#!/bin/bash
# Script de instalación rápida para Portfolio Analyzer Pro
# Para macOS/Linux

echo ""
echo "================================"
echo "Portfolio Analyzer Pro - Setup"
echo "================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python no está instalado"
    echo "Descarga desde: https://www.python.org"
    exit 1
fi

echo "[OK] Python detectado"
python3 --version
echo ""

# Crear entorno virtual
echo "[1/4] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo crear el entorno virtual"
    exit 1
fi
echo "[OK] Entorno virtual creado"

echo ""
echo "[2/4] Activando entorno virtual..."
source venv/bin/activate
echo "[OK] Entorno virtual activado"

echo ""
echo "[3/4] Instalando dependencias..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Hubo un error instalando las dependencias"
    exit 1
fi
echo "[OK] Dependencias instaladas"

echo ""
echo "[4/4] Listo!"
echo ""
echo "================================"
echo "Para ejecutar la aplicación:"
echo ""
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "La aplicación se abrirá en:"
echo "  http://localhost:8501"
echo "================================"
echo ""
