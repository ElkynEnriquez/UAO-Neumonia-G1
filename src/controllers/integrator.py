#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo integrador que combina todos los módulos del proyecto.
Proporciona una interfaz unificada para realizar predicciones completas.
"""

import numpy as np
from src.models.load_model import load_model
from src.services.preprocess_img import preprocess
from src.services.grad_cam import grad_cam


def predict(array, model=None):
    """Realiza predicción completa de neumonía con visualización Grad-CAM.

    Ejecuta el pipeline de predicción: preprocesa la imagen, carga el modelo CNN,
    clasifica el tipo de neumonía, y genera un mapa de calor que resalta las
    zonas de la radiografía relevantes para el diagnóstico.

    Args:
        array (numpy.ndarray): Imagen de radiografía en formato RGB o BGR de
            cualquier tamaño. Se redimensionará automáticamente a 512x512.
        model (tf.keras.Model, optional): Modelo Keras pre-cargado. Si es None,
            se carga desde 'data/models/conv_MLP_84.h5'. Recomendado pre-cargar
            para múltiples predicciones.

    Returns:
        tuple: Tupla con tres elementos (label, proba, heatmap):
            - label (str): Clasificación predicha: "bacteriana" (neumonía
              bacteriana), "normal" (sin neumonía), "viral" (neumonía viral),
              o "desconocido" (error).
            - proba (float): Confianza de la predicción en porcentaje (0-100).
            - heatmap (numpy.ndarray): Imagen RGB 512x512 con mapa de calor
              superpuesto. Zonas rojas indican alta relevancia.

    Raises:
        RuntimeError: Si ocurre error en preprocesamiento, carga del modelo,
            inferencia o generación del Grad-CAM.

    Example:
        Uso básico:

        >>> import cv2
        >>> from src.controllers.integrator import predict
        >>> img = cv2.imread('radiografia.jpg')
        >>> diagnostico, confianza, mapa_calor = predict(img)
        >>> print(f"Resultado: {diagnostico} - Confianza: {confianza:.1f}%")
        Resultado: normal - Confianza: 94.3%

    Note:
        El modelo clasifica en 3 categorías (índice 0=bacteriana, 1=normal, 2=viral).
        Para mejor rendimiento, pre-cargue el modelo y páselo en cada llamada.
    """

    try:
        # 1. Preprocesar la imagen
        batch_array_img = preprocess(array)

        # 2. Cargar modelo si no se proporciona
        if model is None:
            model = load_model()

        # 3. Realizar predicción
        prediction_probs = model.predict(batch_array_img, verbose=0)
        prediction = np.argmax(prediction_probs)
        proba = np.max(prediction_probs) * 100

        # 4. Mapear predicción a etiqueta
        label = ""
        if prediction == 0:
            label = "bacteriana"
        elif prediction == 1:
            label = "normal"
        elif prediction == 2:
            label = "viral"
        else:
            label = "desconocido"

        # 5. Generar mapa de calor Grad-CAM
        heatmap = grad_cam(array, model=model)

        return (label, proba, heatmap)

    except Exception as e:
        raise RuntimeError(f"Error durante la predicción: {str(e)}") from e
