"""Upload the local corpus in data/raw/ to Blob Storage (Floci-AZ)."""

from azure.storage.blob import BlobServiceClient

from common import BLOB_CONNECTION_STRING, BLOB_CONTAINER, BLOB_PREFIX, RAW_DOCS_DIR


def main() -> None:
    files = sorted(RAW_DOCS_DIR.glob("*.md"))
    if not files:
        raise SystemExit(f"No markdown files found in {RAW_DOCS_DIR}")

    service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container = service.get_container_client(BLOB_CONTAINER)
    if not container.exists():
        container.create_container()

    for path in files:
        blob_name = f"{BLOB_PREFIX}{path.name}"
        container.upload_blob(blob_name, path.read_bytes(), overwrite=True)
        print(f"uploaded {blob_name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
