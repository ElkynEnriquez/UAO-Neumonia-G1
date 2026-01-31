#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para leer imágenes en formato DICOM, JPEG, JPG y PNG.
Convierte las imágenes a formatos compatibles para su procesamiento.
"""

import pydicom as dicom
import cv2
import numpy as np
from PIL import Image


def read_dicom_file(path):
    """
    Lee un archivo DICOM y lo convierte a formato RGB para visualización.
    
    Args:
        path (str): Ruta al archivo DICOM (.dcm)
    
    Returns:
        tuple: (img_RGB, img2show) donde:
            - img_RGB: Array numpy en formato RGB para procesamiento
            - img2show: Imagen PIL para visualización en la interfaz
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        Exception: Si hay un error al leer el archivo DICOM
    """
    try:
        # Usar dcmread en lugar de read_file (deprecado en pydicom 2.0+)
        try:
            img = dicom.dcmread(path)
        except AttributeError:
            # Fallback para versiones antiguas de pydicom
            img = dicom.read_file(path)
        img_array = img.pixel_array
        
        # Crear imagen PIL para visualización
        img2show = Image.fromarray(img_array)
        
        # Normalizar y convertir a RGB
        img2 = img_array.astype(float)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
        
        return img_RGB, img2show
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    except Exception as e:
        raise Exception(f"Error al leer archivo DICOM {path}: {str(e)}")


def read_jpg_file(path):
    """
    Lee un archivo de imagen (JPEG, JPG, PNG) y lo prepara para procesamiento.
    
    Args:
        path (str): Ruta al archivo de imagen (.jpeg, .jpg, .png)
    
    Returns:
        tuple: (img_array, img2show) donde:
            - img_array: Array numpy normalizado para procesamiento
            - img2show: Imagen PIL para visualización en la interfaz
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        Exception: Si hay un error al leer el archivo
    """
    try:
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"No se pudo leer la imagen: {path}")
        
        img_array = np.asarray(img)
        
        # Crear imagen PIL para visualización
        img2show = Image.fromarray(img_array)
        
        # Normalizar imagen
        img2 = img_array.astype(float)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        
        return img2, img2show
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    except Exception as e:
        raise Exception(f"Error al leer archivo de imagen {path}: {str(e)}")


def read_image(path):
    """
    Función unificada que detecta automáticamente el tipo de archivo
    y llama a la función de lectura apropiada.
    
    Args:
        path (str): Ruta al archivo de imagen
    
    Returns:
        tuple: (img_array, img2show) según el tipo de archivo
    
    Raises:
        ValueError: Si el formato de archivo no es soportado
    """
    path_lower = path.lower()
    
    if path_lower.endswith('.dcm'):
        return read_dicom_file(path)
    elif path_lower.endswith(('.jpeg', '.jpg', '.png')):
        return read_jpg_file(path)
    else:
        raise ValueError(
            f"Formato de archivo no soportado: {path}\n"
            f"Formatos soportados: .dcm, .jpeg, .jpg, .png"
        )
