from pathlib import Path
from time import perf_counter
import json

from datasets import concatenate_datasets, Dataset

from app.data.loader import load_training_data
from app.ml.baseline import train_model


BASELINE_TRAINING_SAMPLES = 405_404

AUGMENTATION_PATH = Path(
    "data/augmentation/benign_security_hard_negatives.jsonl"
)

MODEL_PATH = Path(
    "models/aegisai_tfidf_v2.joblib"
)

# Repeat hard negatives so they have meaningful influence
# without replacing the original training distribution.
AUGMENTATION_MULTIPLIER = 20


def load_hard_negatives() -> Dataset:
    """Load defensive security hard-negative training examples."""

    if not AUGMENTATION_PATH.exists():
        raise FileNotFoundError(
            f"Hard-negative dataset not found: {AUGMENTATION_PATH}"
        )

    records = []

    with AUGMENTATION_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            record = json.loads(line)

            if "text" not in record or "label" not in record:
                raise ValueError(
                    f"Invalid record on line {line_number}: "
                    "expected 'text' and 'label'."
                )

            if not str(record["text"]).strip():
                raise ValueError(
                    f"Empty text on line {line_number}."
                )

            if int(record["label"]) != 0:
                raise ValueError(
                    f"Hard-negative record on line {line_number} "
                    "must have label 0."
                )

            records.append(
                {
                    "text": str(record["text"]),
                    "label": int(record["label"]),
                }
            )

    if not records:
        raise ValueError(
            "Hard-negative dataset is empty."
        )

    return Dataset.from_list(records)


def main():
    print("Loading original training data...", flush=True)

    start = perf_counter()

    original_dataset = load_training_data(
        include_hlyn=True,
        include_neuralchemy=True,
        include_nemotron=True,
    )

    print(
        f"Loaded {len(original_dataset):,} original samples "
        f"in {perf_counter() - start:.1f}s",
        flush=True,
    )

    print(
        "Loading hard-negative training data...",
        flush=True,
    )

    hard_negatives = load_hard_negatives()

    print(
        f"Loaded {len(hard_negatives):,} hard-negative samples.",
        flush=True,
    )

    print(
        f"Applying augmentation multiplier: "
        f"{AUGMENTATION_MULTIPLIER}x",
        flush=True,
    )

    augmented_datasets = [
        hard_negatives
        for _ in range(AUGMENTATION_MULTIPLIER)
    ]

    combined_dataset = concatenate_datasets(
        [
            original_dataset,
            *augmented_datasets,
        ]
    )

    print(
        f"Original samples:      "
        f"{len(original_dataset):,}",
        flush=True,
    )

    print(
        f"Hard-negative samples:  "
        f"{len(hard_negatives) * AUGMENTATION_MULTIPLIER:,}",
        flush=True,
    )

    print(
        f"Combined samples:      "
        f"{len(combined_dataset):,}",
        flush=True,
    )

    labels = combined_dataset["label"]

    benign_count = sum(
        1 for label in labels if label == 0
    )

    attack_count = sum(
        1 for label in labels if label == 1
    )

    print(
        f"Benign samples:         {benign_count:,}",
        flush=True,
    )

    print(
        f"Attack samples:         {attack_count:,}",
        flush=True,
    )

    print(
        "\nStarting AegisAI V2 training...",
        flush=True,
    )

    start = perf_counter()

    model = train_model(
        combined_dataset["text"],
        combined_dataset["label"],
    )

    print(
        f"Training finished in "
        f"{perf_counter() - start:.1f}s",
        flush=True,
    )

    print(
        "Saving V2 model...",
        flush=True,
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    import joblib

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"V2 model saved to: {MODEL_PATH}",
        flush=True,
    )


if __name__ == "__main__":
    main()
