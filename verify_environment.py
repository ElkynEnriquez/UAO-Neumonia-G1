#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de verificación de ambiente y ejecución de pruebas
Verifica que todas las dependencias estén instaladas correctamente
"""

import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Verifica versión de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 8


def check_module(module_name, import_name=None):
    """Verifica si un módulo está instalado"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"✓ {module_name}")
        return True
    except ImportError:
        print(f"✗ {module_name} - NO INSTALADO")
        return False


def check_all_modules():
    """Verifica todas las dependencias requeridas"""
    print("\n📦 Verificando dependencias...")
    
    modules = [
        ("numpy", "numpy"),
        ("TensorFlow", "tensorflow"),
        ("OpenCV", "cv2"),
        ("Pillow", "PIL"),
        ("pydicom", "pydicom"),
        ("ReportLab", "reportlab"),
        ("Tkinter", "tkinter"),
    ]
    
    results = []
    for module_name, import_name in modules:
        results.append(check_module(module_name, import_name))
    
    return all(results)


def check_data_files():
    """Verifica que existan archivos de datos"""
    print("\n📁 Verificando archivos de datos...")
    
    files = [
        "data/DICOM/viral-2.dcm",
        "data/models/conv_MLP_84.h5",
    ]
    
    all_exist = True
    for filepath in files:
        if Path(filepath).exists():
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - NO ENCONTRADO")
            all_exist = False
    
    return all_exist


def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 50)
    print("VERIFICACIÓN DE AMBIENTE")
    print("=" * 50)
    
    # Verificar Python
    print("\n🐍 Versión Python:")
    check_python_version()
    
    # Verificar módulos
    modules_ok = check_all_modules()
    
    # Verificar archivos
    files_ok = check_data_files()
    
    # Resumen
    print("\n" + "=" * 50)
    if modules_ok and files_ok:
        print("✅ TODO OK - Listo para ejecutar")
        print("\nEjemplos:")
        print("  python cli.py --input data/DICOM/viral-2.dcm --patient-id 123")
        print("  python main.py  (GUI)")
        print("  docker-compose up --build")
        return 0
    else:
        print("❌ Hay problemas - Necesita correcciones")
        if not modules_ok:
            print("\n  Instale las dependencias:")
            print("  . .venv\\Scripts\\Activate.ps1")
            print("  uv pip install -r requirements.txt")
        if not files_ok:
            print("\n  Descargue los archivos faltantes")
        return 1


if __name__ == "__main__":
    sys.exit(main())
