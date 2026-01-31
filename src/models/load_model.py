#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para cargar el modelo de red neuronal convolucional pre-entrenado.
"""

import tensorflow as tf
import os


def load_model(model_path='data/models/conv_MLP_84.h5'):
    """
    Carga el modelo de red neuronal convolucional desde un archivo .h5
    
    Args:
        model_path (str): Ruta al archivo del modelo. Por defecto 'data/models/conv_MLP_84.h5'
    
    Returns:
        tf.keras.Model: Modelo cargado de TensorFlow/Keras
    
    Raises:
        FileNotFoundError: Si el archivo del modelo no existe
        Exception: Si hay un error al cargar el modelo
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"No se encontró el archivo del modelo: {model_path}\n"
            f"Asegúrate de que el archivo existe en el directorio especificado."
        )
    
    try:
        # TensorFlow 2.x requiere eager execution por defecto
        # NO deshabilitar eager execution - esto causa errores con tf.data.Dataset
        # Asegurar que eager execution esté habilitado
        if not tf.executing_eagerly():
            tf.config.run_functions_eagerly(True)
        
        # Cargar el modelo con compile=False para evitar problemas de compatibilidad
        # con parámetros obsoletos como reduction='auto'
        try:
            model = tf.keras.models.load_model(model_path, compile=False)
        except Exception as first_error:
            # Si falla, intentar con custom_objects vacío
            try:
                custom_objects = {}
                model = tf.keras.models.load_model(
                    model_path, 
                    compile=False,
                    custom_objects=custom_objects
                )
            except Exception as second_error:
                # Último intento: cargar sin compile=False
                model = tf.keras.models.load_model(model_path)
        
        return model
    except Exception as e:
        raise Exception(f"Error al cargar el modelo {model_path}: {str(e)}")


# Función de compatibilidad con el código anterior
def model_fun():
    """
    Función de compatibilidad que carga el modelo por defecto.
    Esta función mantiene la compatibilidad con el código existente.
    
    Returns:
        tf.keras.Model: Modelo cargado
    """
    return load_model('data/models/conv_MLP_84.h5')
