from typing import Any

from app.models.dataset import DatasetRecord


def convert_hlyn_record(
    record: dict[str, Any],
    index: int,
) -> DatasetRecord:
    """Convert one Hlyn record into the AegisAI canonical schema."""

    label = int(record["label"])

    threat_type = (
        "benign"
        if label == 0
        else "prompt_injection"
    )

    return DatasetRecord(
        text=str(record["text"]),
        label=label,
        threat_type=threat_type,
        severity=None,
        source_dataset="hlyn",
        source_id=f"train-{index}",
        group_id=None,
        metadata={
            "label_source": "hlyn",
            "threat_type_inferred": label == 1,
        },
    )
