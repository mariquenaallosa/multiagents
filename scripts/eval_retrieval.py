import json
from common import PROJECT_ROOT
from rag import retrieve

QUESTIONS_PATH = PROJECT_ROOT / "data" / "eval" / "questions.json"
K = 4


def main() -> None:
    questions = json.loads(QUESTIONS_PATH.read_text())

    hits = 0
    for item in questions:
        chunks = retrieve(item["question"], k=K)
        retrieved_docs = {chunk["blob_name"] for chunk in chunks}
        relevant = set(item["relevant_docs"])
        recall = len(retrieved_docs & relevant) / len(relevant)
        hit = recall == 1
        if hit:
            hits += 1
        text = " ".join(chunk["content"] for chunk in chunks).lower()
        found = [fact for fact in item["expected_facts"] if fact.lower() in text]
        print(f"      facts: {len(found)}/{len(item['expected_facts'])}  missing={[f for f in item['expected_facts'] if f not in found]}")
        print(f"{'HIT ' if hit else 'MISS'}  {item['id']}  recall={recall:.2f}  {sorted(retrieved_docs)}")

    print(f"\nhit@{K}: {hits}/{len(questions)} = {hits / len(questions):.0%}")


if __name__ == "__main__":
    main()