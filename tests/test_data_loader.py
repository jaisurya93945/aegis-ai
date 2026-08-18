import pytest

from app.data.loader import load_training_data


def test_loads_all_training_data():
    dataset = load_training_data()

    assert len(dataset) == 405404


def test_loads_only_hlyn():
    dataset = load_training_data(
        include_hlyn=True,
        include_neuralchemy=False,
        include_nemotron=False,
    )

    assert len(dataset) == 399741


def test_loads_neuralchemy_and_nemotron():
    dataset = load_training_data(
        include_hlyn=False,
        include_neuralchemy=True,
        include_nemotron=True,
    )

    assert len(dataset) == 5663


def test_requires_at_least_one_dataset():
    with pytest.raises(ValueError):
        load_training_data(
            include_hlyn=False,
            include_neuralchemy=False,
            include_nemotron=False,
        )
