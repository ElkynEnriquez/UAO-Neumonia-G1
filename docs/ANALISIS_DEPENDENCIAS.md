# Análisis de Dependencias - requirements.txt y pyproject.toml

**Fecha:** 31 de enero de 2026

---

## 📊 Dependencias Usadas en el Código

### ✅ Dependencias Necesarias (Confirmadas)

| Paquete | Uso en Código | En requirements.txt | Estado |
|---------|---------------|---------------------|--------|
| `tensorflow` | `src/models/load_model.py` | ✅ Sí | ✅ Correcto |
| `numpy` | `src/services/*.py` | ❌ No | ⚠️ **FALTA** |
| `opencv-python` | `src/services/*.py` | ✅ Sí (como `opencv_python`) | ✅ Correcto |
| `pydicom` | `src/services/read_img.py` | ✅ Sí | ✅ Correcto |
| `pillow` | `src/services/read_img.py`, `src/views/detector_neumonia.py` | ✅ Sí | ✅ Correcto |
| `tkcap` | `src/views/detector_neumonia.py` | ✅ Sí | ✅ Correcto |
| `img2pdf` | `src/views/detector_neumonia.py` | ✅ Sí | ✅ Correcto |
| `tkinter` | `src/views/detector_neumonia.py` | ❌ No (built-in) | ✅ No necesario |

### ❌ Dependencias NO Usadas (Innecesarias)

| Paquete | En requirements.txt | Razón |
|---------|---------------------|-------|
| `pyautogui` | ✅ Sí | ❌ No se usa en ningún archivo |
| `matplotlib` | ✅ Sí | ❌ No se usa en ningún archivo |
| `pandas` | ✅ Sí | ❌ No se usa en ningún archivo |
| `python-xlib` | ✅ Sí | ❌ Solo para Linux, causa problemas en Windows |

---

## ⚠️ Problemas Detectados

### 1. **Falta `numpy` explícitamente**
- **Problema:** `numpy` se usa extensivamente pero no está en `requirements.txt`
- **Impacto:** Aunque viene con TensorFlow, es buena práctica declararlo explícitamente
- **Solución:** Agregar `numpy` con versión específica

### 2. **Dependencias innecesarias**
- **Problema:** `pyautogui`, `matplotlib`, `pandas` no se usan
- **Impacto:** Instalación más lenta, posibles conflictos
- **Solución:** Eliminar del `requirements.txt`

### 3. **`python-xlib` problemático**
- **Problema:** Específico de Linux, causa errores en Windows
- **Impacto:** Puede fallar la instalación en Windows
- **Solución:** Eliminar o hacer condicional

### 4. **Faltan versiones específicas**
- **Problema:** Sin versiones, pueden surgir incompatibilidades
- **Impacto:** Diferentes versiones pueden causar errores
- **Solución:** Agregar versiones mínimas compatibles

### 5. **`pyproject.toml` desincronizado**
- **Problema:** `dependencies = []` vacío aunque existe `requirements.txt`
- **Impacto:** Inconsistencia en gestión de dependencias
- **Solución:** Sincronizar o elegir un solo método

---

## ✅ Solución Propuesta

### `requirements.txt` Corregido

```txt
# Core dependencies
numpy>=1.21.0
tensorflow>=2.10.0

# Image processing
opencv-python>=4.5.0
pillow>=9.0.0
pydicom>=2.3.0

# GUI and utilities
tkcap>=1.0.0
img2pdf>=0.4.0

# Optional: python-xlib (solo para Linux)
# python-xlib>=0.33; sys_platform == "linux"
```

### `pyproject.toml` Corregido

```toml
[project]
name = "uao-neumonia-g2"
version = "0.1.0"
description = "Herramienta para la detección rápida de neumonía mediante Deep Learning"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "numpy>=1.21.0",
    "tensorflow>=2.10.0",
    "opencv-python>=4.5.0",
    "pillow>=9.0.0",
    "pydicom>=2.3.0",
    "tkcap>=1.0.0",
    "img2pdf>=0.4.0",
]
```

---

## 📋 Resumen

### Estado Actual
- ✅ **7 dependencias correctas** de 11
- ❌ **4 dependencias innecesarias** o problemáticas
- ⚠️ **1 dependencia faltante** (`numpy`)
- ⚠️ **Sin versiones especificadas**

### Estado Propuesto
- ✅ **7 dependencias necesarias** (todas correctas)
- ✅ **Versiones especificadas** (compatibilidad garantizada)
- ✅ **Sin dependencias innecesarias**
- ✅ **`pyproject.toml` sincronizado**

---

## 🎯 Recomendación

**Usar `requirements.txt` como fuente principal** y mantener `pyproject.toml` sincronizado, o **usar solo `pyproject.toml`** (más moderno).

**Ventajas de usar solo `pyproject.toml`:**
- Estándar moderno de Python (PEP 621)
- Mejor integración con herramientas modernas
- Un solo archivo para gestionar

**Ventajas de usar `requirements.txt`:**
- Más familiar para la mayoría
- Compatible con más herramientas legacy

---

**¿Aplico las correcciones?**
