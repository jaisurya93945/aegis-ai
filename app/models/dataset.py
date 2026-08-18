from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DatasetRecord:
    """Canonical AegisAI representation of a security dataset sample."""

    text: str
    label: int
    threat_type: str
    severity: str | None
    source_dataset: str
    source_id: str
    group_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("DatasetRecord.text cannot be empty.")

        if self.label not in {0, 1}:
            raise ValueError("DatasetRecord.label must be 0 or 1.")

        if not self.source_dataset.strip():
            raise ValueError(
                "DatasetRecord.source_dataset cannot be empty."
            )

        if not self.source_id.strip():
            raise ValueError(
                "DatasetRecord.source_id cannot be empty."
            )
