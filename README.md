# Herramienta para la Detección Rápida de Neumonía

Deep Learning aplicado en el procesamiento de imágenes radiográficas de tórax en formato DICOM, JPEG y PNG con el fin de clasificarlas en 3 categorías diferentes:

1. **Neumonía Bacteriana**
2. **Neumonía Viral**
3. **Sin Neumonía (Normal)**

Aplicación de una técnica de explicación llamada **Grad-CAM** para resaltar con un mapa de calor las regiones relevantes de la imagen de entrada.

---

## 🚀 Instalación y Uso

### Requisitos Previos

- **Python 3.8 o superior** (probado con Python 3.13.2)
- **TensorFlow 2.10+**

### Instalación

#### Opción 1: Usando `uv` (Recomendado)

```bash
# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar la aplicación
uv run main.py
```

#### Opción 2: Usando `pip` tradicional

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

#### Opción 3: Usando Anaconda

```bash
# Crear entorno conda
conda create -n tf tensorflow python=3.10
conda activate tf

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

---

## 📖 Uso de la Interfaz Gráfica

1. **Ingrese la cédula del paciente** en la caja de texto (opcional)
2. **Presione el botón 'Cargar Imagen'**:
   - Seleccione una imagen del explorador de archivos
   - Formatos soportados: DICOM (.dcm), JPEG (.jpeg, .jpg), PNG (.png)
   - Imágenes de prueba disponibles en `data/DICOM/` y `data/JPG/`
3. **Presione el botón 'Predecir'** y espere unos segundos hasta que observe los resultados
4. **Presione el botón 'Guardar'** para almacenar la información del paciente en un archivo CSV (`historial.csv`)
5. **Presione el botón 'PDF'** para generar un reporte PDF (se guarda en `report/`)
6. **Presione el botón 'Borrar'** si desea cargar una nueva imagen

---

## 📁 Estructura del Proyecto

```
UAO-Neumonia-G2/
├── src/                          # Código fuente (Arquitectura MVC)
│   ├── models/                   # MODELO - Lógica de ML
│   │   └── load_model.py         # Carga del modelo CNN
│   ├── views/                    # VISTA - Interfaz gráfica
│   │   └── detector_neumonia.py # Interfaz gráfica (GUI)
│   ├── controllers/              # CONTROLADOR - Lógica de control
│   │   └── integrator.py         # Integración de módulos
│   └── services/                 # SERVICIOS - Procesamiento
│       ├── read_img.py           # Lectura de imágenes (DICOM/JPG)
│       ├── preprocess_img.py     # Preprocesamiento de imágenes
│       └── grad_cam.py           # Generación de mapas de calor
├── data/                         # Datos del proyecto
│   ├── models/
│   │   └── conv_MLP_84.h5        # Modelo pre-entrenado
│   ├── DICOM/                    # Imágenes de prueba DICOM
│   └── JPG/                      # Imágenes de prueba JPG
│       ├── bacteria/
│       ├── normal/
│       └── virus/
├── report/                       # Reportes PDF generados
├── main.py                       # Punto de entrada principal
├── requirements.txt              # Dependencias del proyecto
└── pyproject.toml                # Configuración del proyecto
```

---

## 🏗️ Arquitectura del Proyecto (MVC)

El proyecto está organizado siguiendo el patrón **Modelo-Vista-Controlador (MVC)**:

### 📂 `src/models/` - MODELO
- **`load_model.py`**: Carga el modelo de red neuronal convolucional pre-entrenado (`conv_MLP_84.h5`)

### 📂 `src/views/` - VISTA
- **`detector_neumonia.py`**: Contiene el diseño de la interfaz gráfica utilizando Tkinter. Los botones llaman métodos contenidos en los controladores y servicios.

### 📂 `src/controllers/` - CONTROLADOR
- **`integrator.py`**: Módulo que integra los demás servicios y retorna solamente lo necesario para ser visualizado en la interfaz gráfica. Retorna la clase, la probabilidad y una imagen del mapa de calor generado por Grad-CAM.

### 📂 `src/services/` - SERVICIOS
- **`read_img.py`**: Lee imágenes en formato DICOM, JPEG, JPG y PNG. Convierte las imágenes a formatos compatibles para su procesamiento.
- **`preprocess_img.py`**: Recibe el arreglo proveniente de `read_img.py`, realiza las siguientes modificaciones:
  - Resize a 512x512
  - Conversión a escala de grises
  - Ecualización del histograma con CLAHE
  - Normalización de la imagen entre 0 y 1
  - Conversión del arreglo de imagen a formato de batch (tensor)
- **`grad_cam.py`**: Recibe la imagen y la procesa, carga el modelo, obtiene la predicción y la capa convolucional de interés para obtener las características relevantes de la imagen.

---

## 🧠 Acerca del Modelo

La red neuronal convolucional implementada (CNN) está basada en el modelo implementado por **F. Pasa, V. Golkov, F. Pfeifer, D. Cremers & D. Pfeifer** en su artículo *"Efficient Deep Network Architectures for Fast Chest X-Ray Tuberculosis Screening and Visualization"*.

### Arquitectura:
- **5 bloques convolucionales**, cada uno contiene 3 convoluciones; dos secuenciales y una conexión 'skip' que evita el desvanecimiento del gradiente a medida que se avanza en profundidad
- **Filtros**: 16, 32, 48, 64 y 80 filtros de 3x3 para cada bloque respectivamente
- **Pooling**: Después de cada bloque convolucional se encuentra una capa de max pooling y después de la última una capa de Average Pooling
- **Capas Dense**: Tres capas fully-connected (Dense) de 1024, 1024 y 3 neuronas respectivamente
- **Regularización**: 3 capas de Dropout al 20%; dos en los bloques 4 y 5 conv y otra después de la 1ra capa Dense

### Modelo Pre-entrenado:
- **Archivo**: `data/models/conv_MLP_84.h5`
- **Ubicación**: `data/models/`

---

## 🔥 Acerca de Grad-CAM

Grad-CAM (Gradient-weighted Class Activation Mapping) es una técnica utilizada para resaltar las regiones de una imagen que son importantes para la clasificación. Un mapeo de activaciones de clase para una categoría en particular indica las regiones de imagen relevantes utilizadas por la CNN para identificar esa categoría.

Grad-CAM realiza el cálculo del gradiente de la salida correspondiente a la clase a visualizar con respecto a las neuronas de una cierta capa de la CNN. Esto permite tener información de la importancia de cada neurona en el proceso de decisión de esa clase en particular. Una vez obtenidos estos pesos, se realiza una combinación lineal entre el mapa de activaciones de la capa y los pesos, de esta manera, se captura la importancia del mapa de activaciones para la clase en particular y se ve reflejado en la imagen de entrada como un mapa de calor con intensidades más altas en aquellas regiones relevantes para la red con las que clasificó la imagen en cierta categoría.

---

## 📊 Archivos Generados

- **`historial.csv`**: Archivo CSV con el historial de predicciones (se guarda en la raíz del proyecto)
- **`report/Reporte*.pdf`**: Reportes PDF generados (se guardan en la carpeta `report/`)

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **TensorFlow/Keras**: Framework de Deep Learning
- **Tkinter**: Interfaz gráfica de usuario
- **OpenCV**: Procesamiento de imágenes
- **Pillow (PIL)**: Manipulación de imágenes
- **PyDICOM**: Lectura de archivos DICOM
- **ReportLab**: Generación de PDFs
- **NumPy**: Operaciones numéricas

---

## 📝 Notas Importantes

- El modelo requiere el archivo `data/models/conv_MLP_84.h5` para funcionar
- Las imágenes de prueba están disponibles en `data/DICOM/` y `data/JPG/`
- Los reportes PDF se guardan automáticamente en la carpeta `report/`
- Compatible con Python 3.8+ (probado con Python 3.13.2)

---

## 👥 Proyecto Original

Realizado por:
- **Isabella Torres Revelo** - https://github.com/isa-tr
- **Nicolas Diaz Salazar** - https://github.com/nicolasdiazsalazar

---

## 📄 Licencia

Este proyecto es parte del trabajo académico de la Universidad Autónoma de Occidente (UAO).

---

**Versión:** 0.1.0  
**Última actualización:** 02 febrero 2026
