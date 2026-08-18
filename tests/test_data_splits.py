from app.data.splits import load_evaluation_data


def test_evaluation_splits_are_fixed():
    dataset = load_evaluation_data()

    assert len(dataset["validation"]) == 941
    assert len(dataset["test"]) == 942
