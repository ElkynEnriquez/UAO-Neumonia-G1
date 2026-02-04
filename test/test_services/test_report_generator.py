# -*- coding: utf-8 -*-


import os
# Asegurarse de que el directorio src está en el sys.path
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import numpy as np

from src.services.report_generator import (format_prediction_output,
                                           generate_pdf_report,
                                           save_results_csv)

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'src')))


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.test_dir = "test_temp_output"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        if os.path.exists(self.test_dir):
            for f in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, f))
            os.rmdir(self.test_dir)

    @patch('src.services.report_generator.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.services.report_generator.os.path.isfile')
    @patch('src.services.report_generator.csv.writer')
    def test_save_results_csv_new_file(self, mock_csv_writer, mock_isfile, mock_open, mock_datetime):
        """Prueba guardar resultados en un archivo CSV nuevo."""
        mock_isfile.return_value = False

        now_mock = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = now_mock

        mock_writer_instance = MagicMock()
        mock_csv_writer.return_value = mock_writer_instance

        result = save_results_csv(
            "P001", "viral", 95.5, filepath="historial_test.csv")

        self.assertTrue(result)
        mock_open.assert_called_with(
            "historial_test.csv", "a", newline='', encoding='utf-8')

        # Verificar que se escribió el encabezado y los datos
        mock_csv_writer.assert_called_once()
        mock_writer_instance.writerow.assert_any_call(
            ["Fecha", "Hora", "Cédula Paciente", "Diagnóstico", "Probabilidad"])
        mock_writer_instance.writerow.assert_any_call(
            ['2023-10-27', '10:30:00', 'P001', 'viral', '95.50%'])

    @patch('src.services.report_generator.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.services.report_generator.os.path.isfile')
    @patch('src.services.report_generator.csv.writer')
    def test_save_results_csv_existing_file(self, mock_csv_writer, mock_isfile, mock_open, mock_datetime):
        """Prueba guardar resultados en un archivo CSV existente."""
        mock_isfile.return_value = True

        now_mock = datetime(2023, 10, 27, 11, 0, 0)
        mock_datetime.now.return_value = now_mock

        mock_writer_instance = MagicMock()
        mock_csv_writer.return_value = mock_writer_instance

        result = save_results_csv(
            "P002", "normal", 99.0, filepath="historial_test.csv")

        self.assertTrue(result)
        mock_open.assert_called_with(
            "historial_test.csv", "a", newline='', encoding='utf-8')

        # El encabezado no debe ser escrito de nuevo
        header_call = unittest.mock.call(
            ["Fecha", "Hora", "Cédula Paciente", "Diagnóstico", "Probabilidad"])
        self.assertNotIn(
            header_call, mock_writer_instance.writerow.call_args_list)

        # Verificar que se escribieron los datos
        mock_writer_instance.writerow.assert_called_with(
            ['2023-10-27', '11:00:00', 'P002', 'normal', '99.00%'])

    @patch('services.report_generator.canvas.Canvas')
    def test_generate_pdf_report_success(self, mock_canvas):
        """Prueba la generación exitosa de un reporte en PDF."""
        mock_pdf = MagicMock()
        mock_canvas.return_value = mock_pdf

        success, path = generate_pdf_report(
            "P003", "bacteriana", 88.8, output_dir=self.test_dir, report_id=1
        )

        self.assertTrue(success)
        self.assertTrue(path.startswith(
            os.path.join(self.test_dir, "Reporte_1_")))
        self.assertTrue(path.endswith(".pdf"))

        mock_canvas.assert_called_once()
        mock_pdf.drawString.assert_called()
        mock_pdf.save.assert_called_once()

    @patch('services.report_generator.canvas.Canvas')
    @patch('services.report_generator.Image.fromarray')
    def test_generate_pdf_report_with_heatmap(self, mock_fromarray, mock_canvas):
        """Prueba la generación de PDF incluyendo un heatmap."""
        mock_pdf = MagicMock()
        mock_canvas.return_value = mock_pdf
        mock_img = MagicMock()
        mock_fromarray.return_value = mock_img

        heatmap = np.uint8(np.random.rand(100, 100) * 255)

        success, path = generate_pdf_report(
            "P004", "viral", 92.3, heatmap_array=heatmap, output_dir=self.test_dir, report_id=2
        )

        self.assertTrue(success)
        mock_fromarray.assert_called_once()
        mock_img.save.assert_called_once()
        mock_pdf.drawImage.assert_called_once()

        # Verificar que el archivo temporal del heatmap se eliminó
        temp_heatmap_path = mock_img.save.call_args[0][0]
        self.assertFalse(os.path.exists(temp_heatmap_path))

    def test_format_prediction_output(self):
        """Prueba el formato de la salida de la predicción para la consola."""
        output = format_prediction_output("bacteriana", 85.123)
        self.assertIn("DIAGNÓSTICO: NEUMONÍA BACTERIANA", output)
        self.assertIn("PROBABILIDAD: 85.12%", output)

        output = format_prediction_output("viral", 95.5)
        self.assertIn("DIAGNÓSTICO: NEUMONÍA VIRAL", output)
        self.assertIn("PROBABILIDAD: 95.50%", output)

        output = format_prediction_output("normal", 99.99)
        self.assertIn("DIAGNÓSTICO: NORMAL", output)
        self.assertIn("PROBABILIDAD: 99.99%", output)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
