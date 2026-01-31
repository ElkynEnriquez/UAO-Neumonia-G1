#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para preprocesar imágenes antes de la predicción.
Realiza las siguientes transformaciones:
- Resize a 512x512
- Conversión a escala de grises
- Ecualización del histograma con CLAHE
- Normalización entre 0 y 1
- Conversión a formato batch (tensor)
"""

import cv2
import numpy as np


def preprocess(array):
    """
    Preprocesa una imagen para que sea compatible con el modelo de CNN.
    
    Args:
        array (numpy.ndarray): Array de imagen en formato RGB o BGR
    
    Returns:
        numpy.ndarray: Array preprocesado en formato batch (1, 512, 512, 1)
    
    Procesamiento realizado:
        1. Redimensiona a 512x512
        2. Convierte a escala de grises
        3. Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization)
        4. Normaliza valores entre 0 y 1
        5. Agrega dimensión de canal y batch
    """
    # 1. Redimensionar a 512x512
    array = cv2.resize(array, (512, 512))
    
    # 2. Convertir a escala de grises
    array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    
    # 3. Aplicar CLAHE para mejorar el contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    array = clahe.apply(array)
    
    # 4. Normalizar entre 0 y 1
    array = array / 255.0
    
    # 5. Agregar dimensión de canal (512, 512) -> (512, 512, 1)
    array = np.expand_dims(array, axis=-1)
    
    # 6. Agregar dimensión de batch (512, 512, 1) -> (1, 512, 512, 1)
    array = np.expand_dims(array, axis=0)
    
    return array
