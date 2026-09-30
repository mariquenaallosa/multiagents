import ollama
import psycopg
from pgvector.psycopg import register_vector
from common import DATABASE_URL, EMBEDDING_MODEL
import sys

def retrieve(question:str, k:int = 4) -> list[dict]:
  vector= ollama.embed(model=EMBEDDING_MODEL, input=[question]).embeddings[0]

  with psycopg.connect(DATABASE_URL) as conn:
    register_vector(conn)
    rows = conn.execute(
      "SELECT blob_name, provider, service, content, embedding <=> %s::vector AS distance "
            "FROM chunks ORDER BY distance LIMIT %s", (vector,k),
    ).fetchall()

  return [
    {
      "blob_name":blob_name,
      "provider": provider,
      "service": service,
      "content": content,
      "distance": distance,
    }
    for blob_name,provider,service,content,distance in rows
  ]

if __name__ == "__main__":
    question = sys.argv[1]
    needle = sys.argv[2] if len(sys.argv) > 2 else None
    for rank, chunk in enumerate(retrieve(question, k=62), start=1):
        mark = "  <== HERE" if needle and needle in chunk["content"] else ""
        print(f"{rank:2d}  {chunk['distance']:.3f}  {chunk['blob_name']}{mark}")