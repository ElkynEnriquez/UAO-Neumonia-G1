#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para el módulo de generación de mapas de calor Grad-CAM.

NOTA: Estos tests requieren cargar el modelo real porque TensorFlow no acepta
mocks para operaciones de gradientes. Los tests son rápidos (~2s cada uno).
"""

import pytest
import numpy as np
import os
from src.services.grad_cam import grad_cam
from src.models.load_model import load_model


@pytest.fixture(scope="module")
def modelo_cargado():
    """Carga el modelo una sola vez para todos los tests."""
    modelo_path = 'data/models/conv_MLP_84.h5'
    if os.path.exists(modelo_path):
        return load_model(modelo_path)
    return None


class TestGradCAM:
    """Pruebas para generación de mapas de calor Grad-CAM."""

    def test_grad_cam_retorna_imagen_correcta(self, modelo_cargado):
        """
        Test: Verificar que Grad-CAM retorna imagen con dimensiones correctas
        Input: Imagen RGB de cualquier tamaño
        Output: Heatmap RGB de 512x512 píxeles
        """
        if modelo_cargado is None:
            pytest.skip("Modelo no disponible")

        # Ejecutar con imagen sintética
        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        heatmap = grad_cam(img_test, model=modelo_cargado)

        # Verificaciones
        assert isinstance(heatmap, np.ndarray), "Debe retornar numpy array"
        assert heatmap.shape == (512, 512, 3), "Heatmap debe ser 512x512x3"
        assert heatmap.dtype == np.uint8, "Debe ser uint8"

    def test_grad_cam_sin_modelo(self):
        """
        Test: Grad-CAM sin pasar modelo (carga automática)
        Input: Imagen sin modelo pre-cargado
        Output: Carga modelo automáticamente y genera heatmap
        """
        modelo_path = 'data/models/conv_MLP_84.h5'
        if not os.path.exists(modelo_path):
            pytest.skip("Modelo no disponible")

        img_test = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        heatmap = grad_cam(img_test, model=None)  # Sin modelo

        # Verificaciones
        assert heatmap is not None, "Debe generar heatmap"
        assert heatmap.shape == (512, 512, 3)

    def test_grad_cam_con_modelo_precargado(self, modelo_cargado):
        """
        Test: Grad-CAM con modelo ya cargado
        Input: Imagen + modelo pre-cargado
        Output: Usa el modelo proporcionado
        """
        if modelo_cargado is None:
            pytest.skip("Modelo no disponible")

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        heatmap = grad_cam(img_test, model=modelo_cargado)

        # Verificaciones
        assert heatmap is not None
        assert heatmap.shape == (512, 512, 3)

    def test_grad_cam_valores_en_rango(self, modelo_cargado):
        """
        Test: Verificar que valores del heatmap están en rango [0-255]
        Input: Imagen cualquiera
        Output: Heatmap con valores uint8 en [0, 255]
        """
        if modelo_cargado is None:
            pytest.skip("Modelo no disponible")

        img_test = np.random.randint(0, 255, (400, 400, 3), dtype=np.uint8)
        heatmap = grad_cam(img_test, model=modelo_cargado)

        # Verificar rango de valores
        assert heatmap.min() >= 0, "Valores mínimos deben ser >= 0"
        assert heatmap.max() <= 255, "Valores máximos deben ser <= 255"

    def test_grad_cam_capa_personalizada(self, modelo_cargado):
        """
        Test: Usar capa convolucional por defecto
        Input: Imagen + nombre de capa default
        Output: Genera heatmap correctamente
        """
        if modelo_cargado is None:
            pytest.skip("Modelo no disponible")

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        heatmap = grad_cam(img_test, model=modelo_cargado,
                           layer_name="conv10_thisone")

        # Verificaciones
        assert heatmap is not None
        assert heatmap.shape == (512, 512, 3)

    def test_grad_cam_formato_rgb(self, modelo_cargado):
        """
        Test: Verificar que heatmap está en formato RGB (no BGR)
        Input: Imagen en cualquier formato
        Output: Heatmap en formato RGB para visualización
        """
        if modelo_cargado is None:
            pytest.skip("Modelo no disponible")

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        heatmap = grad_cam(img_test, model=modelo_cargado)

        # Verificar que tiene 3 canales (RGB)
        assert heatmap.shape[2] == 3, "Debe tener 3 canales (RGB)"

        # Verificar que no es todo ceros
        assert heatmap.max() > 0, "Heatmap debe tener valores > 0"


class TestGradCAMConImagenReal:
    """Pruebas opcionales con imagen real (si existe)."""

    @pytest.mark.skipif(
        not os.path.exists('test/test_data/JPG/test_jpg_1.JPEG'),
        reason="Imágenes de prueba no disponibles"
    )
    def test_grad_cam_con_imagen_jpg_real(self, modelo_cargado):
        """
        Test: Grad-CAM con imagen JPG real
        Input: Imagen JPG real del test_data
        Output: Genera heatmap sin errores
        """
        if modelo_cargado is None:
            pytest.skip("Modelo no disponible")

        # Cargar imagen real
        import cv2
        img_real = cv2.imread('test/test_data/JPG/test_jpg_1.JPEG')

        # Ejecutar con imagen real
        heatmap = grad_cam(img_real, model=modelo_cargado)

        # Verificaciones
        assert heatmap.shape == (512, 512, 3)
        assert heatmap.dtype == np.uint8
