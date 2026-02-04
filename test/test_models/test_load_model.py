#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para carga del modelo de deep learning.

Test para verificar carga correcta del modelo y manejo de errores.
"""

from unittest.mock import patch, MagicMock
import pytest
from src.models.load_model import load_model, model_fun


class TestLoadModel:
    """Pruebas para carga del modelo CNN."""

    def test_archivo_modelo_no_existe(self):
        """
        Test: Intentar cargar modelo que no existe
        Input: Ruta a archivo .h5 inexistente
        Output: Debe lanzar FileNotFoundError
        """
        with pytest.raises(FileNotFoundError, match="No se encontró el archivo del modelo"):
            load_model('modelo_falso_que_no_existe.h5')

    @patch('src.models.load_model.tf.keras.models.load_model')
    @patch('src.models.load_model.os.path.exists')
    def test_carga_exitosa_con_mock(self, mock_exists, mock_tf_load):
        """
        Test: Cargar modelo exitosamente (usando mock)
        Input: Ruta válida a modelo .h5
        Output: Retorna objeto modelo de Keras
        """
        # Configurar mocks
        mock_exists.return_value = True
        mock_modelo = MagicMock()
        mock_modelo.input_shape = (None, 512, 512, 1)
        mock_tf_load.return_value = mock_modelo

        # Ejecutar
        modelo = load_model('data/models/conv_MLP_84.h5')

        # Verificaciones
        assert modelo is not None, "Debe retornar un modelo"
        assert modelo.input_shape == (None, 512, 512, 1)
        mock_tf_load.assert_called_once()

    @patch('src.models.load_model.tf.keras.models.load_model')
    @patch('src.models.load_model.os.path.exists')
    def test_carga_con_compile_false(self, mock_exists, mock_tf_load):
        """
        Test: Verificar que se carga con compile=False
        Input: Ruta a modelo
        Output: TensorFlow load_model se llama con compile=False
        """
        mock_exists.return_value = True
        mock_modelo = MagicMock()
        mock_tf_load.return_value = mock_modelo

        load_model('test_model.h5')

        # Verificar que se intentó cargar con compile=False
        llamadas = mock_tf_load.call_args_list
        assert any('compile' in str(call) for call in llamadas), \
            "Debe intentar cargar con compile=False"

    def test_model_fun_usa_ruta_por_defecto(self):
        """
        Test: Función de compatibilidad model_fun()
        Input: Sin argumentos
        Output: Llama a load_model con ruta por defecto
        """
        with patch('src.models.load_model.load_model') as mock_load:
            mock_load.return_value = MagicMock()

            model_fun()

            mock_load.assert_called_once_with('data/models/conv_MLP_84.h5')


class TestLoadModelReal:
    """Pruebas con el modelo real (si existe)."""

    @pytest.mark.skipif(
        not __import__('os').path.exists('data/models/conv_MLP_84.h5'),
        reason="Modelo real no disponible"
    )
    def test_cargar_modelo_real(self):
        """
        Test: Cargar el modelo real del proyecto
        Input: Ruta al modelo real conv_MLP_84.h5
        Output: Modelo se carga correctamente y tiene estructura esperada

        Nota: Este test solo se ejecuta si el modelo existe.
        """
        modelo = load_model('data/models/conv_MLP_84.h5')

        # Verificaciones básicas
        assert modelo is not None
        assert hasattr(modelo, 'predict'), "Modelo debe tener método predict"
        assert modelo.input_shape[1:] == (512, 512, 1), \
            "Input shape debe ser (512, 512, 1)"
