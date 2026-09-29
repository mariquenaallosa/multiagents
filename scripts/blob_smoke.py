"""Smoke test: upload a blob to Floci-AZ and read it back with the official Azure SDK."""

import os

from azure.storage.blob import BlobServiceClient

# Well-known public development key used by Azurite and compatible emulators.
DEV_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://localhost:4577/devstoreaccount1;"
)

CONTAINER = "documents"
BLOB_NAME = "hello.txt"


def main() -> None:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", DEV_CONNECTION_STRING)
    service = BlobServiceClient.from_connection_string(connection_string)

    container = service.get_container_client(CONTAINER)
    if not container.exists():
        container.create_container()

    container.upload_blob(BLOB_NAME, b"hello from floci", overwrite=True)

    content = container.download_blob(BLOB_NAME).readall()
    print("containers:", [c.name for c in service.list_containers()])
    print("blobs:", [b.name for b in container.list_blobs()])
    print("content:", content.decode())


if __name__ == "__main__":
    main()
