from pathlib import Path

from datasets import load_from_disk


DATASET_PATH = Path("dataset/raw/neuralchemy")


def main() -> None:
    dataset = load_from_disk(str(DATASET_PATH))

    train_groups = set(dataset["train"]["group_id"])
    validation_groups = set(dataset["validation"]["group_id"])
    test_groups = set(dataset["test"]["group_id"])

    train_validation = train_groups & validation_groups
    train_test = train_groups & test_groups
    validation_test = validation_groups & test_groups

    print("AegisAI Dataset Leakage Audit")
    print("=============================")

    print(f"Train groups:      {len(train_groups)}")
    print(f"Validation groups: {len(validation_groups)}")
    print(f"Test groups:       {len(test_groups)}")

    print("\nCross-split group overlap")
    print("-------------------------")

    print(f"Train ∩ Validation: {len(train_validation)}")
    print(f"Train ∩ Test:       {len(train_test)}")
    print(f"Validation ∩ Test:  {len(validation_test)}")

    if not train_validation and not train_test and not validation_test:
        print("\nRESULT: No group overlap detected.")
    else:
        print("\nRESULT: Potential group leakage detected.")


if __name__ == "__main__":
    main()
