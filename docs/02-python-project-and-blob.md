# 02 - Proyecto Python y prueba de Blob Storage

## Objetivo
Crear el proyecto Python y comprobar que el SDK oficial de Azure habla con Floci-AZ.

## Requisitos
- Guía 01 completa.
- Floci-AZ corriendo en otra terminal:
  ```bash
  docker run --rm -p 4577:4577 -p 5672:5672 -p 5673:5673 floci/floci-az:latest
  ```
- `uv` instalado.

## Conceptos
- **uv:** gestor de proyectos y paquetes de Python (de Astral). Reemplaza pyenv + venv + pip.
- **pyproject.toml:** declara nombre, versión de Python y dependencias.
- **uv.lock:** versiones exactas instaladas, para reproducir el entorno.
- **Floci-AZ es un emulador de API:** no tiene UI propia. La UI es un proyecto aparte (`floci-ui`).
- **Storage en memoria:** al detener el contenedor se pierden todos los datos. Los scripts deben poder recrearlos.
- **Connection string de desarrollo:** `devstoreaccount1` y su clave son públicos y compartidos con Azurite. No son un secreto.

## Pasos

### 1. Crear el proyecto
```bash
cd /home/quena/Documentos/capacitaciones/ia-engineer/multiagents
uv init --python 3.12 --name multiagents
```

### 2. Instalar el SDK de Blob Storage
```bash
uv add azure-storage-blob
```

### 3. Correr el script de prueba
```bash
uv run scripts/blob_smoke.py
```
El script crea el container `documents`, sube `hello.txt`, lo lee de vuelta y lo imprime.

## Resultado esperado
```
containers: ['documents']
blobs: ['hello.txt']
content: hello from floci
```

## Cambio a Azure real
Solo cambia la connection string (variable `AZURE_STORAGE_CONNECTION_STRING`). El código no cambia.
