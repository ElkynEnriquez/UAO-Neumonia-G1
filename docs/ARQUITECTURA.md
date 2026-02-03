# Arquitectura del Proyecto UAO-Neumonia-G2

**Fecha:** 31 de enero de 2026  
**Estado:** ✅ Implementado

---

## 📋 Resumen

El proyecto está organizado siguiendo el patrón **Modelo-Vista-Controlador (MVC)** con una arquitectura modular que separa claramente las responsabilidades de cada componente.

---

## 🏗️ Estructura del Proyecto

```
UAO-Neumonia-G2/
│
├── 📂 src/                          # Código fuente
│   │
│   ├── 📂 models/                   # MODELO - Lógica de Machine Learning
│   │   ├── __init__.py
│   │   └── load_model.py            # Carga del modelo CNN pre-entrenado
│   │
│   ├── 📂 views/                    # VISTA - Interfaz gráfica
│   │   ├── __init__.py
│   │   └── detector_neumonia.py    # Interfaz gráfica (GUI) con Tkinter
│   │
│   ├── 📂 controllers/              # CONTROLADOR - Lógica de control
│   │   ├── __init__.py
│   │   └── integrator.py           # Integración de módulos y predicción
│   │
│   └── 📂 services/                 # SERVICIOS - Procesamiento
│       ├── __init__.py
│       ├── read_img.py             # Lectura de imágenes (DICOM/JPG/PNG)
│       ├── preprocess_img.py        # Preprocesamiento de imágenes
│       └── grad_cam.py              # Generación de mapas de calor Grad-CAM
│
├── 📂 data/                         # Datos del proyecto
│   ├── models/
│   │   └── conv_MLP_84.h5          # Modelo pre-entrenado
│   ├── DICOM/                      # Imágenes de prueba DICOM
│   └── JPG/                        # Imágenes de prueba JPG
│       ├── bacteria/
│       ├── normal/
│       └── virus/
│
├── 📂 report/                       # Reportes PDF generados
│
├── 📂 docs/                         # Documentación del proyecto
│
├── 📄 main.py                       # Punto de entrada principal
├── 📄 requirements.txt              # Dependencias del proyecto
├── 📄 pyproject.toml                # Configuración del proyecto
└── 📄 README.md                     # Documentación principal
```

---

## 🎯 Patrón MVC Implementado

### 📂 `src/models/` - MODELO

**Responsabilidad:** Gestión del modelo de Machine Learning.

#### `load_model.py`
- **Función principal:** `load_model(model_path='data/models/conv_MLP_84.h5')`
- **Descripción:** Carga el modelo de red neuronal convolucional pre-entrenado
- **Características:**
  - Validación de existencia del archivo
  - Manejo de errores completo
  - Compatible con TensorFlow 2.x (eager execution)
  - Carga con `compile=False` para evitar problemas de compatibilidad

**Ejemplo de uso:**
```python
from src.models.load_model import load_model

model = load_model()
```

---

### 📂 `src/views/` - VISTA

**Responsabilidad:** Interfaz gráfica de usuario (GUI).

#### `detector_neumonia.py`
- **Clase principal:** `App`
- **Descripción:** Interfaz gráfica desarrollada con Tkinter
- **Funcionalidades:**
  - Carga de imágenes (DICOM, JPG, PNG)
  - Visualización de imágenes originales y con heatmap
  - Campos para cédula del paciente
  - Botones para: Cargar, Predecir, Guardar, Generar PDF, Borrar
  - Manejo de errores con mensajes al usuario

**Flujo de interacción:**
1. Usuario carga imagen → `load_img_file()`
2. Usuario hace clic en "Predecir" → `run_model()`
3. Usuario guarda resultados → `save_results_csv()` o `create_pdf()`

---

### 📂 `src/controllers/` - CONTROLADOR

**Responsabilidad:** Lógica de control y coordinación entre vista y servicios.

#### `integrator.py`
- **Función principal:** `predict(array, model=None)`
- **Descripción:** Integra todos los módulos y proporciona una interfaz unificada
- **Flujo de trabajo:**
  1. Preprocesa la imagen (`preprocess_img.py`)
  2. Carga el modelo si no se proporciona (`load_model.py`)
  3. Realiza la predicción
  4. Mapea la predicción a etiqueta ("bacteriana", "normal", "viral")
  5. Genera el mapa de calor Grad-CAM (`grad_cam.py`)
  6. Retorna `(label, proba, heatmap)`

**Ejemplo de uso:**
```python
from src.controllers.integrator import predict

label, proba, heatmap = predict(image_array)
```

---

### 📂 `src/services/` - SERVICIOS

**Responsabilidad:** Procesamiento de datos y operaciones auxiliares.

#### `read_img.py`
- **Funciones:**
  - `read_dicom_file(path)` - Lee archivos DICOM
  - `read_jpg_file(path)` - Lee archivos JPEG/JPG/PNG
  - `read_image(path)` - **Función unificada** que detecta automáticamente el tipo
- **Características:**
  - Detección automática del formato de archivo
  - Normalización de imágenes DICOM
  - Conversión a formatos compatibles
  - Manejo de errores para archivos inválidos

#### `preprocess_img.py`
- **Función:** `preprocess(array)`
- **Procesamiento:**
  1. Redimensiona a 512x512
  2. Convierte a escala de grises
  3. Aplica CLAHE (ecualización de histograma adaptativa)
  4. Normaliza entre 0 y 1
  5. Convierte a formato batch (tensor)

#### `grad_cam.py`
- **Función:** `grad_cam(array, model=None, layer_name="conv10_thisone")`
- **Descripción:** Genera mapas de calor Grad-CAM para visualización
- **Características:**
  - Cálculo de gradientes usando `tf.GradientTape`
  - Superposición de mapa de calor sobre imagen original
  - Configuración de transparencia
  - Compatible con TensorFlow eager execution

---

## 🔄 Flujo de Datos

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  detector_neumonia  │ (Vista)
│  (GUI - Tkinter)    │
└──────┬──────────────┘
       │
       │ 1. Carga imagen
       ▼
┌─────────────────────┐
│    read_img.py      │ (Servicio)
│  (Lectura archivos) │
└──────┬──────────────┘
       │
       │ 2. Preprocesa
       ▼
┌─────────────────────┐
│  preprocess_img.py  │ (Servicio)
└──────┬──────────────┘
       │
       │ 3. Predice
       ▼
┌─────────────────────┐
│   integrator.py     │ (Controlador)
│  (Coordina módulos) │
└──────┬──────────────┘
       │
       ├──► load_model.py (Modelo)
       ├──► preprocess_img.py (Servicio)
       └──► grad_cam.py (Servicio)
       │
       │ 4. Retorna resultados
       ▼
┌─────────────────────┐
│  detector_neumonia  │ (Vista)
│  (Muestra resultados)│
└─────────────────────┘
```

---

## 📦 Dependencias entre Módulos

```
detector_neumonia.py (views)
    ├──► read_img.py (services)
    └──► integrator.py (controllers)
            ├──► load_model.py (models)
            ├──► preprocess_img.py (services)
            └──► grad_cam.py (services)
                    ├──► preprocess_img.py (services)
                    └──► load_model.py (models)
```

---

## ✅ Principios de Diseño Aplicados

### 1. **Separación de Responsabilidades**
- Cada módulo tiene una responsabilidad única y clara
- La GUI solo maneja la interfaz, no la lógica de negocio

### 2. **Bajo Acoplamiento**
- Los módulos se comunican a través de interfaces bien definidas
- Fácil reemplazar implementaciones sin afectar otros módulos

### 3. **Alta Cohesión**
- Funciones relacionadas están agrupadas en el mismo módulo
- Cada módulo tiene un propósito específico y bien definido

### 4. **Reutilización**
- Los servicios pueden usarse independientemente
- El controlador puede reutilizarse en diferentes contextos

---

## 🔧 Configuración y Rutas

### Rutas Importantes
- **Modelo:** `data/models/conv_MLP_84.h5`
- **Imágenes de prueba:** `data/DICOM/` y `data/JPG/`
- **Reportes PDF:** `report/`
- **Historial CSV:** `historial.csv` (en raíz del proyecto)

### Configuración de Imports
Todos los imports usan rutas absolutas desde `src/`:
```python
from src.models.load_model import load_model
from src.services.read_img import read_image
from src.controllers.integrator import predict
```

---

## 🚀 Ventajas de esta Arquitectura

1. **Mantenibilidad:** Fácil encontrar y modificar código
2. **Testabilidad:** Cada módulo puede probarse independientemente
3. **Escalabilidad:** Fácil agregar nuevas funcionalidades
4. **Legibilidad:** Código organizado y fácil de entender
5. **Reutilización:** Módulos pueden usarse en otros proyectos

---

## 📝 Notas de Implementación

- ✅ Todos los errores críticos han sido corregidos
- ✅ Compatible con Python 3.8+ (probado con Python 3.13.2)
- ✅ Compatible con TensorFlow 2.x (eager execution)
- ✅ Manejo de errores implementado en todos los módulos críticos
- ✅ Documentación con docstrings en todas las funciones principales

---

**Última actualización:** 31 de enero de 2026
