#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de generación de reportes y resultados.
Proporciona funciones compartidas para generar CSV, PDF y reportes de predicción.
Reutilizable desde GUI y CLI.
"""

import os
import csv
from pathlib import Path
from PIL import Image
from datetime import datetime


def save_results_csv(patient_id, label, probability, filepath="historial.csv"):
    """
    Guarda los resultados de una predicción en un archivo CSV.
    
    Args:
        patient_id (str): ID del paciente
        label (str): Etiqueta de la predicción (ej: "bacteriana", "normal", "viral")
        probability (float): Probabilidad de la predicción (0-100)
        filepath (str): Ruta del archivo CSV
    
    Returns:
        bool: True si se guardó exitosamente, False en caso de error
    """
    try:
        # Crear directorio si no existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        file_exists = os.path.isfile(filepath)
        
        with open(filepath, "a", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            
            # Escribir encabezados si el archivo está vacío
            if not file_exists:
                writer.writerow(["Fecha", "Hora", "Cédula Paciente", "Diagnóstico", "Probabilidad"])
            
            # Escribir datos
            now = datetime.now()
            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                patient_id or "N/A",
                label,
                f"{probability:.2f}%"
            ])
        
        return True
    except Exception as e:
        print(f"Error al guardar CSV: {str(e)}")
        return False


def generate_pdf_report(patient_id, label, probability, heatmap_array=None, 
                       output_dir="report", report_id=0):
    """
    Genera un PDF con el reporte de predicción.
    
    Args:
        patient_id (str): ID del paciente
        label (str): Etiqueta de la predicción
        probability (float): Probabilidad de la predicción (0-100)
        heatmap_array (numpy.ndarray, optional): Array del heatmap Grad-CAM
        output_dir (str): Directorio de salida
        report_id (int): Número de reporte para el nombre del archivo
    
    Returns:
        tuple: (success: bool, filepath: str)
    """
    try:
        # Crear directorio si no existe
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
        except ImportError:
            return False, "reportlab no está instalado. Instale con: pip install reportlab"
        
        pdf_filename = f"Reporte_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        # Encabezado
        c.setFont("Helvetica-Bold", 18)
        c.drawString(0.5 * inch, height - 0.5 * inch, 
                    "Reporte de Diagnóstico - Detector de Neumonía")
        
        # Línea separadora
        c.setLineWidth(1)
        c.line(0.5 * inch, height - 0.65 * inch, width - 0.5 * inch, height - 0.65 * inch)
        
        # Información del paciente y resultados
        c.setFont("Helvetica", 12)
        y_position = height - 1.2 * inch
        
        c.drawString(0.5 * inch, y_position, f"Cédula del Paciente: {patient_id or 'N/A'}")
        y_position -= 0.3 * inch
        
        c.drawString(0.5 * inch, y_position, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
        y_position -= 0.3 * inch
        
        c.drawString(0.5 * inch, y_position, f"Hora: {datetime.now().strftime('%H:%M:%S')}")
        y_position -= 0.5 * inch
        
        # Resultados
        c.setFont("Helvetica-Bold", 14)
        c.drawString(0.5 * inch, y_position, "RESULTADO:")
        y_position -= 0.3 * inch
        
        c.setFont("Helvetica", 12)
        diagnosis_text = label.upper()
        c.drawString(0.7 * inch, y_position, f"Diagnóstico: {diagnosis_text}")
        y_position -= 0.3 * inch
        
        c.drawString(0.7 * inch, y_position, f"Probabilidad: {probability:.2f}%")
        y_position -= 0.5 * inch
        
        # Incluir heatmap si está disponible
        if heatmap_array is not None:
            try:
                heatmap_img = Image.fromarray(heatmap_array)
                temp_heatmap = os.path.join(output_dir, f"temp_heatmap_{report_id}.png")
                heatmap_img.save(temp_heatmap)
                
                c.setFont("Helvetica-Bold", 12)
                c.drawString(0.5 * inch, y_position, "Mapa de Calor (Grad-CAM):")
                y_position -= 0.3 * inch
                
                # Dibujar imagen (máximo 4 pulgadas de ancho)
                c.drawImage(temp_heatmap, 0.5 * inch, y_position - 3 * inch, 
                           width=4 * inch, height=4 * inch, preserveAspectRatio=True)
                
                # Limpiar archivo temporal
                if os.path.exists(temp_heatmap):
                    os.remove(temp_heatmap)
            except Exception as e:
                c.setFont("Helvetica", 10)
                c.drawString(0.5 * inch, y_position, f"Nota: No se pudo incluir el heatmap ({str(e)})")
        
        # Footer
        c.setFont("Helvetica", 9)
        c.drawString(0.5 * inch, 0.4 * inch, 
                    "Este reporte fue generado automáticamente por el Sistema de Detección de Neumonía")
        
        c.save()
        return True, pdf_path
    
    except Exception as e:
        return False, f"Error al generar PDF: {str(e)}"


def format_prediction_output(label, probability):
    """
    Formatea el resultado de la predicción para salida en consola.
    
    Args:
        label (str): Etiqueta de la predicción
        probability (float): Probabilidad (0-100)
    
    Returns:
        str: Texto formateado
    """
    diagnosis_map = {
        "bacteriana": "NEUMONÍA BACTERIANA",
        "viral": "NEUMONÍA VIRAL",
        "normal": "NORMAL",
    }
    
    diagnosis_text = diagnosis_map.get(label, label.upper())
    return f"\n{'='*50}\nDIAGNÓSTICO: {diagnosis_text}\nPROBABILIDAD: {probability:.2f}%\n{'='*50}\n"
