# Estructura Simplificada - Reorganización de Archivos Existentes

**Objetivo:** Reorganizar los archivos actuales en una estructura MVC simple, sin crear archivos nuevos.

---

## 📁 Estructura Propuesta (Simplificada)

```
UAO-Neumonia-G2/
│
├── 📂 src/                          # Código fuente
│   │
│   ├── 📂 models/                   # MODELO (Lógica de ML)
│   │   ├── __init__.py
│   │   └── load_model.py           # ← mover load_model.py aquí
│   │
│   ├── 📂 views/                    # VISTA (Interfaz gráfica)
│   │   ├── __init__.py
│   │   └── detector_neumonia.py    # ← mover detector_neumonia.py aquí
│   │
│   ├── 📂 controllers/              # CONTROLADOR (Lógica de control)
│   │   ├── __init__.py
│   │   └── integrator.py           # ← mover integrator.py aquí
│   │
│   └── 📂 services/                 # SERVICIOS (Procesamiento)
│       ├── __init__.py
│       ├── read_img.py             # ← mover read_img.py aquí
│       ├── preprocess_img.py        # ← mover preprocess_img.py aquí
│       └── grad_cam.py             # ← mover grad_cam.py aquí
│
├── 📂 data/                         # DATOS
│   ├── models/                     
│   │   └── conv_MLP_84.h5          # ← mover conv_MLP_84.h5 aquí
│   ├── DICOM/                      # ← mover carpeta DICOM aquí
│   └── JPG/                        # ← mover carpeta JPG aquí
│
├── 📄 main.py                       # Punto de entrada (actualizar imports)
│
├── 📄 requirements.txt              
├── 📄 pyproject.toml                
├── 📄 Dockerfile                    
├── 📄 README.md                     
├── 📄 .gitignore                    
└── [archivos de documentación .md]
```

---

## 🔄 Mapeo de Archivos Actuales

| Archivo Actual | Nueva Ubicación | Acción |
|----------------|-----------------|--------|
| `load_model.py` | `src/models/load_model.py` | Mover |
| `detector_neumonia.py` | `src/views/detector_neumonia.py` | Mover |
| `integrator.py` | `src/controllers/integrator.py` | Mover |
| `read_img.py` | `src/services/read_img.py` | Mover |
| `preprocess_img.py` | `src/services/preprocess_img.py` | Mover |
| `grad_cam.py` | `src/services/grad_cam.py` | Mover |
| `conv_MLP_84.h5` | `data/models/conv_MLP_84.h5` | Mover |
| `DICOM/` | `data/DICOM/` | Mover |
| `JPG/` | `data/JPG/` | Mover |
| `main.py` | `main.py` | Actualizar imports |

---

## 📝 Cambios Necesarios en Imports

### 1. `src/models/load_model.py`
**Sin cambios** - Ya está bien

### 2. `src/services/read_img.py`
**Sin cambios** - Ya está bien

### 3. `src/services/preprocess_img.py`
**Sin cambios** - Ya está bien

### 4. `src/services/grad_cam.py`
**Cambiar:**
```python
# ANTES:
from preprocess_img import preprocess
from load_model import load_model

# DESPUÉS:
from src.services.preprocess_img import preprocess
from src.models.load_model import load_model
```

### 5. `src/controllers/integrator.py`
**Cambiar:**
```python
# ANTES:
from load_model import load_model
from preprocess_img import preprocess
from grad_cam import grad_cam

# DESPUÉS:
from src.models.load_model import load_model
from src.services.preprocess_img import preprocess
from src.services.grad_cam import grad_cam
```

### 6. `src/views/detector_neumonia.py`
**Cambiar:**
```python
# ANTES:
from read_img import read_image
from integrator import predict

# DESPUÉS:
from src.services.read_img import read_image
from src.controllers.integrator import predict
```

### 7. `main.py`
**Cambiar:**
```python
# ANTES:
from detector_neumonia import main

# DESPUÉS:
from src.views.detector_neumonia import main
```

---

## 🎯 Estructura Final (Solo Reorganización)

```
UAO-Neumonia-G2/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── load_model.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── detector_neumonia.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── integrator.py
│   └── services/
│       ├── __init__.py
│       ├── read_img.py
│       ├── preprocess_img.py
│       └── grad_cam.py
├── data/
│   ├── models/
│   │   └── conv_MLP_84.h5
│   ├── DICOM/
│   └── JPG/
├── main.py
└── [archivos de configuración]
```

---

## ✅ Ventajas de esta Estructura Simple

1. **Solo reorganización** - No crea archivos nuevos
2. **MVC claro** - Separación de responsabilidades
3. **Fácil de entender** - Estructura lógica
4. **Mantenible** - Cada tipo de código en su lugar
5. **Escalable** - Fácil agregar nuevos archivos después

---

## 📋 Checklist de Reorganización

- [ ] Crear carpetas: `src/models/`, `src/views/`, `src/controllers/`, `src/services/`, `data/models/`, `data/DICOM/`, `data/JPG/`
- [ ] Crear archivos `__init__.py` en cada carpeta
- [ ] Mover archivos a sus nuevas ubicaciones
- [ ] Actualizar imports en `grad_cam.py`
- [ ] Actualizar imports en `integrator.py`
- [ ] Actualizar imports en `detector_neumonia.py`
- [ ] Actualizar imports en `main.py`
- [ ] Actualizar ruta del modelo en `load_model.py` (si es necesario)
- [ ] Probar que todo funciona

---

## 🔧 Cambios Adicionales Necesarios

### En `src/models/load_model.py`
Actualizar ruta del modelo:
```python
def load_model(model_path='data/models/conv_MLP_84.h5'):  # Nueva ruta
    ...
```

### En `src/views/detector_neumonia.py`
Si hay rutas hardcodeadas a `DICOM/` o `JPG/`, actualizar a `data/DICOM/` y `data/JPG/`

---

**¿Aprobamos esta estructura simplificada? Solo reorganiza lo existente.**
