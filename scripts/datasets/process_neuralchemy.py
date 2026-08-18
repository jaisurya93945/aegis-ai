import json
from pathlib import Path

from datasets import Dataset, DatasetDict, load_from_disk

from app.data.neuralchemy import convert_neuralchemy_record


RAW_PATH = Path("dataset/raw/neuralchemy")
OUTPUT_PATH = Path("dataset/processed/neuralchemy")


def convert_split(split_name, split):
    records = []

    for index, record in enumerate(split):
        converted = convert_neuralchemy_record(
            record,
            split=split_name,
            index=index,
        )

        records.append(
            {
                "text": converted.text,
                "label": converted.label,
                "threat_type": converted.threat_type,
                "severity": converted.severity,
                "source_dataset": converted.source_dataset,
                "source_id": converted.source_id,
                "group_id": converted.group_id,
                "metadata": json.dumps(
                    converted.metadata,
                    ensure_ascii=False,
                ),
            }
        )

    return Dataset.from_list(records)


def main():
    print("Loading raw Neuralchemy dataset...")
    dataset = load_from_disk(str(RAW_PATH))

    processed = DatasetDict()

    for split_name, split in dataset.items():
        print(f"Processing {split_name}: {len(split)} records")

        processed[split_name] = convert_split(
            split_name,
            split,
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed.save_to_disk(str(OUTPUT_PATH))

    print("\nProcessing complete.")
    print(f"Output: {OUTPUT_PATH}")

    for split_name, split in processed.items():
        print(f"{split_name}: {len(split)} records")


if __name__ == "__main__":
    main()
