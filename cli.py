#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interfaz de línea de comandos para la detección de neumonía.
Sin GUI, para ejecución en Docker.
Reutiliza los servicios de la interfaz gráfica.
"""

import argparse
import sys
from pathlib import Path

from src.services.read_img import read_image
from src.controllers.integrator import predict
from src.services.report_generator import (
    save_results_csv,
    generate_pdf_report,
    format_prediction_output
)


def main():
    """Función principal CLI"""
    parser = argparse.ArgumentParser(
        description="Detector de neumonía - Interfaz CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python cli.py --input /ruta/imagen.dcm
  python cli.py -i /ruta/imagen.jpg -p 12345 -o ./reportes
  python cli.py --input imagen.png --patient-id ABC123 --save-csv --save-pdf
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Ruta a la imagen (DICOM, JPG, PNG)"
    )
    parser.add_argument(
        "--patient-id", "-p",
        type=str,
        default="N/A",
        help="ID del paciente (default: N/A)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./report",
        help="Carpeta de salida para reportes (default: ./report)"
    )
    parser.add_argument(
        "--save-csv",
        action="store_true",
        help="Guardar resultados en CSV"
    )
    parser.add_argument(
        "--save-pdf",
        action="store_true",
        help="Guardar reporte en PDF con heatmap"
    )

    args = parser.parse_args()

    # Validar archivo de entrada
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Archivo no encontrado: {args.input}")
        return 1

    # Crear directorio de salida
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Leyendo imagen: {args.input}")
        
        result = read_image(str(input_path))
        
        if result is None:
            print("❌ Error: No se pudo leer la imagen")
            return 1
        
        # Desempacar la tupla
        image_array, _ = result

        print(f"Imagen cargada (shape: {image_array.shape})")
        
        prediction, probability, heatmap = predict(image_array)

        # Mostrar resultado en consola
        output_text = format_prediction_output(prediction, probability)
        print(output_text)
        
        # Guardar en CSV si se solicita
        if args.save_csv:
            csv_path = output_dir / "historial.csv"
            if save_results_csv(args.patient_id, prediction, probability, str(csv_path)):
                print(f"Resultados guardados en: {csv_path}")
            else:
                print(f"❌ No se pudo guardar en CSV")

        # Guardar PDF si se solicita
        if args.save_pdf:
            success, pdf_path = generate_pdf_report(
                patient_id=args.patient_id,
                label=prediction,
                probability=probability,
                heatmap_array=heatmap,
                output_dir=str(output_dir),
                report_id=0
            )
            if success:
                print(f"Reporte PDF guardado en: {pdf_path}")
            else:
                print(f"❌ Error al generar PDF: {pdf_path}")

        return 0

    except Exception as e:
        print(f"❌ Error durante la predicción: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
