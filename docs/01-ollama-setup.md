# 01 - Ollama setup (local LLM)

## Objetivo
Tener un LLM y un modelo de embeddings corriendo en local, sin API key ni costo.

## Requisitos
- Ollama instalado (`which ollama` debe devolver una ruta).
- ~3 GB libres en disco y ~4 GB de RAM libre.

## Conceptos
- **B = billions de parámetros.** `3b` = 3.000 millones de números aprendidos. Más parámetros: mejor calidad, más RAM, más lento.
- **Cuantización (Q4, Q8):** con cuántos bits se guarda cada parámetro. Ollama baja Q4 por defecto.
- **LLM vs embeddings:** el LLM genera texto. El modelo de embeddings convierte texto en un vector; textos con significado parecido dan vectores parecidos. Es la base del vector search en RAG.
- **Regla de memoria (estimación):** ~0,6 GB por cada B en Q4, más 1-2 GB de contexto.

## Pasos

### 1. Descargar el LLM
```bash
ollama pull llama3.2:3b
```
`pull` descarga el modelo al disco (como `docker pull`). Formato `nombre:etiqueta`.

### 2. Descargar el modelo de embeddings
```bash
ollama pull nomic-embed-text
```

### 3. Medir la velocidad
```bash
ollama run llama3.2:3b --verbose "explicame que es un RAG en dos lineas"
```
`--verbose` imprime estadísticas. La métrica clave es `eval rate` (tokens/s al generar).

## Resultado en esta máquina
| Dato | Valor |
|---|---|
| Hardware | 16 cores, 31 GB RAM, GPU Intel integrada (solo CPU) |
| `eval rate` | 15 tok/s |
| `prompt eval rate` | 45 tok/s |

Referencia: >8 tok/s es usable, <3 tok/s es frustrante.

## Observación: alucinación
El modelo respondió que RAG es "Ruta de Acceso y Gestión". Es incorrecto: RAG es *Retrieval Augmented Generation*. Un modelo chico sin contexto inventa con seguridad. Es el problema que RAG ataca, y se va a comparar en el proyecto.

## Comandos útiles
- `ollama list`: modelos descargados.
- `ollama ps`: modelos cargados en memoria y cuánta RAM usan.
- `/bye`: salir del chat interactivo.
- `ollama rm <modelo>`: borrar un modelo.

## Problemas conocidos
- Si cancelás un `pull` con Ctrl+C, se puede repetir el comando y retoma la descarga.
