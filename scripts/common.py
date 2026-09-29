"""Shared configuration for the local RAG scripts."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DOCS_DIR = PROJECT_ROOT / "data" / "raw"

# Well-known public development key used by Azurite and compatible emulators.
BLOB_CONNECTION_STRING = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING",
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://localhost:4577/devstoreaccount1;",
)
BLOB_CONTAINER = "documents"
BLOB_PREFIX = "raw/"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5443/rag")

EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIMENSIONS = 768
CHAT_MODEL = "llama3.2:3b"
