#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para el controlador integrador (predict).

Test del pipeline completo de predicción con mocks.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.controllers.integrator import predict


class TestPredictConMocks:
    """Pruebas del pipeline de predicción usando mocks."""

    @patch('src.controllers.integrator.grad_cam')
    @patch('src.controllers.integrator.load_model')
    @patch('src.controllers.integrator.preprocess')
    def test_predict_neumonia_normal(self, mock_preprocess, mock_load_model, mock_grad_cam):
        """
        Test: Predicción de radiografía normal
        Input: Imagen de radiografía (array numpy)
        Output: label='normal', proba alta (>50%), heatmap válido
        """
        # Configurar mocks
        mock_preprocess.return_value = np.zeros((1, 512, 512, 1))

        mock_modelo = MagicMock()
        # Simular predicción: [bacteriana=0.05, normal=0.90, viral=0.05]
        mock_modelo.predict.return_value = np.array([[0.05, 0.90, 0.05]])
        mock_load_model.return_value = mock_modelo

        mock_grad_cam.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        # Ejecutar predicción
        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        label, proba, heatmap = predict(img_test)

        # Verificaciones
        assert label == 'normal', "Debe clasificar como 'normal'"
        assert proba == 90.0, "Probabilidad debe ser 90%"
        assert isinstance(heatmap, np.ndarray), "Heatmap debe ser numpy array"
        assert heatmap.shape == (512, 512, 3), "Heatmap debe ser 512x512x3"

    @patch('src.controllers.integrator.grad_cam')
    @patch('src.controllers.integrator.load_model')
    @patch('src.controllers.integrator.preprocess')
    def test_predict_neumonia_bacteriana(self, mock_preprocess, mock_load_model, mock_grad_cam):
        """
        Test: Predicción de neumonía bacteriana
        Input: Imagen de radiografía
        Output: label='bacteriana', proba alta
        """
        mock_preprocess.return_value = np.zeros((1, 512, 512, 1))

        mock_modelo = MagicMock()
        # Simular predicción bacteriana: [0.85, 0.10, 0.05]
        mock_modelo.predict.return_value = np.array([[0.85, 0.10, 0.05]])
        mock_load_model.return_value = mock_modelo

        mock_grad_cam.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        label, proba, heatmap = predict(img_test)

        assert label == 'bacteriana'
        assert proba == 85.0

    @patch('src.controllers.integrator.grad_cam')
    @patch('src.controllers.integrator.load_model')
    @patch('src.controllers.integrator.preprocess')
    def test_predict_neumonia_viral(self, mock_preprocess, mock_load_model, mock_grad_cam):
        """
        Test: Predicción de neumonía viral
        Input: Imagen de radiografía
        Output: label='viral', proba alta
        """
        mock_preprocess.return_value = np.zeros((1, 512, 512, 1))

        mock_modelo = MagicMock()
        # Simular predicción viral: [0.05, 0.15, 0.80]
        mock_modelo.predict.return_value = np.array([[0.05, 0.15, 0.80]])
        mock_load_model.return_value = mock_modelo

        mock_grad_cam.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        label, proba, heatmap = predict(img_test)

        assert label == 'viral'
        assert proba == 80.0

    @patch('src.controllers.integrator.grad_cam')
    @patch('src.controllers.integrator.load_model')
    @patch('src.controllers.integrator.preprocess')
    def test_predict_llama_funciones_correctamente(self, mock_preprocess, mock_load_model, mock_grad_cam):
        """
        Test: Verificar que se llaman todas las funciones del pipeline
        Input: Imagen cualquiera
        Output: Se llaman preprocess, load_model, predict y grad_cam
        """
        mock_preprocess.return_value = np.zeros((1, 512, 512, 1))

        mock_modelo = MagicMock()
        mock_modelo.predict.return_value = np.array([[0.1, 0.8, 0.1]])
        mock_load_model.return_value = mock_modelo

        mock_grad_cam.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        predict(img_test)

        # Verificar que se llamaron todas las funciones
        mock_preprocess.assert_called_once()
        mock_load_model.assert_called_once()
        mock_modelo.predict.assert_called_once()
        mock_grad_cam.assert_called_once()

    @patch('src.controllers.integrator.grad_cam')
    @patch('src.controllers.integrator.load_model')
    @patch('src.controllers.integrator.preprocess')
    def test_predict_con_modelo_precargado(self, mock_preprocess, mock_load_model, mock_grad_cam):
        """
        Test: Usar modelo ya cargado (no cargar de nuevo)
        Input: Imagen + modelo pre-cargado
        Output: No se llama a load_model, usa el modelo pasado
        """
        mock_preprocess.return_value = np.zeros((1, 512, 512, 1))
        mock_grad_cam.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        # Modelo pre-cargado
        modelo_existente = MagicMock()
        modelo_existente.predict.return_value = np.array([[0.1, 0.7, 0.2]])

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        label, proba, heatmap = predict(img_test, model=modelo_existente)

        # Verificar que NO se llamó a load_model
        mock_load_model.assert_not_called()
        # Verificar que se usó el modelo pasado
        modelo_existente.predict.assert_called_once()

    @patch('src.controllers.integrator.preprocess')
    def test_predict_error_en_preprocesamiento(self, mock_preprocess):
        """
        Test: Manejo de error durante preprocesamiento
        Input: Imagen que causa error en preprocess
        Output: Debe lanzar RuntimeError con mensaje descriptivo
        """
        # Simular error en preprocess
        mock_preprocess.side_effect = Exception("Error al procesar imagen")

        img_test = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with pytest.raises(RuntimeError, match="Error durante la predicción"):
            predict(img_test)


class TestPredictConImagenReal:
    """Pruebas con imágenes reales del test_data."""

    @pytest.mark.skipif(
        not __import__('os').path.exists('test/test_data/jpg/imagen1.jpg'),
        reason="Imágenes de prueba no disponibles"
    )
    @patch('src.controllers.integrator.grad_cam')
    @patch('src.controllers.integrator.load_model')
    def test_predict_con_imagen_jpg_real(self, mock_load_model, mock_grad_cam):
        """
        Test: Predicción con imagen JPG real del test_data
        Input: Imagen JPG real de test_data
        Output: Pipeline completo funciona con imagen real
        """
        # Cargar imagen real
        import cv2
        img_real = cv2.imread('test/test_data/jpg/imagen1.jpg')

        # Mock solo del modelo y grad_cam
        mock_modelo = MagicMock()
        mock_modelo.predict.return_value = np.array([[0.1, 0.8, 0.1]])
        mock_load_model.return_value = mock_modelo
        mock_grad_cam.return_value = np.zeros((512, 512, 3), dtype=np.uint8)

        # Ejecutar (usa preprocess real)
        label, proba, heatmap = predict(img_real)

        # Verificaciones básicas
        assert label in ['bacteriana', 'normal', 'viral']
        assert 0 <= proba <= 100
        assert heatmap.shape == (512, 512, 3)
