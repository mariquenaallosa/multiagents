# 04 - Embeddings y búsqueda por similitud con pgvector

## Objetivo
Convertir textos en vectores con Ollama, guardarlos en Postgres y buscar por significado.

## Requisitos
- Guías 01 y 03 completas.
- `docker compose up -d` corriendo, con la extensión `vector` activa.
- Modelo `nomic-embed-text` descargado en Ollama.

## Conceptos
- **Embedding:** lista de números (768 en `nomic-embed-text`) que representa el significado de un texto.
- **Similitud:** textos con significado parecido dan vectores cercanos.
- **Distancia coseno (`<=>` en pgvector):** cuanto más chica, más parecidos.
- **Vector store:** base donde se guardan los vectores para buscarlos. Aquí, Postgres con pgvector.
- **Búsqueda por significado:** la consulta "PDF files in the cloud" encuentra el texto de Blob Storage aunque no compartan palabras.
- **Dimensión:** la columna `vector(768)` debe coincidir con la dimensión del modelo. Cambiar de modelo obliga a recrear la columna.
- **Idioma:** `nomic-embed-text` rinde mejor en inglés. Por eso los textos de ejemplo están en inglés.

## Pasos

### 1. Instalar las librerías
```bash
uv add ollama "psycopg[binary]" pgvector
```

### 2. Correr el script
```bash
uv run scripts/embed_smoke.py
```
El script recrea la tabla `chunks_smoke`, inserta 5 textos con sus embeddings y busca los 3 más cercanos a una pregunta.

## Resultado esperado
El texto de Blob Storage debe aparecer primero, con la distancia más baja. Los textos de reembolsos y horarios deben quedar lejos.

## Problemas conocidos
- `connection refused` en el puerto 5443: los contenedores no están levantados (`docker compose up -d`).
- `model "nomic-embed-text" not found`: falta `ollama pull nomic-embed-text`.
- `expected 768 dimensions`: la columna no coincide con el modelo de embeddings.
