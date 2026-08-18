from pathlib import Path

from datasets import load_from_disk


DATASET_PATH = Path("dataset/raw/neuralchemy")


def main() -> None:
    dataset = load_from_disk(str(DATASET_PATH))

    print("\nDataset structure")
    print("=================")

    for split_name, split in dataset.items():
        print(f"\nSplit: {split_name}")
        print(f"Rows: {len(split)}")
        print(f"Columns: {split.column_names}")

        if len(split) > 0:
            print("\nFirst example:")
            print(split[0])


if __name__ == "__main__":
    main()
