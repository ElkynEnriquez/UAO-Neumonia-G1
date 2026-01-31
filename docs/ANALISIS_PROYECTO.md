# Análisis del Proyecto UAO-Neumonia-G2

**Fecha de Análisis:** 30 de enero de 2026  
**Versión del Proyecto:** 0.1.0

---

## 📋 Resumen Ejecutivo

Este proyecto es una herramienta de **detección de neumonía mediante Deep Learning** que utiliza una red neuronal convolucional (CNN) para clasificar imágenes radiográficas de tórax en tres categorías:

1. **Neumonía Bacteriana**
2. **Neumonía Viral**
3. **Sin Neumonía (Normal)**

La aplicación incluye una interfaz gráfica desarrollada con Tkinter y utiliza la técnica **Grad-CAM** para visualizar las regiones de la imagen que son relevantes para la clasificación mediante mapas de calor.

---

## 🎯 Funcionalidad del Proyecto

### Propósito Principal
El software está diseñado para **apoyar el diagnóstico médico** de neumonía mediante el análisis automatizado de imágenes radiográficas de tórax en formato DICOM, JPEG o PNG.

### Características Principales
- **Interfaz gráfica de usuario** (GUI) con Tkinter
- **Carga de imágenes** en formatos DICOM, JPEG, JPG y PNG
- **Predicción automática** de la clase de neumonía
- **Visualización con Grad-CAM** que muestra un mapa de calor sobre las regiones relevantes
- **Exportación de resultados** a CSV y PDF
- **Historial de pacientes** almacenado en archivo CSV

### Arquitectura del Modelo
Según el README, el modelo CNN está basado en el artículo de F. Pasa et al. y contiene:
- 5 bloques convolucionales con 16, 32, 48, 64 y 80 filtros respectivamente
- Capas de Max Pooling y Average Pooling
- 3 capas Dense (1024, 1024, 3 neuronas)
- Regularización con Dropout al 20%

---

## 🔍 Estructura del Proyecto

### Archivos Existentes

```
UAO-Neumonia-G2/
├── detector_neumonia.py    # Archivo principal con GUI y lógica
├── main.py                 # Punto de entrada (actualmente no funcional)
├── requirements.txt        # Dependencias del proyecto
├── pyproject.toml          # Configuración del proyecto
├── Dockerfile              # Configuración para contenedor Docker
├── README.md               # Documentación del proyecto
├── BRANCHING_STRATEGY.md   # Estrategia de ramas Git
└── uv.lock                 # Lock file de dependencias
```

### Archivos Faltantes (Mencionados en README)
El README menciona una arquitectura modular con varios archivos separados que **no existen** en el proyecto actual:
- ❌ `integrator.py` - Módulo integrador
- ❌ `read_img.py` - Lectura de imágenes DICOM
- ❌ `preprocess_img.py` - Preprocesamiento de imágenes
- ❌ `load_model.py` - Carga del modelo
- ❌ `grad_cam.py` - Implementación de Grad-CAM

**Nota:** Parece que toda la funcionalidad está consolidada en `detector_neumonia.py`, lo cual es funcional pero no coincide con la documentación.

### Archivo de Modelo
- ✅ `conv_MLP_84.h5` - Modelo pre-entrenado (existe en el repositorio)
- ⚠️ **Nota:** El README menciona `WilhemNet86.h5` pero el modelo real es `conv_MLP_84.h5`

---

## ⚠️ Errores y Problemas Detectados

### 🔴 **ERRORES CRÍTICOS** (Impiden la ejecución)

#### 1. **Imports Faltantes en `detector_neumonia.py`**

**Líneas 16-17:** Se usa `tf` (TensorFlow) sin importarlo
```python
tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)
```
**Solución requerida:**
```python
import tensorflow as tf
```

**Líneas 28-30:** Se usa `K` (Keras Backend) sin importarlo
```python
grads = K.gradients(output, last_conv_layer.output)[0]
pooled_grads = K.mean(grads, axis=(0, 1, 2))
iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
```
**Solución requerida:**
```python
from tensorflow.keras import backend as K
```

**Línea 71:** Se usa `dicom` sin importarlo
```python
img = dicom.read_file(path)
```
**Solución requerida:**
```python
import pydicom as dicom
```

**Líneas 200, 210, 211:** Se usa `END` sin importarlo
```python
self.text_img1.image_create(END, image=self.img1)
self.text2.insert(END, self.label)
self.text3.insert(END, "{:.2f}".format(self.proba) + "%")
```
**Solución requerida:**
```python
from tkinter import END
```

#### 2. **Función `model_fun()` No Definida**

**Líneas 23 y 54:** Se llama a `model_fun()` pero esta función no existe en el código
```python
model = model_fun()
```

**Solución requerida:** 
- Crear la función `model_fun()` que cargue el modelo desde el archivo `.h5`
- Usar: `tf.keras.models.load_model('conv_MLP_84.h5')` (el modelo correcto)

#### 3. **Nombre del Modelo Incorrecto en Código**

El modelo real es `conv_MLP_84.h5` (existe en el repositorio), pero:
- El README menciona `WilhemNet86.h5` (nombre incorrecto)
- Hay una referencia comentada en línea 55: `# model_cnn = tf.keras.models.load_model('conv_MLP_84.h5')`

**Solución requerida:**
- Actualizar función `model_fun()` para cargar `conv_MLP_84.h5`
- Actualizar README.md para reflejar el nombre correcto del modelo

### 🟡 **PROBLEMAS DE LÓGICA** (Funcionalidad incorrecta)

#### 4. **Carga de Archivos Siempre Usa DICOM**

**Línea 197:** La función `load_img_file()` siempre llama a `read_dicom_file()` incluso cuando el usuario selecciona archivos JPG/PNG
```python
self.array, img2show = read_dicom_file(filepath)
```

**Problema:** Esto causará errores al intentar leer archivos JPG/PNG como DICOM.

**Solución requerida:**
```python
if filepath.lower().endswith('.dcm'):
    self.array, img2show = read_dicom_file(filepath)
else:
    self.array, img2show = read_jpg_file(filepath)
```

#### 5. **Método `delete()` con Errores Potenciales**

**Líneas 240-241:** Intenta eliminar imágenes usando métodos incorrectos
```python
self.text_img1.delete(self.img1, "end")
self.text_img2.delete(self.img2, "end")
```

**Problema:** `Text.delete()` no acepta objetos Image como primer argumento. Debería usar índices o limpiar el contenido de otra manera.

### 🟠 **PROBLEMAS MENORES** (Mejoras recomendadas)

#### 6. **`main.py` No Funcional**

El archivo `main.py` solo contiene un print de prueba y no ejecuta la aplicación principal.

**Solución recomendada:**
```python
from detector_neumonia import main

if __name__ == "__main__":
    main()
```

#### 7. **Dockerfile con Error de Sintaxis**

**Línea 4:** Falta continuidad en el comando RUN
```dockerfile
RUN apt-get update -y && \
    apt-get install python3-opencv -y 
```

**Problema:** La línea 4 debería tener `&&` al final o estar en la misma línea.

**Solución recomendada:**
```dockerfile
RUN apt-get update -y && \
    apt-get install -y python3-opencv
```

#### 8. **`pyproject.toml` con Dependencias Vacías**

El archivo `pyproject.toml` tiene `dependencies = []` aunque existe un `requirements.txt` con las dependencias reales.

**Solución recomendada:** Sincronizar las dependencias entre ambos archivos o usar solo uno.

#### 9. **Uso de `Image.ANTIALIAS` Deprecado**

**Líneas 198 y 206:** Se usa `Image.ANTIALIAS` que está deprecado en versiones recientes de Pillow.

**Solución recomendada:**
```python
# Reemplazar Image.ANTIALIAS con Image.LANCZOS o Image.Resampling.LANCZOS
self.img1 = img2show.resize((250, 250), Image.LANCZOS)
```

#### 10. **Falta de Manejo de Errores**

No hay manejo de excepciones para:
- Archivos corruptos o inválidos
- Modelo no encontrado
- Errores de predicción
- Errores de escritura de archivos

---

## 📊 Análisis de Dependencias

### Dependencias en `requirements.txt`
```
pyautogui
pillow
tkcap
pydicom
img2pdf
opencv_python
matplotlib
pandas
tensorflow
python-xlib
```

### Problemas Potenciales
1. **Falta especificar versiones:** Sin versiones específicas, pueden surgir incompatibilidades
2. **`python-xlib`:** Específico de Linux, puede causar problemas en Windows
3. **`tensorflow`:** Versión no especificada, puede ser muy pesada o incompatible

### Recomendaciones
- Agregar versiones específicas a `requirements.txt`
- Considerar `tensorflow-cpu` para entornos sin GPU
- Remover o hacer condicional `python-xlib` para Windows

---

## ✅ Aspectos Positivos del Proyecto

1. **Documentación clara** en el README sobre la funcionalidad y arquitectura
2. **Interfaz gráfica funcional** con Tkinter
3. **Funcionalidades completas:** carga, predicción, visualización, exportación
4. **Uso de técnicas avanzadas:** Grad-CAM para explicabilidad
5. **Estrategia de ramas Git** bien documentada
6. **Código estructurado** con funciones separadas

---

## 🔧 Recomendaciones de Corrección (Priorizadas)

### Prioridad ALTA (Bloquean ejecución)
1. ✅ Agregar imports faltantes: `tensorflow`, `keras.backend`, `pydicom`, `END`
2. ✅ Implementar función `model_fun()` para cargar `conv_MLP_84.h5`
3. ✅ Actualizar README.md con el nombre correcto del modelo (`conv_MLP_84.h5`)
4. ✅ Corregir lógica de carga de archivos (DICOM vs JPG/PNG)

### Prioridad MEDIA (Afectan funcionalidad)
5. ✅ Corregir método `delete()` para limpiar imágenes correctamente
6. ✅ Agregar manejo de errores básico
7. ✅ Actualizar `main.py` para ejecutar la aplicación

### Prioridad BAJA (Mejoras)
8. ✅ Corregir Dockerfile
9. ✅ Sincronizar dependencias en `pyproject.toml`
10. ✅ Reemplazar `Image.ANTIALIAS` deprecado
11. ✅ Agregar versiones específicas a `requirements.txt`

---

## 📝 Resumen de Estado del Proyecto

| Aspecto | Estado | Notas |
|---------|--------|-------|
| **Compilación** | ❌ **FALLA** | Faltan imports críticos |
| **Ejecución** | ❌ **FALLA** | Función `model_fun()` no existe, modelo faltante |
| **Funcionalidad** | ⚠️ **PARCIAL** | Lógica de carga de archivos incorrecta |
| **Documentación** | ✅ **BUENA** | README completo y claro |
| **Estructura** | ⚠️ **MEJORABLE** | No coincide con documentación modular |
| **Dependencias** | ⚠️ **INCOMPLETA** | Faltan versiones, algunas incompatibles |

---

## 🎯 Conclusión

El proyecto tiene una **base sólida** con una buena idea y documentación clara, pero presenta **errores críticos** que impiden su ejecución. Los principales problemas son:

1. **Imports faltantes** que causarán errores inmediatos
2. **Función de carga del modelo no implementada** (usar `conv_MLP_84.h5`)
3. **Inconsistencia en nombre del modelo** (README menciona `WilhemNet86.h5` pero el real es `conv_MLP_84.h5`)
4. **Lógica incorrecta** para diferentes tipos de archivos

Con las correcciones de **Prioridad ALTA**, el proyecto debería poder ejecutarse correctamente. Las mejoras de **Prioridad MEDIA y BAJA** harían el código más robusto y mantenible.

---

## 📌 Próximos Pasos Sugeridos

1. **Corregir errores críticos** (Prioridad ALTA)
2. **Probar la aplicación** con imágenes de prueba
3. **Agregar tests unitarios** para funciones clave
4. **Refactorizar** según la arquitectura modular documentada (opcional)
5. **Mejorar manejo de errores** y validaciones
6. **Actualizar documentación** si se cambia la estructura

---

**Generado por:** Análisis Automático del Proyecto  
**Última actualización:** 30 de enero de 2026
