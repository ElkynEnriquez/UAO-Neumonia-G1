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
    """
    Realiza una predicción completa: preprocesa la imagen, carga el modelo,
    obtiene la predicción y genera el mapa de calor Grad-CAM.
    
    Args:
        array (numpy.ndarray): Array de imagen en formato RGB/BGR
        model (tf.keras.Model, optional): Modelo pre-cargado. Si es None, se carga automáticamente.
    
    Returns:
        tuple: (label, proba, heatmap) donde:
            - label (str): Etiqueta de la clase predicha ("bacteriana", "normal", "viral")
            - proba (float): Probabilidad de la predicción en porcentaje (0-100)
            - heatmap (numpy.ndarray): Imagen con mapa de calor Grad-CAM superpuesto
    
    Raises:
        Exception: Si hay un error durante el procesamiento
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
        raise Exception(f"Error durante la predicción: {str(e)}")
