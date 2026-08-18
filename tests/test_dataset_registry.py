import pytest

from app.data.registry import list_datasets, load_dataset


def test_lists_all_datasets():
    assert list_datasets() == [
        "hlyn",
        "nemotron",
        "neuralchemy",
    ]


def test_loads_neuralchemy():
    dataset = load_dataset("neuralchemy")

    assert len(dataset["train"]) == 4391
    assert len(dataset["validation"]) == 941
    assert len(dataset["test"]) == 942


def test_loads_hlyn():
    dataset = load_dataset("hlyn")

    assert len(dataset["train"]) == 399741


def test_loads_nemotron():
    dataset = load_dataset("nemotron")

    assert len(dataset["train"]) == 1272


def test_rejects_unknown_dataset():
    with pytest.raises(ValueError):
        load_dataset("unknown")
