import json
from pathlib import Path

from datasets import Dataset, DatasetDict, load_dataset

from app.data.hlyn import convert_hlyn_record


OUTPUT_PATH = Path("dataset/processed/hlyn")


def main():
    print("Loading Hlyn...")

    dataset = load_dataset(
        "hlyn-labs/prompt-injection-judge-deberta-dataset"
    )

    split = dataset["train"]

    records = []

    for index, record in enumerate(split):
        converted = convert_hlyn_record(
            record,
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

    processed = DatasetDict(
        {
            "train": Dataset.from_list(records)
        }
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed.save_to_disk(str(OUTPUT_PATH))

    print("\nProcessing complete.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Records: {len(records)}")


if __name__ == "__main__":
    main()
