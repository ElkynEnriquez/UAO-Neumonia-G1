#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interfaz gráfica para la detección rápida de neumonía.
Utiliza los módulos modulares del proyecto para realizar predicciones.
"""

from tkinter import *
from tkinter import ttk, font, filedialog, Entry, END
from tkinter.messagebox import askokcancel, showinfo, WARNING
import csv
import img2pdf
from PIL import ImageTk, Image

# Importar tkcap de forma opcional (puede fallar en Python 3.11+)
try:
    import tkcap
    TKCAP_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    TKCAP_AVAILABLE = False
    print("Advertencia: tkcap no está disponible. La función de generar PDF puede estar limitada.")

# Importar módulos del proyecto
from src.services.read_img import read_image
from src.controllers.integrator import predict


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Herramienta para la detección rápida de neumonía")

        # BOLD FONT
        fonti = font.Font(weight="bold")

        self.root.geometry("815x560")
        self.root.resizable(0, 0)

        # LABELS
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Cédula Paciente:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        # STRING VARIABLES TO CONTAIN ID AND RESULT
        self.ID = StringVar()
        self.result = StringVar()

        # INPUT BOXES
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)

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
        self.button3 = ttk.Button(self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(self.root, text="PDF", command=self.create_pdf)
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
        self.reportID = 0

        # RUN LOOP
        self.root.mainloop()

    def load_img_file(self):
        """Carga un archivo de imagen (DICOM, JPEG, JPG, PNG)"""
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
                try:
                    # Intentar usar la nueva API de Pillow
                    self.img1 = img2show.resize((250, 250), Image.Resampling.LANCZOS)
                except AttributeError:
                    # Fallback para versiones antiguas
                    self.img1 = img2show.resize((250, 250), Image.LANCZOS)
                
                self.img1 = ImageTk.PhotoImage(self.img1)
                self.text_img1.image_create(END, image=self.img1)
                self.button1["state"] = "enabled"
                
            except Exception as e:
                showinfo(
                    title="Error",
                    message=f"Error al cargar la imagen:\n{str(e)}\n\nPor favor, verifique que el archivo sea válido."
                )

    def run_model(self):
        """Ejecuta el modelo de predicción y muestra los resultados"""
        try:
            if self.array is None:
                showinfo(
                    title="Error",
                    message="Por favor cargue una imagen primero."
                )
                return

            # Usar el módulo integrator para realizar la predicción completa
            self.label, self.proba, self.heatmap = predict(self.array)
            
            # Convertir heatmap a imagen PIL
            self.img2 = Image.fromarray(self.heatmap)
            
            # Redimensionar para visualización
            try:
                self.img2 = self.img2.resize((250, 250), Image.Resampling.LANCZOS)
            except AttributeError:
                self.img2 = self.img2.resize((250, 250), Image.LANCZOS)
            
            self.img2 = ImageTk.PhotoImage(self.img2)
            
            # Limpiar campos antes de insertar nuevos valores
            self.text_img2.delete(1.0, END)
            self.text2.delete(1.0, END)
            self.text3.delete(1.0, END)
            
            # Mostrar resultados
            self.text_img2.image_create(END, image=self.img2)
            self.text2.insert(END, self.label)
            self.text3.insert(END, "{:.2f}".format(self.proba) + "%")
            
        except Exception as e:
            showinfo(
                title="Error",
                message=f"Error al procesar la imagen:\n{str(e)}\n\nPor favor, verifique que el modelo esté disponible."
            )

    def save_results_csv(self):
        """Guarda los resultados en un archivo CSV"""
        try:
            if self.label is None or self.proba is None:
                showinfo(
                    title="Error",
                    message="No hay resultados para guardar. Por favor, realice una predicción primero."
                )
                return

            with open("historial.csv", "a", newline='', encoding='utf-8') as csvfile:
                w = csv.writer(csvfile, delimiter="-")
                w.writerow(
                    [
                        self.text1.get() or "N/A",
                        self.label,
                        "{:.2f}".format(self.proba) + "%"
                    ]
                )
            showinfo(title="Guardar", message="Los datos se guardaron con éxito.")
        except Exception as e:
            showinfo(
                title="Error",
                message=f"Error al guardar los datos:\n{str(e)}"
            )

    def create_pdf(self):
        """Genera un PDF con el reporte de la predicción"""
        import os
        
        try:
            if self.label is None:
                showinfo(
                    title="Error",
                    message="No hay resultados para generar PDF. Por favor, realice una predicción primero."
                )
                return

            # Crear carpeta report si no existe
            reportes_dir = "report"
            if not os.path.exists(reportes_dir):
                os.makedirs(reportes_dir)

            if TKCAP_AVAILABLE:
                # Método original usando tkcap
                cap = tkcap.CAP(self.root)
                ID = "Reporte" + str(self.reportID) + ".jpg"
                img = cap.capture(ID)
                img = Image.open(ID)
                img = img.convert("RGB")
                pdf_path = os.path.join(reportes_dir, f"Reporte{self.reportID}.pdf")
                img.save(pdf_path)
                self.reportID += 1
                showinfo(title="PDF", message=f"El PDF fue generado con éxito: {pdf_path}")
            else:
                # Método alternativo sin tkcap: crear PDF con información básica
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.pdfgen import canvas
                except ImportError:
                    showinfo(
                        title="Error",
                        message="No se puede generar PDF. Instale reportlab: pip install reportlab"
                    )
                    return
                
                pdf_path = os.path.join(reportes_dir, f"Reporte{self.reportID}.pdf")
                c = canvas.Canvas(pdf_path, pagesize=letter)
                width, height = letter
                
                # Agregar información al PDF
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "Reporte de Diagnóstico de Neumonía")
                
                c.setFont("Helvetica", 12)
                y = height - 100
                c.drawString(50, y, f"Cédula Paciente: {self.text1.get() or 'N/A'}")
                y -= 30
                c.drawString(50, y, f"Resultado: {self.label}")
                y -= 30
                c.drawString(50, y, f"Probabilidad: {self.proba:.2f}%")
                
                # Guardar imagen del heatmap si está disponible
                if self.heatmap is not None:
                    try:
                        heatmap_img = Image.fromarray(self.heatmap)
                        temp_path = "temp_heatmap.png"
                        heatmap_img.save(temp_path)
                        c.drawImage(temp_path, 50, y - 200, width=300, height=300)
                        # Limpiar archivo temporal
                        import os
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                    except Exception as e:
                        c.drawString(50, y - 50, f"Nota: No se pudo incluir imagen del heatmap: {str(e)}")
                
                c.save()
                self.reportID += 1
                showinfo(title="PDF", message=f"El PDF fue generado con éxito: {pdf_path}")
                
        except Exception as e:
            showinfo(
                title="Error",
                message=f"Error al generar el PDF:\n{str(e)}"
            )

    def delete(self):
        """Limpia todos los campos y resetea el estado de la aplicación"""
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
    """Función principal que inicia la aplicación"""
    my_app = App()
    return 0


if __name__ == "__main__":
    main()
