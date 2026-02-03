# Análisis de Dependencias - UAO-Neumonia-G2

**Fecha:** 31 de enero de 2026  
**Estado:** ✅ Actualizado y sincronizado

---

## 📊 Dependencias del Proyecto

### Dependencias Principales

| Paquete | Versión | Uso en Código | Estado |
|---------|---------|---------------|--------|
| `numpy` | `>=1.21.0` | `src/services/*.py` | ✅ Necesario |
| `tensorflow` | `>=2.10.0` | `src/models/load_model.py`, `src/services/grad_cam.py` | ✅ Necesario |
| `opencv-python` | `>=4.5.0` | `src/services/preprocess_img.py`, `src/services/grad_cam.py` | ✅ Necesario |
| `pillow` | `>=9.0.0` | `src/services/read_img.py`, `src/views/detector_neumonia.py` | ✅ Necesario |
| `pydicom` | `>=2.3.0` | `src/services/read_img.py` | ✅ Necesario |
| `tkcap` | `>=0.0.1` | `src/views/detector_neumonia.py` (opcional) | ⚠️ Opcional |
| `img2pdf` | `>=0.4.0` | `src/views/detector_neumonia.py` | ✅ Necesario |
| `reportlab` | `>=3.6.0` | `src/views/detector_neumonia.py` (fallback) | ✅ Necesario |

---

## 📦 Uso de Dependencias por Módulo

### `src/models/load_model.py`
- **`tensorflow`**: Carga del modelo CNN pre-entrenado
  ```python
  import tensorflow as tf
  model = tf.keras.models.load_model(model_path, compile=False)
  ```

### `src/services/read_img.py`
- **`pydicom`**: Lectura de archivos DICOM
  ```python
  import pydicom as dicom
  img = dicom.dcmread(path)  # Versión moderna
  ```
- **`opencv-python`**: Procesamiento de imágenes
- **`numpy`**: Operaciones con arrays
- **`pillow`**: Conversión de formatos de imagen

### `src/services/preprocess_img.py`
- **`opencv-python`**: Redimensionamiento, CLAHE, conversión de color
- **`numpy`**: Operaciones con arrays y normalización

### `src/services/grad_cam.py`
- **`tensorflow`**: Cálculo de gradientes con `tf.GradientTape`
- **`numpy`**: Operaciones con arrays
- **`opencv-python`**: Aplicación de colormap y superposición

### `src/views/detector_neumonia.py`
- **`pillow`**: Redimensionamiento de imágenes para GUI
- **`tkcap`**: Captura de ventana para PDF (opcional, fallback disponible)
- **`reportlab`**: Generación alternativa de PDFs
- **`img2pdf`**: Conversión de imágenes a PDF

---

## ✅ Dependencias Correctas (Confirmadas)

### Core Dependencies
```txt
numpy>=1.21.0              # Operaciones numéricas
tensorflow>=2.10.0         # Machine Learning
```

### Image Processing
```txt
opencv-python>=4.5.0       # Procesamiento de imágenes
pillow>=9.0.0              # Manipulación de imágenes
pydicom>=2.3.0             # Lectura de archivos DICOM
```

### GUI and Utilities
```txt
tkcap>=0.0.1               # Captura de ventana (opcional)
img2pdf>=0.4.0             # Conversión de imágenes a PDF
reportlab>=3.6.0           # Generación de PDFs (fallback)
```

---

## ❌ Dependencias Removidas (No Necesarias)

Las siguientes dependencias fueron **removidas** porque no se usan en el código:

| Paquete | Razón de Remoción |
|---------|-------------------|
| `pyautogui` | ❌ No se usa en ningún archivo |
| `matplotlib` | ❌ No se usa en ningún archivo |
| `pandas` | ❌ No se usa en ningún archivo |
| `python-xlib` | ❌ Específico de Linux, causa problemas en Windows |

---

## ⚠️ Dependencias Opcionales

### `tkcap` (Opcional)
- **Estado:** Opcional con fallback
- **Razón:** Requiere `tkinter.tix` que fue removido en Python 3.11+
- **Solución implementada:** 
  - Import opcional con `try-except`
  - Fallback a `reportlab` si `tkcap` no está disponible
- **Ubicación:** `src/views/detector_neumonia.py`

```python
try:
    import tkcap
    USE_TKCAP = True
except ImportError:
    USE_TKCAP = False
    # Usar reportlab como alternativa
```

---

## 🔧 Gestión de Dependencias

### Archivos de Configuración

#### `requirements.txt`
Archivo principal para instalación con `pip`:
```txt
numpy>=1.21.0
tensorflow>=2.10.0
opencv-python>=4.5.0
pillow>=9.0.0
pydicom>=2.3.0
tkcap>=0.0.1
img2pdf>=0.4.0
reportlab>=3.6.0
```

#### `pyproject.toml`
Configuración moderna del proyecto (PEP 621):
```toml
[project]
name = "uao-neumonia-g2"
version = "0.1.0"
description = "Herramienta para la detección rápida de neumonía mediante Deep Learning"
requires-python = ">=3.8"
dependencies = [
    "numpy>=1.21.0",
    "tensorflow>=2.10.0",
    "opencv-python>=4.5.0",
    "pillow>=9.0.0",
    "pydicom>=2.3.0",
    "tkcap>=0.0.1",
    "img2pdf>=0.4.0",
    "reportlab>=3.6.0",
]
```

**Estado:** ✅ Sincronizado con `requirements.txt`

---

## 📋 Instalación de Dependencias

### Opción 1: Usando `pip`
```bash
pip install -r requirements.txt
```

### Opción 2: Usando `uv` (Recomendado)
```bash
uv pip install -r requirements.txt
```

### Opción 3: Usando `pyproject.toml`
```bash
pip install -e .
```

---

## 🔍 Verificación de Dependencias

### Verificar Instalación
```bash
pip list | grep -E "numpy|tensorflow|opencv|pillow|pydicom"
```

### Verificar Versiones
```python
import numpy
import tensorflow as tf
import cv2
import PIL
import pydicom

print(f"NumPy: {numpy.__version__}")
print(f"TensorFlow: {tf.__version__}")
print(f"OpenCV: {cv2.__version__}")
print(f"Pillow: {PIL.__version__}")
print(f"PyDICOM: {pydicom.__version__}")
```

---

## ⚠️ Problemas Conocidos y Soluciones

### 1. `tkcap` en Python 3.11+
**Problema:** `tkinter.tix` fue removido en Python 3.11+  
**Solución:** ✅ Implementado fallback a `reportlab`  
**Estado:** ✅ Resuelto

### 2. `pydicom` API Changes
**Problema:** `read_file()` deprecado en favor de `dcmread()`  
**Solución:** ✅ Implementado con fallback para compatibilidad  
**Estado:** ✅ Resuelto

### 3. TensorFlow Compatibility
**Problema:** Modelo guardado con `reduction='auto'` (deprecated)  
**Solución:** ✅ Carga con `compile=False`  
**Estado:** ✅ Resuelto

### 4. TensorFlow Eager Execution
**Problema:** Grad-CAM requiere eager execution  
**Solución:** ✅ Reescrito usando `tf.GradientTape`  
**Estado:** ✅ Resuelto

---

## 📊 Resumen

### Estado Actual
- ✅ **8 dependencias necesarias** (todas correctas)
- ✅ **Versiones especificadas** (compatibilidad garantizada)
- ✅ **Sin dependencias innecesarias**
- ✅ **`pyproject.toml` sincronizado** con `requirements.txt`
- ✅ **Compatibilidad** con Python 3.8+ y TensorFlow 2.x

### Recomendaciones
1. ✅ Mantener `requirements.txt` y `pyproject.toml` sincronizados
2. ✅ Actualizar versiones cuando sea necesario para seguridad
3. ✅ Probar con diferentes versiones de Python antes de actualizar dependencias principales

---

**Última actualización:** 31 de enero de 2026
