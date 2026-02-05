# Estructura y Documentación de Tests

## Resumen

Se implementaron **38 pruebas unitarias** que cubren los módulos principales del proyecto:
- Lectura de imágenes (DICOM, JPG, PNG)
- Preprocesamiento de imágenes (resize, CLAHE, normalización)
- Carga del modelo de deep learning
- Generación de mapas de calor Grad-CAM
- Generación de reportes (CSV, PDF)
- Pipeline completo de predicción

## Estructura del Directorio de Tests

```
test/
├── __init__.py
├── test_services/
│   ├── __init__.py
│   ├── test_read_img.py          # 8 tests - Lectura de imágenes
│   ├── test_preprocess_img.py    # 6 tests - Preprocesamiento
│   ├── test_grad_cam.py          # 7 tests - Generación de heatmaps
│   └── test_report_generator.py  # 5 tests - Generación de reportes
├── test_models/
│   ├── __init__.py
│   └── test_load_model.py        # 5 tests - Carga del modelo CNN
├── test_controllers/
│   ├── __init__.py
│   └── test_integrator.py        # 7 tests - Pipeline completo
└── test_data/
    ├── JPG/
    │   ├── test_jpg_1.JPEG
    │   ├── test_jpg_2.jpeg
    │   └── test_jpg_3.jpeg
    └── DICOM/
        ├── test_dicom_1.dcm
        └── test_dicom_2.dcm
```

## Librerías de Testing Instaladas

### pytest
**Propósito:** Framework principal de testing para Python.

**Por qué se usa:** Es el estándar de la industria, simple de usar, con excelente soporte para fixtures, marcadores y plugins.

```bash
uv add --dev pytest
```

### pytest-mock
**Propósito:** Extensión de pytest para simplificar el uso de mocks.

**Por qué se usa:** Facilita la creación de objetos mock (simulados) para evitar cargar dependencias pesadas como modelos de TensorFlow en cada test.

```bash
uv add --dev pytest-mock
```

### pytest-cov
**Propósito:** Plugin para medir la cobertura de código.

**Por qué se usa:** Permite saber qué porcentaje del código fuente está siendo probado por los tests, identificando áreas sin cobertura.

```bash
uv add --dev pytest-cov
```

## Conceptos Importantes

### ¿Qué es un Mock?

Un **mock** es un **objeto simulado que imita el comportamiento de objetos reales** de manera controlada.

**¿Por qué usar mocks?**
- **Velocidad:** Evita cargar modelos de 100+ MB en cada test
- **Aislamiento:** Prueba solo la lógica de una función, no sus dependencias
- **Control:** Puedes simular errores o casos específicos fácilmente

**Ejemplo:**
```python
# Sin mock (lento, 5+ segundos por test)
modelo = load_model('data/models/conv_MLP_84.h5')  # Carga 100 MB
resultado = modelo.predict(imagen)

# Con mock (rápido, <0.1 segundos)
mock_modelo = MagicMock()
mock_modelo.predict.return_value = np.array([[0.1, 0.8, 0.1]])
resultado = mock_modelo.predict(imagen)  # No carga nada, retorna valor fijo
```

### ¿Qué es Coverage (Cobertura)?

**Coverage** mide **qué porcentaje del código fuente fue ejecutado** durante los tests.

**Interpretación:**
- **80-100%:** Excelente cobertura (lo ideal)
- **60-80%:** Buena cobertura
- **<60%:** Cobertura insuficiente, muchas líneas sin probar

**¿Por qué es importante?**
- Identifica código que nunca se ejecuta en tests
- Ayuda a encontrar casos no cubiertos
- Da confianza de que el código está bien probado

**Ejemplo de reporte:**
```
Name                           Stmts   Miss  Cover
--------------------------------------------------
src/services/read_img.py          45      3    93%
src/services/preprocess_img.py    32      0   100%
src/models/load_model.py          18      2    89%
--------------------------------------------------
TOTAL                            234     15    94%
```

## Cómo Ejecutar los Tests

**IMPORTANTE:** Todos los comandos deben ejecutarse desde el **directorio raíz del proyecto** (`UAO-Neumonia-G1/`), NO desde el directorio `test/`.

### Ejecutar todos los tests

```bash
uv run pytest test/ -v
```

**Salida esperada:**
```
======================== 33 tests collected in 3.92s =========================
test/test_controllers/test_integrator.py::TestPredictConMocks::test_predict_neumonia_normal PASSED
test/test_controllers/test_integrator.py::TestPredictConMocks::test_predict_neumonia_bacteriana PASSED
...
======================== 32 passed, 1 skipped in 13.06s =========================
```

### Ejecutar tests de un módulo específico

```bash
# Solo tests de lectura de imágenes
uv run pytest test/test_services/test_read_img.py -v

# Solo tests de preprocesamiento
uv run pytest test/test_services/test_preprocess_img.py -v

# Solo tests de Grad-CAM
uv run pytest test/test_services/test_grad_cam.py -v

# Solo tests del modelo
uv run pytest test/test_models/test_load_model.py -v

# Solo tests del integrador
uv run pytest test/test_controllers/test_integrator.py -v
```

### Ejecutar con reporte de cobertura (coverage)

```bash
# Cobertura básica en terminal
uv run pytest test/ --cov=src --cov-report=term

# Cobertura con detalles de líneas faltantes
uv run pytest test/ --cov=src --cov-report=term-missing

# Generar reporte HTML interactivo
uv run pytest test/ --cov=src --cov-report=html
# Luego abrir: htmlcov/index.html en el navegador
```

**Ejemplo de salida:**
```
---------- coverage: platform win32, python 3.12.9 -----------
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src\__init__.py                       0      0   100%
src\controllers\integrator.py        24      0   100%
src\models\load_model.py             18      1    94%
src\services\grad_cam.py             52      3    94%
src\services\preprocess_img.py       32      0   100%
src\services\read_img.py             45      2    96%
-----------------------------------------------------
TOTAL                               171      6    96%
```

### Otros comandos útiles

```bash
# Ejecutar solo tests que fallaron la última vez
uv run pytest test/ --lf

# Detener en el primer fallo
uv run pytest test/ -x

# Ver print() statements aunque pasen los tests
uv run pytest test/ -s

# Mostrar cuántos tests pytest encuentra (sin ejecutar)
uv run pytest test/ --collect-only

# Ejecutar tests en paralelo (requiere pytest-xdist)
uv add --dev pytest-xdist
uv run pytest test/ -n auto
```

## Detalles de Cada Módulo de Tests

### test_read_img.py (8 tests)

**Propósito:** Verificar lectura correcta de imágenes en diferentes formatos.

**Tests incluidos:**
1. `test_leer_jpg_exitoso` - Lee JPG válido
2. `test_leer_jpg_archivo_no_existe` - Error si archivo no existe
3. `test_leer_archivo_no_imagen` - Error si archivo no es imagen
4. `test_leer_dicom_exitoso` - Lee DICOM válido
5. `test_leer_dicom_archivo_no_existe` - Error si DICOM no existe
6. `test_detectar_y_leer_jpg` - Detección automática de JPG
7. `test_detectar_y_leer_dicom` - Detección automática de DICOM
8. `test_formato_no_soportado` - Error con formato inválido

**Ejecutar:**
```bash
uv run pytest test/test_services/test_read_img.py -v
```

**Estrategia:** Usa archivos reales de `test/test_data/` para validar lectura.

---

### test_preprocess_img.py (6 tests)

**Propósito:** Verificar preprocesamiento correcto (resize, normalización, CLAHE).

**Tests incluidos:**
1. `test_preprocess_shape_correcta` - Verifica shape (1, 512, 512, 1)
2. `test_preprocess_normalizacion` - Valores en [0.0, 1.0]
3. `test_preprocess_tipo_dato` - Verifica dtype float
4. `test_preprocess_imagen_pequeña` - Redimensiona desde 256x256
5. `test_preprocess_imagen_grande` - Redimensiona desde 2048x2048
6. `test_preprocess_clahe_aplicado` - Verifica mejora de contraste

**Ejecutar:**
```bash
uv run pytest test/test_services/test_preprocess_img.py -v
```

**Estrategia:** Usa imágenes sintéticas generadas con numpy para probar diferentes tamaños y casos.

---

### test_grad_cam.py (7 tests)

**Propósito:** Verificar generación correcta de mapas de calor Grad-CAM.

**NOTA IMPORTANTE:** Estos tests cargan el modelo real porque TensorFlow no acepta mocks para operaciones de gradientes. Son rápidos (~2s cada uno).

**Tests incluidos:**
1. `test_grad_cam_retorna_imagen_correcta` - Shape 512x512x3
2. `test_grad_cam_sin_modelo` - Carga automática del modelo
3. `test_grad_cam_con_modelo_precargado` - Usa modelo pasado
4. `test_grad_cam_valores_en_rango` - Valores uint8 [0-255]
5. `test_grad_cam_capa_personalizada` - Capa convolucional custom
6. `test_grad_cam_formato_rgb` - Verifica formato RGB
7. `test_grad_cam_con_imagen_jpg_real` - Test con imagen real

**Ejecutar:**
```bash
uv run pytest test/test_services/test_grad_cam.py -v
```

**Estrategia:** Usa fixture `modelo_cargado` que carga el modelo una sola vez para todos los tests.

---

### test_report_generator.py (5 tests)

**Propósito:** Verificar generación correcta de reportes en CSV y PDF.

**Tests incluidos:**
1. `test_save_results_csv_new_file` - Guarda resultados en CSV nuevo con encabezados
2. `test_save_results_csv_existing_file` - Guarda resultados en CSV existente sin encabezados
3. `test_generate_pdf_report_success` - Genera PDF exitosamente
4. `test_generate_pdf_report_with_heatmap` - Genera PDF con heatmap Grad-CAM incluido
5. `test_format_prediction_output` - Formatea salida para consola correctamente

**Ejecutar:**
```bash
uv run pytest test/test_services/test_report_generator.py -v
```

**Estrategia:** Usa mocks para `csv.writer`, `canvas.Canvas`, `datetime` y operaciones de archivos para evitar crear archivos reales durante los tests. Simula la fecha/hora para verificaciones precisas.

---

### test_load_model.py (5 tests)

**Propósito:** Verificar carga correcta del modelo CNN.

**Tests incluidos:**
1. `test_archivo_modelo_no_existe` - Error si modelo no existe
2. `test_carga_exitosa_con_mock` - Carga exitosa (con mock)
3. `test_carga_con_compile_false` - Verifica compile=False
4. `test_model_fun_usa_ruta_por_defecto` - Función de compatibilidad
5. `test_cargar_modelo_real` - Test con modelo real

**Ejecutar:**
```bash
uv run pytest test/test_models/test_load_model.py -v
```

**Estrategia:** Usa mocks para tests rápidos, más un test con modelo real para validación completa.

---

### test_integrator.py (7 tests)

**Propósito:** Verificar pipeline completo de predicción.

**Tests incluidos:**
1. `test_predict_neumonia_normal` - Predicción normal
2. `test_predict_neumonia_bacteriana` - Predicción bacteriana
3. `test_predict_neumonia_viral` - Predicción viral
4. `test_predict_llama_funciones_correctamente` - Verifica llamadas
5. `test_predict_con_modelo_precargado` - No carga modelo si ya existe
6. `test_predict_error_en_preprocesamiento` - Manejo de errores
7. `test_predict_con_imagen_jpg_real` - Test con imagen real (skipped si no hay imágenes)

**Ejecutar:**
```bash
uv run pytest test/test_controllers/test_integrator.py -v
```

**Estrategia:** Usa mocks para `preprocess`, `load_model` y `grad_cam` para aislar la lógica del integrador.

---

## Interpretación de Resultados

### Tests Pasando

```
======================== 32 passed, 1 skipped in 13.06s =========================
```

- **32 passed:** Tests que se ejecutaron y pasaron correctamente
- **1 skipped:** Tests marcados como opcionales (ej: requieren imágenes no disponibles)
- **13.06s:** Tiempo total de ejecución

### Tests Fallando

```
====================== 1 failed, 32 passed in 13.24s ==============

FAILED test/test_services/test_read_img.py::test_leer_jpg_exitoso
```

Cuando un test falla, pytest muestra:
- **Archivo y función:** Dónde ocurrió el fallo
- **Línea de código:** Qué línea falló
- **Mensaje de error:** Por qué falló
- **Valores esperados vs obtenidos**

**Ejemplo de error:**
```python
E   AssertionError: assert 512 == 256
E    +  where 512 = (512, 512, 3)[0]
```

Esto indica que se esperaba 256 pero se obtuvo 512.

---
