#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para cargar el modelo de red neuronal convolucional pre-entrenado.
"""

import os
import tensorflow as tf


def load_model(model_path='data/models/conv_MLP_84.h5'):
    """Carga el modelo de clasificación de neumonía desde un archivo .h5.

    Lee y carga un modelo de red neuronal convolucional pre-entrenado guardado en
    formato HDF5 (.h5). La función implementa múltiples estrategias de carga para
    garantizar compatibilidad con diferentes versiones de TensorFlow y configuraciones
    del modelo guardado.

    El proceso de carga incluye:
        1. Verificación de existencia del archivo
        2. Asegurar que eager execution esté habilitado
        3. Intentar carga con compile=False (recomendado)
        4. Fallback con custom_objects si falla el primer intento
        5. Último intento con configuración por defecto

    Args:
        model_path (str, optional): Ruta relativa o absoluta al archivo del modelo
            en formato .h5. Debe apuntar a un modelo Keras válido guardado con
            model.save(). Por defecto 'data/models/conv_MLP_84.h5'.

    Returns:
        tf.keras.Model: Modelo de Keras cargado y listo para hacer predicciones.
            El modelo retorna probabilidades para 3 clases: Normal, Neumonía
            Bacteriana, y Neumonía Viral.

    Raises:
        FileNotFoundError: Si el archivo especificado en model_path no existe en
            el sistema de archivos.
        RuntimeError: Si ocurre un error durante la carga del modelo. Esto puede
            incluir: archivo corrupto, formato inválido, incompatibilidad de versión
            de TensorFlow, o errores de memoria.

    Example:
        Uso básico con ruta por defecto:

        >>> from src.models.load_model import load_model
        >>> model = load_model()
        >>> print(model.input_shape)  # (None, 512, 512, 1)

        Uso con ruta personalizada:

        >>> model = load_model('models/mi_modelo.h5')
        >>> predictions = model.predict(img_array)
        >>> print(predictions[0])  # [0.95, 0.03, 0.02]

    Note:
        - La función carga el modelo con compile=False para evitar problemas con
          parámetros obsoletos en versiones antiguas de TensorFlow.
        - Eager execution se habilita automáticamente si está deshabilitado.
        - El modelo debe haber sido entrenado para imágenes de 512×512 píxeles
          en escala de grises.
        - Para uso en producción, considere cargar el modelo una sola vez y
          reutilizarlo para múltiples predicciones.
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
        except Exception:
            # Si falla, intentar con custom_objects vacío
            try:
                custom_objects = {}
                model = tf.keras.models.load_model(
                    model_path,
                    compile=False,
                    custom_objects=custom_objects
                )
            except Exception:
                # Último intento: cargar sin compile=False
                model = tf.keras.models.load_model(model_path)

        return model
    except Exception as e:
        raise RuntimeError(
            f"Error al cargar el modelo {model_path}: {str(e)}") from e


# Función de compatibilidad con el código anterior
def model_fun():
    """
    Función de compatibilidad que carga el modelo por defecto.
    Esta función mantiene la compatibilidad con el código existente.

    Returns:
        tf.keras.Model: Modelo cargado
    """
    return load_model('data/models/conv_MLP_84.h5')
