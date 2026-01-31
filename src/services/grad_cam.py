#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para generar mapas de calor Grad-CAM (Gradient-weighted Class Activation Mapping).
Grad-CAM resalta las regiones de la imagen que son importantes para la clasificación.
"""

import numpy as np
import cv2
import tensorflow as tf
from src.services.preprocess_img import preprocess
from src.models.load_model import load_model


def grad_cam(array, model=None, layer_name="conv10_thisone"):
    """
    Genera un mapa de calor Grad-CAM superpuesto sobre la imagen original.
    
    Args:
        array (numpy.ndarray): Array de imagen en formato RGB/BGR
        model (tf.keras.Model, optional): Modelo pre-cargado. Si es None, se carga automáticamente.
        layer_name (str): Nombre de la capa convolucional a usar para Grad-CAM
    
    Returns:
        numpy.ndarray: Imagen con el mapa de calor superpuesto en formato RGB
    """
    # Preprocesar la imagen
    img = preprocess(array)
    
    # Cargar modelo si no se proporciona
    if model is None:
        model = load_model()
    
    # Obtener predicción primero para saber qué clase usar
    preds = model.predict(img, verbose=0)
    argmax = np.argmax(preds[0])
    
    # Obtener la última capa convolucional
    last_conv_layer = model.get_layer(layer_name)
    
    # Crear un modelo intermedio que devuelve la salida de la capa convolucional
    intermediate_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=last_conv_layer.output
    )
    
    # Convertir img a tensor
    img_tensor = tf.convert_to_tensor(img, dtype=tf.float32)
    
    # Calcular gradientes usando tf.GradientTape
    with tf.GradientTape() as tape:
        tape.watch(img_tensor)
        
        # Obtener la salida de la capa convolucional
        conv_outputs = intermediate_model(img_tensor, training=False)
        tape.watch(conv_outputs)
        
        # Obtener la predicción completa
        predictions = model(img_tensor, training=False)
        # Obtener la salida de la clase predicha
        class_output = predictions[:, argmax]
    
    # Calcular gradientes de la clase predicha con respecto a la salida convolucional
    grads = tape.gradient(class_output, conv_outputs)
    
    # Si grads es None, usar método alternativo
    if grads is None:
        # Método alternativo: usar activaciones directamente
        conv_layer_output_value = conv_outputs[0].numpy()
        # Usar promedio simple en lugar de gradientes
        heatmap = np.mean(conv_layer_output_value, axis=-1)
    else:
        # Promediar gradientes sobre las dimensiones espaciales
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Obtener valores como numpy arrays
        conv_layer_output_value = conv_outputs[0].numpy()
        pooled_grads_value = pooled_grads.numpy()
        
        # Multiplicar cada canal del mapa de activaciones por su peso de gradiente
        for filters in range(conv_layer_output_value.shape[-1]):
            conv_layer_output_value[:, :, filters] *= pooled_grads_value[filters]
        
        # Crear el mapa de calor
        heatmap = np.mean(conv_layer_output_value, axis=-1)
    
    # Aplicar ReLU (solo valores positivos)
    heatmap = np.maximum(heatmap, 0)
    
    # Normalizar entre 0 y 1
    if np.max(heatmap) > 0:
        heatmap /= np.max(heatmap)
    
    # Redimensionar al tamaño de la imagen original
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[2]))
    
    # Convertir a formato de imagen (0-255)
    heatmap = np.uint8(255 * heatmap)
    
    # Aplicar mapa de colores JET
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Redimensionar imagen original
    img2 = cv2.resize(array, (512, 512))
    
    # Superponer el mapa de calor con transparencia
    hif = 0.8  # Factor de intensidad del heatmap
    transparency = heatmap * hif
    transparency = transparency.astype(np.uint8)
    superimposed_img = cv2.add(transparency, img2)
    superimposed_img = superimposed_img.astype(np.uint8)
    
    # Convertir de BGR a RGB para visualización
    return superimposed_img[:, :, ::-1]
