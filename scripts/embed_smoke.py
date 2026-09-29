"""Smoke test: embed texts with Ollama, store them in pgvector and run a similarity search."""

import ollama
import psycopg
from pgvector.psycopg import register_vector

DATABASE_URL = "postgresql://app:app@localhost:5443/rag"
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIMENSIONS = 768

TEXTS = [
    "Azure Blob Storage stores unstructured files such as documents and images.",
    "Azure Cosmos DB is a globally distributed NoSQL database.",
    "Azure Functions runs small pieces of code without managing servers.",
    "Refunds are processed within 10 business days after the return is received.",
    "Our office is open from Monday to Friday, 9am to 6pm.",
]

QUERY = "Where can I keep my PDF files in the cloud?"


def embed(texts: list[str]) -> list[list[float]]:
    return ollama.embed(model=EMBEDDING_MODEL, input=texts).embeddings


def main() -> None:
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)

        conn.execute("DROP TABLE IF EXISTS chunks_smoke")
        conn.execute(
            f"CREATE TABLE chunks_smoke ("
            f"id serial PRIMARY KEY, content text, embedding vector({EMBEDDING_DIMENSIONS}))"
        )

        for text, vector in zip(TEXTS, embed(TEXTS)):
            conn.execute(
                "INSERT INTO chunks_smoke (content, embedding) VALUES (%s, %s)",
                (text, vector),
            )

        query_vector = embed([QUERY])[0]
        rows = conn.execute(
            "SELECT content, embedding <=> %s::vector AS distance "
            "FROM chunks_smoke ORDER BY distance LIMIT 3",
            (query_vector,),
        ).fetchall()

    print(f"query: {QUERY}\n")
    for content, distance in rows:
        print(f"{distance:.3f}  {content}")


if __name__ == "__main__":
    main()
