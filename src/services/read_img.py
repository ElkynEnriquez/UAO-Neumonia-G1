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
    """Lee un archivo DICOM y lo convierte a formato RGB.

    Procesa un archivo DICOM médico extrayendo el array de píxeles, normalizando
    los valores y convirtiéndolo a formato RGB para su uso en el modelo de predicción
    y visualización en la interfaz gráfica.

    Args:
        path (str): Ruta absoluta o relativa al archivo DICOM (.dcm).

    Returns:
        tuple: Una tupla de dos elementos:
            - img_RGB (numpy.ndarray): Array en formato RGB con shape (H, W, 3)
              y dtype uint8, normalizado al rango [0, 255]. Listo para
              procesamiento por el modelo.
            - img2show (PIL.Image): Objeto Image de PIL/Pillow en escala de grises,
              listo para visualización en widgets de tkinter.

    Raises:
        FileNotFoundError: Si el archivo especificado no existe en la ruta.
        RuntimeError: Si ocurre un error al leer o procesar el archivo DICOM
            (formato inválido, archivo corrupto, etc.).

    Example:
        >>> from src.services.read_img import read_dicom_file
        >>> img_array, img_pil = read_dicom_file('data/DICOM/radiografia.dcm')
        >>> print(img_array.shape)  # (512, 512, 3)
        >>> print(type(img_pil))     # <class 'PIL.Image.Image'>
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
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No se encontró el archivo: {path}") from e
    except Exception as e:
        raise RuntimeError(
            f"Error al leer archivo DICOM {path}: {str(e)}") from e


def read_jpg_file(path):
    """Lee un archivo de imagen JPEG/PNG y lo prepara para procesamiento.

    Carga imágenes en formatos comunes (JPEG, PNG) usando OpenCV, normaliza los
    valores de píxeles y prepara tanto el array numpy como el objeto PIL para
    procesamiento y visualización.

    Args:
        path (str): Ruta absoluta o relativa al archivo de imagen (.jpeg, .jpg, .png).

    Returns:
        tuple: Una tupla de dos elementos:
            - img_array (numpy.ndarray): Array normalizado con shape (H, W, 3)
              y dtype uint8 en rango [0, 255]. Listo para procesamiento.
            - img2show (PIL.Image): Objeto Image de PIL/Pillow, listo para
              visualización en widgets de tkinter.

    Raises:
        FileNotFoundError: Si el archivo especificado no existe en la ruta.
        RuntimeError: Si ocurre un error al leer la imagen (formato no válido,
            archivo corrupto, etc.) o si cv2.imread retorna None.

    Example:
        >>> from src.services.read_img import read_jpg_file
        >>> img_array, img_pil = read_jpg_file('data/JPG/normal/imagen.jpg')
        >>> print(img_array.shape)  # (1024, 1024, 3)
        >>> img_pil.show()  # Muestra la imagen en el visor por defecto
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
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No se encontró el archivo: {path}") from e
    except Exception as e:
        raise RuntimeError(
            f"Error al leer archivo de imagen {path}: {str(e)}") from e


def read_image(path):
    """Detecta automáticamente el formato y lee la imagen con la función apropiada.

    Función de conveniencia que examina la extensión del archivo y delega la
    lectura a read_dicom_file() o read_jpg_file() según corresponda. Simplifica
    el código del cliente al no requerir verificación manual del tipo de archivo.

    Args:
        path (str): Ruta al archivo de imagen. Puede ser DICOM (.dcm), JPEG
            (.jpeg, .jpg) o PNG (.png).

    Returns:
        tuple: Una tupla (img_array, img2show) cuyo contenido depende del tipo
            de archivo detectado. Ver read_dicom_file() o read_jpg_file() para
            detalles específicos.

    Raises:
        ValueError: Si la extensión del archivo no corresponde a ningún formato
            soportado (.dcm, .jpeg, .jpg, .png).
        FileNotFoundError: Si el archivo no existe (propagado desde las funciones
            de lectura específicas).
        RuntimeError: Si hay error al procesar el archivo (propagado desde las
            funciones de lectura específicas).

    Example:
        >>> from src.services.read_img import read_image
        >>> # Funciona con cualquier formato soportado
        >>> img1, pil1 = read_image('imagen.dcm')
        >>> img2, pil2 = read_image('imagen.jpg')
        >>> img3, pil3 = read_image('imagen.png')

    Note:
        Esta es la función recomendada para uso general, ya que maneja
        automáticamente diferentes formatos sin requerir lógica adicional.
    """
    path_lower = path.lower()

    if path_lower.endswith('.dcm'):
        return read_dicom_file(path)
    if path_lower.endswith(('.jpeg', '.jpg', '.png')):
        return read_jpg_file(path)

    raise ValueError(
        f"Formato de archivo no soportado: {path}\n"
        f"Formatos soportados: .dcm, .jpeg, .jpg, .png"
    )
