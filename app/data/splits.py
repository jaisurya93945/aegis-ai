from datasets import DatasetDict

from app.data.registry import load_dataset


def load_evaluation_data() -> DatasetDict:
    """Return the fixed Neuralchemy validation/test splits."""

    dataset = load_dataset("neuralchemy")

    return DatasetDict(
        {
            "validation": dataset["validation"],
            "test": dataset["test"],
        }
    )
