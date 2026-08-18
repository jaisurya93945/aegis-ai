from datasets import concatenate_datasets

from app.data.registry import load_dataset


def load_training_data(
    include_hlyn: bool = True,
    include_neuralchemy: bool = True,
    include_nemotron: bool = True,
):
    """Load training data from selected processed datasets."""

    datasets = []

    if include_hlyn:
        datasets.append(load_dataset("hlyn")["train"])

    if include_neuralchemy:
        datasets.append(load_dataset("neuralchemy")["train"])

    if include_nemotron:
        datasets.append(load_dataset("nemotron")["train"])

    if not datasets:
        raise ValueError("At least one dataset must be enabled.")

    return concatenate_datasets(datasets)
