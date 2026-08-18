from collections import Counter
from pathlib import Path

from datasets import load_from_disk


DATASET_PATH = Path("dataset/raw/neuralchemy")


def profile_split(name: str, split) -> None:
    labels = Counter(split["label"])
    categories = Counter(split["category"])
    sources = Counter(split["source"])
    severities = Counter(
        value for value in split["severity"] if value
    )

    augmented = Counter(split["augmented"])

    hard_negative_count = sum(
        "hard_negative" in tags
        for tags in split["tags"]
    )

    texts = split["text"]
    unique_texts = len(set(texts))

    groups = set(split["group_id"])

    print(f"\n=== {name.upper()} ===")
    print(f"Rows: {len(split)}")
    print(f"Unique texts: {unique_texts}")
    print(f"Duplicate texts: {len(split) - unique_texts}")
    print(f"Unique groups: {len(groups)}")
    print(f"Labels: {dict(labels)}")
    print(f"Categories: {dict(categories)}")
    print(f"Sources: {dict(sources)}")
    print(f"Severities: {dict(severities)}")
    print(f"Augmented: {dict(augmented)}")
    print(f"Hard negatives: {hard_negative_count}")


def main() -> None:
    dataset = load_from_disk(str(DATASET_PATH))

    print("AegisAI Dataset Profile")
    print("=======================")
    print(f"Dataset path: {DATASET_PATH}")

    for name, split in dataset.items():
        profile_split(name, split)


if __name__ == "__main__":
    main()
