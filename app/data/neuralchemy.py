from typing import Any

from app.models.dataset import DatasetRecord


def convert_neuralchemy_record(
    record: dict[str, Any],
    split: str,
    index: int,
) -> DatasetRecord:
    """Convert one Neuralchemy record into the AegisAI schema."""

    label = int(record["label"])
    category = str(record["category"])

    threat_type = (
        "benign"
        if label == 0
        else category
    )

    severity = str(record["severity"]).strip() or None

    source_id = f"{split}-{index}"

    metadata = {
        "original_source": record.get("source"),
        "augmented": record.get("augmented"),
        "tags": record.get("tags", []),
    }

    return DatasetRecord(
        text=str(record["text"]),
        label=label,
        threat_type=threat_type,
        severity=severity,
        source_dataset="neuralchemy",
        source_id=source_id,
        group_id=record.get("group_id"),
        metadata=metadata,
    )
