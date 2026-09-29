# Fuentes del corpus

Los archivos de `data/raw/` **no se versionan** (contenido con copyright de terceros). Para recrearlos, bajá estas páginas y guardalas como markdown, con el front matter (`provider`, `service`, `source`) que usa el pipeline.

| Archivo | Proveedor | Fuente |
|---|---|---|
| `azure-blob-storage.md` | azure | https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction |
| `azure-cosmos-db.md` | azure | https://learn.microsoft.com/en-us/azure/cosmos-db/introduction |
| `azure-functions.md` | azure | https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview |
| `aws-s3.md` | aws | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html |
| `aws-dynamodb.md` | aws | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html |
| `aws-lambda.md` | aws | https://docs.aws.amazon.com/lambda/latest/dg/welcome.html |

## Notas
- Las páginas se obtuvieron con una herramienta de extracción web y se limpiaron a mano (sin metadatos ni enlaces). `aws-s3.md` y `aws-dynamodb.md` están **condensados**: se omitieron secciones de precios, cumplimiento y primeros pasos.
- Cada archivo lleva su URL de origen en el front matter.
- Contenido consultado el 2026-09-29.
