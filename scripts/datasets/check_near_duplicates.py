import json
from pathlib import Path

from datasets import load_from_disk
from rapidfuzz import process, fuzz


DATASET_PATH = Path("dataset/raw/neuralchemy")
REPORT_DIR = Path("dataset/reports")
REPORT_PATH = REPORT_DIR / "neuralchemy_near_duplicates.json"

SIMILARITY_THRESHOLD = 95
CANDIDATE_LIMIT = 3


def find_matches(source_name, source_texts, target_name, target_texts):
    matches = []

    for source_index, source_text in enumerate(source_texts):
        candidates = process.extract(
            source_text,
            target_texts,
            scorer=fuzz.ratio,
            limit=CANDIDATE_LIMIT,
            score_cutoff=SIMILARITY_THRESHOLD,
        )

        for target_text, score, target_index in candidates:
            matches.append(
                {
                    "split_a": source_name,
                    "index_a": source_index,
                    "split_b": target_name,
                    "index_b": target_index,
                    "similarity": round(score, 2),
                    "text_a": source_text,
                    "text_b": target_text,
                }
            )

    return matches


def main():
    dataset = load_from_disk(str(DATASET_PATH))

    train_texts = dataset["train"]["text"]
    validation_texts = dataset["validation"]["text"]
    test_texts = dataset["test"]["text"]

    print("AegisAI Near-Duplicate Audit")
    print("============================")
    print(f"Threshold: {SIMILARITY_THRESHOLD}")
    print(f"Candidate limit: {CANDIDATE_LIMIT}")

    all_matches = []

    comparisons = [
        ("train", train_texts, "validation", validation_texts),
        ("train", train_texts, "test", test_texts),
        ("validation", validation_texts, "test", test_texts),
    ]

    for source_name, source_texts, target_name, target_texts in comparisons:
        print(f"\nChecking {source_name} -> {target_name}...")

        matches = find_matches(
            source_name,
            source_texts,
            target_name,
            target_texts,
        )

        all_matches.extend(matches)

        print(f"Potential matches: {len(matches)}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "dataset": "neuralchemy/Prompt-injection-dataset",
        "threshold": SIMILARITY_THRESHOLD,
        "candidate_limit": CANDIDATE_LIMIT,
        "total_matches": len(all_matches),
        "matches": all_matches,
    }

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\nAudit complete.")
    print(f"Total potential matches: {len(all_matches)}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
