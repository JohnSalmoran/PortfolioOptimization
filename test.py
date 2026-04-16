"""
test.py
Script para verificar que todo está funcionando
"""

import sys
import importlib

print("=" * 60)
print("VERIFICACIÓN DE INSTALACIÓN")
print("=" * 60)
print()

# Lista de paquetes a verificar
paquetes = [
    'streamlit',
    'pandas',
    'numpy',
    'yfinance',
    'scipy',
    'plotly',
    'openpyxl'
]

print("Verificando paquetes requeridos...\n")

todos_ok = True

for paquete in paquetes:
    try:
        mod = importlib.import_module(paquete)
        version = getattr(mod, '__version__', 'N/A')
        print(f"✅ {paquete:15} {version}")
    except ImportError:
        print(f"❌ {paquete:15} NO INSTALADO")
        todos_ok = False

print()

if todos_ok:
    print("=" * 60)
    print("✅ TODO OK - Puedes ejecutar: streamlit run app.py")
    print("=" * 60)
else:
    print("=" * 60)
    print("❌ Faltan paquetes - Ejecuta: pip install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)

print()

# Prueba de módulos locales
print("Verificando módulos locales...\n")

try:
    from modules import (
        descargar_datos,
        calcular_rendimientos,
        validar_datos,
        OptimizadorPortafolios
    )
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ INSTALACIÓN VERIFICADA")
print("=" * 60)
print()
print("Próximos pasos:")
print("1. Ejecuta: streamlit run app.py")
print("2. O ejecuta: python ejemplo_uso.py")
print()
