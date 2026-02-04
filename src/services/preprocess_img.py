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
    """Preprocesa una imagen radiográfica para inferencia del modelo CNN.

    Aplica una secuencia de transformaciones para convertir una imagen de entrada
    de cualquier tamaño y formato a la representación específica requerida por el
    modelo de clasificación de neumonía. El proceso garantiza que la imagen tenga
    las dimensiones, contraste, escala y formato correctos.

    La pipeline de transformación consiste en:
        1. **Redimensionamiento**: Escala la imagen a 512×512 píxeles usando
           interpolación bilineal (comportamiento por defecto de cv2.resize).
        2. **Conversión a escala de grises**: Transforma la imagen RGB/BGR a un
           canal único usando la conversión estándar de OpenCV.
        3. **Ecualización CLAHE**: Aplica Contrast Limited Adaptive Histogram
           Equalization para mejorar el contraste local, especialmente útil en
           radiografías donde ciertas estructuras pueden tener bajo contraste.
        4. **Normalización**: Escala los valores de píxel del rango [0, 255] a
           [0.0, 1.0] dividiendo por 255.0.
        5. **Expansión de dimensiones**: Agrega dimensión de canal y dimensión
           de batch para cumplir con el formato tensor (batch, height, width, channels).

    Args:
        array (numpy.ndarray): Array de imagen en formato RGB o BGR. Puede ser de
            cualquier tamaño (height, width, 3). Dtype típicamente uint8 con valores
            en rango [0, 255]. También acepta imágenes ya en escala de grises
            (height, width), aunque la conversión BGR2GRAY puede fallar en ese caso.

    Returns:
        numpy.ndarray: Array preprocesado con forma (1, 512, 512, 1) y dtype float32
            o float64. Los valores están normalizados en el rango [0.0, 1.0]. Listo
            para ser usado como entrada al método model.predict().

    Raises:
        cv2.error: Si la imagen de entrada está vacía o tiene dimensiones inválidas
            que impiden el redimensionamiento o la conversión de color.
        ValueError: Si el array de entrada no tiene el número correcto de dimensiones.
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
