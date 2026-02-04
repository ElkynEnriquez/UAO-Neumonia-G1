# Guía Rápida - Ejecutar con Docker

## Requisitos Previos

- Docker instalado ([Descargar](https://www.docker.com/products/docker-desktop))
- Imágenes de datos en `data/DICOM/` o `data/JPG/`

## Opción 1: Docker Compose (RECOMENDADO)

### Pasos:

```bash
# 1. Construir la imagen
docker-compose build

# 2. Ejecutar predicción
docker-compose run neumonia --input /data/DICOM/viral-2.dcm --patient-id 12345 --save-csv --save-pdf

# 3. Los resultados se guardan en ./report
```

### Ejemplos adicionales:

```bash
# Solo predicción (sin guardar)
docker-compose run neumonia --input /data/JPG/virus/1.jpg

# Con pdf
docker-compose run neumonia --input /data/DICOM/normal(2).dcm -p ABC123 --save-pdf

# Procesar batch de imágenes
docker-compose run neumonia --input /data/JPG/normal/1.jpg --save-csv
docker-compose run neumonia --input /data/JPG/normal/2.jpg --save-csv
```

## Opción 2: Docker Directo

### Pasos:

```bash
# 1. Construir imagen
docker build -t neumonia-detector .

# 2. Ejecutar
docker run -v $(pwd)/data:/data $(pwd)/report:/app/report `
  neumonia-detector --input /data/DICOM/viral-2.dcm --patient-id 12345 --save-csv --save-pdf
```

### Notas para Windows PowerShell:

- Usar backtick (`) para continuación de línea
- Las rutas usan `/` dentro del contenedor
- `$(pwd)` da la ruta actual

## Opción 3: Sin Docker (Local)

### Pasos:

```bash
# 1. Activar venv
.venv\Scripts\Activate.ps1

# 2. Ejecutar CLI
python cli.py --input data/DICOM/viral-2.dcm --patient-id 12345 --save-csv --save-pdf

# 3. O ejecutar GUI
python main.py
```

## Estructura de Carpetas

```
proyecto/
├── data/
│   ├── DICOM/
│   │   ├── viral-2.dcm
│   │   ├── normal(3).dcm
│   │   └── ...
│   ├── JPG/
│   │   ├── virus/
│   │   ├── normal/
│   │   └── bacteria/
│   └── models/
│       └── conv_MLP_84.h5
├── report/          ← Los resultados se guardan aquí
│   ├── historial.csv
│   ├── Reporte_0_*.pdf
│   └── ...
└── ...
```

## Opciones de Línea de Comandos

```bash
--input, -i          [REQUERIDO] Ruta de la imagen dentro del contenedor
--patient-id, -p     ID del paciente (default: N/A)
--output, -o         Carpeta de salida (default: /app/report)
--save-csv           Guardar resultados en CSV
--save-pdf           Generar PDF con heatmap
```

## Resultados Generados

### CSV (report/historial.csv)
```
Fecha,Hora,Cédula Paciente,Diagnóstico,Probabilidad
2026-02-02,23:42:24,12345,viral,95.31%
2026-02-02,23:43:15,ABC123,normal,91.50%
```

### PDF
- Archivo: `Reporte_0_YYYYMMDD_HHMMSS.pdf`
- Contiene:
  - Información del paciente
  - Diagnóstico (Normal/Bacteriana/Viral)
  - Probabilidad del diagnóstico
  - Mapa de calor Grad-CAM

## Solución de Problemas

### "Error: Cannot connect to Docker daemon"
```bash
# Iniciar Docker Desktop (Windows)
# O en Linux:
sudo systemctl start docker
```

### "Error: docker: command not found"
- Instalar Docker desde https://www.docker.com/products/docker-desktop

### "Error reading image"
- Verificar que la ruta de archivo sea correcta
- Usar `/data/` para archivos en el contenedor (no `.\data\`)

### Archivos no se guardan
- Verificar permisos de carpeta `./report`
- Usar `--save-csv --save-pdf` para guardar resultados

## Docker Compose en Detalle

### docker-compose.yml
```yaml
version: '3.8'
services:
  neumonia:
    build: .                          # Construir desde Dockerfile
    container_name: neumonia-detector
    volumes:
      - ./data:/data                  # Acceso a datos locales
      - ./report:/app/report          # Guardar resultados
    environment:
      - PYTHONUNBUFFERED=1            # Output en tiempo real
    stdin_open: true
    tty: true
```

### Dockerfile
```dockerfile
FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "cli.py"]
```

## Monitorear Resultados

```bash
# Ver CSV en tiempo real
docker-compose run neumonia --input /data/JPG/normal/1.jpg --save-csv
type report\historial.csv

# Generar multiple reportes
for ($i=1; $i -le 3; $i++) {
  docker-compose run neumonia --input /data/JPG/normal/$i.jpg --save-csv --save-pdf
}
```

## Tips

1. **Reutilizar imagen**: Una vez construida, es más rápido ejecutar
2. **Batch processing**: Crear script que llame CLI múltiples veces
3. **CSV acumulado**: Los resultados se agregan al archivo existente
4. **Limpieza**: `docker-compose down` para detener contenedores

## Contacto/Soporte

Si encuentras problemas:
1. Verifica que Docker esté ejecutándose
2. Comprueba permisos de carpetas
3. Ejecuta `docker-compose logs` para ver errores
