from pathlib import Path

from datasets import load_from_disk


DATASET_PATH = Path("dataset/raw/neuralchemy")


def main() -> None:
    dataset = load_from_disk(str(DATASET_PATH))

    train_texts = set(dataset["train"]["text"])
    validation_texts = set(dataset["validation"]["text"])
    test_texts = set(dataset["test"]["text"])

    train_validation = train_texts & validation_texts
    train_test = train_texts & test_texts
    validation_test = validation_texts & test_texts

    print("AegisAI Exact Text Leakage Audit")
    print("================================")

    print(f"Train texts:      {len(train_texts)}")
    print(f"Validation texts: {len(validation_texts)}")
    print(f"Test texts:       {len(test_texts)}")

    print("\nCross-split exact text overlap")
    print("------------------------------")

    print(f"Train ∩ Validation: {len(train_validation)}")
    print(f"Train ∩ Test:       {len(train_test)}")
    print(f"Validation ∩ Test:  {len(validation_test)}")

    if not train_validation and not train_test and not validation_test:
        print("\nRESULT: No exact text overlap detected.")
    else:
        print("\nRESULT: Exact text overlap detected.")

        if train_validation:
            print("\nExamples: Train ∩ Validation")
            for text in list(train_validation)[:5]:
                print(f"- {text}")

        if train_test:
            print("\nExamples: Train ∩ Test")
            for text in list(train_test)[:5]:
                print(f"- {text}")

        if validation_test:
            print("\nExamples: Validation ∩ Test")
            for text in list(validation_test)[:5]:
                print(f"- {text}")


if __name__ == "__main__":
    main()
