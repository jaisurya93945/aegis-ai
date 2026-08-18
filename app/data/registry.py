from pathlib import Path

from datasets import load_from_disk


DATASET_ROOT = Path("dataset/processed")


DATASETS = {
    "neuralchemy": DATASET_ROOT / "neuralchemy",
    "hlyn": DATASET_ROOT / "hlyn",
    "nemotron": DATASET_ROOT / "nemotron",
}


def load_dataset(name: str):
    """Load a processed AegisAI dataset by name."""

    if name not in DATASETS:
        raise ValueError(
            f"Unknown dataset: {name}. "
            f"Available: {sorted(DATASETS)}"
        )

    path = DATASETS[name]

    if not path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {path}"
        )

    return load_from_disk(str(path))


def list_datasets() -> list[str]:
    """Return registered dataset names."""

    return sorted(DATASETS)
