# 03 - Infraestructura local con Docker Compose

## Objetivo
Levantar Floci-AZ y Postgres con pgvector con un solo comando.

## Requisitos
- Docker con el plugin Compose (`docker compose version`).
- Puertos libres: 4577 (Floci) y 5443 (Postgres).

## Conceptos
- **Docker Compose:** describe varios contenedores en un archivo (`docker-compose.yml`) y los maneja juntos.
- **Volumen (`pgdata`):** guarda los datos de Postgres fuera del contenedor. Sobreviven a `docker compose down`.
- **Floci-AZ guarda todo en memoria:** al bajarlo se pierden sus datos. Los scripts deben poder recrearlos.
- **pgvector:** extensión de Postgres para guardar vectores y buscar por similitud. Reemplaza a Azure AI Search como vector store en local.
- **Healthcheck:** Docker consulta periódicamente si Postgres está listo (`pg_isready`).

## Pasos

### 1. Levantar los servicios
```bash
docker compose up -d
```
`-d` los deja en segundo plano.

### 2. Ver el estado
```bash
docker compose ps
```
Postgres debe aparecer como `healthy`.

### 3. Activar pgvector
```bash
docker compose exec postgres psql -U app -d rag -c "CREATE EXTENSION IF NOT EXISTS vector; SELECT extversion FROM pg_extension WHERE extname='vector';"
```

### 4. Probar Blob
```bash
uv run scripts/blob_smoke.py
```

## Comandos útiles
- `docker compose logs -f floci-az`: ver los logs de un servicio.
- `docker compose down`: detener y borrar contenedores. Conserva el volumen.
- `docker compose down -v`: además borra el volumen (pierde los datos de Postgres).

## Conexiones
| Servicio | Dirección |
|---|---|
| Floci-AZ | `http://localhost:4577` |
| Postgres | `postgresql://app:app@localhost:5443/rag` |

## Problemas conocidos
- `port is already allocated`: hay otro contenedor usando el puerto. Detenelo o cambiá el puerto de la izquierda en `ports`.
