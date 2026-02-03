# Estructura de Pruebas Unitarias

**Fecha:** 31 de enero de 2026  
**Estado:** 📋 Recomendación

---

## 📍 Ubicación Recomendada

Según las mejores prácticas de Python (PEP8) y estándares comunes, la carpeta de tests debe ubicarse en la **raíz del proyecto**, al mismo nivel que `src/`.

---

## 📁 Estructura Propuesta

```
UAO-Neumonia-G2/
├── src/                    # Código fuente
│   ├── models/
│   ├── views/
│   ├── controllers/
│   └── services/
├── tests/                   # ← AQUÍ: Carpeta de pruebas unitarias
│   ├── __init__.py
│   ├── test_models/
│   │   ├── __init__.py
│   │   └── test_load_model.py
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_read_img.py
│   │   ├── test_preprocess_img.py
│   │   └── test_grad_cam.py
│   ├── test_controllers/
│   │   ├── __init__.py
│   │   └── test_integrator.py
│   └── test_views/
│       ├── __init__.py
│       └── test_detector_neumonia.py
├── data/                    # Datos
├── report/                  # Reportes PDF
├── main.py
└── requirements.txt
```

---

## ✅ Opción Recomendada: `tests/` en la raíz

**Ventajas:**
- ✅ Estándar de la industria
- ✅ Compatible con pytest, unittest, nose
- ✅ Separación clara entre código y tests
- ✅ Fácil de encontrar y mantener
- ✅ Compatible con CI/CD

**Ubicación:**
```
UAO-Neumonia-G2/
└── tests/              ← Carpeta aquí
```

---

## 🔄 Alternativa: `tests/` dentro de `src/`

**Estructura alternativa:**
```
UAO-Neumonia-G2/
└── src/
    ├── models/
    ├── views/
    ├── controllers/
    ├── services/
    └── tests/          ← Alternativa (menos común)
```

**Desventajas:**
- ❌ Menos común en proyectos Python
- ❌ Puede confundirse con código de producción
- ❌ Más difícil de excluir en distribuciones

---

## 📋 Estructura Detallada Recomendada

```
tests/
├── __init__.py                    # Hace que tests sea un paquete
├── conftest.py                    # Configuración de pytest (opcional)
│
├── test_models/                   # Pruebas de modelos
│   ├── __init__.py
│   └── test_load_model.py         # Pruebas de carga del modelo
│
├── test_services/                 # Pruebas de servicios
│   ├── __init__.py
│   ├── test_read_img.py           # Pruebas de lectura de imágenes
│   ├── test_preprocess_img.py     # Pruebas de preprocesamiento
│   └── test_grad_cam.py           # Pruebas de Grad-CAM
│
├── test_controllers/              # Pruebas de controladores
│   ├── __init__.py
│   └── test_integrator.py        # Pruebas del integrador
│
└── test_views/                    # Pruebas de vistas (GUI)
    ├── __init__.py
    └── test_detector_neumonia.py  # Pruebas de la interfaz
```

---

## 🎯 Recomendación Final

**Crear la carpeta `tests/` en la raíz del proyecto**, al mismo nivel que `src/` y `data/`.

**Razones:**
1. ✅ Es el estándar más común en Python
2. ✅ Compatible con todas las herramientas de testing
3. ✅ Fácil de encontrar y mantener
4. ✅ Separación clara entre código y tests
5. ✅ Compatible con CI/CD y herramientas de cobertura

---

## 📝 Ejemplo de Estructura Final

```
UAO-Neumonia-G2/
├── src/                    # Código fuente
│   ├── models/
│   ├── views/
│   ├── controllers/
│   └── services/
├── tests/                   # ← CREAR AQUÍ
│   ├── __init__.py
│   ├── test_models/
│   ├── test_services/
│   ├── test_controllers/
│   └── test_views/
├── data/                    # Datos
├── report/                  # Reportes
├── main.py
└── requirements.txt
```

---

## 🚀 Comandos para Crear la Estructura

```bash
# Crear carpeta tests
mkdir tests

# Crear subcarpetas
mkdir tests\test_models
mkdir tests\test_services
mkdir tests\test_controllers
mkdir tests\test_views

# Crear archivos __init__.py
New-Item tests\__init__.py
New-Item tests\test_models\__init__.py
New-Item tests\test_services\__init__.py
New-Item tests\test_controllers\__init__.py
New-Item tests\test_views\__init__.py
```

---

## 📝 Ejemplos de Tests

### Ejemplo: Test de `load_model.py`
```python
# tests/test_models/test_load_model.py
import pytest
from src.models.load_model import load_model

def test_load_model_exists():
    """Test que el modelo se carga correctamente"""
    model = load_model()
    assert model is not None

def test_load_model_invalid_path():
    """Test que maneja correctamente rutas inválidas"""
    with pytest.raises(FileNotFoundError):
        load_model('ruta/invalida/modelo.h5')
```

### Ejemplo: Test de `read_img.py`
```python
# tests/test_services/test_read_img.py
import pytest
from src.services.read_img import read_image

def test_read_dicom_file():
    """Test lectura de archivo DICOM"""
    array, img_show = read_image('data/DICOM/normal (2).dcm')
    assert array is not None
    assert img_show is not None

def test_read_jpg_file():
    """Test lectura de archivo JPG"""
    array, img_show = read_image('data/JPG/normal/NORMAL2-IM-1144-0001.jpeg')
    assert array is not None
    assert img_show is not None
```

---

## 🛠️ Herramientas Recomendadas

### pytest (Recomendado)
```bash
pip install pytest pytest-cov
```

### Ejecutar Tests
```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=src --cov-report=html

# Ejecutar tests específicos
pytest tests/test_models/
```

---

**Última actualización:** 31 de enero de 2026
