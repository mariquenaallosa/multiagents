# 05 - Pipeline RAG y evaluación de la búsqueda

## Objetivo
Armar un RAG mínimo sobre documentación de Azure y AWS, y medir qué tan bien funciona la etapa de búsqueda (retrieval).

## Requisitos
- Guías 01 a 04 completas.
- `docker compose up -d` corriendo (Floci-AZ, Postgres con pgvector, pgAdmin).
- Ollama con `llama3.2:3b` y `nomic-embed-text`.

## Flujo del pipeline
```
data/raw/*.md ──upload_docs.py──▶ Blob ──ingest.py──▶ chunks + embeddings ──▶ Postgres (tabla chunks)
pregunta ──embedding──▶ búsqueda por similitud (top-k) ──▶ prompt con contexto ──▶ llama3.2 ──▶ respuesta
```

## Archivos
| Archivo | Responsabilidad |
|---|---|
| `scripts/common.py` | Constantes compartidas (conexiones, modelos) |
| `scripts/upload_docs.py` | Sube `data/raw/*.md` a Blob |
| `scripts/chunking.py` | Parsea el front matter y trocea el texto |
| `scripts/ingest.py` | Blob → chunks → embeddings → tabla `chunks` |
| `scripts/rag.py` | Función `retrieve(question, k)` reutilizable |
| `scripts/ask.py` | Pregunta → búsqueda → prompt → respuesta |
| `scripts/eval_retrieval.py` | Mide la búsqueda contra `data/eval/questions.json` |

## Conceptos
- **Chunk:** fragmento de un documento (~800 caracteres, con 100 de solapamiento).
- **Embedding:** vector de 768 números (dimensión fija por modelo).
- **Top-k:** los k fragmentos más cercanos a la pregunta.
- **Distancia coseno (`<=>`):** menor distancia, más parecido.
- **Ventana de contexto:** máximo de tokens que ve el modelo (`llama3.2`: 4096 en esta instalación).
- **Temperatura 0:** el modelo elige siempre la palabra más probable; respuestas repetibles.
- **Hit / recall por documento:** ¿se recuperaron los documentos relevantes?
- **Datos esperados (`expected_facts`):** ¿aparece en el contexto el dato que responde la pregunta? Es más estricto que mirar solo el documento.

## Pasos
```bash
uv run scripts/upload_docs.py        # sube los documentos a Blob
uv run scripts/ingest.py             # genera chunks y embeddings (62 chunks de 6 documentos)
uv run scripts/ask.py                # pregunta con y sin contexto
uv run scripts/eval_retrieval.py     # evalúa la búsqueda
```

Inspeccionar el ranking completo de una pregunta y la posición del fragmento correcto:
```bash
uv run scripts/rag.py "<pregunta>" "<texto que debe contener el fragmento>" | rg HERE
```

## Hallazgos
1. **Sin contexto, el modelo alucina con seguridad:** definió RAG mal y afirmó cosas contrarias a los documentos (por ejemplo, que S3 es un servicio distribuido globalmente).
2. **Con contexto, mejora pero no es perfecto:** se colaron afirmaciones no respaldadas. La fluidez no es exactitud.
3. **La búsqueda global puede quedar desbalanceada** en preguntas comparativas (3 fragmentos de S3, 1 de Blob). Filtrar por metadato (`WHERE provider = ...`) equilibra el contexto.
4. **Un prompt demasiado estricto provoca falsos "no sé".** Hubo que permitir explícitamente comparar y pedir que indique qué falta.
5. **Métrica por documento demasiado indulgente:** Q6 dio recall 1.00 por documento pero 0/3 datos esperados.
6. **En Q6 el fragmento correcto quedó en el puesto 10 de 62** (distancia 0,437 frente a 0,344 del primero). Con `k=4` no entra. Hipótesis pendiente de verificar: una búsqueda por palabras clave lo encontraría, porque la frase del documento coincide casi literal con la pregunta.

## Resultados de la evaluación (k=4, 7 preguntas)
| Métrica | Resultado |
|---|---|
| hit@4 por documento | 7/7 |
| Datos esperados en el contexto | 6/7 preguntas completas; Q6 con 0/3 |

## Problemas conocidos
- El solapamiento de 100 caracteres puede cortar una palabra por la mitad (`usiness`). No rompe la búsqueda, pero conviene cortar en un espacio.
- Los textos con `k` alto consumen contexto: con un modelo de 3B, más fragmentos no siempre mejora la respuesta.
- La comparación de datos esperados por texto exacto es frágil (sinónimos, guiones).
- El set de evaluación es chico (7 preguntas) y casi todas nombran el servicio explícitamente.

## Próximos pasos
- Búsqueda híbrida (texto completo de Postgres + vectores) y medir contra Q6.
- Evaluación de las respuestas del LLM (fidelidad al contexto) con LLM-as-Judge.
- Cambiar el chunking para cortar por títulos.
