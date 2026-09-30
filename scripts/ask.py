import ollama
import psycopg
from common import EMBEDDING_MODEL, DATABASE_URL, CHAT_MODEL
from pgvector.psycopg import register_vector

question = "What is the difference between Azure blob Storage and Amazon S3?"

response = ollama.embed(model= EMBEDDING_MODEL, input=[question])
vector = response.embeddings[0]
rows = []

with psycopg.connect(DATABASE_URL) as conn:
  register_vector(conn)
  for provider in ("azure", "aws"):
    rows += conn.execute("SELECT provider, service, content, embedding <=> %s::vector AS distance "
        "FROM chunks WHERE provider = %s ORDER BY distance LIMIT 2",
        (vector, provider),
    ).fetchall()

for provider, service, content, distance in rows:
  print(f"{distance:.3f} {provider}/{service} {content[:80]}")

context = "\n\n".join(
    f"[{provider} / {service}]\n{content}"
    for provider, service, content, distance in rows
)

messages = [
    {
        "role": "system",
        "content": (
            "You answer questions using ONLY the provided context. "
            "When asked to compare, list what the context says about each item "
            "and point out the differences you can infer from those facts. "
            "If key information is missing, say exactly what is missing. "
            "Always mention which provider (Azure or AWS) each fact comes from."
        ),
    },
    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
]

answer = ollama.chat(model=CHAT_MODEL, messages=messages, options={"temperature": 0})
print("\n=== WITH CONTEXT (RAG) ===")
print(answer.message.content)
print("\nprompt tokens:", answer.prompt_eval_count)


baseline = ollama.chat(
    model=CHAT_MODEL,
    messages=[{"role": "user", "content": question}],
    options={"temperature": 0},
)
print("\n=== WITHOUT CONTEXT ===")
print(baseline.message.content)