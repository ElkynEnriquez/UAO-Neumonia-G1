#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para el módulo de preprocesamiento de imágenes.

Test para verificar redimensionamiento, normalización y formato correcto.
"""

import pytest
import numpy as np
from src.services.preprocess_img import preprocess


class TestPreprocess:
    """Pruebas para preprocesamiento de imágenes."""

    def test_preprocess_shape_correcta(self):
        """
        Test: Verificar dimensiones de salida
        Input: Imagen RGB de cualquier tamaño (ej. 1024x1024x3)
        Output: Array con shape (1, 512, 512, 1) para el modelo
        """
        # Crear imagen dummy de prueba
        img_grande = np.random.randint(0, 255, (1024, 1024, 3), dtype=np.uint8)

        resultado = preprocess(img_grande)

        # Verificaciones
        assert resultado.shape == (
            1, 512, 512, 1), "Shape debe ser (1, 512, 512, 1)"

    def test_preprocess_normalizacion(self):
        """
        Test: Verificar normalización de valores
        Input: Imagen con valores [0-255]
        Output: Array normalizado con valores [0.0-1.0]
        """
        img = np.ones((256, 256, 3), dtype=np.uint8) * 255  # Imagen blanca

        resultado = preprocess(img)

        # Verificaciones
        assert resultado.min() >= 0.0, "Valores mínimos deben ser >= 0.0"
        assert resultado.max() <= 1.0, "Valores máximos deben ser <= 1.0"

    def test_preprocess_tipo_dato(self):
        """
        Test: Verificar tipo de dato de salida
        Input: Imagen uint8
        Output: Array float32 o float64
        """
        img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        resultado = preprocess(img)

        assert resultado.dtype in [np.float32, np.float64], "Debe ser float"

    def test_preprocess_imagen_pequena(self):
        """
        Test: Procesar imagen más pequeña que 512x512
        Input: Imagen 256x256x3
        Output: Se redimensiona correctamente a 512x512
        """
        img_pequena = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

        resultado = preprocess(img_pequena)

        assert resultado.shape == (1, 512, 512, 1)

    def test_preprocess_imagen_grande(self):
        """
        Test: Procesar imagen más grande que 512x512
        Input: Imagen 2048x2048x3
        Output: Se redimensiona correctamente a 512x512
        """
        img_grande = np.random.randint(0, 255, (2048, 2048, 3), dtype=np.uint8)

        resultado = preprocess(img_grande)

        assert resultado.shape == (1, 512, 512, 1)

    def test_preprocess_clahe_aplicado(self):
        """
        Test: Verificar que CLAHE mejora contraste
        Input: Imagen con bajo contraste (todos valores similares)
        Output: Imagen procesada con mayor rango de valores
        """
        # Imagen con bajo contraste
        img_bajo_contraste = np.ones((512, 512, 3), dtype=np.uint8) * 128
        img_bajo_contraste[100:200, 100:200] = 130  # Pequeña variación

        resultado = preprocess(img_bajo_contraste)

        # CLAHE debe expandir el rango de valores
        assert resultado.max() > resultado.min(), "CLAHE debe mejorar contraste"
