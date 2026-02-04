#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para el módulo de lectura de imágenes.

Test básicos para verificar lectura correcta de archivos DICOM, JPG y PNG.
"""

import tempfile
import pytest
import numpy as np
from PIL import Image

from src.services.read_img import read_jpg_file, read_dicom_file, read_image


class TestReadJpgFile:
    """Pruebas para lectura de archivos JPG/PNG."""

    def test_leer_jpg_exitoso(self):
        """
        Test: Leer archivo JPG válido
        Input: Ruta a imagen JPG en test_data/jpg/
        Output: Tupla (array numpy, imagen PIL) válidos
        """
        # Usar una de tus imágenes de prueba
        img_array, img_pil = read_jpg_file('test/test_data/JPG/test_jpg_1.JPEG')

        # Verificaciones
        assert isinstance(img_array, np.ndarray), "Debe retornar numpy array"
        assert isinstance(img_pil, Image.Image), "Debe retornar imagen PIL"
        assert img_array.dtype == np.uint8, "Array debe ser uint8"
        assert len(img_array.shape) == 3, "Debe tener 3 dimensiones (H, W, C)"

    def test_leer_jpg_archivo_no_existe(self):
        """
        Test: Intentar leer archivo que no existe
        Input: Ruta a archivo inexistente
        Output: Debe lanzar FileNotFoundError
        """
        with pytest.raises((FileNotFoundError, RuntimeError)):
            read_jpg_file('test/test_data/JPG/no_existe.jpg')

    def test_leer_archivo_no_imagen(self):
        """
        Test: Intentar leer archivo que no es imagen
        Input: Archivo de texto .txt
        Output: Debe lanzar RuntimeError
        """
        # Crear archivo temporal txt para la prueba

        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"No soy una imagen")
            temp_path = f.name

        with pytest.raises(RuntimeError):
            read_jpg_file(temp_path)


class TestReadDicomFile:
    """Pruebas para lectura de archivos DICOM."""

    def test_leer_dicom_exitoso(self):
        """
        Test: Leer archivo DICOM válido
        Input: Ruta a archivo .dcm en test_data/dicom/
        Output: Tupla (array RGB, imagen PIL) válidos
        """
        img_array, img_pil = read_dicom_file(
            'test/test_data/DICOM/test_dicom_1.dcm')

        # Verificaciones
        assert isinstance(img_array, np.ndarray), "Debe retornar numpy array"
        assert isinstance(img_pil, Image.Image), "Debe retornar imagen PIL"
        assert len(img_array.shape) == 3, "Debe tener 3 dimensiones (RGB)"
        assert img_array.shape[2] == 3, "Debe tener 3 canales RGB"

    def test_leer_dicom_archivo_no_existe(self):
        """
        Test: Intentar leer DICOM inexistente
        Input: Ruta a archivo .dcm que no existe
        Output: Debe lanzar FileNotFoundError
        """
        with pytest.raises(FileNotFoundError):
            read_dicom_file('test/test_data/dicom/no_existe.dcm')


class TestReadImage:
    """Pruebas para función unificada de lectura."""

    def test_detectar_y_leer_jpg(self):
        """
        Test: Detección automática de formato JPG
        Input: Ruta a archivo .jpg
        Output: Lee correctamente usando read_jpg_file
        """
        img_array, img_pil = read_image('test/test_data/JPG/test_jpg_1.JPEG')

        assert isinstance(img_array, np.ndarray)
        assert isinstance(img_pil, Image.Image)

    def test_detectar_y_leer_dicom(self):
        """
        Test: Detección automática de formato DICOM
        Input: Ruta a archivo .dcm
        Output: Lee correctamente usando read_dicom_file
        """
        img_array, _ = read_image('test/test_data/DICOM/test_dicom_1.dcm')

        assert isinstance(img_array, np.ndarray)
        assert img_array.shape[2] == 3  # RGB

    def test_formato_no_soportado(self):
        """
        Test: Intentar leer formato no soportado
        Input: Archivo con extensión .txt
        Output: Debe lanzar ValueError indicando formato no soportado
        """
        with pytest.raises(ValueError, match="Formato de archivo no soportado"):
            read_image('test/test_data/archivo.txt')
