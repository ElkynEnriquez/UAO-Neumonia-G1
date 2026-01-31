# Guía de Ejecución del Proyecto - Paso a Paso

**Proyecto:** UAO-Neumonia-G2  
**Tipo:** Aplicación de escritorio con interfaz gráfica (GUI)

---

## 📋 ¿Qué es este proyecto?

Es una **aplicación de escritorio** con interfaz gráfica que permite:
- Cargar imágenes radiográficas de tórax (DICOM, JPG, PNG)
- Clasificar automáticamente si hay neumonía (bacteriana, viral o normal)
- Mostrar un mapa de calor (Grad-CAM) que resalta las áreas relevantes
- Guardar resultados en CSV y generar reportes PDF

---

## 🚀 Cómo Ejecutar el Proyecto

### Opción 1: Usando `uv` (Recomendado)

```bash
# Desde la raíz del proyecto
uv run main.py
```

### Opción 2: Usando Python tradicional

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python main.py
```

### Opción 3: Ejecutar directamente el módulo de vista

```bash
python -m src.views.detector_neumonia
```

---

## 🖥️ ¿Qué verás al ejecutar?

Al ejecutar `main.py`, se abrirá una **ventana gráfica** (GUI) con:

```
┌─────────────────────────────────────────────────────────┐
│  SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE        │
│                    NEUMONÍA                              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [Imagen Radiográfica]    [Imagen con Heatmap]          │
│  ┌─────────────┐          ┌─────────────┐              │
│  │             │          │             │              │
│  │   (vacío)   │          │   (vacío)   │              │
│  │             │          │             │              │
│  └─────────────┘          └─────────────┘              │
│                                                           │
│  Cédula Paciente: [________]  Resultado: [______]       │
│                              Probabilidad: [____]       │
│                                                           │
│  [Cargar Imagen] [Predecir] [Guardar] [PDF] [Borrar]   │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Pasos para Usar la Aplicación

### Paso 1: Ejecutar la aplicación
```bash
uv run main.py
```
O simplemente:
```bash
python main.py
```

### Paso 2: Cargar una imagen
1. Haz clic en el botón **"Cargar Imagen"**
2. Selecciona una imagen:
   - Formato DICOM (`.dcm`) desde `data/DICOM/`
   - Formato JPG/PNG desde `data/JPG/`
3. La imagen aparecerá en el panel izquierdo

### Paso 3: Ingresar cédula del paciente (opcional)
- Escribe la cédula en el campo "Cédula Paciente"

### Paso 4: Realizar predicción
1. Haz clic en el botón **"Predecir"**
2. Espera unos segundos mientras se procesa
3. Verás:
   - **Resultado:** bacteriana, viral o normal
   - **Probabilidad:** porcentaje de confianza
   - **Heatmap:** imagen con mapa de calor en el panel derecho

### Paso 5: Guardar resultados (opcional)
- **"Guardar"**: Guarda los resultados en `historial.csv`
- **"PDF"**: Genera un reporte PDF con la información

### Paso 6: Limpiar para nueva imagen
- Haz clic en **"Borrar"** para limpiar todo y cargar otra imagen

---

## 🔧 Solución de Problemas

### Error: "No module named 'tkinter.tix'"

**Causa:** `tkcap` requiere `tkinter.tix` que fue removido en Python 3.11+

**Solución:** Ya está corregido. El código ahora maneja `tkcap` de forma opcional. Si no está disponible, usa un método alternativo para generar PDFs.

### Error: "No se encontró el archivo del modelo"

**Causa:** El modelo `conv_MLP_84.h5` no está en `data/models/`

**Solución:** Asegúrate de que el archivo `data/models/conv_MLP_84.h5` existe

### Error: "ModuleNotFoundError"

**Causa:** Faltan dependencias instaladas

**Solución:**
```bash
pip install -r requirements.txt
```

---

## 📁 Estructura del Proyecto (Para Referencia)

```
UAO-Neumonia-G2/
├── main.py                    # ← Punto de entrada (EJECUTAR ESTE)
├── src/
│   ├── views/
│   │   └── detector_neumonia.py  # ← Interfaz gráfica (GUI)
│   ├── controllers/
│   │   └── integrator.py         # ← Lógica de predicción
│   ├── services/                  # ← Procesamiento de imágenes
│   └── models/                   # ← Carga del modelo ML
├── data/
│   ├── models/
│   │   └── conv_MLP_84.h5        # ← Modelo pre-entrenado
│   ├── DICOM/                    # ← Imágenes de prueba DICOM
│   └── JPG/                      # ← Imágenes de prueba JPG
└── requirements.txt              # ← Dependencias
```

---

## ✅ Checklist de Ejecución

- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Modelo existe en `data/models/conv_MLP_84.h5`
- [ ] Python 3.8+ instalado
- [ ] Ejecutar `python main.py` o `uv run main.py`
- [ ] Ventana gráfica se abre correctamente
- [ ] Puedes cargar una imagen de prueba

---

## 🎯 Resumen Rápido

1. **Ejecutar:** `python main.py` o `uv run main.py`
2. **Vista:** Se abre una ventana gráfica automáticamente
3. **Usar:** Botones en la interfaz para cargar, predecir, guardar
4. **No necesitas:** Abrir archivos manualmente, la GUI lo hace todo

---

**¿Listo para ejecutar?** Simplemente ejecuta:
```bash
python main.py
```

¡Y la ventana gráfica aparecerá automáticamente! 🚀
