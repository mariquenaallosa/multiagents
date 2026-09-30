"""Read documents from Blob Storage, chunk them, embed them and store them in pgvector."""

import ollama
import psycopg
from azure.storage.blob import BlobServiceClient
from pgvector.psycopg import register_vector

from chunking import chunk_text, parse_front_matter
from common import (
    BLOB_CONNECTION_STRING,
    BLOB_CONTAINER,
    BLOB_PREFIX,
    DATABASE_URL,
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
)


def read_documents() -> list[tuple[str, str]]:
    service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container = service.get_container_client(BLOB_CONTAINER)
    return [
        (blob.name, container.download_blob(blob.name).readall().decode("utf-8"))
        for blob in container.list_blobs(name_starts_with=BLOB_PREFIX)
    ]


def main() -> None:
    documents = read_documents()
    if not documents:
        raise SystemExit("No documents found in Blob Storage. Run upload_docs.py first.")

    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)

        conn.execute("DROP TABLE IF EXISTS chunks")
        conn.execute(
            f"CREATE TABLE chunks ("
            f"id serial PRIMARY KEY, blob_name text, provider text, service text, "
            f"source text, chunk_index int, content text, "
            f"embedding vector({EMBEDDING_DIMENSIONS}))"
        )

        total = 0
        for blob_name, text in documents:
            metadata, body = parse_front_matter(text)
            chunks = chunk_text(body)
            embeddings = ollama.embed(model=EMBEDDING_MODEL, input=chunks).embeddings

            for index, (content, embedding) in enumerate(zip(chunks, embeddings)):
                conn.execute(
                    "INSERT INTO chunks "
                    "(blob_name, provider, service, source, chunk_index, content, embedding) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        blob_name,
                        metadata.get("provider"),
                        metadata.get("service"),
                        metadata.get("source"),
                        index,
                        content,
                        embedding,
                    ),
                )
            total += len(chunks)
            print(f"{blob_name}: {len(chunks)} chunks")

    print(f"\n{total} chunks stored from {len(documents)} documents")


if __name__ == "__main__":
    main()
