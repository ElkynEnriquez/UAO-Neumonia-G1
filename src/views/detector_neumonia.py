#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interfaz gráfica para la detección rápida de neumonía.
Utiliza los módulos modulares del proyecto para realizar predicciones.
"""

import os
from tkinter import Tk, StringVar, Text, END
from tkinter import ttk, font, filedialog
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image

# Importar módulos del proyecto
from src.services.read_img import read_image
from src.controllers.integrator import predict
from src.services.report_generator import save_results_csv, generate_pdf_report


class App:
    """Interfaz gráfica de usuario para detección de neumonía.

    Esta clase implementa una aplicación GUI basada en Tkinter que permite
    cargar imágenes médicas (DICOM, JPEG, PNG), ejecutar predicciones de
    neumonía utilizando un modelo de deep learning, visualizar mapas de
    calor (Grad-CAM), y generar reportes en formato CSV y PDF.

    Attributes:
        root (Tk): Ventana principal de la aplicación.
        patient_id (StringVar): Variable que almacena la cédula del paciente.
        result (StringVar): Variable para almacenar el resultado de la predicción.
        array (np.ndarray): Matriz numpy de la imagen cargada para el modelo.
        img1 (ImageTk.PhotoImage): Imagen original redimensionada para visualización.
        img2 (ImageTk.PhotoImage): Heatmap redimensionado para visualización.
        label (str): Etiqueta de clasificación ("Normal", "Neumonía Bacteriana", etc.).
        proba (float): Probabilidad de la predicción en porcentaje.
        heatmap (np.ndarray): Mapa de calor generado por Grad-CAM.
        report_id (int): Contador para generar nombres únicos de reportes PDF.
    """

    def __init__(self):
        """Inicializa la aplicación GUI y sus componentes.

        Crea la ventana principal, configura todos los widgets (etiquetas, botones,
        campos de entrada, áreas de imagen), define sus posiciones usando geometría
        absoluta, inicializa las variables de estado, y ejecuta el bucle principal
        de Tkinter.

        La ventana tiene un tamaño fijo de 815x560 píxeles y no es redimensionable.
        El foco inicial se establece en el campo de cédula del paciente.
        """
        self.root = Tk()
        self.root.title("Herramienta para la detección rápida de neumonía")

        # BOLD FONT
        fonti = font.Font(weight="bold")

        self.root.geometry("815x560")
        self.root.resizable(False, False)

        # LABELS
        self.lab1 = ttk.Label(
            self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Cédula Paciente:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        # STRING VARIABLES TO CONTAIN PATIENT ID AND RESULT
        self.patient_id = StringVar()
        self.result = StringVar()

        # INPUT BOXES
        self.text1 = ttk.Entry(
            self.root, textvariable=self.patient_id, width=10)

        # IMAGE INPUT BOXES
        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        # BUTTONS
        self.button1 = ttk.Button(
            self.root, text="Predecir", state="disabled", command=self.run_model
        )
        self.button2 = ttk.Button(
            self.root, text="Cargar Imagen", command=self.load_img_file
        )
        self.button3 = ttk.Button(
            self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(
            self.root, text="PDF", command=self.create_pdf)
        self.button6 = ttk.Button(
            self.root, text="Guardar", command=self.save_results_csv
        )

        # WIDGETS POSITIONS
        self.lab1.place(x=110, y=65)
        self.lab2.place(x=545, y=65)
        self.lab3.place(x=500, y=350)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=122, y=25)
        self.lab6.place(x=500, y=400)
        self.button1.place(x=220, y=460)
        self.button2.place(x=70, y=460)
        self.button3.place(x=670, y=460)
        self.button4.place(x=520, y=460)
        self.button6.place(x=370, y=460)
        self.text1.place(x=200, y=350)
        self.text2.place(x=610, y=350, width=90, height=30)
        self.text3.place(x=610, y=400, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=500, y=90)

        # FOCUS ON PATIENT ID
        self.text1.focus_set()

        # Variables de estado
        self.array = None
        self.img1 = None
        self.img2 = None
        self.label = None
        self.proba = None
        self.heatmap = None

        # NUMERO DE IDENTIFICACIÓN PARA GENERAR PDF
        self.report_id = 0

        # RUN LOOP
        self.root.mainloop()

    def load_img_file(self):
        """Carga un archivo de imagen médica desde el sistema de archivos.

        Abre un diálogo de selección de archivo que permite al usuario elegir
        imágenes en formatos DICOM (.dcm), JPEG (.jpeg, .jpg) o PNG (.png).
        Utiliza la función `read_image` del módulo services para detectar
        automáticamente el tipo de archivo y procesarlo adecuadamente.

        La imagen se redimensiona a 250x250 píxeles para visualización en la GUI
        y se habilita el botón de predicción tras una carga exitosa.

        Raises:
            Exception: Si ocurre un error al leer o procesar la imagen, se captura
                y se muestra un mensaje de error al usuario mediante un diálogo.
                Los errores pueden incluir: archivo corrupto, formato no válido,
                problemas de lectura de DICOM, etc.

        Note:
            Actualiza `self.array` con la matriz numpy para el modelo y `self.img1`
            con la imagen PIL redimensionada para visualización.
        """
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select image",
            filetypes=(
                ("DICOM", "*.dcm"),
                ("JPEG", "*.jpeg"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
                ("All files", "*.*"),
            ),
        )
        if filepath:
            try:
                # Usar la función unificada que detecta automáticamente el tipo de archivo
                self.array, img2show = read_image(filepath)

                # Redimensionar y convertir para visualización
                # Usar LANCZOS en lugar de ANTIALIAS (deprecado)
                # Redimensionar con filtro compatible
                self.img1 = img2show.resize((250, 250), RESAMPLE_LANCZOS)
                self.img1 = ImageTk.PhotoImage(self.img1)
                self.text_img1.image_create(END, image=self.img1)
                self.button1["state"] = "enabled"

            except Exception as e:
                showinfo(
                    title="Error",
                    message=f"Error al cargar la imagen:\n{str(e)}\n\nPor favor, verifique que el archivo sea válido."
                )

    def run_model(self):
        """Ejecuta el modelo de predicción de neumonía y muestra los resultados.

        Utiliza el controlador `predict` del módulo integrator para realizar
        la predicción completa: carga el modelo, preprocesa la imagen, ejecuta
        la inferencia, genera el mapa de calor Grad-CAM, y obtiene la etiqueta
        de clasificación con su probabilidad.

        Los resultados se muestran en la interfaz: el heatmap en el panel derecho,
        la etiqueta de clase en el campo de resultado, y la probabilidad formateada
        como porcentaje.

        Raises:
            Exception: Si ocurre un error durante la predicción (modelo no disponible,
                error en preprocesamiento, fallo en Grad-CAM, etc.), se captura y
                se muestra un mensaje al usuario.

        Note:
            Requiere que se haya cargado una imagen previamente.
        """
        try:
            if self.array is None:
                showinfo(
                    title="Error",
                    message="Por favor cargue una imagen primero."
                )
                return

            # Usar el módulo integrator para realizar la predicción completa
            self.label, self.proba, self.heatmap = predict(self.array)

            # Convertir heatmap a imagen PIL y redimensionar para visualización
            self.img2 = Image.fromarray(self.heatmap).resize(
                (250, 250), RESAMPLE_LANCZOS)
            self.img2 = ImageTk.PhotoImage(self.img2)

            # Limpiar campos antes de insertar nuevos valores
            self.text_img2.delete(1.0, END)
            self.text2.delete(1.0, END)
            self.text3.delete(1.0, END)

            # Mostrar resultados
            self.text_img2.image_create(END, image=self.img2)
            self.text2.insert(END, self.label)
            self.text3.insert(END, f"{self.proba:.2f}%")

        except Exception as e:
            showinfo(
                title="Error",
                message=f"Error al procesar la imagen:\n{str(e)}\n\nPor favor, verifique que el modelo esté disponible."
            )

    def save_results_csv(self):
        """Guarda los resultados de la predicción en un archivo CSV.

        Añade una nueva fila al archivo `historial.csv` con la información de:
        - Cédula del paciente (o "N/A" si está vacío)
        - Etiqueta de clasificación
        - Probabilidad formateada con 2 decimales

        El archivo se abre en modo append para preservar registros anteriores.
        El delimitador utilizado es el guion ("-").

        Raises:
            Exception: Si ocurre un error de I/O al escribir el archivo (permisos,
                disco lleno, etc.), se captura y se notifica al usuario.

        Note:
            Requiere que exista una predicción previa (`self.label` y `self.proba`
            deben estar definidos).
        """
        try:
            if self.label is None or self.proba is None:
                showinfo(
                    title="Error",
                    message="No hay resultados para guardar. Por favor, realice una predicción primero."
                )
                return

            # Usar el servicio compartido de reportes
            if save_results_csv(
                patient_id=self.text1.get() or "N/A",
                label=self.label,
                probability=self.proba,
                filepath="historial.csv"
            ):
                showinfo(title="Guardar", message="Los datos se guardaron con éxito.")
            else:
                showinfo(title="Error", message="No se pudieron guardar los datos.")
        except Exception as e:
            showinfo(
                title="Error",
                message=f"Error al guardar los datos:\n{str(e)}"
            )

    def create_pdf(self):
        """Genera un PDF con el reporte de la predicción"""
        try:
            if self.label is None:
                showinfo(
                    title="Error",
                    message="No hay resultados para generar PDF. Por favor, realice una predicción primero."
                )
                return

            # Usar el servicio compartido de reportes
            success, result = generate_pdf_report(
                patient_id=self.text1.get() or "N/A",
                label=self.label,
                probability=self.proba,
                heatmap_array=self.heatmap,
                output_dir="report",
                report_id=self.reportID
            )
            
            if success:
                self.reportID += 1
                showinfo(title="PDF", message=f"El PDF fue generado con éxito:\n{result}")
            else:
                showinfo(title="Error", message=f"Error al generar PDF:\n{result}")
                
        except Exception as e:
            showinfo(
                title="Error",
                message=f"Error al generar el PDF:\n{str(e)}"
            )

    def delete(self):
        """Limpia todos los campos y resetea el estado de la aplicación.

        Solicita confirmación al usuario mediante un diálogo. Si se confirma,
        borra:
        - Todos los campos de texto (cédula, resultado, probabilidad)
        - Las imágenes mostradas (original y heatmap)
        - Todas las variables de estado (array, img1, img2, label, proba, heatmap)

        También deshabilita el botón de predicción hasta que se cargue una
        nueva imagen.

        Note:
            Esta operación no elimina archivos ni registros guardados, solo
            limpia la interfaz y el estado en memoria.
        """
        answer = askokcancel(
            title="Confirmación",
            message="Se borrarán todos los datos.",
            icon=WARNING
        )
        if answer:
            # Limpiar campos de texto
            self.text1.delete(0, "end")
            self.text2.delete(1.0, "end")
            self.text3.delete(1.0, "end")

            # Limpiar imágenes
            self.text_img1.delete(1.0, "end")
            self.text_img2.delete(1.0, "end")

            # Resetear variables
            self.array = None
            self.img1 = None
            self.img2 = None
            self.label = None
            self.proba = None
            self.heatmap = None

            # Deshabilitar botón de predicción
            self.button1["state"] = "disabled"

            showinfo(title="Borrar", message="Los datos se borraron con éxito")


def main():
    """Función principal que inicia la aplicación.

    Crea una instancia de la clase App, lo que inicializa la interfaz
    gráfica y ejecuta el bucle principal de eventos de Tkinter.

    Returns:
        int: Código de salida 0 indicando ejecución exitosa.

    Example:
        Ejecutar desde línea de comandos:

        >>> python -m src.views.detector_neumonia

        O importar y ejecutar:

        >>> from src.views.detector_neumonia import main
        >>> main()
        0
    """
    App()
    return 0


if __name__ == "__main__":
    main()
